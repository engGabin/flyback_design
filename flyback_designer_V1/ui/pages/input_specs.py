"""
pages/input_specs.py — Input Specifications page.

User enters: Vac_min, Vac_max, f_line, P_out, V_out, eta, f_sw, D_max.
On any change the full calc chain is triggered via recalc_all().
Computed I_out and P_in are shown as read-only results.
"""

from PyQt6.QtWidgets import QPushButton, QHBoxLayout
from PyQt6.QtCore    import Qt

from ..widgets.common import PageBase, LabeledInput, ResultRow, SectionHeader
from engine.calc_engine import recalc_all


class InputSpecsPage(PageBase):

    def __init__(self, ds, parent=None):
        super().__init__(ds, title="Input specifications", parent=parent)

    # ---------------------------------------------------------------- #
    def _build_ui(self):
        cl = self._content_layout

        # ── AC input ────────────────────────────────────────────────
        cl.addWidget(SectionHeader("AC input range"))

        self._vac_min = LabeledInput(
            "Minimum input voltage  V_ac_min", "V AC",
            min_val=0, max_val=600, decimals=1, default=85.0,
            tooltip="Lowest guaranteed AC input (e.g. 85 V for universal range)")
        self._vac_max = LabeledInput(
            "Maximum input voltage  V_ac_max", "V AC",
            min_val=0, max_val=800, decimals=1, default=528.0,
            tooltip="Highest AC input — 528 V covers 3-phase 400 V L-N peak")
        self._f_line = LabeledInput(
            "Line frequency  f_line", "Hz",
            min_val=45, max_val=65, decimals=0, default=50.0)

        cl.addWidget(self._vac_min)
        cl.addWidget(self._vac_max)
        cl.addWidget(self._f_line)

        # ── Output ──────────────────────────────────────────────────
        cl.addWidget(SectionHeader("Output requirements"))

        self._p_out = LabeledInput(
            "Output power  P_out", "W",
            min_val=0.1, max_val=500, decimals=1, default=10.0)
        self._v_out = LabeledInput(
            "Output voltage  V_out", "V DC",
            min_val=1, max_val=400, decimals=2, default=12.0)
        self._eta = LabeledInput(
            "Target efficiency  η", "%",
            min_val=50, max_val=99, decimals=1, default=80.0,
            tooltip="Used to size input capacitor and estimate losses")

        cl.addWidget(self._p_out)
        cl.addWidget(self._v_out)
        cl.addWidget(self._eta)

        # ── Switching ───────────────────────────────────────────────
        cl.addWidget(SectionHeader("Switching parameters"))

        self._f_sw = LabeledInput(
            "Switching frequency  f_sw", "kHz",
            min_val=20, max_val=500, decimals=1, default=65.0)
        self._d_max = LabeledInput(
            "Maximum duty cycle  D_max", "—",
            min_val=0.1, max_val=0.7, decimals=2, default=0.45,
            tooltip="Typical 0.40–0.45 for flyback DCM; limits at Vbulk_min")

        cl.addWidget(self._f_sw)
        cl.addWidget(self._d_max)

        # ── Computed results ────────────────────────────────────────
        cl.addWidget(SectionHeader("Computed"))

        self._r_i_out  = ResultRow("Output current  I_out",  "A",    decimals=3)
        self._r_p_in   = ResultRow("Input power  P_in",      "W",    decimals=2)
        self._r_vb_min = ResultRow("Bulk voltage min  V_bulk_min", "V", decimals=1)
        self._r_vb_max = ResultRow("Bulk voltage max  V_bulk_max", "V", decimals=1)

        cl.addWidget(self._r_i_out)
        cl.addWidget(self._r_p_in)
        cl.addWidget(self._r_vb_min)
        cl.addWidget(self._r_vb_max)

        # ── Apply button ────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self._btn_apply = QPushButton("Apply & recalculate")
        self._btn_apply.setFixedWidth(180)
        self._btn_apply.clicked.connect(self._save_to_state)
        btn_row.addWidget(self._btn_apply)
        cl.addLayout(btn_row)

    # ---------------------------------------------------------------- #
    def _load_from_state(self):
        ds = self.ds
        self._vac_min.value = ds.Vac_min
        self._vac_max.value = ds.Vac_max
        self._f_line.value  = ds.f_line
        self._p_out.value   = ds.P_out
        self._v_out.value   = ds.V_out
        self._eta.value     = ds.eta * 100          # stored as 0–1
        self._f_sw.value    = ds.f_sw / 1e3         # stored as Hz
        self._d_max.value   = ds.D_max
        self.refresh()

    # ---------------------------------------------------------------- #
    def _save_to_state(self):
        ds = self.ds
        ds.Vac_min = self._vac_min.value
        ds.Vac_max = self._vac_max.value
        ds.f_line  = self._f_line.value
        ds.P_out   = self._p_out.value
        ds.V_out   = self._v_out.value
        ds.eta     = self._eta.value / 100.0
        ds.f_sw    = self._f_sw.value * 1e3
        ds.D_max   = self._d_max.value
        ds.I_out   = ds.P_out / max(ds.V_out, 0.001)
        recalc_all(ds)
        ds.notify("input_specs")
        self.refresh()

    # ---------------------------------------------------------------- #
    def refresh(self):
        ds = self.ds
        self._r_i_out.set_value(ds.I_out)
        self._r_p_in.set_value(ds.P_in)
        self._r_vb_min.set_value(ds.V_bulk_min)
        self._r_vb_max.set_value(ds.V_bulk_max)
