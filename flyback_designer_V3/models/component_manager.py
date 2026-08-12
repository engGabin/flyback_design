import os
import json

# Define original default data to seed JSON files if they don't exist

DEFAULT_CORES = [
    {"ref": "E25/13/7", "geometry": "E", "Ae": 52.0, "Aw": 62.0, "Ap": 3224.0, "Ve": 2500.0, "AL": 250.0, "le": 57.5, "ln": 52.0, "weight": 14.0, "mu_core": 1800.0, "window_length": 15.6, "Pv": 0.0},
    {"ref": "E30/15/7", "geometry": "E", "Ae": 60.0, "Aw": 115.0, "Ap": 6900.0, "Ve": 3400.0, "AL": 320.0, "le": 67.0, "ln": 60.0, "weight": 22.0, "mu_core": 1800.0, "window_length": 19.5, "Pv": 0.0},
    {"ref": "E32/16/9", "geometry": "E", "Ae": 83.0, "Aw": 130.0, "Ap": 10790.0, "Ve": 4700.0, "AL": 350.0, "le": 74.0, "ln": 67.0, "weight": 26.0, "mu_core": 1800.0, "window_length": 21.0, "Pv": 0.0},
    {"ref": "E36/18/11", "geometry": "E", "Ae": 111.0, "Aw": 175.0, "Ap": 19425.0, "Ve": 7200.0, "AL": 430.0, "le": 81.0, "ln": 74.0, "weight": 35.0, "mu_core": 1800.0, "window_length": 23.0, "Pv": 0.0},
    {"ref": "E42/20/15", "geometry": "E", "Ae": 178.0, "Aw": 240.0, "Ap": 42720.0, "Ve": 14000.0, "AL": 590.0, "le": 97.0, "ln": 87.0, "weight": 70.0, "mu_core": 1800.0, "window_length": 27.5, "Pv": 0.0},
    {"ref": "ETD29", "geometry": "ETD", "Ae": 76.0, "Aw": 100.0, "Ap": 7600.0, "Ve": 5470.0, "AL": 280.0, "le": 72.0, "ln": 53.0, "weight": 28.0, "mu_core": 1800.0, "window_length": 22.0, "Pv": 0.0},
    {"ref": "ETD34", "geometry": "ETD", "Ae": 97.1, "Aw": 123.0, "Ap": 11943.3, "Ve": 7740.0, "AL": 355.0, "le": 78.6, "ln": 60.0, "weight": 40.0, "mu_core": 1800.0, "window_length": 25.6, "Pv": 0.0},
    {"ref": "ETD39", "geometry": "ETD", "Ae": 125.0, "Aw": 177.0, "Ap": 22125.0, "Ve": 11500.0, "AL": 449.0, "le": 92.2, "ln": 69.0, "weight": 60.0, "mu_core": 1800.0, "window_length": 29.3, "Pv": 0.0},
    {"ref": "RM10", "geometry": "RM", "Ae": 96.0, "Aw": 35.0, "Ap": 3360.0, "Ve": 5600.0, "AL": 1900.0, "le": 44.0, "ln": 52.0, "weight": 23.0, "mu_core": 1800.0, "window_length": 10.5, "Pv": 0.0},
]

DEFAULT_CONTROLLERS = [
    {"ref": "ICE2QR4565G", "manuf": "Infineon", "v_max": 800, "package": "DIP8", "psr": True, "notes": "StackFET, 65 kHz, 4 W OB"},
    {"ref": "ICE5QR4780AG", "manuf": "Infineon", "v_max": 800, "package": "DIP8", "psr": True, "notes": "StackFET, 80 kHz, 5 W OB"},
    {"ref": "VIPER35HD", "manuf": "ST", "v_max": 800, "package": "DIP8", "psr": True, "notes": "StackFET, 60 kHz"},
    {"ref": "VIPER35LD", "manuf": "ST", "v_max": 800, "package": "SOP8", "psr": True, "notes": "StackFET, 60 kHz SMD"},
    {"ref": "NCP1379", "manuf": "ON Semi", "v_max": 600, "package": "SOP8", "psr": False, "notes": "CRM/DCM, external MOSFET"},
    {"ref": "LNK306P", "manuf": "PI", "v_max": 700, "package": "DIP8", "psr": True, "notes": "LinkSwitch, 360 mA max"},
    {"ref": "TEA1721", "manuf": "NXP", "v_max": 800, "package": "DIP8", "psr": False, "notes": "SSR, external MOSFET"},
]

DEFAULT_MOSFETS = [
    {"ref": "IPW90R120C3", "v_ds": 900, "rds_on": 120, "package": "TO247", "qg": 54},
    {"ref": "IPW90R250C3", "v_ds": 900, "rds_on": 250, "package": "TO247", "qg": 29},
    {"ref": "STW11NM80", "v_ds": 800, "rds_on": 420, "package": "TO247", "qg": 20},
    {"ref": "IPD60R385C7", "v_ds": 600, "rds_on": 385, "package": "TO252", "qg": 8},
    {"ref": "SPA07N65C3", "v_ds": 650, "rds_on": 570, "package": "TO220", "qg": 24},
    {"ref": "FCH072N65S3", "v_ds": 650, "rds_on": 72, "package": "TO247", "qg": 175},
]

class ComponentManager:
    """Manages component databases (Ferrites, MOSFETs, Controllers).
    Handles saving/loading from JSON for persistence.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ComponentManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
        
    def _initialize(self):
        # Determine the paths
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(base_dir, "data")
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        self.files = {
            "cores": os.path.join(self.data_dir, "cores_db.json"),
            "controllers": os.path.join(self.data_dir, "controllers_db.json"),
            "mosfets": os.path.join(self.data_dir, "mosfets_db.json"),
        }
        
        self.defaults = {
            "cores": DEFAULT_CORES,
            "controllers": DEFAULT_CONTROLLERS,
            "mosfets": DEFAULT_MOSFETS,
        }
        
        # In-memory storage
        self.data = {}
        self.load_all()

    def load_all(self):
        """Loads all components from JSON. If missing, creates them from defaults."""
        for key, filepath in self.files.items():
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    try:
                        self.data[key] = json.load(f)
                    except json.JSONDecodeError:
                        self.data[key] = self.defaults[key][:]
            else:
                self.data[key] = self.defaults[key][:]
                self.save(key)
                
    def save(self, key: str):
        """Saves a specific component category to JSON."""
        with open(self.files[key], "w", encoding="utf-8") as f:
            json.dump(self.data[key], f, indent=4)
            
    def get_components(self, key: str) -> list[dict]:
        """Returns the list of components for a given category."""
        return self.data.get(key, [])
        
    def add_component(self, key: str, comp_data: dict):
        """Adds a new component to the specified category."""
        if key in self.data:
            # Optionally check if ref already exists and update, or just append
            existing_index = next((i for i, c in enumerate(self.data[key]) if c["ref"] == comp_data["ref"]), None)
            if existing_index is not None:
                self.data[key][existing_index] = comp_data
            else:
                self.data[key].append(comp_data)
            self.save(key)
            
    def delete_component(self, key: str, ref: str):
        """Deletes a component by reference from the specified category."""
        if key in self.data:
            self.data[key] = [c for c in self.data[key] if c["ref"] != ref]
            self.save(key)
