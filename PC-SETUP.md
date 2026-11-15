# Installer le projet sur ton PC (rendu avec ta carte graphique)

Sur le serveur cloud, 15 s de 3D prennent ~26 min (pas de carte graphique). Sur un PC avec un GPU récent, c'est beaucoup plus rapide.
Tu fais ces étapes une seule fois. Ensuite tu ouvres Claude Code dans le dossier du projet et tu lui parles comme ici.

## 1. Installer les outils (Windows)
Ouvre **PowerShell** et colle ces lignes une par une :
```powershell
winget install Git.Git
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.12
winget install Gyan.FFmpeg
```
Ferme PowerShell et rouvre-le (pour qu'il trouve les nouveaux outils), puis vérifie :
```powershell
git --version; node -v; python --version; ffmpeg -version
```
`node -v` doit afficher **v22** ou plus. Mets aussi à jour le **pilote de ta carte graphique** (NVIDIA GeForce Experience / AMD Adrenalin).

## 2. Récupérer le projet
```powershell
cd $HOME\Documents
git clone https://github.com/Maxesca2325/Maxesca2325.git
cd Maxesca2325
git checkout claude/eloquent-mccarthy-i4hoki
npm install
python -m pip install numpy pillow faster-whisper yt-dlp
```

## 3. Ta clé ai33 (seulement si tu utilises les voix ai33)
Sur ton PC, la clé n'est pas ajoutée automatiquement comme dans le cloud. Mets-la dans une variable d'environnement (jamais dans un fichier du projet) :
```powershell
setx AI33_API_KEY "ta_clé_ici"
```
Puis ferme et rouvre PowerShell.

## 4. Installer et lancer Claude Code
```powershell
npm install -g @anthropic-ai/claude-code
cd $HOME\Documents\Maxesca2325
claude
```
(Ou l'application Claude Desktop → onglet Code → ouvre le dossier `Maxesca2325`.)
Les skills (animated-shorts, hyperframes, script-writer…) sont déjà dans le projet : rien à installer en plus.

## 5. Faire un rendu
```powershell
cd hf
npm run render
```
La vidéo sort dans `hf\renders\`. Dans le texte qui s'affiche à la fin, cherche **"hardware gpu"** (ta carte graphique est utilisée) au lieu de **"software gpu"**. Si c'est "software", dis-le à Claude : il ajoutera `--browser-gpu`.

## Garder le PC et le cloud synchronisés
Avant de travailler : `git pull`. Après : demande à Claude de faire un commit et un push.
