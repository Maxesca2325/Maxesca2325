# Binance dans l'app Claude (web + mobile)

Ce dossier est un **connecteur personnalisé** pour Claude. Une fois installé, tu peux écrire à Claude, même depuis ton téléphone :

- « Quel est le prix du BTC ? » / « Montre-moi mes soldes »
- « Analyse l'ETH sur les 7 derniers jours »
- « Achète pour 20 € de BTC » / « Vends 0,001 BTC »
- « Mets un ordre d'achat de BTC à 60 000 € »

Claude te demande ton accord avant chaque outil qui passe un ordre (tu peux régler ça dans les paramètres du connecteur).

## Sécurités intégrées

| Protection | Réglage dans `.env` |
|---|---|
| Testnet (argent fictif) par défaut | `BINANCE_TESTNET=true` |
| Montant max par ordre | `MAX_ORDER_QUOTE=25` |
| Montant max par jour (achats + ventes) | `DAILY_MAX_QUOTE=100` |
| Seules certaines paires peuvent être tradées | `ALLOWED_SYMBOLS=...` |
| Interrupteur général | `TRADING_ENABLED=false` |
| URL secrète (sans elle, le serveur répond 404) | `MCP_SECRET_TOKEN` |
| Journal de chaque ordre | `data/journal.jsonl` |

Et côté Binance, **la clé API n'a jamais la permission « Retraits »**. Même si quelqu'un volait la clé, il ne pourrait pas sortir l'argent du compte.

---

## Installation (environ 30 min, une seule fois)

### 1. Créer une clé Testnet (argent fictif)

1. Va sur **https://testnet.binance.vision** et connecte-toi avec GitHub.
2. Clique sur **Generate HMAC_SHA256 Key**, donne-lui un nom, puis note l'**API Key** et la **Secret Key**.
   Le compte Testnet reçoit automatiquement des faux BTC, ETH, USDT…

### 2. Louer un petit serveur en Europe

Binance bloque les serveurs situés aux États-Unis. Il faut donc un serveur **en France ou en Allemagne**.
- Par exemple **Hetzner** (CX22, environ 4 €/mois, Allemagne) ou **OVH VPS** (France).
- Système : **Ubuntu 24.04**.
- Note l'**adresse IP** du serveur, par ex. `51.15.20.30`.

### 3. Installer sur le serveur

Connecte-toi au serveur. Sur Mac, ouvre le Terminal. Sur Windows, ouvre PowerShell.

```bash
ssh root@51.15.20.30
```

Puis, sur le serveur :

```bash
curl -fsSL https://get.docker.com | sh          # installe Docker
git clone https://github.com/Maxesca2325/Maxesca2325.git
cd Maxesca2325/binance-mcp
mkdir -p data && chmod 777 data
cp .env.example .env
openssl rand -hex 32                              # copie le résultat : c'est ton jeton secret
nano .env
```

> Le dépôt est privé : GitHub demandera ton nom d'utilisateur, puis un **jeton d'accès** comme mot de passe (GitHub → Settings → Developer settings → Personal access tokens). Autre solution : télécharge le dossier en ZIP sur ton PC et envoie-le avec `scp -r binance-mcp root@51.15.20.30:`.

Dans `nano`, remplis :
- `DOMAIN=` : l'IP **avec des tirets** + `.sslip.io`, par ex. `51-15-20-30.sslip.io` (c'est gratuit, aucun nom de domaine à acheter).
- `MCP_SECRET_TOKEN=` : le résultat de `openssl rand -hex 32`.
- `BINANCE_API_KEY=` et `BINANCE_API_SECRET=` : les clés Testnet.

Pour enregistrer : `Ctrl+O`, `Entrée`, puis `Ctrl+X`. Ensuite :

```bash
docker compose up -d --build
docker compose logs binance-mcp     # doit afficher "Binance MCP : mode TESTNET ..."
curl https://51-15-20-30.sslip.io/health    # doit répondre : ok
```

### 4. Ajouter le connecteur dans Claude

1. Sur **claude.ai** (navigateur) : **Paramètres → Connecteurs → Ajouter un connecteur personnalisé**.
2. Nom : `Binance`
3. URL : `https://51-15-20-30.sslip.io/mcp/TON_JETON_SECRET`
   (ton domaine + `/mcp/` + le jeton de l'étape 3).
4. Valide. Le connecteur apparaît aussi dans l'**app mobile** Claude, avec le même compte.

> Cette URL est comme un mot de passe : ne la partage avec personne.

Dans une conversation, active le connecteur Binance avec le bouton **+** ou le menu des outils, puis demande : **« Quel est mon statut Binance ? »**. Claude doit répondre « TESTNET ».

---

## Passer à l'argent réel (seulement après avoir testé)

1. Sur **binance.com** : **Profil → Gestion des API → Créer une API → Générée par le système**.
2. Permissions : coche **seulement** « Activer la lecture » et « Activer le trading Spot et sur marge ».
   **Ne coche jamais « Activer les retraits ».**
3. **Restriction d'accès IP** : choisis « Restreindre l'accès aux IP de confiance » et ajoute l'IP de ton serveur.
4. Sur le serveur : `nano .env`, mets `BINANCE_TESTNET=false` et les nouvelles clés, puis :
   ```bash
   docker compose up -d
   ```
5. Commence avec de petits montants. Les limites `MAX_ORDER_QUOTE` et `DAILY_MAX_QUOTE` restent actives.

## Arrêt d'urgence

- **Le plus rapide (depuis ton téléphone)** : app Binance → Gestion des API → **supprimer la clé**.
- Ou sur le serveur : `docker compose down`.
- Ou `TRADING_ENABLED=false` dans `.env`, puis `docker compose up -d`. La lecture des prix et des soldes continue de marcher, mais plus aucun ordre ne passe.

## Commandes utiles sur le serveur

```bash
cd ~/Maxesca2325/binance-mcp
cat data/journal.jsonl            # tous les ordres passés
docker compose logs -f            # suivre ce qui se passe
git pull && docker compose up -d --build   # mettre à jour
```

## Outils disponibles pour Claude

`statut`, `prix`, `marche_24h`, `bougies`, `soldes`, `ordres_ouverts`, `historique` (lecture seule)
`acheter`, `vendre`, `ordre_limite`, `annuler_ordre` (passent ou annulent des ordres)

## Tester sans Binance (développeurs)

```bash
pip install -r requirements.txt
python tests/test_mock.py     # faux Binance local : signature, limites, arrondis, URL secrète
```

## À savoir

- Claude agit **quand tu lui demandes**. Il ne trade pas tout seul en continu.
- Aucun outil ne garantit des gains. Le trading de crypto peut faire perdre tout l'argent engagé. N'investis que ce que tu acceptes de perdre.
