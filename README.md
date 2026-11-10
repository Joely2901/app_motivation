# Motivation Quotidienne

Application Android (Python + Kivy) affichant des citations motivantes.
Compatible Android 7.0 (API 24) et supérieur.

## Fonctions
- Citation du jour (change chaque jour)
- Bouton « Nouvelle citation » (au hasard)
- Favoris sauvegardés sur le téléphone

## Obtenir l'APK (méthode la plus simple : GitHub Actions)
1. Créez un dépôt GitHub gratuit et envoyez-y tout le contenu de ce dossier
   (y compris le dossier `.github`).
2. Onglet **Actions** → « Build APK » → **Run workflow** (ou simple push).
3. Après ~20-30 min, ouvrez l'exécution terminée → **Artifacts** → `motivation-apk`.
4. Décompressez et copiez `motivation-1.0.0-...-debug.apk` sur le téléphone.

## Compiler soi-même (Linux / WSL2 Ubuntu)
```
sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config \
  zlib1g-dev libncurses5-dev libtinfo5 cmake libffi-dev libssl-dev
pip install buildozer "cython<3.1"
buildozer -v android debug
```
L'APK sera dans `bin/`.

## Installer sur le téléphone
Réglages → Sécurité → autoriser les « sources inconnues » (ou
« Installer des applications inconnues » pour votre gestionnaire de fichiers),
puis ouvrez le fichier .apk.

## Tester sur PC
```
pip install kivy
python main.py
```
