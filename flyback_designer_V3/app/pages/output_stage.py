from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from app.widgets.common import PageBase, LabeledInput, ResultRow, SectionHeader

class OutputStagePage(PageBase):

    def __init__(self, ds, res, parent=None):
        super().__init__(ds, res, title="Output Stage", parent=parent)

    def _build_ui(self):
        cl = self._content_layout

        # ------------------------------------------------------------
        # OUTPUT: Recommended Capacitances
        # ------------------------------------------------------------
        box_rec = QFrame()
        box_rec.setObjectName("ResultsContainerRec")
        box_rec.setStyleSheet("QFrame#ResultsContainerRec { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_rec = QVBoxLayout(box_rec)
        lay_rec.setContentsMargins(20, 16, 20, 20)
        lay_rec.addWidget(SectionHeader("Recommended Output Capacitance"))

        self._r_cout1 = ResultRow("Output 1 Capacitance", "µF", decimals=2)
        self._r_cout1_esr = ResultRow("Maximal ESR for the capacitance of Output 1", "mΩ", decimals=2)
        self._r_cout2 = ResultRow("Output 2 Capacitance", "µF", decimals=2)
        self._r_cout2_esr = ResultRow("Maximal ESR for the capacitance of Output 2", "mΩ", decimals=2)

        lay_rec.addWidget(self._r_cout1)
        lay_rec.addWidget(self._r_cout1_esr)
        lay_rec.addWidget(self._r_cout2)
        lay_rec.addWidget(self._r_cout2_esr)
        
        cl.addWidget(box_rec)
        cl.addSpacing(20)

        # ------------------------------------------------------------
        # INPUTS: Chosen Capacitances
        # ------------------------------------------------------------
        cl.addWidget(SectionHeader("Chosen Output Capacitances (Datasheet)"))
        
        self._in_cout1 = LabeledInput("Chosen Output 1 Capacitance", "µF", decimals=2, default=1000.0)
        self._in_cout1_esr = LabeledInput("Chosen Output 1 ESR", "mΩ", decimals=2, default=50.0)
        self._in_cout2 = LabeledInput("Chosen Output 2 Capacitance", "µF", decimals=2, default=100.0)
        self._in_cout2_esr = LabeledInput("Chosen Output 2 ESR", "mΩ", decimals=2, default=50.0)

        inputs = [self._in_cout1, self._in_cout1_esr, self._in_cout2, self._in_cout2_esr]
        for inp in inputs:
            cl.addWidget(inp)
        
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        btn = QPushButton("Calculate Ripples")
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
        cl.addSpacing(20)

        # ------------------------------------------------------------
        # OUTPUT: Calculated Ripples
        # ------------------------------------------------------------
        box_rip = QFrame()
        box_rip.setObjectName("ResultsContainerRip")
        box_rip.setStyleSheet("QFrame#ResultsContainerRip { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_rip = QVBoxLayout(box_rip)
        lay_rip.setContentsMargins(20, 16, 20, 20)
        lay_rip.addWidget(SectionHeader("Calculated Output Voltage Ripples"))

        self._r_rip1 = ResultRow("Output 1 Ripple", "V", decimals=3)
        self._r_rip2 = ResultRow("Output 2 Ripple", "V", decimals=3)

        lay_rip.addWidget(self._r_rip1)
        lay_rip.addWidget(self._r_rip2)
        
        cl.addWidget(box_rip)
        cl.addSpacing(20)

    def showEvent(self, event):
        super().showEvent(event)
        from models.calc_engine import calc_output_capacitance
        try:
            calc_output_capacitance(self.ds, self.res)
        except Exception:
            pass
        self.refresh()

    def _load_from_state(self):
        ds = self.ds
        res = self.res
        from models.calc_engine import calc_output_capacitance
        try:
            calc_output_capacitance(ds, res)
        except Exception as e:
            QMessageBox.warning(self, "Calculation Error", f"An error occurred during calculation of the output capacitances:\n{e}")
            return

        if ds.C_out1 > 0: self._in_cout1.value = ds.C_out1 * 1e6
        elif res.C_out1 > 0: self._in_cout1.value = res.C_out1 * 1e6
        
        if ds.C_out1_esr > 0: self._in_cout1_esr.value = ds.C_out1_esr * 1e3
        elif res.C_out1_esr > 0: self._in_cout1_esr.value = res.C_out1_esr * 1e3
        
        if ds.C_out2 > 0: self._in_cout2.value = ds.C_out2 * 1e6
        elif res.C_out2 > 0: self._in_cout2.value = res.C_out2 * 1e6
        
        if ds.C_out2_esr > 0: self._in_cout2_esr.value = ds.C_out2_esr * 1e3
        elif res.C_out2_esr > 0: self._in_cout2_esr.value = res.C_out2_esr * 1e3

    def _save_to_state(self):
        ds = self.ds
        ds.C_out1 = self._in_cout1.value * 1e-6
        ds.C_out1_esr = self._in_cout1_esr.value * 1e-3
        ds.C_out2 = self._in_cout2.value * 1e-6
        ds.C_out2_esr = self._in_cout2_esr.value * 1e-3

        from models.calc_engine import calc_output_voltages
        try:
            calc_output_voltages(ds, self.res)
        except Exception as e:
            QMessageBox.warning(self, "Calculation Error", f"An error occurred during calculation of the output voltages ripples:\n{e}")
            return
            
        ds.notify("output_stage")
        self.refresh()

    def refresh(self):
        res = self.res
        ds = self.ds
        
        self._r_cout1.set_value(res.C_out1 * 1e6)
        self._r_cout1_esr.set_value(res.C_out1_esr * 1e3)
        self._r_cout2.set_value(res.C_out2 * 1e6)
        self._r_cout2_esr.set_value(res.C_out2_esr * 1e3)

        self._r_rip1.set_value(ds.ripple_v1_calc)
        self._r_rip2.set_value(ds.ripple_v2_calc)
