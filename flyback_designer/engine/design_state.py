"""
DesignState — single source of truth for all design parameters.
All UI pages read from and write to this object.
Signals notify dependent pages when upstream values change.
"""

from dataclasses import dataclass, field
from PyQt6.QtCore import QObject, pyqtSignal


class DesignStateSignals(QObject):
    """Qt signals emitted when DesignState sections change."""
    input_specs_changed   = pyqtSignal()
    input_stage_changed   = pyqtSignal()
    structure_changed     = pyqtSignal()
    transformer_changed   = pyqtSignal()
    waveforms_changed     = pyqtSignal()
    wire_sections_changed = pyqtSignal()
    losses_changed        = pyqtSignal()
    snubber_changed       = pyqtSignal()
    output_stage_changed  = pyqtSignal()
    any_changed           = pyqtSignal()


@dataclass
class DesignState:
    """
    Central data model for the flyback power supply designer.
    Grouped by design stage; computed results sit alongside user inputs.
    """

    # ------------------------------------------------------------------ #
    # 1 — Input specifications (user-entered)
    # ------------------------------------------------------------------ #
    Vac_min: float = 85.0       # V  — minimum AC input voltage
    Vac_max: float = 528.0      # V  — maximum AC input voltage
    f_line:  float = 50.0       # Hz — line frequency
    P_out:   float = 10.0       # W  — output power
    V_out:   float = 12.0       # V  — output voltage
    I_out:   float = 0.833      # A  — output current (= P_out / V_out)
    eta:     float = 0.80       # —  — target efficiency
    f_sw:    float = 65e3       # Hz — switching frequency
    D_max:   float = 0.45       # —  — maximum duty cycle

    # ------------------------------------------------------------------ #
    # 2 — Input stage (computed)
    # ------------------------------------------------------------------ #
    V_bulk_min:   float = 0.0   # V  — minimum bulk voltage after rectifier
    V_bulk_max:   float = 0.0   # V  — maximum bulk voltage after rectifier
    C_in:         float = 0.0   # µF — bulk input capacitor
    C_in_voltage: float = 0.0   # V  — capacitor voltage rating
    t_hold:       float = 0.010 # s  — hold-up time target (10 ms default)
    I_in_rms:     float = 0.0   # A  — input RMS current
    P_in:         float = 0.0   # W  — input power (= P_out / eta)

    # ------------------------------------------------------------------ #
    # 3 — Switching structure
    # ------------------------------------------------------------------ #
    # "stackfet" | "driver_ext" | "ic_only"
    structure_type: str = "stackfet"
    V_mosfet:       float = 1000.0  # V  — MOSFET voltage rating
    controller_ref: str   = ""      # e.g. "ICE2QR4565G"
    mosfet_ref:     str   = ""      # e.g. "IPW90R120C3"

    # ------------------------------------------------------------------ #
    # 4 — Transformer (user + computed)
    # ------------------------------------------------------------------ #
    L_mag:       float = 0.0    # mH  — magnetising inductance
    N_p:         int   = 0      # —   — primary turns
    N_s:         int   = 0      # —   — secondary turns
    n:           float = 0.0    # —   — turns ratio Np/Ns
    V_or:        float = 0.0    # V   — output voltage reflected to primary
    core_ref:    str   = ""     # e.g. "E25/13/7"
    A_e:         float = 0.0    # mm² — effective core area
    A_w:         float = 0.0    # mm² — winding area
    A_L:         float = 0.0    # nH/t² — inductance factor
    l_gap:       float = 0.0    # mm  — air gap length
    B_max:       float = 0.0    # T   — peak flux density

    # ------------------------------------------------------------------ #
    # 5 — Waveforms (computed, DCM assumed)
    # ------------------------------------------------------------------ #
    I_pk_pri:    float = 0.0    # A  — primary peak current
    I_rms_pri:   float = 0.0    # A  — primary RMS current
    I_rms_sec:   float = 0.0    # A  — secondary RMS current
    I_pk_sec:    float = 0.0    # A  — secondary peak current
    t_on:        float = 0.0    # µs — on-time at Vbulk_min
    t_off:       float = 0.0    # µs — off-time (demagnetisation)
    D_actual:    float = 0.0    # —  — actual duty cycle

    # ------------------------------------------------------------------ #
    # 6 — Wire sections
    # ------------------------------------------------------------------ #
    J_pri:       float = 4.0    # A/mm² — primary current density
    J_sec:       float = 4.0    # A/mm² — secondary current density
    S_pri_mm2:   float = 0.0    # mm²   — primary wire cross-section
    S_sec_mm2:   float = 0.0    # mm²   — secondary wire cross-section
    AWG_pri:     str   = ""
    AWG_sec:     str   = ""
    use_litz:    bool  = False

    # ------------------------------------------------------------------ #
    # 7 — Losses (computed)
    # ------------------------------------------------------------------ #
    P_sw:        float = 0.0    # W — switching losses (MOSFET)
    P_cond:      float = 0.0    # W — conduction losses (MOSFET)
    P_core:      float = 0.0    # W — core losses
    P_diode:     float = 0.0    # W — output diode losses
    P_total_loss:float = 0.0    # W — total estimated losses
    eta_actual:  float = 0.0    # — — actual efficiency estimate

    # ------------------------------------------------------------------ #
    # 8 — Snubber (RCD)
    # ------------------------------------------------------------------ #
    V_clamp:     float = 0.0    # V  — clamp voltage
    C_snub:      float = 0.0    # nF — snubber capacitor
    R_snub:      float = 0.0    # kΩ — snubber resistor
    P_snub:      float = 0.0    # W  — snubber dissipation
    V_spike_est: float = 0.0    # V  — estimated spike without snubber
    L_leak:      float = 0.0    # µH — estimated leakage inductance

    # ------------------------------------------------------------------ #
    # 9 — Output stage
    # ------------------------------------------------------------------ #
    V_diode_fwd: float = 0.5    # V  — output diode forward voltage
    I_diode_avg: float = 0.0    # A  — average diode current
    diode_ref:   str   = ""
    C_out:       float = 0.0    # µF — output capacitor
    C_out_esr:   float = 0.0    # mΩ — output cap ESR
    V_ripple:    float = 0.0    # mV — output voltage ripple
    has_postfilter: bool = False
    L_pf:        float = 0.0    # µH — post-filter inductance
    C_pf:        float = 0.0    # µF — post-filter capacitor

    # ------------------------------------------------------------------ #
    # Qt signal hub (not serialised)
    # ------------------------------------------------------------------ #
    def __post_init__(self):
        self.signals = DesignStateSignals()

    def notify(self, section: str):
        """
        Emit the appropriate signal after a section's values change.
        Also always emits any_changed for global listeners (e.g. status bar).
        """
        sig_map = {
            "input_specs":   self.signals.input_specs_changed,
            "input_stage":   self.signals.input_stage_changed,
            "structure":     self.signals.structure_changed,
            "transformer":   self.signals.transformer_changed,
            "waveforms":     self.signals.waveforms_changed,
            "wire_sections": self.signals.wire_sections_changed,
            "losses":        self.signals.losses_changed,
            "snubber":       self.signals.snubber_changed,
            "output_stage":  self.signals.output_stage_changed,
        }
        if section in sig_map:
            sig_map[section].emit()
        self.signals.any_changed.emit()

    def to_dict(self) -> dict:
        """Serialise to plain dict (for JSON project file)."""
        import dataclasses
        d = dataclasses.asdict(self)
        d.pop("signals", None)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "DesignState":
        """Restore from a plain dict (loaded from JSON project file)."""
        import dataclasses
        fields = {f.name for f in dataclasses.fields(cls)}
        filtered = {k: v for k, v in d.items() if k in fields}
        return cls(**filtered)
