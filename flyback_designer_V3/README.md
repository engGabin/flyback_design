# Flyback Designer App

Professional desktop software application dedicated to the complete design and simulation of **Flyback** switched-mode power supplies (SMPS).

Designed for power electronics engineers, this software provides a step-by-step workflow to calculate electrical constraints, design the high-frequency transformer, select power components (MOSFET, diodes, capacitors), and estimate thermal losses.

---

## Main features

1. **Sidebar menu** : the left navigation bar represents the major design steps of a power supply. Follow the steps from top to bottom.
The application is designed as a chronological workflow. Follow the pages in the left sidebar from top to bottom:
1. **Input Specifications**: Defines the main electrical constraints (AC/DC input range, required output power, switching frequency, target efficiency) and computes the required *Bulk Capacitor* to ensure the Hold-up time.
2. **Structure**: allows you to visually select your primary switch architecture (e.g., *Controller + external MOSFET*, *Integrated Controller*, or *Driver + MOSFET*) as well as other component's parameters (diodes, capacitors).
3. **Pre-Design (DCM)**: calculates the fundamental magnetic constraints, including primary inductance ($L_p$), maximum peak currents, and the theoretical turns ratio to ensure operation in Discontinuous Conduction Mode (DCM).
4. **Transformer**: selects the magnetic core from the database and computes the theoretical number of turns based on the maximum allowed magnetic flux density ($B_{max}$).
5. **Transformer Calc**: refines the transformer design by adjusting the theoretical turns to integers, calculates the new exact magnetic flux, and determines the theoretical air gap length.
6. **Transformer Recap**: provides a summarized table of all final transformer parameters.
7. **Wire Sections**: computes the RMS currents and recommends the optimal wire gauges for the primary, auxiliary, and secondary windings to prevent skin effect issues.
8. **Snubber**: designs the RCD or TVS clamp network necessary to protect the primary switch from destructive voltage spikes caused by the transformer's leakage inductance.
9. **Output Stage**: configures the secondary capacitors and calculates the theoretical high-frequency output voltage ripples.
10. **Losses & Efficiency**: the final step allows you to select the exact components (MOSFETs, Diodes, Controllers) from the database and runs a deep analysis of all conduction, switching, and core losses to determine the true overall efficiency of your power supply.
11. **Mathematical Reference (Formulas)** : a dedicated tab displaying all design equations used by the software with high-quality typographic rendering.
12. **Database** : a database for the components used in Flyback converter is available and adjustable. You can add, delete, or modify components.

---

## Global architecture (MVC)

This project relies on a strict **Model-View-Controller (MVC)** architecture developed with `PyQt6`. The main objective is to completely separate the graphical interface (display) from the calculation engine (mathematics).

- **The Model (the Brain)** : completely unaware of the user interface. It takes variables, executes physical calculations, and returns results.
- **The View & Controller (the GUI)** : manages the display, captures user inputs, requests calculations from the Model, and renders the results on screen.

This separation ensures the software is robust, maintainable, and allows the calculation engine to be reused independently (e.g., for a new web-based version).

---

## Folder structure

```text
Flyback_Design_App/
│
├── README.md                       # This presentation document
├── requirements.txt                # Liste des dépedance python (PyQt6, etc.)
├── main.py                         # point d'entrer de l'application
│
├── models/                         # MOTEUR DE CALCULS & VARIABLES
│   ├── __init__.py                 # Permet d'identifier le dossier comme un package python
│   ├── component_manager.py        # Gère l'ajout et la gestion des composants
│   ├── flyback_states.py           # Contient les classes (FlybackState, FlybackResults) stockant les variables
│   ├── snubber_state.py            # Contient les classes (snubber_state, snubber_results) stockant les variables relatives au snubber
│   ├── camc_snubber.py             # Moteur contenant toutes les formules de conception du snubber
│   └── calc_engine.py              # Moteur contenant toutes les formules de conception
│
├── app/                            # INTERFACE UTILISATEUR GRAPHIQUES 
│   ├── __init__.py           
│   ├── main_window.py              # Fenêtre principale, orchestre les menus et détient la mémoire globale
│   ├── pages/                      # Dossier contenant les différentes pages de l'application
│   │   ├── __init__.py       
│   │   ├── input_specs.py          # Page des spécifications d'entrée
│   │   ├── pre_design.py           # Page de pré-conception
│   │   ├── structure.py            # Page avec la structure choisie (cascode, ...)
│   │   ├── transformer.py          # Page pour le choix du transformateur et les premières indications
│   │   ├── transformer_calc.py     # Page des calculs finaux du transformateur
│   │   ├── losses.py               # Page des pertes
│   │   ├── snubber.py              # Page du snubber
│   │   └── output_stage.py         # Page de l'étage de sortie
│   ├── tabs/                       # Onglets transversaux (Component database, Reference formulas)
│   │   ├── __init__.py      
│   │   ├── component_db.py         # Base de données des composants
│   │   ├── formulas_ref.py         # Référence des formules
│   │   └── formulas_ref_web.py     # Référence des formules en LaTeX
│   └── widgets/              
│       ├── __init__.py 
│       ├── component_dialog.py     # fenetre de dialogue pour l'ajout de composants
│       └── common.py               # "Boîte à outils": composants graphiques réutilisables
│
└── scratch/                        # Scripts utilitaires de développement
    └── gen_web.py                  # Génère le site web de l'application
```
---

## How to use the application?

The application is designed as a chronological workflow.

1. **Sidebar menu** : the left navigation bar represents the major design steps of a power supply. Follow the steps from top to bottom.
2. **Parameter input** : on each page, boxes with a darker/blue-tinted background are editable by the user. These represent the design specifications or assumptions.
3. **Applying calculations** : click the action button (e.g., *Apply and recalculate*) at the bottom of the page.
4. **Reading results** : light gray boxes contain the values computed by the software. They are read-only and serve as the foundation for the next page.

> **Tip** : if you wonder where a calculated value comes from, navigate to the **Formulas & Reference** cross-functional tab, which clearly lists all mathematical equations running in the background.


The application features a top menu bar that provides quick access to essential project management and database tools:
### File
Manages your project's state. Projects are saved as `.json` files, allowing you to share them or resume your work later.
- **New project** (`Ctrl+N`): resets the application to its  default state.
- **Open project...** (`Ctrl+O`): loads a previously saved `.json` project file.
- **Save project** (`Ctrl+S`): saves your current progress.
- **Save as...** (`Ctrl+Shift+S`): saves your progress as a new file.
- **Quit** (`Ctrl+Q`): exits the application.

### Edit
Provides tools to recalculate everything or manage the internal databases.
- **Compile** (`Ctrl+Shift+C`): forces a global recalculation of all formulas across the entire application (useful to ensure everything is up to date).
- **Add a component** / **Delete a component**: opens a dialog to manually add or remove a MOSFET, Controller, or Core from the internal JSON databases. This allows you to customize the software with your own manufacturer components

### View
Controls the graphical interface layout.
- **Show info panel** (`Ctrl+I`): toggles the right-side information dock (which displays real-time messages, warnings, and the current efficiency summary).
### Help
- **About**: displays the software's version and credits.

---


## Prerequisites and installation

**Required Software:**
- Python 3.10 or higher
- Pip (Python Package Installer)

**Installation:**
Open a terminal in the project's root folder and run the following command to install the necessary GUI and scientific libraries:
```bash
python -m pip install -r requirements.txt
```
*(Optional)* If you are using the high-quality LaTeX rendering engine, ensure you have executed `python -m pip install PyQt6-WebEngine`.

**Launch:**
To start the software, simply run the root file:
```bash
python main.py
```
