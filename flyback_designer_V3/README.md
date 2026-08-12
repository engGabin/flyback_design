# Flyback Designer App

Professional desktop software application dedicated to the complete design and simulation of **Flyback** switched-mode power supplies (SMPS).

Designed for power electronics engineers, this software provides a step-by-step workflow to calculate electrical constraints, design the high-frequency transformer, select power components (MOSFET, diodes, capacitors), and estimate thermal losses.

---

## 🎯 Main Features

- **Power Budget & Input Filter** : Calculates the *Bulk Capacitor* to meet *Hold-up time* and mains ripple constraints.
- **Pre-design (DCM)** : Computes the magnetizing inductance, theoretical turns ratio, and peak currents.
- **Semiconductor Selection** : Evaluates voltage stress ($V_{DS(max)}$, $V_{RRM}$) for the primary switch and secondary diode.
- **Detailed Transformer Design** : Fine-tunes the transformer with integer turns, calculates theoretical air gap, and provides a manufacturer summary.
- **Wire Cross-Sections** : Recommends copper sections (Litz wire / solid wire) based on current density and skin effect.
- **Losses & Efficiency Calculation** : Estimates conduction/switching losses (MOSFET), core losses (Steinmetz equation), and diode losses.
- **Protection (Clamp Circuit)** : Designs an RCD / TVS network (Snubber) to protect the transistor from leakage inductance spikes.
- **Mathematical Reference (Formulas)** : A dedicated tab displaying all design equations used by the software with high-quality typographic rendering.

---

## 🏗 Global Architecture (MVC)

This project relies on a strict **Model-View-Controller (MVC)** architecture developed with `PyQt6`. The main objective is to completely separate the graphical interface (display) from the calculation engine (mathematics).

- **The Model (The Brain)** : Completely unaware of the user interface. It takes variables, executes physical calculations, and returns results.
- **The View & Controller (UI)** : Manages the display, captures user inputs, requests calculations from the Model, and renders the results on screen.

This separation ensures the software is **robust**, **maintainable**, and allows the calculation engine to be reused independently (e.g., for a web-based version).

---

## 📂 File and Folder Organization

```text
Flyback_Design_App/
│
├── README.md                 # This presentation document
├── requirements.txt          # Python dependencies list (PyQt6, etc.)
├── main.py                   # Application entry point
│
├── models/                   # THE MODEL (Mathematical logic)
│   ├── flyback_states.py     # Contains classes (FlybackState, FlybackResults) storing variables
│   └── calc_engine.py        # Engine containing all design formulas
│
├── app/                      # THE VIEW & CONTROLLER (Graphical User Interface)
│   ├── main_window.py        # Main window, orchestrates menus and holds global memory
│   ├── pages/                # The different calculation steps (1 file = 1 UI page)
│   │   ├── input_specs.py
│   │   ├── transformer.py
│   │   └── ...
│   ├── tabs/                 # Cross-functional tabs (Component database, Reference formulas)
│   │   └── formula_ref_web.py 
│   └── widgets/              
│       └── common.py         # "Toolkit": reusable custom widgets (input fields, headers)
│
└── scratch/                  # Development utility scripts
```

### Interdependencies and Data Flow (Who commands whom?)

1. **The Orchestrator (`main_window.py`)** : Starts the application, creates the sidebar menu, and generates the `FlybackState` and `FlybackResults` memory objects. It then distributes them to all "Pages".
2. **The Workers (`app/pages/*.py`)** : When the user edits a field and clicks "Apply/Calculate", the Page reads the visual interface, updates the `FlybackState`, and **directly calls** the associated calculation function in `calc_engine.py`.
3. **The Brain (`calc_engine.py`)** : Retrieves the `FlybackState`, executes mathematical operations blindly, and updates the `FlybackResults`.
4. **Visual Update** : Once the calculation is complete, the Page regains control, reads the new values from `FlybackResults`, and refreshes the screen for the user.

---

## 🚀 How to use the application?

The application is designed as a chronological workflow.

1. **Sidebar Menu (Navigation)** : The left navigation bar represents the major design steps of a power supply. Follow the steps from top to bottom.
2. **Parameter Input** : On each page, boxes with a light (or light gray) background are editable by the user. These represent the design specifications or assumptions (frequency, voltage, safety margins).
3. **Applying Calculations** : Click the action button (e.g., *Apply and recalculate*) at the bottom of the page.
4. **Reading Results** : Darker/blue-tinted boxes contain the values computed by the software. They are read-only and serve as the foundation for the next page.

> **Tip** : If you wonder where a calculated value comes from, navigate to the **Formulas & Reference** cross-functional tab, which clearly lists all mathematical equations running in the background.

---

## 💻 Prerequisites and Installation

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
