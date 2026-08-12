from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QFrame, QVBoxLayout, QMessageBox
from PyQt6.QtCore    import Qt

from app.widgets.common import PageBase, LabeledInput, ResultRow, SectionHeader
from models.calc_engine import calc_preDesign_transformer

class PreDesignPage(PageBase):

    def __init__(self, ds, res, parent=None):
        super().__init__(ds, res, title="Pre-Design Calculations", parent=parent)

    def _build_ui(self):
        cl = self._content_layout
        res = self.res
        ds = self.ds

        # ------------------------------------------------------------
        # PRE-DESIGN CHOICES (Inputs)
        # ------------------------------------------------------------
        cl.addWidget(SectionHeader("Pre-design section"))

        self._d_max = LabeledInput(
            "Maximum duty cycle", "",
            min_val=0.01, max_val=0.99, decimals=2, default=0.61,
            tooltip="D_max")
        self._f_sw = LabeledInput(
            "Switching frequency", "kHz",
            min_val=10, max_val=500, decimals=1, default=132.0,
            tooltip="f_sw")
        self._krp = LabeledInput(
            "Ripple factor (Krp)", "",
            min_val=0.01, max_val=1.0, decimals=2, default=1.0,
            tooltip="1 for DCM, <1 for CCM")
        self._j_max = LabeledInput(
            "Max current density", "A/mm²",
            min_val=0.01, max_val=20, decimals=2, default=6.0,
            tooltip="J_max")
        self._b_max = LabeledInput(
            "Max flux density", "T",
            min_val=0.01, max_val=1.0, decimals=4, default=0.3092,
            tooltip="B_max")
        self._ku = LabeledInput(
            "Window utilization factor", "",
            min_val=0.01, max_val=1.0, decimals=2, default=0.4,
            tooltip="Ku")
        self._c_bulk = LabeledInput(
            "Chosen bulk capacitance", "µF",
            min_val=0.00, max_val=1000, decimals=2, default=0.0,
            tooltip="Actual value selected for the capacitor")

        cl.addWidget(self._d_max)
        cl.addWidget(self._f_sw)
        cl.addWidget(self._krp)
        cl.addWidget(self._j_max)
        cl.addWidget(self._b_max)
        cl.addWidget(self._ku)
        cl.addWidget(self._c_bulk)

        # ------------------------------------------------------------
        # TRANSFORMER PRE-DESIGN (Box 1)
        # ------------------------------------------------------------
        cl.addSpacing(20)
        box1 = QFrame()
        box1.setObjectName("ResultsContainer1")
        box1.setStyleSheet("""
            QFrame#ResultsContainer1 {
                background-color: #273A56;
                border-radius: 8px;
                border: 1px solid #3E5C76;
            }
        """)
        lay1 = QVBoxLayout(box1)
        lay1.setContentsMargins(20, 16, 20, 20)
        lay1.addWidget(SectionHeader("Transformer Requirements"))

        self._r_lp = ResultRow("Primary inductance", "µH", decimals=2, tooltip="Lp")
        self._r_Np_Ns1 = ResultRow("Turns ratio primary to secondary 1", "", decimals=2, tooltip="Np_Ns1")
        self._r_aeaw = ResultRow("Area product", "cm⁴", decimals=4, tooltip="AeAw")
        
        lay1.addWidget(self._r_lp)   
        lay1.addWidget(self._r_Np_Ns1)
        lay1.addWidget(self._r_aeaw)
        cl.addWidget(box1)

        # ------------------------------------------------------------
        # VOLTAGES (Box 2)
        # ------------------------------------------------------------
        cl.addSpacing(20)
        box2 = QFrame()
        box2.setObjectName("ResultsContainer2")
        box2.setStyleSheet("""
            QFrame#ResultsContainer2 {
                background-color: #273A56;
                border-radius: 8px;
                border: 1px solid #3E5C76;
            }
        """)
        lay2 = QVBoxLayout(box2)
        lay2.setContentsMargins(20, 16, 20, 20)
        lay2.addWidget(SectionHeader("Voltages"))

        self._r_v_bulk_min = ResultRow("Minimum bulk voltage", "V", decimals=2, tooltip="v_bulk_min")
        self._r_v_bulk_min_nh = ResultRow("Min bulk voltage (with hold-up)", "V", decimals=2, tooltip="v_bulk_min_nH")
        self._r_vor = ResultRow("Reflected voltage", "V", decimals=2, tooltip="vor_calc")
        lay2.addWidget(self._r_v_bulk_min)
        lay2.addWidget(self._r_v_bulk_min_nh)
        lay2.addWidget(self._r_vor)
        cl.addWidget(box2)

        # ------------------------------------------------------------
        # PRIMARY CURRENTS (Box 3)
        # ------------------------------------------------------------
        cl.addSpacing(20)
        box3 = QFrame()
        box3.setObjectName("ResultsContainer3")
        box3.setStyleSheet("""
            QFrame#ResultsContainer3 {
                background-color: #273A56;
                border-radius: 8px;
                border: 1px solid #3E5C76;
            }
        """)
        lay3 = QVBoxLayout(box3)
        lay3.setContentsMargins(20, 16, 20, 20)
        lay3.addWidget(SectionHeader("Primary Currents"))

        self._r_ip_max = ResultRow("Maximum current (I_p_max)", "A", decimals=3)
        self._r_ip_rms = ResultRow("RMS current (I_p_rms)", "A", decimals=3)
        self._r_ip_avg = ResultRow("Average current (I_p_avg)", "A", decimals=3)
        self._r_ip_avg_on = ResultRow("Average current when ON", "A", decimals=3)
        self._r_ip_delta = ResultRow("Current ripple (delta_I_p)", "A", decimals=3)
        self._r_ip_valley = ResultRow("Current valley (I_p_valley)", "A", decimals=3)
        self._r_ip_dc = ResultRow("DC component (I_p_dc)", "A", decimals=3)
        self._r_ip_ac = ResultRow("AC component (I_p_ac)", "A", decimals=3)

        lay3.addWidget(self._r_ip_max)
        lay3.addWidget(self._r_ip_rms)
        lay3.addWidget(self._r_ip_avg)
        lay3.addWidget(self._r_ip_avg_on)
        lay3.addWidget(self._r_ip_delta)
        lay3.addWidget(self._r_ip_valley)
        lay3.addWidget(self._r_ip_dc)
        lay3.addWidget(self._r_ip_ac)
        cl.addWidget(box3)

        # ------------------------------------------------------------
        # SECONDARY CURRENTS (Box 4)
        # ------------------------------------------------------------
        cl.addSpacing(20)
        box4 = QFrame()
        box4.setObjectName("ResultsContainer4")
        box4.setStyleSheet("""
            QFrame#ResultsContainer4 {
                background-color: #273A56;
                border-radius: 8px;
                border: 1px solid #3E5C76;
            }
        """)
        lay4 = QVBoxLayout(box4)
        lay4.setContentsMargins(20, 16, 20, 20)
        lay4.addWidget(SectionHeader("Secondary Currents"))

        self._r_is_max = ResultRow("Maximum current (I_s_max)", "A", decimals=3)
        self._r_is_rms = ResultRow("RMS current (I_s_rms)", "A", decimals=3)
        self._r_iout1 = ResultRow("Output 1 current", "A", decimals=3)
        self._r_iout2 = ResultRow("Output 2 current", "A", decimals=3)
        self._r_iaux = ResultRow("Auxiliary current", "A", decimals=3)

        lay4.addWidget(self._r_is_max)
        lay4.addWidget(self._r_is_rms)
        lay4.addWidget(self._r_iout1)
        lay4.addWidget(self._r_iout2)
        lay4.addWidget(self._r_iaux)
        cl.addWidget(box4)

        # ------------------------------------------------------------
        # APPLY BUTTON
        # ------------------------------------------------------------
        cl.addSpacing(10)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        btn = QPushButton("Apply and recalculate")
        btn.setStyleSheet("""
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
        btn.clicked.connect(self._save_to_state)
        btn_row.addWidget(btn)
        cl.addLayout(btn_row)

    # ---------------------------------------------------------------- #
    def _load_from_state(self):
        ds = self.ds
        self._d_max.value = ds.D_max
        self._f_sw.value = ds.f_sw / 1e3
        self._krp.value = ds.Krp
        self._j_max.value = ds.J_max
        self._b_max.value = ds.B_max
        self._ku.value = ds.Ku
        
        # Default to the calculated required capacitance if the user hasn't chosen one yet
        if ds.c_bulk == 0.0:
            self._c_bulk.value = self.res.c_bulk_calc * 1e6
        else:
            self._c_bulk.value = ds.c_bulk * 1e6
            
        self.refresh()

    def showEvent(self, event):
        super().showEvent(event)
        from models.calc_engine import calc_preDesign_transformer
        try:
            self.ds.c_bulk = self._c_bulk.value * 1e-6
            calc_preDesign_transformer(self.ds, self.res)
            self.refresh()
        except Exception:
            pass

    # ---------------------------------------------------------------- #
    def _save_to_state(self):
        ds = self.ds
        res = self.res

        ds.D_max = self._d_max.value
        ds.f_sw = self._f_sw.value * 1e3
        ds.Krp = self._krp.value
        ds.J_max = self._j_max.value
        ds.B_max = self._b_max.value
        ds.Ku = self._ku.value
        ds.c_bulk = self._c_bulk.value * 1e-6

        try:
            calc_preDesign_transformer(ds, res)
        except Exception as e:
            QMessageBox.warning(self, "Calculation Error", f"An error occurred during calculation:\n{e}")
            return

        ds.notify("input_stage")
        self.refresh()

    # ---------------------------------------------------------------- #
    def refresh(self):
        ds = self.ds
        res = self.res

        # Box 1
        self._r_lp.set_value(res.Lp_calc * 1e6) # H -> uH
        self._r_aeaw.set_value(res.AeAw_calc * 1e6) # Assuming it's m4 -> mm4 (1m4 = 1e6 mm4)
        self._r_Np_Ns1.set_value(res.Np_Ns1_calc)

        # Box 2
        self._r_v_bulk_min.set_value(ds.v_bulk_min)
        self._r_v_bulk_min_nh.set_value(ds.v_bulk_min_nH)
        self._r_vor.set_value(res.vor_calc)

        # Box 3
        self._r_ip_max.set_value(res.i_p_max_calc)
        self._r_ip_rms.set_value(res.i_p_rms_calc)
        self._r_ip_avg.set_value(res.i_p_avg_calc)
        self._r_ip_avg_on.set_value(res.i_p_avg_on_calc)
        self._r_ip_delta.set_value(res.delta_i_p_calc)
        self._r_ip_valley.set_value(res.i_p_valley_calc)
        self._r_ip_dc.set_value(res.i_p_dc_calc)
        self._r_ip_ac.set_value(res.i_p_ac_calc)

        # Box 4
        self._r_is_max.set_value(res.i_s_max_calc)
        self._r_is_rms.set_value(res.i_s_rms_calc)
        self._r_iout1.set_value(ds.i_out1)
        self._r_iout2.set_value(ds.i_out2)
        self._r_iaux.set_value(ds.i_aux)
