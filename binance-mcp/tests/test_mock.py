"""Test de bout en bout avec un faux Binance (aucune vraie clé, aucun vrai ordre).

    pip install -r requirements.txt
    python tests/test_mock.py
"""

import asyncio
import hashlib
import hmac
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

import httpx
import uvicorn
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

SECRET = "fake-secret"
TOKEN = "t" * 40
FAKE_PORT, MCP_PORT = 9101, 9102
orders = []


def _verify(request):
    raw = urlsplit(str(request.url)).query
    query, _, sig = raw.rpartition("&signature=")
    good = hmac.new(SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    assert sig == good, "signature invalide"
    assert request.headers["X-MBX-APIKEY"] == "fake-key"
    return dict(parse_qsl(query))


async def time_(r): return JSONResponse({"serverTime": int(time.time() * 1000)})
async def price(r): return JSONResponse({"symbol": r.query_params["symbol"], "price": "50000.00"})
async def info(r):
    return JSONResponse({"symbols": [{
        "symbol": r.query_params["symbol"], "baseAsset": "BTC", "quoteAsset": "EUR", "quoteAssetPrecision": 8,
        "filters": [{"filterType": "LOT_SIZE", "stepSize": "0.00001000"},
                    {"filterType": "PRICE_FILTER", "tickSize": "0.01000000"},
                    {"filterType": "NOTIONAL", "minNotional": "5.00000000"}]}]})
async def account(r):
    _verify(r)
    return JSONResponse({"balances": [{"asset": "EUR", "free": "1000.00", "locked": "0"},
                                      {"asset": "BTC", "free": "0.01", "locked": "0"}]})
async def order(r):
    p = _verify(r)
    orders.append(p)
    qty = p.get("quantity") or str(round(float(p["quoteOrderQty"]) / 50000, 8))
    quote = p.get("quoteOrderQty") or str(float(qty) * 50000)
    return JSONResponse({"orderId": len(orders), "status": "FILLED", "executedQty": qty, "cummulativeQuoteQty": quote})


fake = Starlette(routes=[
    Route("/api/v3/time", time_), Route("/api/v3/ticker/price", price),
    Route("/api/v3/exchangeInfo", info), Route("/api/v3/account", account),
    Route("/api/v3/order", order, methods=["POST"]),
])


async def call(s, name, **args):
    res = await s.call_tool(name, args)
    text = res.content[0].text
    return res.isError, (text if res.isError else json.loads(text))


async def main():
    url = f"http://127.0.0.1:{MCP_PORT}/mcp/{TOKEN}"
    async with streamablehttp_client(url) as (read, write, _):
        async with ClientSession(read, write) as s:
            await s.initialize()
            names = sorted(t.name for t in (await s.list_tools()).tools)
            print("outils :", names)
            assert "acheter" in names and "soldes" in names

            err, st = await call(s, "statut"); print("statut :", st); assert st["mode"].startswith("TESTNET")
            err, p = await call(s, "prix", symbole="btc/eur"); assert p == {"symbole": "BTCEUR", "prix": "50000"}
            err, b = await call(s, "soldes"); assert len(b["soldes"]) == 2

            err, a = await call(s, "acheter", symbole="BTCEUR", montant=20); print("achat :", a)
            assert not err and a["statut"] == "FILLED" and orders[-1]["quoteOrderQty"] == "20"

            err, msg = await call(s, "acheter", symbole="BTCEUR", montant=30); print("trop gros :", msg)
            assert err and "maximum par ordre" in msg

            err, msg = await call(s, "acheter", symbole="DOGEEUR", montant=10); assert err and "pas autorisé" in msg
            err, msg = await call(s, "acheter", symbole="BTCEUR", montant=2); assert err and "au moins" in msg

            err, v = await call(s, "vendre", symbole="BTCEUR", quantite=0.0003456); print("vente :", v)
            assert not err and orders[-1]["quantity"] == "0.00034"  # arrondi au pas de 0.00001

            err, l = await call(s, "ordre_limite", symbole="BTCEUR", cote="ACHAT", quantite=0.0002, prix=49999.999)
            assert not err and orders[-1]["price"] == "49999.99" and orders[-1]["type"] == "LIMIT"

            # 20 + 17 + 10 = 47 utilisés ; limite jour 52 -> un ordre de 5 passe, puis refus
            err, _ = await call(s, "acheter", symbole="BTCEUR", montant=5); assert not err
            err, msg = await call(s, "acheter", symbole="BTCEUR", montant=5); print("limite jour :", msg)
            assert err and "limite du jour" in msg

    # Mauvais jeton -> 404, et rien d'autre n'est exposé
    async with httpx.AsyncClient() as c:
        r = await c.post(f"http://127.0.0.1:{MCP_PORT}/mcp/{'x' * 40}", json={})
        assert r.status_code == 404, r.status_code
        assert (await c.get(f"http://127.0.0.1:{MCP_PORT}/health")).text == "ok"
    print("\nTOUS LES TESTS PASSENT")


if __name__ == "__main__":
    threading.Thread(target=uvicorn.run, args=(fake,), kwargs={"port": FAKE_PORT, "log_level": "warning"},
                     daemon=True).start()
    state = tempfile.mkdtemp()
    env = {**os.environ, "BINANCE_API_KEY": "fake-key", "BINANCE_API_SECRET": SECRET,
           "BINANCE_BASE_URL": f"http://127.0.0.1:{FAKE_PORT}", "MCP_SECRET_TOKEN": TOKEN,
           "PORT": str(MCP_PORT), "STATE_DIR": state, "ALLOWED_SYMBOLS": "BTCEUR",
           "MAX_ORDER_QUOTE": "25", "DAILY_MAX_QUOTE": "52"}
    srv = subprocess.Popen([sys.executable, str(Path(__file__).parent.parent / "server.py")], env=env)
    try:
        for _ in range(50):
            try:
                httpx.get(f"http://127.0.0.1:{MCP_PORT}/health"); break
            except httpx.HTTPError:
                time.sleep(0.2)
        asyncio.run(main())
        print("journal :\n" + Path(state, "journal.jsonl").read_text())
    finally:
        srv.terminate()
