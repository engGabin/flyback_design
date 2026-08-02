# Flyback Designer App
Application de dimensionnement et de simulation pour alimentations à découpage Flyback.

## Electrical Specification
First, the designer will provide the following input specifications, which will be “fixed” for the entire design (fixed in the sense that they will not be calculated multiple times)

| Parameters    | Unit      | Description                                           | fixe/calc |
|---------------|-----------|-------------------------------------------------------|-----------|
| vac_min       | V         | Minimum AC input                                      | fixe      |
| vac_max       | V         | Maximum AC input                                      | fixe      |
| f             | Hz        | Output power                                          | fixe      |
| v_out1        | V         | Output voltage of winding 1                           | fixe      |
| p_out1        | W         | Output power of winding 1                             | fixe      |
| v_out2        | V         | Output voltage of winding 2                           | fixe      |
| p_out2        | W         | Output power of winding 2                             | fixe      |
| v_aux         | V         | Output voltage of auxiliary winding                   | fixe      |
| p_aux         | W         | Output power of auxiliary winding                     | fixe      |
| η             | -         | Efficiency                                            | fixe      |
| delta_v_bulk  | -         | Maximum voltage ripple allowed on the bulk capacitor  | fixe      |
| Nh            | -         | Number of hold-up required                            | fixe      |

## Bulk Capacitor Calculation

### Bulk Capacitor Value Choice



## Architecture
Ce projet utilise une architecture MVC (Modèle-Vue-Contrôleur) avec PyQt6 :
- **Engine** : Logique métier et formules mathématiques.
- **UI** : Interface graphique modulaire.


Flyback_Design_App/
│
├── README.md                
├── requirements.txt          # Liste des bibliothèques nécessaires
├── main.py                   
│
├── data/                     # Base de données
│   └── components.json       # (Plus tard) Stockera les listes de contrôleurs, transfos, etc.
│
├── engine/                   # LE MODÈLE (Cerveau mathématique)
│   ├── __init__.py
│   ├── design_state.py       # Stocke toutes les variables (Vin, Vout, Lp, etc.)
│   └── calc_engine.py        # Contient toutes les formules physiques de dimensionnement
│
├── tests/                    # (Plus tard) Pour vérifier que nos formules sont justes
│
└── ui/                       # LA VUE & LE CONTRÔLEUR (L'interface)
    ├── __init__.py
    ├── main_window.py        # La fenêtre principale et le menu latéral
    ├── pages/                # Les différentes étapes du design (1 page = 1 fichier)
    │   ├── __init__.py
    │   ├── step1_inputs.py   # Spécifications d'entrée
    │   ├── step2_input_stage.py # Étage d'entrée
    │   └── ...
    ├── tabs/                 # Les onglets transversaux (Infos routage, Résumé formules)
    │   └── formula_ref.py
    └── widgets/              # Nos "briques Lego" visuelles réutilisables
        ├── __init__.py
        └── common.py         # Les jolis champs de saisie, les titres de section, etc.

## engine
### design_state.py
Ce module gère l'état global de l'application. L'utilisation du décorateur @dataclass permet une définition optimisée du modèle de données. Le cœur du système repose sur une architecture réactive : l'attribut state_changed = pyqtSignal() assure la liaison avec l'interface utilisateur. Ainsi, l'appel à la fonction recalc_all() (suite au clic sur "Calculer") modifie l'état des données et émet le signal, garantissant une synchronisation immédiate de l'affichage. »

### calc_engine.py
Le module calc_engine.py est conçu de manière agnostique vis-à-vis de l'interface utilisateur (UI). Son périmètre est exclusivement restreint à la logique algorithmique. Cette isolation des responsabilités assure une forte réutilisabilité du code : le moteur de calcul peut être intégré au sein d'autres environnements (comme une application web) sans aucune altération du code source.

## ui
### widgets/common.py
Cette section repose sur une approche orientée composants. Elle définit la classe LabeledInput, un widget personnalisé qui encapsule le triptyque standard : libellé, champ de saisie et unité. Cette conception respecte le principe DRY (Don't Repeat Yourself) : elle évite la redondance de code lors de l'instanciation des nombreuses variables du modèle Flyback, tout en garantissant un affichage homogène.

