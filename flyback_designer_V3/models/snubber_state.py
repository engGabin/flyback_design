from PyQt6.QtCore import QObject, pyqtSignal
from dataclasses import dataclass

class SnubberSignals(QObject):
    snubber_changed = pyqtSignal()
    any_changed = pyqtSignal()

@dataclass
class SnubberState:
    # Inputs
    k_cl: float = 0.0           # [-]
    k_Vwm: float = 0.0          # [-]

    delta_v_sn: float = 0.0     # [V]
    sn_f_sw: float = 0.0        # [Hz]

    sn_i_p_max: float = 0.0     # [A]
    sn_Vout: float = 0.0        # [V]

    sn_Lp: float = 0.0          # [H]
    sn_Llk: float = 0.0         # [H]
    sn_Cp: float = 0.0          # [F]
    sn_v_F: float = 0.0         # [V]
    sn_Np: float = 0.0          # [-]
    sn_Ns: float = 0.0          # [-]
    
    def __post_init__(self):
        self.signals = SnubberSignals()

    def notify(self, section: str = ""):
        self.signals.snubber_changed.emit()
        self.signals.any_changed.emit()


@dataclass
class SnubberResults:
    # Outputs
    v_sn: float = 0.0
    p_sn: float = 0.0
    r_sn: float = 0.0
    c_sn: float = 0.0
    v_clamp: float = 0.0
    v_rwm: float = 0.0
    sn_vor: float = 0.0
