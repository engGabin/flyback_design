# Flyback Designer

A Python desktop application for the systematic design of offline flyback
power supplies. Targets DCM operation over a wide input range (85–528 V AC),
with a focus on industrial applications.

---

## Architecture at a glance

```
flyback_designer/
│
├── main.py                         # Entry point (python main.py)
│
├── engine/
│   ├── design_state.py             # DesignState dataclass — single source of truth
│   ├── calc_engine.py              # Pure-Python calculation functions
│   └── __init__.py
│
├── ui/
│   ├── main_window.py              # QMainWindow: sidebar + stack + dock
│   ├── pages/
│   │   ├── input_specs.py          # ✅ Implemented — first working page
│   │   ├── stubs.py                # 🔲 All other pages (placeholder)
│   │   └── __init__.py
│   ├── tabs/
│   │   ├── formula_ref.py          # ✅ Implemented — HTML formula browser
│   │   ├── component_db.py         # ✅ Implemented — core/MOSFET/ctrl tables
│   │   └── __init__.py
│   └── widgets/
│       ├── common.py               # LabeledInput, ResultRow, PageBase, …
│       └── __init__.py
│
├── data/
│   ├── cores_db.json               # (to be added) ferrite core parameters
│   └── controllers_db.json         # (to be added) controller IC parameters
│
├── tests/
│   └── test_calc_engine.py         # (to be added)
│
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python main.py
```

---

## Key concepts

### DesignState
Every design parameter lives in `engine/design_state.py`.
Pages read from and write to this shared object.
After writing, a page calls `recalc_all(ds)` then `ds.notify("section_name")`
to trigger Qt signals that refresh downstream pages automatically.

### CalcEngine
`engine/calc_engine.py` contains pure functions — no Qt, no side effects.
Each function takes a `DesignState`, updates it in-place, and returns it.
This makes unit-testing straightforward:
```python
from engine.design_state import DesignState
from engine.calc_engine  import calc_input_stage

ds = DesignState(Vac_min=85, Vac_max=528, P_out=10, eta=0.80)
calc_input_stage(ds)
assert ds.V_bulk_min > 100
```

### PageBase
All design pages inherit from `ui/widgets/common.py::PageBase`.
Subclasses implement three methods:
- `_build_ui()`       — create widgets and add to `self._content_layout`
- `_load_from_state()` — populate widgets from `self.ds`
- `_save_to_state()`  — write fields to `self.ds`, call recalc, call notify
- `refresh()`         — called automatically via Qt signals when upstream changes

---

## Development roadmap

| Stage                  | Status   | Next step                               |
|------------------------|----------|-----------------------------------------|
| Input specifications   | ✅ Done  | Unit tests                              |
| Input stage            | 🔲 Stub  | Implement page + C_in sizing            |
| Switching structure    | 🔲 Stub  | Radio buttons + controller lookup       |
| Transformer            | 🔲 Stub  | Core selector + N_p/N_s calculator     |
| Current waveforms      | 🔲 Stub  | Matplotlib plot (DCM trapezoid)         |
| Wire sections          | 🔲 Stub  | AWG table + Litz check                  |
| Losses                 | 🔲 Stub  | Steinmetz + Rds_on breakdown            |
| Snubber                | 🔲 Stub  | RCD calculator + V_DS margin plot       |
| Output stage           | 🔲 Stub  | C_out + ripple + diode selector         |
| LTSpice integration    | 🔲 Future| NetlistGen + subprocess runner          |
| PDF / LaTeX export     | 🔲 Future| Design report generator                 |

---

## Design parameters (default values)

| Parameter | Default | Description                          |
|-----------|---------|--------------------------------------|
| Vac_min   | 85 V    | Minimum AC input                     |
| Vac_max   | 528 V   | Maximum AC input (3-phase L-N)       |
| P_out     | 10 W    | Output power                         |
| V_out     | 12 V    | Output voltage                       |
| η         | 0.80    | Target efficiency                    |
| f_sw      | 65 kHz  | Switching frequency                  |
| D_max     | 0.45    | Maximum duty cycle                   |
| t_hold    | 10 ms   | Hold-up time                         |
