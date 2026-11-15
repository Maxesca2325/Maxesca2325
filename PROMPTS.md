# Les prompts à copier-coller (PC Windows)

## Étape 0, à la main (une seule fois)
Installe l'application **Claude** pour Windows : https://claude.ai/download → connecte-toi → onglet **Code** → choisis le dossier **Documents**.

## Prompt 1 : installation (une seule fois)
```
Installe tout pour mon projet de vidéos, sur ce PC Windows, étape par étape, et corrige toi-même chaque erreur :
1. Vérifie et installe avec winget seulement ce qui manque : Git, Node.js LTS (22 ou plus), Python 3.12, FFmpeg. Rouvre le terminal si besoin pour qu'ils soient trouvés.
2. Clone https://github.com/Maxesca2325/Maxesca2325.git dans Documents, puis fais git checkout claude/eloquent-mccarthy-i4hoki.
3. Dans le projet : npm install, puis python -m pip install numpy pillow faster-whisper yt-dlp.
4. Si la variable AI33_API_KEY n'existe pas, dis-moi exactement la commande setx à taper moi-même (ne me demande jamais la clé dans le chat).
5. Fais un rendu test : cd hf puis npm run render. Dis-moi si la carte graphique est utilisée ("hardware gpu") et combien de temps ça a pris.
6. Écris "Installation terminée" et ouvre ensuite le dossier du projet pour les prochaines conversations.
```

## Prompt 2 : une vidéo complète (à chaque fois, nouvelle conversation dans le dossier Maxesca2325)
```
Fais une vidéo.
```
Ou plus précis :
```
Fais une vidéo : [ton idée, ou "trouve une idée"]. Voix : [identifiant ai33 ou chemin de ton fichier audio].
```
Pour la suite d'une série :
```
Fais la partie 2 de [nom de la série] : les commentaires ont voté [A ou B].
```
Claude suit tout seul le skill animated-shorts ("ONE-PROMPT MODE") : idée → script → voix sans blancs → plans → 3D → bruitages → vérifications → rendu 60 i/s → légende TikTok. Il ne te pose une question que s'il est bloqué (par exemple pour choisir la voix la première fois).
