# 📅 Planification des Spécialités

Application de bureau permettant la répartition automatique des élèves dans des groupes de spécialités selon leurs choix, avec gestion des contraintes de taille de groupe et de créneaux horaires.

## 🎯 Fonctionnalités

- **Import CSV** : Chargement des élèves et de leurs choix de spécialités depuis un fichier CSV
- **Répartition intelligente** : Algorithme automatique de placement des élèves dans les groupes
- **Contraintes paramétrables** :
  - Taille minimale et maximale des groupes
  - Nombre maximum de groupes par spécialité
  - Gestion des créneaux horaires
- **Interface graphique intuitive** :
  - Configuration simple des paramètres
  - Fenêtre de résultats avec résumé détaillé
  - Conseils automatiques en cas d'élèves non placés
- **Export multiple** :
  - Planning par élève (CSV)
  - Planning par groupe (CSV)
  - Liste des élèves non placés (CSV)
- **Aide intégrée** : Guide d'utilisation avec exemples de format CSV

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- tkinter (généralement inclus avec Python)

### Installation des dépendances

1. Cloner le repository :
```bash
git clone https://github.com/KerdanetYvan/planification_spe.git
cd planification_spe
```

2. Créer un environnement virtuel (recommandé) :
```bash
python -m venv .venv
```

3. Activer l'environnement virtuel :
- Windows :
  ```bash
  .venv\Scripts\activate
  ```
- Linux/Mac :
  ```bash
  source .venv/bin/activate
  ```

4. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## 💻 Utilisation

### Lancement de l'application GUI

```bash
python gui_main.py
```

### Lancement en ligne de commande (legacy)

```bash
python main.py
```

### Format du fichier CSV d'entrée

Le fichier CSV doit contenir au minimum les colonnes suivantes :

```csv
Nom,Prénom,Spécialité 1,Spécialité 2,Spécialité 3
Dupont,Marie,Maths,PC,SVT
Martin,Pierre,SVT,HGGSP,SES
...
```

**Remarques importantes** :
- La première ligne doit contenir les en-têtes
- Les colonnes "Nom" et "Prénom" sont obligatoires
- Au moins une colonne de spécialité doit être présente
- Le séparateur peut être une virgule (,) ou un point-virgule (;)
- L'encodage recommandé est UTF-8

### Exemple de paramètres

**Pour une petite classe (120-150 élèves)** :
- Min. élèves par groupe : 8
- Max. élèves par groupe : 12
- Max. groupes par spécialité : 3-4

**Pour une grande classe (200+ élèves)** :
- Min. élèves par groupe : 10
- Max. élèves par groupe : 15
- Max. groupes par spécialité : 5-6

## 📁 Structure du projet

```
planification_spe/
├── classes/
│   ├── __init__.py
│   ├── models.py          # Modèles de données (Student, TimeSlot, Group)
│   └── planner.py         # Algorithme de planification
├── utils/
│   ├── __init__.py
│   └── utils.py           # Fonctions utilitaires (import/export CSV)
├── build/                 # Fichiers de build (PyInstaller)
├── gui_main.py            # Interface graphique principale
├── main.py                # Script CLI (legacy)
├── gui_main.spec          # Configuration PyInstaller
├── README.md
├── LICENSE
└── requirements.txt
```

## 🛠️ Technologies utilisées

- **Python 3.x** : Langage de programmation principal
- **tkinter** : Interface graphique
- **CSV** : Gestion des fichiers d'import/export
- **PyInstaller** : Création d'exécutables (optionnel)

## 🏗️ Architecture

### Classes principales

#### `Student` (models.py)
Représente un élève avec ses informations personnelles et ses choix de spécialités.

#### `TimeSlot` (models.py)
Représente un créneau horaire disponible pour les cours de spécialités.

#### `Group` (models.py)
Représente un groupe d'élèves pour une spécialité donnée sur un créneau spécifique.

#### `Planner` (planner.py)
Gère l'algorithme de répartition des élèves dans les groupes en respectant les contraintes.

**Algorithme de planification** :
1. Tri des élèves par nombre de contraintes (priorité aux élèves avec moins de choix)
2. Pour chaque élève :
   - Recherche du groupe le moins rempli pour chaque spécialité
   - Vérification des contraintes (capacité, créneaux disponibles)
   - Placement de l'élève ou ajout à la liste des non placés

### Interface utilisateur

#### `PlanningApp` (gui_main.py)
Fenêtre principale de l'application avec :
- Sélection du fichier CSV
- Configuration des paramètres
- Lancement de la génération

#### `ResultsWindow` (gui_main.py)
Fenêtre de résultats affichant :
- Résumé de la planification
- Conseils personnalisés si nécessaire
- Options d'export

#### `HelpWindow` (gui_main.py)
Fenêtre d'aide avec documentation complète pour les utilisateurs.

## 🔧 Développement

### Exécution des tests

```bash
# À implémenter
python -m pytest tests/
```

### Création d'un exécutable

```bash
pyinstaller gui_main.spec
```

L'exécutable sera généré dans le dossier `dist/`.

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Guidelines

- Respectez le style de code existant
- Commentez les fonctions complexes
- Testez vos modifications avant de soumettre
- Mettez à jour la documentation si nécessaire

## 📝 TODO / Améliorations futures

- [ ] Ajout de tests unitaires
- [ ] Support de formats supplémentaires (Excel, JSON)
- [ ] Visualisation graphique des plannings
- [ ] Export au format PDF
- [ ] Sauvegarde/chargement des configurations
- [ ] Gestion de profils multiples
- [ ] Statistiques et analyses des répartitions
- [ ] Internationalisation (i18n)

## 🐛 Problèmes connus

- Sur certains systèmes, l'encodage UTF-8 avec BOM peut causer des problèmes d'import CSV
- Les très grands fichiers (>1000 élèves) peuvent ralentir l'interface

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

**Yvan KERDANET**

- GitHub: [@KerdanetYvan](https://github.com/KerdanetYvan)

## 🙏 Remerciements

- Merci à tous les utilisateurs testeurs qui ont contribué à l'amélioration de l'application
- Inspiré par les besoins réels de planification dans l'enseignement secondaire

---

© 2025 Yvan KERDANET - Tous droits réservés
