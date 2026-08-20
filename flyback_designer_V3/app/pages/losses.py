"""
pages/losses.py
"""

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from app.widgets.common import PageBase, SectionHeader, ResultRow
from models.calc_engine import calc_mosfet_losses, calc_diode_losses, calc_pfe_losses, calc_capacitor_losses, snubber_losses

class LossesPage(PageBase):
    def _build_ui(self):
        # ---------------------------------------------------------
        # MOSFET Losses Box
        # ---------------------------------------------------------
        self.box_mosfet = QFrame()
        self.box_mosfet.setObjectName("BoxLossesMosfet")
        self.box_mosfet.setStyleSheet("QFrame#BoxLossesMosfet { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_mosfet = QVBoxLayout(self.box_mosfet)
        lay_mosfet.setContentsMargins(20, 16, 20, 20)
        
        lay_mosfet.addWidget(SectionHeader("MOSFET Losses", center=True))
        
        self.res_P_cond = ResultRow("Conduction losses", "W")
        self.res_P_sw = ResultRow("Switching losses", "W")
        self.res_P_mosfet = ResultRow("Total losses", "W")
        
        lay_mosfet.addWidget(self.res_P_cond)
        lay_mosfet.addWidget(self.res_P_sw)
        lay_mosfet.addWidget(self.res_P_mosfet)
        
        lay_btn_mosfet = QHBoxLayout()
        lay_btn_mosfet.addStretch()
        self.btn_calc_mosfet = QPushButton("Calculate MOSFET Losses")
        self.btn_calc_mosfet.setStyleSheet(
            "QPushButton { background-color: #3E5C76; color: #F0EBD8; border-radius: 4px; padding: 6px 12px; font-weight: bold; } "
            "QPushButton:hover { background-color: #4A6E8C; }"
        )
        self.btn_calc_mosfet.clicked.connect(self._on_calc_mosfet)
        lay_btn_mosfet.addWidget(self.btn_calc_mosfet)
        lay_mosfet.addLayout(lay_btn_mosfet)
        
        self._content_layout.addWidget(self.box_mosfet)
        self._content_layout.addSpacing(10)
        
        # ---------------------------------------------------------
        # Controller
        # ---------------------------------------------------------
        self.box_ctrl = QFrame()
        self.box_ctrl.setObjectName("BoxLossesCtrl")
        self.box_ctrl.setStyleSheet("QFrame#BoxLossesCtrl { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_ctrl = QVBoxLayout(self.box_ctrl)
        lay_ctrl.setContentsMargins(20, 16, 20, 20)
        lay_ctrl.addWidget(SectionHeader("Controller Losses", center=True))
        
        self.res_ctrl_cond = ResultRow("Conduction losses", "W")
        self.res_ctrl_sw = ResultRow("Switching losses", "W")
        self.res_ctrl_tot = ResultRow("Total losses", "W")
        lay_ctrl.addWidget(self.res_ctrl_cond)
        lay_ctrl.addWidget(self.res_ctrl_sw)
        lay_ctrl.addWidget(self.res_ctrl_tot)
        
        lay_btn_ctrl = QHBoxLayout()
        lay_btn_ctrl.addStretch()
        self.btn_calc_ctrl = QPushButton("Calculate Controller Losses")
        self.btn_calc_ctrl.setStyleSheet(
            "QPushButton { background-color: #3E5C76; color: #F0EBD8; border-radius: 4px; padding: 6px 12px; font-weight: bold; } "
            "QPushButton:hover { background-color: #4A6E8C; }"
        )
        self.btn_calc_ctrl.clicked.connect(self._on_calc_ctrl)
        lay_btn_ctrl.addWidget(self.btn_calc_ctrl)
        lay_ctrl.addLayout(lay_btn_ctrl)
        
        self._content_layout.addWidget(self.box_ctrl)
        self._content_layout.addSpacing(10)

        # ---------------------------------------------------------
        # Input Capacitor (Bulk)
        # ---------------------------------------------------------
        self.box_c_in = QFrame()
        self.box_c_in.setObjectName("BoxLossesCIn")
        self.box_c_in.setStyleSheet("QFrame#BoxLossesCIn { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_c_in = QVBoxLayout(self.box_c_in)
        lay_c_in.setContentsMargins(20, 16, 20, 20)
        lay_c_in.addWidget(SectionHeader("Bulk capacitor losses", center=True))
        
        self.res_c_bulk = ResultRow("Capacitor losses", "W")
        lay_c_in.addWidget(self.res_c_bulk)
        
        lay_btn_c_in = QHBoxLayout()
        lay_btn_c_in.addStretch()
        self.btn_calc_c_in = QPushButton("Calculate Capacitor Losses")
        self.btn_calc_c_in.setStyleSheet(
            "QPushButton { background-color: #3E5C76; color: #F0EBD8; border-radius: 4px; padding: 6px 12px; font-weight: bold; } "
            "QPushButton:hover { background-color: #4A6E8C; }"
        )
        self.btn_calc_c_in.clicked.connect(self._on_calc_c_in)
        lay_btn_c_in.addWidget(self.btn_calc_c_in)
        lay_c_in.addLayout(lay_btn_c_in)
        
        self._content_layout.addWidget(self.box_c_in)
        self._content_layout.addSpacing(10)

        # ---------------------------------------------------------
        # Output Stage 1
        # ---------------------------------------------------------
        self.box_out1 = QFrame()
        self.box_out1.setObjectName("BoxLossesOut1")
        self.box_out1.setStyleSheet("QFrame#BoxLossesOut1 { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_out1 = QVBoxLayout(self.box_out1)
        lay_out1.setContentsMargins(20, 16, 20, 20)
        lay_out1.addWidget(SectionHeader("Losses of the first output stage", center=True))
        
        self.res_d1_cond = ResultRow("Diode conduction losses", "W")
        self.res_d1_sw = ResultRow("Diode switching losses", "W")
        self.res_d1_tot = ResultRow("Total diode 1 losses", "W")
        lay_out1.addWidget(self.res_d1_cond)
        lay_out1.addWidget(self.res_d1_sw)
        lay_out1.addWidget(self.res_d1_tot)
        
        self.res_c1_out1_tot = ResultRow("Capacitor 1 losses", "W")
        self.res_c2_out1_tot = ResultRow("Capacitor 2 losses", "W")
        lay_out1.addWidget(self.res_c1_out1_tot)
        lay_out1.addWidget(self.res_c2_out1_tot)
        
        lay_btn_out1 = QHBoxLayout()
        lay_btn_out1.addStretch()
        self.btn_calc_out1 = QPushButton("Calculate First Output Losses")
        self.btn_calc_out1.setStyleSheet(
            "QPushButton { background-color: #3E5C76; color: #F0EBD8; border-radius: 4px; padding: 6px 12px; font-weight: bold; } "
            "QPushButton:hover { background-color: #4A6E8C; }"
        )
        self.btn_calc_out1.clicked.connect(self._on_calc_out1)
        lay_btn_out1.addWidget(self.btn_calc_out1)
        lay_out1.addLayout(lay_btn_out1)
        
        self._content_layout.addWidget(self.box_out1)
        self._content_layout.addSpacing(10)

        # ---------------------------------------------------------
        # Output 2 Diode & Capacitors
        # ---------------------------------------------------------
        self.box_d2 = QFrame()
        # ---------------------------------------------------------
        # Output Stage 2
        # ---------------------------------------------------------
        self.box_out2 = QFrame()
        self.box_out2.setObjectName("BoxLossesOut2")
        self.box_out2.setStyleSheet("QFrame#BoxLossesOut2 { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_out2 = QVBoxLayout(self.box_out2)
        lay_out2.setContentsMargins(20, 16, 20, 20)
        lay_out2.addWidget(SectionHeader("Losses of the second output stage", center=True))
        
        self.res_d2_cond = ResultRow("Diode conduction losses", "W")
        self.res_d2_sw = ResultRow("Diode switching losses", "W")
        self.res_d2_tot = ResultRow("Total diode 2 losses", "W")
        lay_out2.addWidget(self.res_d2_cond)
        lay_out2.addWidget(self.res_d2_sw)
        lay_out2.addWidget(self.res_d2_tot)
        
        self.res_c1_out2_tot = ResultRow("Capacitor 1 losses", "W")
        self.res_c2_out2_tot = ResultRow("Capacitor 2 losses", "W")
        lay_out2.addWidget(self.res_c1_out2_tot)
        lay_out2.addWidget(self.res_c2_out2_tot)
        
        lay_btn_out2 = QHBoxLayout()
        lay_btn_out2.addStretch()
        self.btn_calc_out2 = QPushButton("Calculate Second Output Losses")
        self.btn_calc_out2.setStyleSheet(
            "QPushButton { background-color: #3E5C76; color: #F0EBD8; border-radius: 4px; padding: 6px 12px; font-weight: bold; } "
            "QPushButton:hover { background-color: #4A6E8C; }"
        )
        self.btn_calc_out2.clicked.connect(self._on_calc_out2)
        lay_btn_out2.addWidget(self.btn_calc_out2)
        lay_out2.addLayout(lay_btn_out2)
        
        self._content_layout.addWidget(self.box_out2)
        self._content_layout.addSpacing(10)

        # ---------------------------------------------------------
        # Snubber Diode & Snubber
        # ---------------------------------------------------------
        self.box_sn_diode = QFrame()
        self.box_sn_diode.setObjectName("BoxLossesSnDiode")
        self.box_sn_diode.setStyleSheet("QFrame#BoxLossesSnDiode { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_sn_diode = QVBoxLayout(self.box_sn_diode)
        lay_sn_diode.setContentsMargins(20, 16, 20, 20)
        lay_sn_diode.addWidget(SectionHeader("Snubber Diode Losses", center=True))
        
        self.res_sn_diode_cond = ResultRow("Conduction losses", "W")
        self.res_sn_diode_sw = ResultRow("Switching losses", "W")
        self.res_sn_diode_tot = ResultRow("Total diode snubber losses", "W")
        lay_sn_diode.addWidget(self.res_sn_diode_cond)
        lay_sn_diode.addWidget(self.res_sn_diode_sw)
        lay_sn_diode.addWidget(self.res_sn_diode_tot)
        
        lay_btn_sn_diode = QHBoxLayout()
        lay_btn_sn_diode.addStretch()
        self.btn_calc_sn_diode = QPushButton("Calculate Snubber Diode Losses")
        self.btn_calc_sn_diode.setStyleSheet(
            "QPushButton { background-color: #3E5C76; color: #F0EBD8; border-radius: 4px; padding: 6px 12px; font-weight: bold; } "
            "QPushButton:hover { background-color: #4A6E8C; }"
        )
        self.btn_calc_sn_diode.clicked.connect(self._on_calc_sn_diode)
        lay_btn_sn_diode.addWidget(self.btn_calc_sn_diode)
        lay_sn_diode.addLayout(lay_btn_sn_diode)
        
        self._content_layout.addWidget(self.box_sn_diode)
        self._content_layout.addSpacing(10)

        self.box_snubber = QFrame()
        self.box_snubber.setObjectName("BoxLossesSnubber")
        self.box_snubber.setStyleSheet("QFrame#BoxLossesSnubber { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_snubber = QVBoxLayout(self.box_snubber)
        lay_snubber.setContentsMargins(20, 16, 20, 20)
        lay_snubber.addWidget(SectionHeader("Snubber Circuit Losses", center=True))
        
        self.res_snubber_tot = ResultRow("Snubber losses", "W")
        lay_snubber.addWidget(self.res_snubber_tot)
        
        lay_btn_snubber = QHBoxLayout()
        lay_btn_snubber.addStretch()
        self.btn_calc_snubber = QPushButton("Calculate Snubber Losses")
        self.btn_calc_snubber.setStyleSheet(
            "QPushButton { background-color: #3E5C76; color: #F0EBD8; border-radius: 4px; padding: 6px 12px; font-weight: bold; } "
            "QPushButton:hover { background-color: #4A6E8C; }"
        )
        self.btn_calc_snubber.clicked.connect(self._on_calc_snubber)
        lay_btn_snubber.addWidget(self.btn_calc_snubber)
        lay_snubber.addLayout(lay_btn_snubber)
        
        self._content_layout.addWidget(self.box_snubber)
        self._content_layout.addSpacing(10)
        
        self._content_layout.addStretch()

    def _on_calc_mosfet(self):
        ds = self.ds
        res = self.res
        try:
            msg = calc_mosfet_losses(ds, res, type="MOSFET")
            if "All OK" in msg:
                QMessageBox.information(self, "Success", msg)
            else:
                QMessageBox.warning(self, "Missing Values", msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not calculate MOSFET losses:\n{str(e)}")

        ds.notify("losses")
        self.refresh()

    # ====================================================
    # Controller losses 
    # ====================================================
    def _on_calc_ctrl(self): 
        ds = self.ds
        res = self.res
        try:
            msg = calc_mosfet_losses(ds, res, type="IC")
            if "All OK" in msg:
                QMessageBox.information(self, "Success", msg)
            else:
                QMessageBox.warning(self, "Missing Values", msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not calculate Controller losses:\n{str(e)}")
            
        ds.notify("losses")
        self.refresh()
    
    # ====================================================
    # Input capacitor (Bulk) losses
    # ====================================================
    def _on_calc_c_in(self): 
        ds = self.ds
        res = self.res
        try: 
            msg = calc_capacitor_losses("C_bulk", ds, res)
            if "All OK" in msg:
                QMessageBox.information(self, "Success", msg)
            else:
                QMessageBox.warning(self, "Missing Values", msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not calculate input capacitor losses:\n{str(e)}")
        ds.notify("losses")
        self.refresh()

    # ====================================================
    # First output stage losses
    # ====================================================
    def _on_calc_out1(self): 
        ds = self.ds
        res = self.res
        try:
            ds.P_cond_diode1, ds.P_sw_diode1, ds.P_diode1 = calc_diode_losses(ds.diode1, ds.type_diode1, ds, res)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not calculate Diode 1 losses:\n{str(e)}")
            
        warnings = []
        try:
            msg1 = calc_capacitor_losses("C1_out1", ds, res)
            if "missing" in msg1: warnings.append(msg1)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not calculate Capacitor 1 losses:\n{str(e)}")
            
        if getattr(ds, "C2_out1", 0.0) > 0:
            try:
                msg2 = calc_capacitor_losses("C2_out1", ds, res)
                if "missing" in msg2: warnings.append(msg2)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not calculate Capacitor 2 losses:\n{str(e)}")
        else:
            ds.P_c2_out1 = 0.0

        if warnings:
            QMessageBox.warning(self, "Missing Values", "\n\n".join(warnings))
        else:
            QMessageBox.information(self, "Success", "All OK: No missing values for Output 1 capacitors calculations.")

        ds.notify("losses")
        self.refresh()

    # ====================================================
    # Second output stage losses
    # ====================================================
    def _on_calc_out2(self): 
        ds = self.ds
        res = self.res
        try:
            ds.P_cond_diode2, ds.P_sw_diode2, ds.P_diode2 = calc_diode_losses(ds.diode2, getattr(ds, "type_diode2", "Standard"), ds, res)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not calculate Diode 2 losses:\n{str(e)}")
            
        warnings = []
        try:
            msg1 = calc_capacitor_losses("C1_out2", ds, res)
            if "missing" in msg1: warnings.append(msg1)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not calculate Output 2 Capacitor 1 losses:\n{str(e)}")
            
        if getattr(ds, "C2_out2", 0.0) > 0:
            try:
                msg2 = calc_capacitor_losses("C2_out2", ds, res)
                if "missing" in msg2: warnings.append(msg2)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not calculate Output 2 Capacitor 2 losses:\n{str(e)}")
        else:
            ds.P_c2_out2 = 0.0

        if warnings:
            QMessageBox.warning(self, "Missing Values", "\n\n".join(warnings))
        else:
            QMessageBox.information(self, "Success", "All OK: No missing values for Output 2 capacitors calculations.")

        ds.notify("losses")
        self.refresh()
    
    # ====================================================
    # Snubber diode losses 
    # ====================================================
    def _on_calc_sn_diode(self): pass
    
    # ====================================================
    # Snubber losses 
    # ====================================================
    def _on_calc_snubber(self): pass


    def refresh(self):
        ds = self.ds
        res = self.res

        self.res_P_cond.set_value(ds.P_cond)
        self.res_P_sw.set_value(ds.P_sw)
        self.res_P_mosfet.set_value(ds.P_mosfet)

        self.res_ctrl_cond.set_value(ds.P_cond_ctr)
        self.res_ctrl_sw.set_value(ds.P_sw_ctr)
        self.res_ctrl_tot.set_value(ds.P_ctr)

        self.res_c_bulk.set_value(ds.P_c_bulk)
        
        self.res_d1_cond.set_value(ds.P_cond_diode1)
        self.res_d1_sw.set_value(ds.P_sw_diode1)
        self.res_d1_tot.set_value(ds.P_diode1)
        self.res_c1_out1_tot.set_value(getattr(ds, "P_c1_out1", 0.0))
        self.res_c2_out1_tot.set_value(getattr(ds, "P_c2_out1", 0.0))

        self.res_d2_cond.set_value(ds.P_cond_diode2)
        self.res_d2_sw.set_value(ds.P_sw_diode2)
        self.res_d2_tot.set_value(ds.P_diode2)
        self.res_c1_out2_tot.set_value(getattr(ds, "P_c1_out2", 0.0))
        self.res_c2_out2_tot.set_value(getattr(ds, "P_c2_out2", 0.0))

        self.res_sn_diode_cond.set_value(ds.P_sn_diode)
        self.res_snubber_tot.set_value(ds.P_snubber)

        # Visibility logic for optional components
        self.res_c2_out1_tot.setVisible(getattr(ds, "C2_out1", 0.0) > 0)
        
        has_out2 = getattr(ds, "enable_out2", False)
        self.box_out2.setVisible(has_out2)
        self.res_c2_out2_tot.setVisible(has_out2 and getattr(ds, "C2_out2", 0.0) > 0)
