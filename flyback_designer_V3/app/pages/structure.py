from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, 
    QCheckBox, QFrame, QMessageBox, QComboBox, QDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
import os

from app.widgets.common import (
    PageBase, SectionHeader, LabeledInput, LabeledTextInput, LabeledComboBox, HLine
)
from models.flyback_states import FlybackState, FlybackResults


class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class ImageViewer(QDialog):
    def __init__(self, img_path, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        lay = QVBoxLayout(self)
        lbl = QLabel()
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pix = QPixmap(img_path)
        lbl.setPixmap(pix.scaled(1200, 800, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        lay.addWidget(lbl)


class StructurePage(PageBase):
    """
    Page for selecting the flyback structure (MOSFET, Controller) 
    and defining datasheet components parameters.
    """
    
    def _build_ui(self):
        btn_style = """
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
        """
        
        chk_style = """
            QCheckBox {
                background-color: #3E5C76;
                color: #F0EBD8;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 13px;
                margin-top: 5px;
                margin-bottom: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox:hover {
                background-color: #4A6E8C;
            }
        """

        # =================================================================================
        # 1. Structure Selection
        # =================================================================================
        self._content_layout.addWidget(SectionHeader("Choix de la Structure", center=True))
        
        # Image layout
        lay_images = QHBoxLayout()
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_stackfet = os.path.join(base_dir, "assets", "flyback_mosfet_controller.PNG")
        img_driver = os.path.join(base_dir, "assets", "flytback_driver_mosfet.PNG")
        img_ic = os.path.join(base_dir, "assets", "flyback_controller.PNG")
        
        self.lbl_img_stackfet = ClickableLabel()
        self.lbl_img_driver = ClickableLabel()
        self.lbl_img_ic = ClickableLabel()
        
        def setup_img(lbl, path, title):
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("background-color: #2E3440; border: 1px solid #4C566A; border-radius: 4px; padding: 5px;")
            if os.path.exists(path):
                pix = QPixmap(path)
                lbl.setPixmap(pix.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                lbl.setCursor(Qt.CursorShape.PointingHandCursor)
                lbl.setToolTip(f"Click to enlarge: {title}")
                lbl.clicked.connect(lambda p=path, t=title: ImageViewer(p, t, self).exec())
            else:
                lbl.setText("[ Image not found ]")
        
        setup_img(self.lbl_img_stackfet, img_stackfet, "Stackfet (Controller + MOSFET)")
        setup_img(self.lbl_img_driver, img_driver, "Driver Ext + MOSFET")
        setup_img(self.lbl_img_ic, img_ic, "Controller Seul (IC Only)")
        
        lay_images.addWidget(self.lbl_img_stackfet)
        lay_images.addWidget(self.lbl_img_driver)
        lay_images.addWidget(self.lbl_img_ic)
        
        self._content_layout.addLayout(lay_images)
        self._content_layout.addSpacing(10)
        
        # Combo choice
        self.combo_structure = LabeledComboBox(
            "Type de structure", 
            ["stackfet (Controller + MOSFET)", "Driver + MOSFET", "Controller only"]
        )
        self.combo_structure._lbl.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.combo_structure._combo.setStyleSheet("font-size: 14px; padding: 5px;")
        self.combo_structure._combo.setMinimumWidth(250)
        
        lay_center = QHBoxLayout()
        lay_center.addStretch()
        lay_center.addWidget(self.combo_structure)
        lay_center.addStretch()
        self.combo_structure._combo.currentTextChanged.connect(self._on_structure_changed)
        self._content_layout.addLayout(lay_center)
        self._content_layout.addSpacing(20)
        
        # =================================================================================
        # 2. MOSFET Box
        # =================================================================================
        self.box_mosfet = QFrame()
        self.box_mosfet.setObjectName("BoxMosfet")
        self.box_mosfet.setStyleSheet("QFrame#BoxMosfet { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_mosfet = QVBoxLayout(self.box_mosfet)
        lay_mosfet.setContentsMargins(20, 16, 20, 20)
        lay_mosfet.addWidget(SectionHeader("External MOSFET", center=True))
        
        self.ui_mosfet_ref = LabeledTextInput("Référence", tooltip="Ex: IPW90R120C3")
        self.ui_MOS_vds_max = LabeledInput("Drain-source breakdown voltage", "V", 
            min_val=0, max_val=1e6, decimals=0, tooltip="Vds max")
        self.ui_r_ds_on = LabeledInput("Drain-source on-state resistance", "Ω", 
            min_val=0, decimals=4, tooltip="Rds(on)")
        self.ui_MOS_Eoss = LabeledInput("Output stored energy", "µJ", 
            min_val=0, decimals=2, tooltip="Eoss")
        self.ui_MOS_coss = LabeledInput("Output capacitance", "pF", 
            min_val=0, decimals=2, tooltip="Coss")
        self.ui_MOS_r_th = LabeledInput("Thermal resistance", "°C/W", 
            min_val=0, decimals=2, tooltip="Rth")
        self.ui_MOS_ton = LabeledInput("Turn-on delay time", "ns", 
            min_val=0, decimals=2, tooltip="t_on")
        self.ui_MOS_toff = LabeledInput("Turn-off delay time", "ns", 
            min_val=0, decimals=2, tooltip="t_off")
        self.ui_MOS_kt100 = LabeledInput("kt100", "", 
            min_val=0, decimals=2, tooltip="kt100")
        self.ui_MOS_Rthjc = LabeledInput("Thermal resistance from junction to case", "°C/W", 
            min_val=0, decimals=2, tooltip="Rth(j-c)")
        self.ui_MOS_Rthcs = LabeledInput("Thermal resistance from case to sink", "°C/W", 
            min_val=0, decimals=2, tooltip="Rth(c-s)")
        self.ui_MOS_Rthsa = LabeledInput("Thermal resistance from sink to ambient", "°C/W", 
            min_val=0, decimals=2, tooltip="Rth(s-a)")
        
        for w in [self.ui_mosfet_ref, self.ui_MOS_vds_max, self.ui_r_ds_on, self.ui_MOS_Eoss, 
                  self.ui_MOS_coss, self.ui_MOS_r_th, self.ui_MOS_ton, self.ui_MOS_toff, 
                  self.ui_MOS_kt100, self.ui_MOS_Rthjc, self.ui_MOS_Rthcs, self.ui_MOS_Rthsa]:
            lay_mosfet.addWidget(w)
            
        lay_btn1 = QHBoxLayout()
        lay_btn1.addStretch()
        btn_save_mosfet = QPushButton("Enregistrer MOSFET")
        btn_save_mosfet.setStyleSheet(btn_style)
        btn_save_mosfet.clicked.connect(self._save_to_state)
        lay_btn1.addWidget(btn_save_mosfet)
        lay_mosfet.addLayout(lay_btn1)
        self._content_layout.addWidget(self.box_mosfet)
        self._content_layout.addSpacing(10)

        # =================================================================================
        # 3. Controller Box
        # =================================================================================
        self.box_ctrl = QFrame()
        self.box_ctrl.setObjectName("BoxCtrl")
        self.box_ctrl.setStyleSheet("QFrame#BoxCtrl { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_ctrl = QVBoxLayout(self.box_ctrl)
        lay_ctrl.setContentsMargins(20, 16, 20, 20)
        lay_ctrl.addWidget(SectionHeader("Contrôleur (IC)", center=True))
        
        self.ui_ctrl_ref = LabeledTextInput("Référence", tooltip="Ex: ICE2QR4565G")
        self.ui_ctr_vds_max = LabeledInput("Drain-source breakdown voltage", "V", 
            min_val=0,max_val=1e6, decimals=0, tooltip="Vds max")
        self.ui_ctr_r_ds_on = LabeledInput("Drain-source on-state resistance", "Ω", 
            min_val=0, decimals=2, tooltip="Rds(on)")
        self.ui_ctr_Eoss = LabeledInput("Output stored energy", "µJ", 
            min_val=0, decimals=2, tooltip="Eoss")
        self.ui_ctr_coss = LabeledInput("Output capacitance", "pF", 
            min_val=0, decimals=2, tooltip="Coss")
        self.ui_ctr_r_th = LabeledInput("Thermal resistance", "°C/W", 
            min_val=0, decimals=2, tooltip="Rth")
        self.ui_ctr_ton = LabeledInput("Turn-on delay time", "ns", 
            min_val=0, decimals=2, tooltip="t_on")
        self.ui_ctr_toff = LabeledInput("Turn-off delay time", "ns", 
            min_val=0, decimals=2, tooltip="t_off")
        self.ui_ctr_kt100 = LabeledInput("kt100", "", 
            min_val=0, decimals=2, tooltip="kt100")
        self.ui_ctr_Rthjc = LabeledInput("Thermal resistance from junction to case", "°C/W", 
            min_val=0, decimals=2, tooltip="Rth(j-c)")
        self.ui_ctr_Rthcs = LabeledInput("Thermal resistance from case to sink", "°C/W", 
            min_val=0, decimals=2, tooltip="Rth(c-s)")
        self.ui_ctr_Rthsa = LabeledInput("Thermal resistance from sink to ambient", "°C/W", 
            min_val=0, decimals=2, tooltip="Rth(s-a)")
        
        for w in [self.ui_ctrl_ref, self.ui_ctr_vds_max, self.ui_ctr_r_ds_on, self.ui_ctr_Eoss, 
                  self.ui_ctr_coss, self.ui_ctr_r_th, self.ui_ctr_ton, self.ui_ctr_toff, 
                  self.ui_ctr_kt100, self.ui_ctr_Rthjc, self.ui_ctr_Rthcs, self.ui_ctr_Rthsa]:
            lay_ctrl.addWidget(w)
            
        lay_btn2 = QHBoxLayout()
        lay_btn2.addStretch()
        btn_save_ctrl = QPushButton("Enregistrer Contrôleur")
        btn_save_ctrl.setStyleSheet(btn_style)
        btn_save_ctrl.clicked.connect(self._save_to_state)
        lay_btn2.addWidget(btn_save_ctrl)
        lay_ctrl.addLayout(lay_btn2)
        self._content_layout.addWidget(self.box_ctrl)
        self._content_layout.addSpacing(10)

        # =================================================================================
        # 4. Input Capacitors
        # =================================================================================
        box_cin = QFrame()
        box_cin.setObjectName("BoxCin")
        box_cin.setStyleSheet("QFrame#BoxCin { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_cin_main = QVBoxLayout(box_cin)
        lay_cin_main.setContentsMargins(20, 16, 20, 20)
        lay_cin_main.addWidget(SectionHeader("Input Capacitor(s)", center=True))
        
        self.ui_c_bulk = LabeledInput("Capacitor", "µF", min_val=0, max_val=1e6, decimals=3, 
            tooltip="C_bulk (value)")
        self.ui_c_bulk_esr = LabeledInput("ESR", "mΩ", min_val=0, max_val=1e6, decimals=3, 
            tooltip="C_bulk_esr (value)")
        self.ui_num_c_bulk_series = LabeledInput("Number of capacitors in series", "", decimals=0, max_val=10,
            tooltip="Number of bulk capacitors in series")
        lay_cin_main.addWidget(self.ui_c_bulk)
        lay_cin_main.addWidget(self.ui_c_bulk_esr)
        lay_cin_main.addWidget(self.ui_num_c_bulk_series)
        
        lay_btn3 = QHBoxLayout()
        lay_btn3.addStretch()
        btn_save_cin = QPushButton("Enregistrer Capas d'entrée")
        btn_save_cin.setStyleSheet(btn_style)
        btn_save_cin.clicked.connect(self._save_to_state)
        lay_btn3.addWidget(btn_save_cin)
        lay_cin_main.addLayout(lay_btn3)
        self._content_layout.addWidget(box_cin)
        self._content_layout.addSpacing(10)

        # =================================================================================
        # 5. Output 1
        # =================================================================================
        box_out1 = QFrame()
        box_out1.setObjectName("BoxOut1")
        box_out1.setStyleSheet("QFrame#BoxOut1 { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_out1 = QVBoxLayout(box_out1)
        lay_out1.setContentsMargins(20, 16, 20, 20)
        lay_out1.addWidget(SectionHeader("Output Diode & Capacitor(s) (Winding 1)", center=True))
        
        self.ui_diode1_ref = LabeledTextInput("Référence Diode 1")
        self.ui_type_diode1 = LabeledComboBox("Type Diode", ["Standard", "Ultra-fast", "Schottky"])
        self.ui_V_F1 = LabeledInput("Forward voltage", "V", decimals=2, min_val=0, max_val=100, 
            tooltip="V_F (value)")
        self.ui_r_d1 = LabeledInput("Dynamic resistance", "Ω", decimals=2, min_val=0, max_val=1e3, 
            tooltip="r_d (value)")
        self.ui_Qrr_d1 = LabeledInput("Reverse recovered charge", "nC", decimals=2, min_val=0, max_val=1e6, 
            tooltip="Qrr (value)")
        self.ui_Cj_d1 = LabeledInput("Total junction capacitance", "pF", decimals=2, min_val=0, max_val=1e3, 
            tooltip="Cj (value)")
        for w in [self.ui_diode1_ref, self.ui_type_diode1, self.ui_V_F1, self.ui_r_d1, self.ui_Qrr_d1, self.ui_Cj_d1]:
            lay_out1.addWidget(w)
            
        lay_out1.addWidget(HLine())
        self.ui_C1_out1 = LabeledInput("Output capacitor", "µF", min_val=0, max_val=1e6, decimals=2, 
            tooltip="C1_out1 (value)")
        self.ui_C1_out1_ESR = LabeledInput("Output capacitor ESR", "mΩ", min_val=0, max_val=1e6, decimals=2, 
            tooltip="C1_out1_ESR (value)")
        lay_out1.addWidget(self.ui_C1_out1)
        lay_out1.addWidget(self.ui_C1_out1_ESR)
        
        self.chk_C2_out1 = QCheckBox("Add a second output capacitor (C2)")
        self.chk_C2_out1.setStyleSheet(chk_style)
        self.chk_C2_out1.stateChanged.connect(self._toggle_c2_out1)
        lay_out1.addWidget(self.chk_C2_out1)
        
        self.box_c2_out1 = QWidget()
        lay_c2_out1 = QVBoxLayout(self.box_c2_out1)
        lay_c2_out1.setContentsMargins(0, 0, 0, 0)
        self.ui_C2_out1 = LabeledInput("Second output capacitor", "µF", min_val=0, max_val=1e6, decimals=2, 
            tooltip="C2_out1 (value)")
        self.ui_C2_out1_ESR = LabeledInput("Second output capacitor ESR", "mΩ", min_val=0, max_val=1e6, decimals=2, 
            tooltip="C2_out1_ESR (value)")
        lay_c2_out1.addWidget(self.ui_C2_out1)
        lay_c2_out1.addWidget(self.ui_C2_out1_ESR)
        lay_out1.addWidget(self.box_c2_out1)

        lay_btn4 = QHBoxLayout()
        lay_btn4.addStretch()
        btn_save_out1 = QPushButton("Save Output 1")
        btn_save_out1.setStyleSheet(btn_style)
        btn_save_out1.clicked.connect(self._save_to_state)
        lay_btn4.addWidget(btn_save_out1)
        lay_out1.addLayout(lay_btn4)
        self._content_layout.addWidget(box_out1)
        self._content_layout.addSpacing(10)

        # =================================================================================
        # 6. Output 2 (Optional)
        # =================================================================================
        self.chk_enable_out2 = QCheckBox("Enable the second winding (Output 2)")
        self.chk_enable_out2.setStyleSheet(chk_style)
        self.chk_enable_out2.stateChanged.connect(self._toggle_out2)
        self._content_layout.addWidget(self.chk_enable_out2)
        
        self.box_out2 = QFrame()
        self.box_out2.setObjectName("BoxOut2")
        self.box_out2.setStyleSheet("QFrame#BoxOut2 { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_out2 = QVBoxLayout(self.box_out2)
        lay_out2.setContentsMargins(20, 16, 20, 20)
        
        lay_out2.addWidget(SectionHeader("Output Diode & Capacitor(s) (Winding 2)", center=True))
        self.ui_diode2_ref = LabeledTextInput("Diode Reference")
        self.ui_type_diode2 = LabeledComboBox("Diode Type", ["Standard", "Ultra-fast", "Schottky"])
        self.ui_V_F2 = LabeledInput("Forward voltage", "V", decimals=2, min_val=0, max_val=100, 
            tooltip="V_F (value)")
        self.ui_r_d2 = LabeledInput("Dynamic resistance", "Ω", decimals=2, min_val=0, max_val=1e3, 
            tooltip="r_d (value)")
        self.ui_Qrr_d2 = LabeledInput("Reverse recovered charge", "nC", decimals=2, min_val=0, max_val=1e6, 
            tooltip="Qrr (value)")
        self.ui_Cj_d2 = LabeledInput("Total junction capacitance", "pF", decimals=2, min_val=0, max_val=1e3, 
            tooltip="Cj (value)")
        for w in [self.ui_diode2_ref, self.ui_type_diode2, self.ui_V_F2, self.ui_r_d2, self.ui_Qrr_d2, self.ui_Cj_d2]:
            lay_out2.addWidget(w)
            
        lay_out2.addWidget(HLine())
        self.ui_C1_out2 = LabeledInput("Output capacitor", "µF", min_val=0, max_val=1e6, decimals=2, 
            tooltip="C1_out2 (value)")
        self.ui_C1_out2_ESR = LabeledInput("Output capacitor ESR", "mΩ", min_val=0, max_val=1e6, decimals=2, 
            tooltip="C1_out2_ESR (value)")
        lay_out2.addWidget(self.ui_C1_out2)
        lay_out2.addWidget(self.ui_C1_out2_ESR)
        
        self.chk_C2_out2 = QCheckBox("Add a second output capacitor (C2)")
        self.chk_C2_out2.setStyleSheet(chk_style)
        self.chk_C2_out2.stateChanged.connect(self._toggle_c2_out2)
        lay_out2.addWidget(self.chk_C2_out2)
        
        self.box_c2_out2 = QWidget()
        lay_c2_out2_in = QVBoxLayout(self.box_c2_out2)
        lay_c2_out2_in.setContentsMargins(0, 0, 0, 0)
        self.ui_C2_out2 = LabeledInput("Second output capacitor", "µF", min_val=0, max_val=1e6, decimals=2, 
            tooltip="C2_out2 (value)")
        self.ui_C2_out2_ESR = LabeledInput("Second output capacitor ESR", "mΩ", min_val=0, max_val=1e6, decimals=2, 
            tooltip="C2_out2_ESR (value)")
        lay_c2_out2_in.addWidget(self.ui_C2_out2)
        lay_c2_out2_in.addWidget(self.ui_C2_out2_ESR)
        lay_out2.addWidget(self.box_c2_out2)
        
        lay_btn5 = QHBoxLayout()
        lay_btn5.addStretch()
        btn_save_out2 = QPushButton("Save Output 2")
        btn_save_out2.setStyleSheet(btn_style)
        btn_save_out2.clicked.connect(self._save_to_state)
        lay_btn5.addWidget(btn_save_out2)
        lay_out2.addLayout(lay_btn5)
        self._content_layout.addWidget(self.box_out2)
        self._content_layout.addSpacing(10)

        # =================================================================================
        # 7. Snubber
        # =================================================================================
        box_snubber = QFrame()
        box_snubber.setObjectName("BoxSnubber")
        box_snubber.setStyleSheet("QFrame#BoxSnubber { background-color: #273A56; border-radius: 8px; border: 1px solid #3E5C76; }")
        lay_snub = QVBoxLayout(box_snubber)
        lay_snub.setContentsMargins(20, 16, 20, 20)
        lay_snub.addWidget(SectionHeader("Snubber Diode & Capacitor", center=True))
        
        self.ui_snubber_diode_ref = LabeledTextInput("Snubber Diode Reference")
        self.ui_snubber_diode_type = LabeledComboBox("Snubber Diode Type", ["Standard", "Ultra-fast", "Schottky"])
        self.ui_V_F_sn = LabeledInput("Forward voltage", "V", decimals=2, min_val=0, max_val=100, 
            tooltip="V_F (value)")
        self.ui_r_d_sn = LabeledInput("Dynamic resistance", "Ω", decimals=2, min_val=0, max_val=1e3, 
            tooltip="r_d (value)")
        self.ui_Qrr_d_sn = LabeledInput("Reverse recovered charge", "nC", decimals=2, min_val=0, max_val=1e6, 
            tooltip="Qrr (value)")
        self.ui_Cj_d_sn = LabeledInput("Total junction capacitance", "pF", decimals=2, min_val=0, max_val=1e3, 
            tooltip="Cj (value)")
        for w in [self.ui_snubber_diode_ref, self.ui_snubber_diode_type, self.ui_V_F_sn, self.ui_r_d_sn, self.ui_Qrr_d_sn, self.ui_Cj_d_sn]:
            lay_snub.addWidget(w)
            
        lay_snub.addWidget(HLine())
        self.ui_C_sn = LabeledInput("Snubber capacitor", "nF", min_val=0, max_val=1e6, decimals=2, 
            tooltip="C_sn (value)")
        self.ui_C_sn_ESR = LabeledInput("Snubber capacitor ESR", "mΩ", min_val=0, max_val=1e6, decimals=2, 
            tooltip="C_sn_ESR (value)")
        lay_snub.addWidget(self.ui_C_sn)
        lay_snub.addWidget(self.ui_C_sn_ESR)
        
        lay_btn6 = QHBoxLayout()
        lay_btn6.addStretch()
        btn_save_snubber = QPushButton("Save Snubber")
        btn_save_snubber.setStyleSheet(btn_style)
        btn_save_snubber.clicked.connect(self._save_to_state)
        lay_btn6.addWidget(btn_save_snubber)
        lay_snub.addLayout(lay_btn6)
        self._content_layout.addWidget(box_snubber)
        
        # =================================================================================
        # 8. Global Save
        # =================================================================================
        self._content_layout.addSpacing(20)
        lay_global_btn = QHBoxLayout()
        lay_global_btn.addStretch()
        self.btn_save_global = QPushButton("Save All Components")
        self.btn_save_global.setStyleSheet(btn_style)
        self.btn_save_global.clicked.connect(self._save_global)
        lay_global_btn.addWidget(self.btn_save_global)
        lay_global_btn.addStretch()
        self._content_layout.addLayout(lay_global_btn)
        
        # Initial state
        self._toggle_c2_out1()
        self._toggle_c2_out2()
        self._toggle_out2()


    def _on_structure_changed(self, text: str):
        default_style = "background-color: #2E3440; border: 1px solid #4C566A; border-radius: 4px; padding: 5px;"
        highlight_style = "background-color: #3E5C76; border: 2px solid #F0EBD8; border-radius: 4px; padding: 5px;"
        
        self.lbl_img_stackfet.setStyleSheet(default_style)
        self.lbl_img_driver.setStyleSheet(default_style)
        self.lbl_img_ic.setStyleSheet(default_style)

        # Handle enabling/disabling
        if "stackfet" in text:
            # Controller + MOSFET
            self.box_mosfet.setEnabled(True)
            self.box_ctrl.setEnabled(True)
            self.lbl_img_stackfet.setStyleSheet(highlight_style)
        elif "driver_ext" in text:
            # MOSFET only
            self.box_mosfet.setEnabled(True)
            self.box_ctrl.setEnabled(False)
            self.lbl_img_driver.setStyleSheet(highlight_style)
        elif "ic_only" in text:
            # Controller only
            self.box_mosfet.setEnabled(False)
            self.box_ctrl.setEnabled(True)
            self.lbl_img_ic.setStyleSheet(highlight_style)


    def _toggle_c2_out1(self):
        self.box_c2_out1.setVisible(self.chk_C2_out1.isChecked())
        
    def _toggle_c2_out2(self):
        self.box_c2_out2.setVisible(self.chk_C2_out2.isChecked())
        
    def _toggle_out2(self):
        self.box_out2.setVisible(self.chk_enable_out2.isChecked())

    def _load_from_state(self):
        # 1. Structure
        struct = self.ds.structure_type
        if struct == "stackfet":
            self.combo_structure.current_text = "stackfet (Controller + MOSFET)"
        elif struct == "driver_ext":
            self.combo_structure.current_text = "driver_ext (Driver + MOSFET)"
        elif struct == "ic_only":
            self.combo_structure.current_text = "ic_only (Controller seul)"
            
        # 2. MOSFET
        self.ui_mosfet_ref.text = self.ds.mosfet_ref
        self.ui_MOS_vds_max.value = self.ds.MOS_vds_max
        self.ui_r_ds_on.value = self.ds.r_ds_on
        self.ui_MOS_Eoss.value = self.ds.MOS_Eoss * 1e6
        self.ui_MOS_coss.value = self.ds.MOS_coss * 1e12
        self.ui_MOS_r_th.value = self.ds.MOS_r_th
        self.ui_MOS_ton.value = self.ds.MOS_ton * 1e9
        self.ui_MOS_toff.value = self.ds.MOS_toff * 1e9
        self.ui_MOS_kt100.value = self.ds.MOS_kt100
        self.ui_MOS_Rthjc.value = self.ds.MOS_Rthjc
        self.ui_MOS_Rthcs.value = self.ds.MOS_Rthcs
        self.ui_MOS_Rthsa.value = self.ds.MOS_Rthsa
        
        # 3. Controller
        self.ui_ctrl_ref.text = self.ds.controller_ref
        self.ui_ctr_vds_max.value = self.ds.ctr_vds_max
        self.ui_ctr_r_ds_on.value = self.ds.ctr_r_ds_on
        self.ui_ctr_Eoss.value = self.ds.ctr_Eoss * 1e6
        self.ui_ctr_coss.value = self.ds.ctr_coss * 1e12
        self.ui_ctr_r_th.value = self.ds.ctr_r_th
        self.ui_ctr_ton.value = self.ds.ctr_ton * 1e9
        self.ui_ctr_toff.value = self.ds.ctr_toff * 1e9
        self.ui_ctr_kt100.value = self.ds.ctr_kt100
        self.ui_ctr_Rthjc.value = self.ds.ctr_Rthjc
        self.ui_ctr_Rthcs.value = self.ds.ctr_Rthcs
        self.ui_ctr_Rthsa.value = self.ds.ctr_Rthsa
        
        # 4. Input Capas 
        self.ui_c_bulk.value = self.ds.c_bulk * 1e6
        self.ui_c_bulk_esr.value = self.ds.C_bulk_esr * 1e3
        self.ui_num_c_bulk_series.value = self.ds.num_c_bulk_series
            
        # 5. Output 1
        self.ui_diode1_ref.text = self.ds.output_diode1_ref
        if self.ds.type_diode1:
            self.ui_type_diode1.current_text = self.ds.type_diode1
        self.ui_V_F1.value = self.ds.V_F1
        self.ui_r_d1.value = self.ds.r_d1
        self.ui_Qrr_d1.value = self.ds.Qrr_d1 * 1e9
        self.ui_Cj_d1.value = self.ds.Cj_d1 * 1e12
        
        self.ui_C1_out1.value = self.ds.C1_out1
        self.ui_C1_out1_ESR.value = self.ds.C1_out1_ESR * 1e3
        self.ui_C2_out1.value = self.ds.C2_out1
        self.ui_C2_out1_ESR.value = self.ds.C2_out1_ESR * 1e3
        if self.ds.C2_out1 > 0:
            self.chk_C2_out1.setChecked(True)
            
        # 6. Output 2
        self.chk_enable_out2.setChecked(self.ds.enable_out2)
            
        self.ui_diode2_ref.text = self.ds.output_diode2_ref
        if self.ds.type_diode2:
            self.ui_type_diode2.current_text = self.ds.type_diode2
        self.ui_V_F2.value = self.ds.V_F2
        self.ui_r_d2.value = self.ds.r_d2
        self.ui_Qrr_d2.value = self.ds.Qrr_d2 * 1e9
        self.ui_Cj_d2.value = self.ds.Cj_d2 * 1e12
        
        self.ui_C1_out2.value = self.ds.C1_out2
        self.ui_C1_out2_ESR.value = self.ds.C1_out2_ESR * 1e3
        self.ui_C2_out2.value = self.ds.C2_out2
        self.ui_C2_out2_ESR.value = self.ds.C2_out2_ESR * 1e3
        if self.ds.C2_out2 > 0:
            self.chk_C2_out2.setChecked(True)
            
        # 7. Snubber
        self.ui_snubber_diode_ref.text = self.ds.snubber_diode_ref
        if self.ds.snubber_diode_type:
            self.ui_snubber_diode_type.current_text = self.ds.snubber_diode_type
        self.ui_V_F_sn.value = self.ds.V_F_sn
        self.ui_r_d_sn.value = self.ds.r_d_sn
        self.ui_Qrr_d_sn.value = self.ds.Qrr_d_sn * 1e9
        self.ui_Cj_d_sn.value = self.ds.Cj_d_sn * 1e12
        
        self.ui_C_sn.value = self.ds.C_sn * 1e9
        self.ui_C_sn_ESR.value = self.ds.C_sn_ESR * 1e3
        
        # Trigger combo logic
        self._on_structure_changed(self.combo_structure.current_text)

    def _save_to_state(self):
        """
        Gathers UI values into the global FlybackState, scales back to standard units.
        """
        # 1. Structure
        struct = self.combo_structure.current_text
        if "stackfet" in struct:
            self.ds.structure_type = "stackfet"
        elif "driver_ext" in struct:
            self.ds.structure_type = "driver_ext"
        elif "ic_only" in struct:
            self.ds.structure_type = "ic_only"
            
        # 2. MOSFET
        self.ds.mosfet_ref = self.ui_mosfet_ref.text
        self.ds.MOS_vds_max = self.ui_MOS_vds_max.value
        self.ds.r_ds_on = self.ui_r_ds_on.value
        self.ds.MOS_Eoss = self.ui_MOS_Eoss.value * 1e-6
        self.ds.MOS_coss = self.ui_MOS_coss.value * 1e-12
        self.ds.MOS_r_th = self.ui_MOS_r_th.value
        self.ds.MOS_ton = self.ui_MOS_ton.value * 1e-9
        self.ds.MOS_toff = self.ui_MOS_toff.value * 1e-9
        self.ds.MOS_kt100 = self.ui_MOS_kt100.value
        self.ds.MOS_Rthjc = self.ui_MOS_Rthjc.value
        self.ds.MOS_Rthcs = self.ui_MOS_Rthcs.value
        self.ds.MOS_Rthsa = self.ui_MOS_Rthsa.value
        
        # 3. Controller
        self.ds.controller_ref = self.ui_ctrl_ref.text
        self.ds.ctr_vds_max = self.ui_ctr_vds_max.value
        self.ds.ctr_r_ds_on = self.ui_ctr_r_ds_on.value
        self.ds.ctr_Eoss = self.ui_ctr_Eoss.value * 1e-6
        self.ds.ctr_coss = self.ui_ctr_coss.value * 1e-12
        self.ds.ctr_r_th = self.ui_ctr_r_th.value
        self.ds.ctr_ton = self.ui_ctr_ton.value * 1e-9
        self.ds.ctr_toff = self.ui_ctr_toff.value * 1e-9
        self.ds.ctr_kt100 = self.ui_ctr_kt100.value
        self.ds.ctr_Rthjc = self.ui_ctr_Rthjc.value
        self.ds.ctr_Rthcs = self.ui_ctr_Rthcs.value
        self.ds.ctr_Rthsa = self.ui_ctr_Rthsa.value
        
        # 4. Input Capas
        self.ds.c_bulk = self.ui_c_bulk.value * 1e-6
        self.ds.C_bulk_esr = self.ui_c_bulk_esr.value * 1e-3
        self.ds.num_c_bulk_series = int(self.ui_num_c_bulk_series.value) if self.ui_num_c_bulk_series.value > 0 else 1
            
        # 5. Output 1
        self.ds.output_diode1_ref = self.ui_diode1_ref.text
        self.ds.type_diode1 = self.ui_type_diode1.current_text
        self.ds.V_F1 = self.ui_V_F1.value
        self.ds.r_d1 = self.ui_r_d1.value
        self.ds.Qrr_d1 = self.ui_Qrr_d1.value * 1e-9
        self.ds.Cj_d1 = self.ui_Cj_d1.value * 1e-12
        
        self.ds.C1_out1 = self.ui_C1_out1.value
        self.ds.C1_out1_ESR = self.ui_C1_out1_ESR.value * 1e-3
        if self.chk_C2_out1.isChecked():
            self.ds.C2_out1 = self.ui_C2_out1.value
            self.ds.C2_out1_ESR = self.ui_C2_out1_ESR.value * 1e-3
        else:
            self.ds.C2_out1 = 0.0
            self.ds.C2_out1_ESR = 0.0
            
        # 6. Output 2
        self.ds.enable_out2 = self.chk_enable_out2.isChecked()
        if self.chk_enable_out2.isChecked():
            self.ds.output_diode2_ref = self.ui_diode2_ref.text
            self.ds.type_diode2 = self.ui_type_diode2.current_text
            self.ds.V_F2 = self.ui_V_F2.value
            self.ds.r_d2 = self.ui_r_d2.value
            self.ds.Qrr_d2 = self.ui_Qrr_d2.value * 1e-9
            self.ds.Cj_d2 = self.ui_Cj_d2.value * 1e-12
            
            self.ds.C1_out2 = self.ui_C1_out2.value
            self.ds.C1_out2_ESR = self.ui_C1_out2_ESR.value * 1e-3
            if self.chk_C2_out2.isChecked():
                self.ds.C2_out2 = self.ui_C2_out2.value
                self.ds.C2_out2_ESR = self.ui_C2_out2_ESR.value * 1e-3
            else:
                self.ds.C2_out2 = 0.0
                self.ds.C2_out2_ESR = 0.0
        else:
            self.ds.output_diode2_ref = ""
            self.ds.V_F2 = 0.0
            self.ds.C1_out2 = 0.0
            self.ds.C2_out2 = 0.0
            
        # 7. Snubber
        self.ds.snubber_diode_ref = self.ui_snubber_diode_ref.text
        self.ds.snubber_diode_type = self.ui_snubber_diode_type.current_text
        self.ds.V_F_sn = self.ui_V_F_sn.value
        self.ds.r_d_sn = self.ui_r_d_sn.value
        self.ds.Qrr_d_sn = self.ui_Qrr_d_sn.value * 1e-9
        self.ds.Cj_d_sn = self.ui_Cj_d_sn.value * 1e-12
        
        self.ds.C_sn = self.ui_C_sn.value * 1e-9
        self.ds.C_sn_ESR = self.ui_C_sn_ESR.value * 1e-3
        
        self.ds.notify("structure")

    def _save_global(self):
        self._save_to_state()
        QMessageBox.information(self, "Succès", "Tous les composants ont été enregistrés avec succès.")
        
    def refresh(self):
        self._load_from_state()
