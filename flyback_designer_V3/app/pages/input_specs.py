
from re import L
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QFrame, QVBoxLayout, QMessageBox
from PyQt6.QtCore    import Qt

from app.widgets.common import PageBase, LabeledInput, ResultRow, SectionHeader
from models.calc_engine import *

class InputSpecsPage(PageBase):

    def __init__(self, ds, res, parent=None):
        super().__init__(ds, res, title="Input specifications", parent=parent)

    def _build_ui(self):
        cl = self._content_layout

        # ------------------------------------------------------------
        # AC INPUT
        # ------------------------------------------------------------
        cl.addWidget(SectionHeader("AC input range"))

        self._vac_min = LabeledInput(
            "Minimum input voltage", "Vac",
            min_val=0, max_val=600, decimals=1, default=85.0,
            tooltip="Lowest guaranteed AC input")
        self._vac_max = LabeledInput(
            "Maximum input voltage", "Vac",
            min_val=0, max_val=800, decimals=1, default=528.0,
            tooltip="Highest AC input")
        self._f_line = LabeledInput(
            "Line frequency", "Hz",
            min_val=45, max_val=65, decimals=0, default=50.0,
            tooltip="Nominal line frequency")

        cl.addWidget(self._vac_min)
        cl.addWidget(self._vac_max)
        cl.addWidget(self._f_line)

        # ------------------------------------------------------------
        # OUTPUT
        # ------------------------------------------------------------
        cl.addWidget(SectionHeader("Output requirements"))

        self._p_out = LabeledInput(
            "Output power 1", "W",
            min_val=0, max_val=50, decimals=1, default=10.0,
            tooltip="Output power of winding 1")
        self._v_out = LabeledInput(
            "Output voltage 1", "V",
            min_val=0, max_val=100, decimals=1, default=12.0,
            tooltip="Output voltage of winding 1")
        self._delta_Vout1 = LabeledInput(
            "Output voltage ripple 1", "%",
            min_val=0, max_val=100, decimals=2, default=1.0,
            tooltip="Output voltage ripple of winding 1")
        self._p_out2 = LabeledInput(
            "Output power 2", "W",
            min_val=0, max_val=50, decimals=1, default=0.0,
            tooltip="Output power of winding 2")
        self._v_out2 = LabeledInput(
            "Output voltage 2", "V",
            min_val=0, max_val=100, decimals=1, default=0.0,
            tooltip="Output voltage of winding 2")
        self._delta_Vout2 = LabeledInput(
            "Output voltage ripple 2", "%",
            min_val=0, max_val=100, decimals=2, default=1.0,
            tooltip="Output voltage ripple of winding 2")
        self._p_aux = LabeledInput(
            "Auxiliary power", "W",
            min_val=0, max_val=50, decimals=1, default=0.0,
            tooltip="Power of auxiliary winding")
        self._v_aux = LabeledInput(
            "Auxiliary voltage", "V",
            min_val=0, max_val=100, decimals=1, default=0.0,
            tooltip="Voltage of auxiliary winding")
        self._eta = LabeledInput(
            "Target efficiency", "%",
            min_val=0, max_val=99, decimals=1, default=85.0,
            tooltip="Efficiency at full load")

        cl.addWidget(self._p_out)
        cl.addWidget(self._v_out)
        cl.addWidget(self._delta_Vout1) 
        cl.addWidget(self._p_out2)
        cl.addWidget(self._v_out2)
        cl.addWidget(self._delta_Vout2)
        cl.addWidget(self._p_aux)
        cl.addWidget(self._v_aux)
        cl.addWidget(self._eta)

        # ------------------------------------------------------------
        # BULK PARAMETERS CHOICES
        # ------------------------------------------------------------
        cl.addWidget(SectionHeader("Bulk parameters"))

        self._delta_v_bulk = LabeledInput(
            "Bulk voltage ripple", "%",
            min_val=0, max_val=100, decimals=1, default=25.0,
            tooltip="Maximum bulk voltage ripple allowed")
        self._n_H = LabeledInput(
            "Number of hold-up required", "—",
            min_val=0, max_val=5, decimals=0, default=1,
            tooltip="Number of hold-up required to meet the standards required for the project")
        
        cl.addWidget(self._delta_v_bulk)
        cl.addWidget(self._n_H)

        # ------------------------------------------------------------
        # PRE-DESIGN CHOICES
        # ------------------------------------------------------------
        cl.addWidget(SectionHeader("Pre-design choices"))

        self._f_sw = LabeledInput(
            "Switching frequency", "kHz",
            min_val=0, max_val=500, decimals=1, default=132.0)
        self._d_max = LabeledInput(
            "Maximum duty cycle", "—",
            min_val=0, max_val=1, decimals=2, default=0.62,
            tooltip="Typical 0.62–0.65 for DCM operations with wide input voltage range")
        self._k_rp = LabeledInput(
            "Ripple current coefficient", "—",
            min_val=0, max_val=1, decimals=2, default=1.00,
            tooltip="Current ripple coefficient")

        cl.addWidget(self._f_sw)
        cl.addWidget(self._d_max)
        cl.addWidget(self._k_rp)

        # ------------------------------------------------------------
        # COMPUTED RESULTS
        # ------------------------------------------------------------
        cl.addSpacing(20)

        results_frame = QFrame()
        results_frame.setObjectName("ResultsContainer")
        results_frame.setStyleSheet("""
            QFrame#ResultsContainer {
                background-color: #273A56;
                border-radius: 8px;
                border: 1px solid #3E5C76;
            }
        """)
        results_layout = QVBoxLayout(results_frame)
        results_layout.setContentsMargins(20, 16, 20, 20)
        
        results_layout.addWidget(SectionHeader("Computed"))

        self._r_i_out1  = ResultRow("Output current 1", "A",    decimals=3)
        self._r_i_out2  = ResultRow("Output current 2", "A",    decimals=3)
        self._r_i_aux  = ResultRow("Auxiliary output current", "A",    decimals=3)
        self._r_p_out_total   = ResultRow("Total output power", "W",    decimals=2)
        self._r_p_in   = ResultRow("Input power", "W",    decimals=2)
        self._r_v_in_min = ResultRow("Input voltage min", "V", decimals=1)
        self._r_v_in_max = ResultRow("Input voltage max", "V", decimals=1)

        results_layout.addWidget(self._r_i_out1)
        results_layout.addWidget(self._r_i_out2)
        results_layout.addWidget(self._r_i_aux)
        results_layout.addWidget(self._r_p_out_total)
        results_layout.addWidget(self._r_p_in)
        results_layout.addWidget(self._r_v_in_min)
        results_layout.addWidget(self._r_v_in_max)

        cl.addWidget(results_frame)

        # ------------------------------------------------------------
        # COMPUTED BULK CA  PACITANCE
        # ------------------------------------------------------------
        cl.addSpacing(20)

        bulk_frame = QFrame()
        bulk_frame.setObjectName("BulkContainer")
        bulk_frame.setStyleSheet("""
            QFrame#BulkContainer {
                background-color: #273A56;
                border-radius: 8px;
                border: 1px solid #3E5C76;
            }
        """)
        bulk_layout = QVBoxLayout(bulk_frame)
        bulk_layout.setContentsMargins(20, 16, 20, 20)
        
        bulk_layout.addWidget(SectionHeader("Bulk capacitance"))

        self._r_c_bulk_calc = ResultRow("Required bulk capacitance", "µF", decimals=2)
        self._r_c_bulk_std = ResultRow("Standard bulk capacitance", "µF", decimals=1)
        self._r_v_bulk_min = ResultRow("Bulk voltage min", "V", decimals=2)
        self._r_v_bulk_min_nH = ResultRow("Minimum bulk voltage with hold-up", "V", decimals=2)

        bulk_layout.addWidget(self._r_c_bulk_calc)
        bulk_layout.addWidget(self._r_c_bulk_std)
        bulk_layout.addWidget(self._r_v_bulk_min)
        bulk_layout.addWidget(self._r_v_bulk_min_nH)

        cl.addWidget(bulk_frame)

        # ------------------------------------------------------------
        # APPLY BUTTON
        # ------------------------------------------------------------
        btn_row = QHBoxLayout()
        # ajoute un "ressort" (un espace vide extensible) tout à gauche de cette ligne. 
        # Conséquence : tout ce qu'on ajoutera ensuite dans cette ligne sera "poussé" vers la droite. 
        # C'est l'astuce classique en Qt pour aligner un bouton à droite.
        btn_row.addStretch()
        self._btn_apply = QPushButton("Apply and recalculate")
        self._btn_apply.setStyleSheet("""
            QPushButton {
                background-color: #3E5C76;
                color: #F0EBD8;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4A6E8C;
            }
            QPushButton:pressed {
                background-color: #273A56;
            }
        """)
        self._btn_apply.clicked.connect(self._save_to_state)

        # place le bouton à l'intérieur de la ligne horizontale (à droite du "ressort")
        btn_row.addWidget(self._btn_apply)
        # prend toute cette ligne horizontale (le ressort + le bouton) et la dépose tout en bas du layout vertical principal (cl)
        cl.addLayout(btn_row)

    # ---------------------------------------------------------------- #
    def _load_from_state(self):
        ds = self.ds
        self._vac_min.value = ds.vac_min
        self._vac_max.value = ds.vac_max
        self._f_line.value  = ds.f_line
        self._p_out.value   = ds.p_out1
        self._v_out.value   = ds.v_out1
        self._eta.value     = ds.eta * 100          # stored as 0–1
        self._f_sw.value    = ds.f_sw / 1e3         # stored as Hz
        self._d_max.value   = ds.D_max
        self.refresh()
        
    def showEvent(self, event):
        super().showEvent(event)
        try:
            calc_inputPower(self.ds, self.res)
            calc_bulkCapacitance(self.res, self.ds)
            self.refresh()
        except Exception:
            pass

    # ---------------------------------------------------------------- #
    def _save_to_state(self):
        ds = self.ds
        rs = self.res
        ds.vac_min = self._vac_min.value
        ds.vac_max = self._vac_max.value
        ds.f_line  = self._f_line.value
        ds.p_out1   = self._p_out.value
        ds.v_out1   = self._v_out.value
        ds.delta_Vout1 = self._delta_Vout1.value
        ds.p_out2   = self._p_out2.value
        ds.v_out2   = self._v_out2.value
        ds.delta_Vout2 = self._delta_Vout2.value
        ds.p_aux   = self._p_aux.value
        ds.v_aux   = self._v_aux.value
        ds.eta     = self._eta.value / 100.0
        ds.delta_v_bulk = self._delta_v_bulk.value / 100.0
        ds.Nh      = self._n_H.value
        ds.f_sw    = self._f_sw.value * 1e3
        ds.D_max   = self._d_max.value
        try:
            calc_inputPower(ds)
            calc_bulkCapacitance(rs, ds)
        except Exception as e:
            QMessageBox.warning(self, "Calculation Error", f"An error occurred during calculation:\n{e}")
            return
        ds.notify("input_specs")
        self.refresh()

    # ---------------------------------------------------------------- #
    def refresh(self):
        ds = self.ds
        rs = self.res
        self._r_i_out1.set_value(ds.i_out1)
        self._r_i_out2.set_value(ds.i_out2)
        self._r_i_aux.set_value(ds.i_aux)
        self._r_p_out_total.set_value(ds.p_out_total)
        self._r_p_in.set_value(ds.p_in)
        self._r_v_in_min.set_value(ds.v_in_min)
        self._r_v_in_max.set_value(ds.v_in_max)

        self._r_c_bulk_calc.set_value(rs.c_bulk_calc * 1e6)
        self._r_c_bulk_std.set_value(rs.c_bulk_std * 1e6)
        self._r_v_bulk_min_nH.set_value(rs.v_bulk_min_nH_calc)
        self._r_v_bulk_min.set_value(rs.v_bulk_min_calc)
