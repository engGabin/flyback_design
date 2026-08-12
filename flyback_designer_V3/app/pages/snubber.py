from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel
from PyQt6.QtCore import Qt
from app.widgets.common import PageBase, LabeledInput, ResultRow, SectionHeader
from PyQt6.QtGui import QPixmap

class SnubberPage(PageBase):

    def __init__(self, ds, res, parent=None):
        super().__init__(ds, res, title="Clamp Circuit Design", parent=parent)

    def _build_ui(self):
        cl = self._content_layout

        # ------------------------------------------------------------
        # INPUTS
        # ------------------------------------------------------------
        cl.addWidget(SectionHeader("Clamp Circuit Inputs"))
        
        self._k_cl = LabeledInput("Facteur d'estimation de la tension du clamp", "-", decimals=1, default=1.5)
        self._k_Vwm = LabeledInput("Facteur d'estimation de la tension du clamp", "-", decimals=1, default=1.2)
        self._delta_v_sn = LabeledInput("Variation de tension autorisée sur le snubber", "-", decimals=2, default=0.1)
        self._sn_f_sw = LabeledInput("Switching frequency", "kHz", decimals=2, default=115.0)
        self._sn_Lp = LabeledInput("Primary inductance", "µH", decimals=2, default=800)
        self._sn_Np = LabeledInput("Primary turns", "-", decimals=2, default=11.10)
        self._sn_Ns = LabeledInput("Secondary turns", "-", decimals=2, default=1)
        self._sn_Cp = LabeledInput("Parasitic capacitance of the transformer", "pF", decimals=2, default=0.0)
        self._sn_Llk = LabeledInput("Leakage inductance", "µH", decimals=2, default=18.0)
        self._sn_Vout = LabeledInput("Output voltage", "V", decimals=2, default=12.0)
        self._sn_v_F = LabeledInput("Diode forward voltage", "V", decimals=1, default=0.7)
        self._sn_i_p_max = LabeledInput("Peak primary current", "A", decimals=3, default=0.371)

        inputs = [
            self._k_cl, self._k_Vwm, self._delta_v_sn, self._sn_f_sw, 
            self._sn_Lp, self._sn_Np, self._sn_Ns, self._sn_Cp, self._sn_Llk, self._sn_Vout, 
            self._sn_v_F, self._sn_i_p_max
        ]
        
        # We can add them directly to the layout or wrap in a QFrame
        for inp in inputs:
            cl.addWidget(inp)
        
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        btn = QPushButton("Calculate Clamp Circuit")
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
        # OUTPUTS
        # ------------------------------------------------------------
        # General Snubber Results
        box_gen = QFrame()
        box_gen.setObjectName("ResultsContainerGen")
        box_gen.setStyleSheet("QFrame#ResultsContainerGen { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_gen = QVBoxLayout(box_gen)
        lay_gen.setContentsMargins(20, 16, 20, 20)
        lay_gen.addWidget(SectionHeader("Clamp Circuit Calculations"))

        self._r_sn_vor = ResultRow("Reflected voltage", "V", decimals=3)
        self._r_v_sn = ResultRow("Clamp circuit voltage", "V", decimals=3)
        self._r_p_sn = ResultRow("Clamp circuit power", "W", decimals=3)

        lay_gen.addWidget(self._r_sn_vor)
        lay_gen.addWidget(self._r_v_sn)
        lay_gen.addWidget(self._r_p_sn)
        
        cl.addWidget(box_gen)
        cl.addSpacing(20)

        # RCD Snubber
        box_rcd = QFrame()
        box_rcd.setObjectName("ResultsContainerRCD")
        box_rcd.setStyleSheet("QFrame#ResultsContainerRCD { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_rcd = QVBoxLayout(box_rcd)
        lay_rcd.setContentsMargins(20, 16, 20, 20)
        lay_rcd.addWidget(SectionHeader("RCD Clamp Circuit"))

        self._r_r_sn = ResultRow("Resistance", "kΩ", decimals=3)
        self._r_c_sn = ResultRow("Capacitance", "nF", decimals=3)

        lay_rcd.addWidget(self._r_r_sn)
        lay_rcd.addWidget(self._r_c_sn)
        
        cl.addWidget(box_rcd)
        cl.addSpacing(20)

        # TVS Clamp Circuit
        box_tvs = QFrame()
        box_tvs.setObjectName("ResultsContainerTVS")
        box_tvs.setStyleSheet("QFrame#ResultsContainerTVS { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_tvs = QVBoxLayout(box_tvs)
        lay_tvs.setContentsMargins(20, 16, 20, 20)
        lay_tvs.addWidget(SectionHeader("TVS Clamp Circuit"))

        self._r_v_clamp = ResultRow("TVS clamp voltage", "V", decimals=3)
        self._r_v_rwm = ResultRow("TVS working peak reverse voltage", "V", decimals=3)

        lay_tvs.addWidget(self._r_v_clamp)
        lay_tvs.addWidget(self._r_v_rwm)
        
        cl.addWidget(box_tvs)
        cl.addSpacing(20)

        # ------------------------------------------------------------
        # IMAGES (Commented out)
        # ------------------------------------------------------------
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_dir = os.path.join(base_dir, "assets")

        cl.addWidget(SectionHeader("Clamp Circuit Topologies"))
        img_layout = QHBoxLayout()
        
        # Image 1 (RCD Snubber)
        img1 = QLabel()
        img1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img1.setStyleSheet("background-color: white; border: 1px solid #3E5C76; padding: 20px;")
        
        path1 = os.path.join(img_dir, "RCD_snubber_circuit.PNG")
        pixmap1 = QPixmap(path1)
        if not pixmap1.isNull():
            # Scale down if it's too big, keeping aspect ratio
            pixmap1 = pixmap1.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            img1.setPixmap(pixmap1)
        else:
            img1.setText("Image 1 introuvable")
        
        img_layout.addWidget(img1)
        cl.addLayout(img_layout)

    def showEvent(self, event):
        super().showEvent(event)
        from models.calc_snubber import calc_snubber
        try:
            calc_snubber(self.ds, self.res)
            self.refresh()
        except Exception:
            pass

    def _load_from_state(self):
        ds = self.ds
        ds.k_cl = self._k_cl.value
        ds.k_Vwm = self._k_Vwm.value
        ds.delta_v_sn = self._delta_v_sn.value
        ds.sn_f_sw = self._sn_f_sw.value * 1e3
        ds.sn_Lp = self._sn_Lp.value * 1e-6
        ds.sn_Np = self._sn_Np.value
        ds.sn_Ns = self._sn_Ns.value
        ds.sn_Cp = self._sn_Cp.value * 1e-12
        ds.sn_Llk = self._sn_Llk.value * 1e-6
        ds.sn_Vout = self._sn_Vout.value
        ds.sn_v_F = self._sn_v_F.value
        ds.sn_i_p_max = self._sn_i_p_max.value


    def _on_calc_clicked(self):
        ds = self.ds
        ds.k_cl = self._k_cl.value
        ds.k_Vwm = self._k_Vwm.value
        ds.delta_v_sn = self._delta_v_sn.value
        ds.sn_f_sw = self._sn_f_sw.value * 1e3
        ds.sn_Lp = self._sn_Lp.value * 1e-6
        ds.sn_Np = self._sn_Np.value
        ds.sn_Ns = self._sn_Ns.value
        ds.sn_Cp = self._sn_Cp.value * 1e-12
        ds.sn_Llk = self._sn_Llk.value * 1e-6
        ds.sn_Vout = self._sn_Vout.value
        ds.sn_v_F = self._sn_v_F.value
        ds.sn_i_p_max = self._sn_i_p_max.value

        from models.calc_snubber import calc_snubber
        try:
            calc_snubber(ds, self.res)
        except Exception as e:
            QMessageBox.warning(self, "Calculation Error", f"An error occurred during calculation:\n{e}")
            return
            
        ds.notify("snubber")
        self.refresh()

    def refresh(self):
        res = self.res
        self._r_v_sn.set_value(res.v_sn)
        self._r_p_sn.set_value(res.p_sn)
        self._r_r_sn.set_value(res.r_sn)
        self._r_c_sn.set_value(res.c_sn)
        self._r_v_clamp.set_value(res.v_clamp)
        self._r_v_rwm.set_value(res.v_rwm)
        self._r_sn_vor.set_value(res.sn_vor)
