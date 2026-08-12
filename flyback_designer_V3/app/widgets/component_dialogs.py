from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit,
    QPushButton, QFormLayout, QWidget, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt
from models.component_manager import ComponentManager

class AddComponentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add a Component")
        self.setMinimumWidth(400)
        self.mgr = ComponentManager()
        self._build_ui()

    def _build_ui(self):
        lay = QVBoxLayout(self)

        # Type selection
        type_lay = QHBoxLayout()
        type_lbl = QLabel("Component Type:")
        self.cb_type = QComboBox()
        self.cb_type.addItems(["Ferrite Core", "Controller", "MOSFET"])
        self.cb_type.currentTextChanged.connect(self._on_type_changed)
        type_lay.addWidget(type_lbl)
        type_lay.addWidget(self.cb_type)
        lay.addLayout(type_lay)

        # Dynamic form container
        self.form_container = QWidget()
        self.form_lay = QFormLayout(self.form_container)
        lay.addWidget(self.form_container)

        # Buttons
        btn_lay = QHBoxLayout()
        self.btn_save = QPushButton("Save")
        self.btn_save.setStyleSheet("background-color: #3E5C76; color: white; padding: 6px; font-weight: bold;")
        self.btn_save.clicked.connect(self._on_save)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_lay.addStretch()
        btn_lay.addWidget(self.btn_save)
        btn_lay.addWidget(self.btn_cancel)
        lay.addLayout(btn_lay)

        # Initialize form
        self.inputs = {}
        self._on_type_changed(self.cb_type.currentText())

    def _clear_form(self):
        while self.form_lay.count() > 0:
            item = self.form_lay.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.inputs.clear()

    def _add_input(self, key, label, is_bool=False):
        if is_bool:
            widget = QCheckBox()
            self.inputs[key] = widget
            self.form_lay.addRow(label, widget)
        else:
            widget = QLineEdit()
            self.inputs[key] = widget
            self.form_lay.addRow(label, widget)

    def _on_type_changed(self, ctype):
        self._clear_form()
        if ctype == "Ferrite Core":
            self._add_input("ref", "Reference:")
            self._add_input("geometry", "Geometry (e.g. E, RM):")
            self._add_input("Ae", "Ae (mm²):")
            self._add_input("Aw", "Aw (mm²):")
            self._add_input("Ap", "Ap (mm⁴):")
            self._add_input("Ve", "Ve (mm³):")
            self._add_input("AL", "AL (nH/t²):")
            self._add_input("le", "le (mm):")
            self._add_input("ln", "ln (mm):")
            self._add_input("weight", "Weight (g):")
            self._add_input("mu_core", "µ core:")
            self._add_input("window_length", "Window Length (mm):")
            self._add_input("Pv", "Pv:")
        elif ctype == "Controller":
            self._add_input("ref", "Reference:")
            self._add_input("manuf", "Manufacturer:")
            self._add_input("v_max", "V_max (V):")
            self._add_input("package", "Package:")
            self._add_input("psr", "Primary Side Reg (PSR):", is_bool=True)
            self._add_input("notes", "Notes:")
        elif ctype == "MOSFET":
            self._add_input("ref", "Reference:")
            self._add_input("v_ds", "V_DS (V):")
            self._add_input("rds_on", "Rds_on (mΩ):")
            self._add_input("package", "Package:")
            self._add_input("qg", "Qg (nC):")

    def _get_float(self, text, field_name):
        try:
            return float(text.replace(',', '.'))
        except ValueError:
            raise ValueError(f"Field '{field_name}' must be a valid number.")

    def _on_save(self):
        ctype = self.cb_type.currentText()
        comp_data = {}
        
        try:
            for key, widget in self.inputs.items():
                if isinstance(widget, QCheckBox):
                    comp_data[key] = widget.isChecked()
                else:
                    text = widget.text().strip()
                    if not text:
                        raise ValueError("All text fields must be filled.")
                    
                    # Convert specific fields to float based on type
                    float_fields = {
                        "Ferrite Core": ["Ae", "Aw", "Ap", "Ve", "AL", "le", "ln", "weight", "mu_core", "window_length", "Pv"],
                        "Controller": ["v_max"],
                        "MOSFET": ["v_ds", "rds_on", "qg"]
                    }
                    
                    if key in float_fields.get(ctype, []):
                        comp_data[key] = self._get_float(text, key)
                    else:
                        comp_data[key] = text
                        
            # Map UI type to internal DB key
            type_map = {
                "Ferrite Core": "cores",
                "Controller": "controllers",
                "MOSFET": "mosfets"
            }
            
            self.mgr.add_component(type_map[ctype], comp_data)
            self.accept()
            
        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))


class DeleteComponentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete a Component")
        self.setMinimumWidth(300)
        self.mgr = ComponentManager()
        self._build_ui()

    def _build_ui(self):
        lay = QVBoxLayout(self)

        # Type selection
        type_lay = QHBoxLayout()
        type_lbl = QLabel("Component Type:")
        self.cb_type = QComboBox()
        self.cb_type.addItems(["Ferrite Core", "Controller", "MOSFET"])
        self.cb_type.currentTextChanged.connect(self._on_type_changed)
        type_lay.addWidget(type_lbl)
        type_lay.addWidget(self.cb_type)
        lay.addLayout(type_lay)

        # Component Selection
        ref_lay = QHBoxLayout()
        ref_lbl = QLabel("Component:")
        self.cb_ref = QComboBox()
        ref_lay.addWidget(ref_lbl)
        ref_lay.addWidget(self.cb_ref)
        lay.addLayout(ref_lay)

        # Buttons
        btn_lay = QHBoxLayout()
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setStyleSheet("background-color: #F44336; color: white; padding: 6px; font-weight: bold;")
        self.btn_delete.clicked.connect(self._on_delete)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_lay.addStretch()
        btn_lay.addWidget(self.btn_delete)
        btn_lay.addWidget(self.btn_cancel)
        lay.addLayout(btn_lay)

        self._on_type_changed(self.cb_type.currentText())

    def _on_type_changed(self, ctype):
        self.cb_ref.clear()
        type_map = {
            "Ferrite Core": "cores",
            "Controller": "controllers",
            "MOSFET": "mosfets"
        }
        db_key = type_map[ctype]
        components = self.mgr.get_components(db_key)
        for comp in components:
            self.cb_ref.addItem(comp["ref"])

    def _on_delete(self):
        ctype = self.cb_type.currentText()
        ref = self.cb_ref.currentText()
        
        if not ref:
            return
            
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete {ref}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            type_map = {
                "Ferrite Core": "cores",
                "Controller": "controllers",
                "MOSFET": "mosfets"
            }
            self.mgr.delete_component(type_map[ctype], ref)
            self.accept()
