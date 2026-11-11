# Inventory

Application de bureau pour gérer un **stock de composants électroniques** (résistances, LED, circuits intégrés...), écrite en **Python** avec **[Flet](https://flet.dev)**.

On range ses composants par catégories, avec une photo, une quantité et une description. On ajoute ou retire du stock en quelques clics. Tout est sauvegardé automatiquement.

## Fonctionnalités

- **Liste du stock** groupée par catégorie, triée par nom, avec un filtre par catégorie.
- **Ajout d'un composant** : nom, catégorie, photo, quantité, description.
- **Catégories personnalisées** : on crée les siennes directement depuis le formulaire.
- **Page de détail** de chaque composant, avec un champ quantité et des boutons **Add** / **Remove**.
- **Contrôles** : nom unique, quantité valide, impossible de retirer plus que le stock disponible.
- **Sauvegarde automatique** après chaque modification. Les photos sont copiées dans le dossier de données.

## Installation

Prérequis : **Python 3.12 ou plus récent** (le projet est développé avec Python 3.14 et Flet 1.1).

```bash
git clone <url-du-depot>
cd Inventory

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

## Lancement

Depuis le dossier du projet :

```bash
python main.py
```

Au premier lancement, le stock est vide. Pour commencer :

1. Clique sur **＋** (en bas à droite).
2. Crée une catégorie dans le champ **New category**, puis valide avec **＋**.
3. Remplis le formulaire et clique sur **Save**.
4. Sur la page d'accueil, clique sur un composant pour ajouter ou retirer du stock.

## Structure du projet

```
main.py                     Point d'entrée
src/
  core/
    userInterface.py        Routage entre les pages, création du stock
    stock.py                Classe Stock : données et règles de gestion
    views/
      home.py               Page d'accueil (liste du stock)
      newComponent.py       Formulaire d'ajout
      componentDetail.py    Détail d'un composant et mouvements de stock
  utils/
    save.py                 Classe Save : lecture / écriture des fichiers
data/                       Données de l'utilisateur (créé automatiquement, non versionné)
  inventory.json
  pictures/
```

## Architecture

Le code est découpé en trois couches, chacune avec une seule responsabilité :

```
Vues (Home, NewComponent, ComponentDetail)    affichage et saisie
        │  appellent les méthodes de Stock
        ▼
Stock                                         règles de gestion
        │  demande une sauvegarde après chaque changement
        ▼
Save                                          fichiers (JSON + photos)
```

- **Les vues** ne modifient jamais les données elles-mêmes. Elles appellent `Stock` et affichent le résultat ou le message d'erreur.
- **`Stock`** contient toutes les règles. Quand une opération est refusée, il lève une `StockError` dont le message est affiché à l'utilisateur. Les règles s'appliquent donc partout, quelle que soit la page qui fait la demande.
- **`Save`** ne connaît que des fichiers. Il écrit d'abord dans un fichier temporaire, puis remplace l'ancien en une seule opération : une coupure pendant l'écriture ne corrompt pas la sauvegarde.

## Format des données

`data/inventory.json` :

```json
{
  "categories": ["Resistors", "LEDs"],
  "components": [
    {
      "name": "LED rouge 5mm",
      "category": "LEDs",
      "picture": "3f2a9c...e1.jpg",
      "quantity": 42,
      "description": "Diffuse, 20 mA"
    }
  ]
}
```

- `name` sert d'**identifiant** : il est unique, sans tenir compte des majuscules ni des espaces en début et fin.
- `picture` est le nom de la copie dans `data/pictures/`, ou `null` s'il n'y a pas de photo.

> Le dossier `data/` est exclu de git. Pense à le sauvegarder de ton côté si ton stock est important.

## Limites actuelles et pistes

- Il n'est pas encore possible de **modifier** ni de **supprimer** un composant ou une catégorie.
- Pas encore de version **web / téléphone** : le choix de la photo devra être adapté.
- Stockage en JSON, adapté à un seul utilisateur. Pour plusieurs appareils en même temps, il faudrait passer à une base de données comme SQLite.

## Auteur

Tao Serveaux
