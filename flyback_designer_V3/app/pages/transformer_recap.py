from models.calc_engine import *
from PyQt6.QtWidgets import (
    QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from app.widgets.common import PageBase, LabeledInput, SectionHeader, ResultRow
from PyQt6.QtGui import QFont

class TransformerRecapPage(PageBase):

    def __init__(self, ds, res, parent=None):
        super().__init__(ds, res, title="Transformer Recap", parent=parent)

    def _build_ui(self):
        cl = self._content_layout
        res = self.res
        ds = self.ds

        # ------------------------------------------------------------
        # TRANSFORMER ADJUSTMENTS (Inputs)
        # ------------------------------------------------------------
        cl.addWidget(SectionHeader("Transformer Adjustments"))
        
        self._Np = LabeledInput("Primary turns (Np)", "", decimals=2, default=11.10)
        self._Ns1 = LabeledInput("Secondary turns 1 (Ns1)", "", decimals=2, default=1.0)
        self._Ns2 = LabeledInput("Secondary turns 2 (Ns2)", "", decimals=2, default=0.0)
        self._Naux = LabeledInput("Auxiliary turns (Naux)", "", decimals=2, default=0.0)
        
        cl.addWidget(self._Np)
        cl.addWidget(self._Ns1)
        cl.addWidget(self._Ns2)
        cl.addWidget(self._Naux)
        
        # Apply Button (Right Aligned)
        cl.addSpacing(10)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        self._btn_apply = QPushButton("Apply Changes")
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
        self._btn_apply.clicked.connect(self._on_save_clicked)
        btn_row.addWidget(self._btn_apply)
        cl.addLayout(btn_row)

        # ------------------------------------------------------------
        # CORE & INDUCTANCE (Box 1)
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
        lay1.addWidget(SectionHeader("Core and Inductance"))
        
        self._r_lp_real = ResultRow("Real inductance", "µH", decimals=2)
        self._r_bmax_real = ResultRow("Maximum flux density", "T", decimals=4)
        self._r_lg = ResultRow("Air gap length", "mm", decimals=3)
        self._r_fringing = ResultRow("Fringing flux factor", "", decimals=3)
        
        lay1.addWidget(self._r_lp_real)
        lay1.addWidget(self._r_bmax_real)
        lay1.addWidget(self._r_lg)
        lay1.addWidget(self._r_fringing)
        
        cl.addWidget(box1)

        # ------------------------------------------------------------
        # WINDINGS LENGHTS (Box 1.1)
        # ------------------------------------------------------------
        cl.addSpacing(20)
        box1_1 = QFrame()
        box1_1.setObjectName("ResultsContainer1_1")
        box1_1.setStyleSheet("""
            QFrame#ResultsContainer1_1 {
                background-color: #273A56;
                border-radius: 8px;
                border: 1px solid #3E5C76;
            }
        """)
        lay1_1 = QVBoxLayout(box1_1)
        lay1_1.setContentsMargins(20, 16, 20, 20)
        lay1_1.addWidget(SectionHeader("Windings Lengths"))
        
        self._r_np_ns1 = ResultRow("Turns ratio Np/Ns1", "", decimals=3)
        self._r_np_ns2 = ResultRow("Turns ratio Np/Ns2", "", decimals=3)
        self._r_np_naux = ResultRow("Turns ratio Np/Naux", "", decimals=3)
        self._r_lp = ResultRow("Length of primary winding", "mm", decimals=3)
        self._r_ls1 = ResultRow("Length of secondary 1 winding", "mm", decimals=3)
        self._r_ls2 = ResultRow("Length of secondary 2 winding", "mm", decimals=3)
        self._r_laus = ResultRow("Length of auxiliary winding", "mm", decimals=3)

        lay1_1.addWidget(self._r_np_ns1)
        lay1_1.addWidget(self._r_np_ns2)
        lay1_1.addWidget(self._r_np_naux) 
        lay1_1.addWidget(self._r_lp)   
        lay1_1.addWidget(self._r_ls1)
        lay1_1.addWidget(self._r_ls2)
        lay1_1.addWidget(self._r_laus)  
        
        cl.addWidget(box1_1)

        # ------------------------------------------------------------
        # VOLTAGES & DUTY CYCLES (Box 2)
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
        lay2.addWidget(SectionHeader("Voltages and Duty Cycles"))
        
        self._r_vor = ResultRow("Reflected voltage", "V", decimals=2)
        self._r_vds_on = ResultRow("Switch voltage on", "V", decimals=2)
        self._r_dout = ResultRow("Secondary duty cycle", "", decimals=3)
        self._r_dm = ResultRow("Dead time duty cycle", "", decimals=3)
        
        lay2.addWidget(self._r_vor)
        lay2.addWidget(self._r_vds_on)
        lay2.addWidget(self._r_dout)
        lay2.addWidget(self._r_dm)
        
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
        
        self._r_ip_max = ResultRow("Max primary current", "A", decimals=2)
        self._r_ip_rms = ResultRow("RMS primary current", "A", decimals=2)
        self._r_ip_avg = ResultRow("Avg primary current", "A", decimals=2)
        self._r_ip_avg_on = ResultRow("Avg primary current on", "A", decimals=2)
        self._r_ip_ripple = ResultRow("Primary current ripple", "A", decimals=2)
        self._r_ip_valley = ResultRow("Primary current valley", "A", decimals=2)
        self._r_ip_dc = ResultRow("DC primary current", "A", decimals=2)
        self._r_ip_ac = ResultRow("AC primary current", "A", decimals=2)
        
        lay3.addWidget(self._r_ip_max)
        lay3.addWidget(self._r_ip_rms)
        lay3.addWidget(self._r_ip_avg)
        lay3.addWidget(self._r_ip_avg_on)
        lay3.addWidget(self._r_ip_ripple)
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
        
        self._r_is1_max = ResultRow("Max secondary current", "A", decimals=2)
        self._r_is1_rms = ResultRow("RMS secondary current", "A", decimals=2)
        self._r_is1_dc = ResultRow("DC secondary current", "A", decimals=2)
        self._r_is1_ac = ResultRow("AC secondary current", "A", decimals=2)
        self._r_i_out1 = ResultRow("Output current", "A", decimals=2)
        
        lay4.addWidget(self._r_is1_max)
        lay4.addWidget(self._r_is1_rms)
        lay4.addWidget(self._r_is1_dc)
        lay4.addWidget(self._r_is1_ac)
        lay4.addWidget(self._r_i_out1)
        
        cl.addWidget(box4)
        
        cl.addSpacing(20)

    # ---------------------------------------------------------------- #
    def _on_save_clicked(self):
        reply = QMessageBox.question(
            self, 
            "Apply Changes", 
            "Are you sure you want to apply these changes?\nThis will overwrite the current values in the Flyback state.",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        if reply == QMessageBox.StandardButton.Ok:
            self._save_to_state()
            self.refresh()

    def _load_from_state(self):
        ds = self.ds
        self._Np.value = ds.Np
        self._Ns1.value = ds.Ns1
        self._Ns2.value = ds.Ns2
        self._Naux.value = ds.Naux

    def showEvent(self, event):
        super().showEvent(event)
        from models.calc_engine import calc_flybackState
        try:
            calc_flybackState(self.ds, self.res)
            self.refresh()
        except Exception:
            pass

    def _save_to_state(self):
        ds = self.ds
        res = self.res
        ds.Np = self._Np.value
        ds.Ns1 = self._Ns1.value
        ds.Ns2 = self._Ns2.value
        ds.Naux = self._Naux.value

        try:
            calc_flybackState(ds, res)
        except Exception as e:
            QMessageBox.warning(self, "Calculation Error", f"An error occurred during calculation:\n{e}")
            return
        ds.notify("transformer_recap")
        self.refresh()

    def refresh(self):
        ds = self.ds
        # Output Box 1
        self._r_lp_real.set_value(ds.Lp_real * 1e6) # H to uH
        self._r_bmax_real.set_value(ds.B_max_real)
        self._r_lg.set_value(ds.lg)
        self._r_fringing.set_value(ds.Fringing)

        # Output Box 1_1
        self._r_np_ns1.set_value(ds.Np_Ns1)
        self._r_np_ns2.set_value(ds.Np_Ns2)
        self._r_np_naux.set_value(ds.Np_Naux)
        self._r_lp.set_value(ds.lp)
        self._r_ls1.set_value(ds.ls1)
        self._r_ls2.set_value(ds.ls2)
        self._r_laus.set_value(ds.laux)
        
        # Output Box 2
        self._r_vor.set_value(ds.vor)
        self._r_vds_on.set_value(ds.vds_on)
        self._r_dout.set_value(ds.D_out)
        self._r_dm.set_value(ds.D_m)
        
        # Output Box 3
        self._r_ip_max.set_value(ds.i_p_max)
        self._r_ip_rms.set_value(ds.i_p_rms)
        self._r_ip_avg.set_value(ds.i_p_avg)
        self._r_ip_avg_on.set_value(ds.i_p_avg_on)
        self._r_ip_ripple.set_value(ds.delta_i_p)
        self._r_ip_valley.set_value(ds.i_p_valley)
        self._r_ip_dc.set_value(ds.i_p_dc)
        self._r_ip_ac.set_value(ds.i_p_ac)
        
        # Output Box 4
        self._r_is1_max.set_value(ds.i_s1_max)
        self._r_is1_rms.set_value(ds.i_s1_rms)
        self._r_is1_dc.set_value(ds.i_s1_dc)
        self._r_is1_ac.set_value(ds.i_s1_ac)
        self._r_i_out1.set_value(ds.i_out1)
