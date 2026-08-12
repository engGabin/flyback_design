from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel
from PyQt6.QtCore import Qt
from app.widgets.common import PageBase, LabeledInput, ResultRow, SectionHeader
from models.calc_engine import calc_wire_sections, check_core_window_fit

class WireSectionsPage(PageBase):

    def __init__(self, ds, res, parent=None):
        super().__init__(ds, res, title="Wire Sections", parent=parent)

    def _build_ui(self):
        cl = self._content_layout

        # ------------------------------------------------------------
        # OUTPUT 1: Calculated Wire Sections
        # ------------------------------------------------------------
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
        lay1.addWidget(SectionHeader("Calculated Wire Sections"))

        self._r_delta = ResultRow("Skin depth", "cm", decimals=4)
        self._r_sw = ResultRow("Max wire area", "mm²", decimals=4)
        self._r_dp_calc = ResultRow("Calculated primary diameter", "mm", decimals=3)  
        self._r_ds1_calc = ResultRow("Calculated sec1 diameter", "mm", decimals=3)    
        self._r_ds2_calc = ResultRow("Calculated sec2 diameter", "mm", decimals=3)
        self._r_daux_calc = ResultRow("Calculated aux diameter", "mm", decimals=3)

        lay1.addWidget(self._r_delta)
        lay1.addWidget(self._r_sw)
        lay1.addWidget(self._r_dp_calc)
        lay1.addWidget(self._r_ds1_calc)
        lay1.addWidget(self._r_ds2_calc)
        lay1.addWidget(self._r_daux_calc)

        cl.addWidget(box1)
        cl.addSpacing(20)

        # ------------------------------------------------------------
        # INPUT: Wire Selection
        # ------------------------------------------------------------
        cl.addWidget(SectionHeader("Wire Selection"))
        
        self._dp = LabeledInput("Primary wire diameter", "mm", decimals=2)
        self._ds1 = LabeledInput("Secondary 1 wire diameter", "mm", decimals=2)
        self._ds2 = LabeledInput("Secondary 2 wire diameter", "mm", decimals=2)
        self._daux = LabeledInput("Auxiliary wire diameter", "mm", decimals=2)

        cl.addWidget(self._dp)
        cl.addWidget(self._ds1)
        cl.addWidget(self._ds2)
        cl.addWidget(self._daux)
        
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        btn = QPushButton("Update Wire Sections")
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
        btn.clicked.connect(self._on_calc_clicked)
        btn_row.addWidget(btn)
        cl.addLayout(btn_row)
        cl.addSpacing(20)

        # ------------------------------------------------------------
        # OUTPUT 2: Selected Wire Sections Recap
        # ------------------------------------------------------------
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
        lay2.addWidget(SectionHeader("Selected Wire Sections Recap"))

        self._r_dp = ResultRow("Primary diameter", "mm", decimals=3)
        self._r_sp_eff = ResultRow("Effective primary area", "mm²", decimals=3)
        self._r_strands_p = ResultRow("Number of primary strands", "", decimals=0)
        
        self._r_ds1 = ResultRow("Secondary 1 diameter", "mm", decimals=3)
        self._r_ss1_eff = ResultRow("Effective secondary 1 area", "mm²", decimals=3)
        self._r_strands_s1 = ResultRow("Number of secondary 1 strands", "", decimals=0)
        
        self._r_ds2 = ResultRow("Secondary 2 diameter", "mm", decimals=3)
        self._r_ss2_eff = ResultRow("Effective secondary 2 area", "mm²", decimals=3)
        self._r_strands_s2 = ResultRow("Number of secondary 2 strands", "", decimals=0)
        
        self._r_daux = ResultRow("Auxiliary diameter", "mm", decimals=3)
        self._r_saux_eff = ResultRow("Effective auxiliary area", "mm²", decimals=3)
        self._r_strands_aux = ResultRow("Number of auxiliary strands", "", decimals=0)

        from PyQt6.QtGui import QFont
        self._lbl_AeAw_status = QLabel("")
        self._lbl_AeAw_status.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._lbl_AeAw_status.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))

        lay2.addWidget(self._r_dp)
        lay2.addWidget(self._r_sp_eff)
        lay2.addWidget(self._r_strands_p)
        lay2.addWidget(self._r_ds1)
        lay2.addWidget(self._r_ss1_eff)
        lay2.addWidget(self._r_strands_s1)
        lay2.addWidget(self._r_ds2)
        lay2.addWidget(self._r_ss2_eff)
        lay2.addWidget(self._r_strands_s2)
        lay2.addWidget(self._r_daux)
        lay2.addWidget(self._r_saux_eff)
        lay2.addWidget(self._r_strands_aux)
        lay2.addWidget(self._lbl_AeAw_status)

        cl.addWidget(box2)
        cl.addStretch()

    def _load_from_state(self):
        ds = self.ds
        self._dp.value = ds.Dp
        self._ds1.value = ds.Ds1
        self._ds2.value = ds.Ds2
        self._daux.value = ds.Daux

    def showEvent(self, event):
        super().showEvent(event)
        # Compute ideal wire sections automatically when navigating to this page
        from models.calc_engine import calc_wire_sections
        try:
            calc_wire_sections(self.ds, self.res)
            check_core_window_fit(self.ds, self.res)
            self.refresh()
        except Exception:
            pass

    def _on_calc_clicked(self):
        ds = self.ds
        ds.Dp = self._dp.value
        ds.Ds1 = self._ds1.value
        ds.Ds2 = self._ds2.value
        ds.Daux = self._daux.value

        try:
            calc_wire_sections(ds, self.res)
        except Exception as e:
            QMessageBox.warning(self, "Calculation Error", f"An error occurred during calculation:\n{e}")
            return

        try:
            check_core_window_fit(ds, self.res)
        except Exception as e:
            QMessageBox.warning(self, "Calculation Error", f"An error occurred during calculation:\n{e}")
            return
            
        ds.notify("wire_sections")
        self.refresh()

    def refresh(self):
        res = self.res
        ds = self.ds
        
        self._r_delta.set_value(ds.delta_cm)
        self._r_sw.set_value(res.s_w_calc)
        
        self._r_dp_calc.set_value(res.Dp_calc)
        self._r_ds1_calc.set_value(res.Ds1_calc)
        self._r_ds2_calc.set_value(res.Ds2_calc)
        self._r_daux_calc.set_value(res.Daux_calc)

        # Selected Recap
        self._r_dp.set_value(ds.Dp)
        self._r_sp_eff.set_value(ds.Sp_eff)
        self._r_strands_p.set_value(ds.strands_p)
        
        self._r_ds1.set_value(ds.Ds1)
        self._r_ss1_eff.set_value(ds.Ss1_eff)
        self._r_strands_s1.set_value(ds.strands_s1)
        
        self._r_ds2.set_value(ds.Ds2)
        self._r_ss2_eff.set_value(ds.Ss2_eff)
        self._r_strands_s2.set_value(ds.strands_s2)
        
        self._r_daux.set_value(ds.Daux)
        self._r_saux_eff.set_value(ds.Saux_eff)
        self._r_strands_aux.set_value(ds.strands_aux)

        if res.Aw_used_calc > 0:
            if res.Aw_used_calc < ds.Aw:
                self._lbl_AeAw_status.setText("OK : total copper area fits within the core window area")
                self._lbl_AeAw_status.setStyleSheet("color: #4CAF50;") # Green
            else:
                self._lbl_AeAw_status.setText("ERROR : total copper area does not fit within the core window area")
                self._lbl_AeAw_status.setStyleSheet("color: #F44336;") # Red
        else:
            self._lbl_AeAw_status.setText("")

        
