"""Serveur MCP Binance : connecteur personnalisé pour l'app Claude (web + mobile).

Claude appelle ces outils quand tu lui demandes (prix, soldes, acheter, vendre...).
Sécurités : URL secrète, paires autorisées, montant max par ordre et par jour,
Testnet par défaut, journal de chaque ordre. Configuration : fichier .env.
"""

import datetime as dt
import hashlib
import hmac
import json
import logging
import os
import time
from decimal import ROUND_DOWN, Decimal
from pathlib import Path
from typing import Literal
from urllib.parse import urlencode

import httpx
import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations
from starlette.requests import Request
from starlette.responses import PlainTextResponse

# ---------------------------------------------------------------- configuration

API_KEY = os.environ.get("BINANCE_API_KEY", "").strip()
API_SECRET = os.environ.get("BINANCE_API_SECRET", "").strip()
TESTNET = os.environ.get("BINANCE_TESTNET", "true").strip().lower() != "false"
BASE_URL = os.environ.get("BINANCE_BASE_URL") or (
    "https://testnet.binance.vision" if TESTNET else "https://api.binance.com"
)
TOKEN = os.environ.get("MCP_SECRET_TOKEN", "").strip()
MAX_ORDER = Decimal(os.environ.get("MAX_ORDER_QUOTE", "25"))
DAILY_MAX = Decimal(os.environ.get("DAILY_MAX_QUOTE", "100"))
ALLOWED = {
    s.strip().upper()
    for s in os.environ.get("ALLOWED_SYMBOLS", "BTCUSDT,ETHUSDT,BTCEUR,ETHEUR").split(",")
    if s.strip()
}
TRADING_ENABLED = os.environ.get("TRADING_ENABLED", "true").strip().lower() != "false"
PORT = int(os.environ.get("PORT", "8000"))
STATE_DIR = Path(os.environ.get("STATE_DIR", "./data"))
JOURNAL = STATE_DIR / "journal.jsonl"

if len(TOKEN) < 32:
    raise SystemExit(
        "MCP_SECRET_TOKEN manquant ou trop court (32 caractères minimum).\n"
        "Génère-le avec : openssl rand -hex 32"
    )


logging.getLogger("httpx").setLevel(logging.WARNING)  # pas de signatures dans les logs


class BinanceError(Exception):
    pass


# ---------------------------------------------------------------- client Binance

_http = httpx.Client(base_url=BASE_URL, timeout=15)
_time_offset_ms: int | None = None
_symbols: dict[str, dict] = {}


def _check(r: httpx.Response):
    if r.status_code == 451:
        raise BinanceError(
            "Binance refuse ce serveur à cause de son pays (HTTP 451). "
            "Le serveur doit être en Europe (ex. France, Allemagne)."
        )
    try:
        data = r.json()
    except ValueError:
        raise BinanceError(f"Réponse Binance illisible (HTTP {r.status_code}).")
    if r.status_code >= 400:
        if isinstance(data, dict):
            raise BinanceError(f"Erreur Binance {data.get('code')} : {data.get('msg')}")
        raise BinanceError(f"Erreur Binance HTTP {r.status_code}.")
    return data


def _public(path: str, **params):
    return _check(_http.get(path, params={k: v for k, v in params.items() if v is not None}))


def _signed(method: str, path: str, **params):
    global _time_offset_ms
    if not API_KEY or not API_SECRET:
        raise BinanceError("Clés API Binance manquantes (BINANCE_API_KEY / BINANCE_API_SECRET dans .env).")
    if _time_offset_ms is None:
        _time_offset_ms = _public("/api/v3/time")["serverTime"] - int(time.time() * 1000)
    params = {k: v for k, v in params.items() if v is not None}
    params["timestamp"] = int(time.time() * 1000) + _time_offset_ms
    params["recvWindow"] = 5000
    query = urlencode(params)
    sig = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    r = _http.request(method, f"{path}?{query}&signature={sig}", headers={"X-MBX-APIKEY": API_KEY})
    return _check(r)


def _clean(symbol: str) -> str:
    return symbol.upper().replace("/", "").replace("-", "").replace(" ", "")


def _tradable(symbol: str) -> str:
    symbol = _clean(symbol)
    if symbol not in ALLOWED:
        raise BinanceError(
            f"{symbol} n'est pas autorisé pour le trading. Paires autorisées : "
            f"{', '.join(sorted(ALLOWED))} (ALLOWED_SYMBOLS dans .env)."
        )
    return symbol


def _info(symbol: str) -> dict:
    if symbol not in _symbols:
        s = _public("/api/v3/exchangeInfo", symbol=symbol)["symbols"][0]
        f = {x["filterType"]: x for x in s["filters"]}
        notional = f.get("NOTIONAL") or f.get("MIN_NOTIONAL") or {}
        _symbols[symbol] = {
            "base": s["baseAsset"],
            "quote": s["quoteAsset"],
            "step": Decimal(f["LOT_SIZE"]["stepSize"]),
            "tick": Decimal(f["PRICE_FILTER"]["tickSize"]),
            "quote_step": Decimal(10) ** -int(s.get("quoteAssetPrecision", s.get("quotePrecision", 8))),
            "min_notional": Decimal(notional.get("minNotional", "0")),
        }
    return _symbols[symbol]


def _floor(value: Decimal, step: Decimal) -> Decimal:
    return (value / step).to_integral_value(rounding=ROUND_DOWN) * step if step > 0 else value


def _s(d: Decimal) -> str:
    """Decimal -> texte sans notation scientifique (ce que Binance attend)."""
    text = format(d.normalize(), "f")
    return text if text not in ("-0", "") else "0"


def _price(symbol: str) -> Decimal:
    return Decimal(_public("/api/v3/ticker/price", symbol=symbol)["price"])


# ---------------------------------------------------------------- limites + journal


def _today() -> str:
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


def _spent_today() -> Decimal:
    total = Decimal(0)
    if JOURNAL.exists():
        for line in JOURNAL.read_text().splitlines():
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("date") == _today() and e.get("ok"):
                total += Decimal(e["montant"])
    return total


def _check_limits(symbol: str, notional: Decimal):
    if not TRADING_ENABLED:
        raise BinanceError("Le trading est désactivé (TRADING_ENABLED=false dans .env).")
    quote = _info(symbol)["quote"]
    if notional > MAX_ORDER:
        raise BinanceError(
            f"Refusé : {_s(notional)} {quote} dépasse le maximum par ordre ({_s(MAX_ORDER)}). "
            "Change MAX_ORDER_QUOTE dans .env si tu veux plus."
        )
    spent = _spent_today()
    if spent + notional > DAILY_MAX:
        raise BinanceError(
            f"Refusé : limite du jour atteinte ({_s(spent)} déjà utilisés sur {_s(DAILY_MAX)}). "
            "Remise à zéro à minuit UTC."
        )
    minimum = _info(symbol)["min_notional"]
    if notional < minimum:
        raise BinanceError(f"Refusé : Binance demande au moins {_s(minimum)} {quote} par ordre sur {symbol}.")


def _log(entry: dict):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    entry = {"date": _today(), "heure_utc": dt.datetime.now(dt.timezone.utc).strftime("%H:%M:%S"),
             "testnet": TESTNET, **entry}
    with JOURNAL.open("a") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _place(symbol: str, side: str, notional: Decimal, **params) -> dict:
    _check_limits(symbol, notional)
    base = {"symbole": symbol, "cote": side, "type": params.get("type"), "montant": _s(notional)}
    try:
        o = _signed("POST", "/api/v3/order", symbol=symbol, side=side, newOrderRespType="FULL", **params)
    except BinanceError as e:
        _log({**base, "ok": False, "erreur": str(e)})
        raise
    executed = Decimal(o.get("executedQty", "0"))
    spent = Decimal(o.get("cummulativeQuoteQty", "0"))
    real = spent if spent > 0 else notional
    _log({**base, "montant": _s(real), "ok": True, "id_ordre": o.get("orderId"), "statut": o.get("status")})
    info = _info(symbol)
    return {
        "mode": "TESTNET (argent fictif)" if TESTNET else "RÉEL",
        "id_ordre": o.get("orderId"),
        "statut": o.get("status"),
        "symbole": symbol,
        "cote": side,
        "quantite_executee": f"{_s(executed)} {info['base']}",
        "montant_execute": f"{_s(spent)} {info['quote']}",
        "prix_moyen": _s(spent / executed) if executed > 0 else None,
        "utilise_aujourdhui": f"{_s(_spent_today())} / {_s(DAILY_MAX)}",
    }


# ---------------------------------------------------------------- serveur MCP

mcp = FastMCP(
    "Binance",
    instructions=(
        "Outils pour le compte Binance de l'utilisateur. Le mode (TESTNET = argent fictif, ou RÉEL) "
        "est donné par l'outil statut : appelle-le avant le premier ordre et dis toujours à "
        "l'utilisateur dans quel mode tu es. Avant d'acheter ou vendre, rappelle le montant exact et "
        "la paire. Les montants sont dans la monnaie de cotation de la paire (EUR pour BTCEUR, "
        "USDT pour BTCUSDT). Ne promets jamais de gains."
    ),
    host="0.0.0.0",
    port=PORT,
    streamable_http_path=f"/mcp/{TOKEN}",
    stateless_http=True,
    json_response=True,
    # Derrière Caddy (HTTPS) avec un domaine public : la protection "localhost" ne s'applique pas.
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)

READ = ToolAnnotations(readOnlyHint=True, openWorldHint=True)
TRADE = ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=False, openWorldHint=True)


@mcp.custom_route("/health", methods=["GET"])
async def health(_: Request):
    return PlainTextResponse("ok")


@mcp.tool(annotations=READ)
def statut() -> dict:
    """Mode (TESTNET ou RÉEL), paires autorisées, limites et montant déjà utilisé aujourd'hui."""
    return {
        "mode": "TESTNET (argent fictif)" if TESTNET else "RÉEL (vrai argent)",
        "trading_active": TRADING_ENABLED,
        "paires_autorisees": sorted(ALLOWED),
        "max_par_ordre": _s(MAX_ORDER),
        "max_par_jour": _s(DAILY_MAX),
        "utilise_aujourdhui": _s(_spent_today()),
        "note": "Montants dans la monnaie de cotation de la paire (EUR, USDT...).",
    }


@mcp.tool(annotations=READ)
def prix(symbole: str) -> dict:
    """Prix actuel d'une paire, ex. BTCEUR, ETHUSDT."""
    symbol = _clean(symbole)
    return {"symbole": symbol, "prix": _s(_price(symbol))}


@mcp.tool(annotations=READ)
def marche_24h(symbole: str) -> dict:
    """Variation, plus haut, plus bas et volume sur 24 h d'une paire."""
    d = _public("/api/v3/ticker/24hr", symbol=_clean(symbole))
    return {
        "symbole": d["symbol"],
        "prix": d["lastPrice"],
        "variation_pct": d["priceChangePercent"],
        "plus_haut": d["highPrice"],
        "plus_bas": d["lowPrice"],
        "volume_quote": d["quoteVolume"],
    }


@mcp.tool(annotations=READ)
def bougies(
    symbole: str,
    intervalle: Literal["1m", "5m", "15m", "1h", "4h", "1d", "1w"] = "1h",
    nombre: int = 48,
) -> dict:
    """Historique des prix (bougies) pour analyser une tendance. nombre : 1 à 200."""
    rows = _public("/api/v3/klines", symbol=_clean(symbole), interval=intervalle,
                   limit=max(1, min(int(nombre), 200)))
    return {
        "symbole": _clean(symbole),
        "intervalle": intervalle,
        "colonnes": ["ouverture_utc", "ouverture", "haut", "bas", "cloture", "volume"],
        "bougies": [
            [dt.datetime.fromtimestamp(r[0] / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%M"),
             r[1], r[2], r[3], r[4], r[5]]
            for r in rows
        ],
    }


@mcp.tool(annotations=READ)
def soldes() -> dict:
    """Soldes du compte Spot (seulement les cryptos que tu possèdes)."""
    acc = _signed("GET", "/api/v3/account", omitZeroBalances="true")
    rows = []
    for b in acc.get("balances", []):
        free, locked = Decimal(b["free"]), Decimal(b["locked"])
        if free + locked > 0:
            rows.append({"actif": b["asset"], "disponible": _s(free), "bloque_en_ordre": _s(locked)})
    return {"mode": "TESTNET (argent fictif)" if TESTNET else "RÉEL", "soldes": rows}


@mcp.tool(annotations=READ)
def ordres_ouverts(symbole: str | None = None) -> dict:
    """Ordres limites en attente (tous, ou pour une paire)."""
    rows = _signed("GET", "/api/v3/openOrders", symbol=_clean(symbole) if symbole else None)
    return {"ordres": [
        {"id_ordre": o["orderId"], "symbole": o["symbol"], "cote": o["side"], "type": o["type"],
         "quantite": o["origQty"], "prix": o["price"], "execute": o["executedQty"]}
        for o in rows
    ]}


@mcp.tool(annotations=READ)
def historique(symbole: str, nombre: int = 20) -> dict:
    """Tes derniers trades exécutés sur une paire (1 à 100)."""
    rows = _signed("GET", "/api/v3/myTrades", symbol=_clean(symbole), limit=max(1, min(int(nombre), 100)))
    return {"trades": [
        {"date_utc": dt.datetime.fromtimestamp(t["time"] / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%M"),
         "cote": "ACHAT" if t["isBuyer"] else "VENTE", "prix": t["price"], "quantite": t["qty"],
         "montant": t["quoteQty"], "frais": f"{t['commission']} {t['commissionAsset']}"}
        for t in rows
    ]}


@mcp.tool(annotations=TRADE)
def acheter(symbole: str, montant: float) -> dict:
    """Achat immédiat au prix du marché pour un MONTANT dans la monnaie de cotation.
    Ex. symbole=BTCEUR, montant=20 -> achète pour 20 EUR de BTC."""
    symbol = _tradable(symbole)
    amount = _floor(Decimal(str(montant)), _info(symbol)["quote_step"])
    return _place(symbol, "BUY", amount, type="MARKET", quoteOrderQty=_s(amount))


@mcp.tool(annotations=TRADE)
def vendre(symbole: str, quantite: float | None = None, montant: float | None = None) -> dict:
    """Vente immédiate au prix du marché. Donne SOIT quantite (en crypto, ex. 0.001 BTC),
    SOIT montant (dans la monnaie de cotation, ex. 20 EUR)."""
    symbol = _tradable(symbole)
    info = _info(symbol)
    if (quantite is None) == (montant is None):
        raise BinanceError("Donne soit quantite, soit montant (pas les deux).")
    if montant is not None:
        amount = _floor(Decimal(str(montant)), info["quote_step"])
        return _place(symbol, "SELL", amount, type="MARKET", quoteOrderQty=_s(amount))
    qty = _floor(Decimal(str(quantite)), info["step"])
    if qty <= 0:
        raise BinanceError(f"Quantité trop petite (pas minimum {_s(info['step'])} {info['base']}).")
    return _place(symbol, "SELL", qty * _price(symbol), type="MARKET", quantity=_s(qty))


@mcp.tool(annotations=TRADE)
def ordre_limite(symbole: str, cote: Literal["ACHAT", "VENTE"], quantite: float, prix: float) -> dict:
    """Place un ordre à un prix fixé (exécuté seulement si le marché atteint ce prix).
    quantite en crypto (ex. 0.001 BTC), prix dans la monnaie de cotation."""
    symbol = _tradable(symbole)
    info = _info(symbol)
    qty = _floor(Decimal(str(quantite)), info["step"])
    price = _floor(Decimal(str(prix)), info["tick"])
    if qty <= 0 or price <= 0:
        raise BinanceError("Quantité ou prix trop petit.")
    side = "BUY" if cote == "ACHAT" else "SELL"
    return _place(symbol, side, qty * price, type="LIMIT", timeInForce="GTC",
                  quantity=_s(qty), price=_s(price))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True))
def annuler_ordre(symbole: str, id_ordre: int) -> dict:
    """Annule un ordre en attente (voir ordres_ouverts pour l'id)."""
    o = _signed("DELETE", "/api/v3/order", symbol=_clean(symbole), orderId=int(id_ordre))
    _log({"symbole": o["symbol"], "cote": o["side"], "type": "ANNULATION", "montant": "0", "ok": False,
          "id_ordre": o["orderId"]})
    return {"id_ordre": o["orderId"], "statut": o["status"]}


if __name__ == "__main__":
    print(f"Binance MCP : mode {'TESTNET' if TESTNET else 'RÉEL'}, port {PORT}, "
          f"max {_s(MAX_ORDER)}/ordre, {_s(DAILY_MAX)}/jour, paires {sorted(ALLOWED)}")
    # access_log=False : sinon l'URL secrète apparaîtrait dans les logs.
    uvicorn.run(mcp.streamable_http_app(), host="0.0.0.0", port=PORT, access_log=False)
