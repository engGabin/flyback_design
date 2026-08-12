# =======================================================
# File : flyback_states.py
# Author : Gabin SBAFFI
# Date : 2026-07-29
# Description : this file contains all variables necessaries for design
# =======================================================

import math
from PyQt6.QtCore import QObject, pyqtSignal
from dataclasses import dataclass

@dataclass
class FlybackState:
    """This class serves solely as a memory (internal database).
        It stores the input specifications (what the user types)."""

    # ========================================================
    # 1. INPUT SPECIFICATIONS (user input)
    # ========================================================
    vac_min: float = 85.0          # Minimum AC input voltage [V]
    vac_max: float = 528.0         # Maximum AC input voltage [V]
    f_line: float = 50.0           # Line frequency [Hz]

    p_out1: float = 7.0            # Output power 1 [W]
    v_out1: float = 12.0           # Output voltage 1 [V]
    i_out1: float = 0.0            # Output current 1 [A]
    p_out2: float = 0.0            # Output power 2 [W]
    v_out2: float = 0.0            # Output voltage 2 [V]
    i_out2: float = 0.0            # Output current 2 [A]
    p_aux: float = 0.0             # Auxiliary output power [W]
    v_aux: float = 0.0             # Auxiliary output voltage [V]
    i_aux: float = 0.0             # Auxiliary output current [A]

    p_out_total: float = 0.0
    p_in: float = 0.0    

    Nh: float = 1.0                # Number of Hold-Ups
    delta_v_bulk: float = 0.25     # Maximum voltage ripple allowed on the bulk capacitor
    
    # ========================================================
    # 2. INPUT STAGE (computed)
    # ========================================================
    v_in_max: float = 0.0          # maximum input voltage 
    v_in_min: float = 0.0          # minimum input voltage 
    v_bulk_min: float = 0.0        # minimum bulk voltage based on the voltage drop across a capacitor
    v_bulk_min_nH: float = 0.0     # minimum bulk voltage based on the voltage drop across a capacitor with hold-up
    c_bulk: float = 0.0            # Input bulk capacitor [F]

    # ========================================================
    # 3. SWITCHING STRUCTURE
    # ========================================================
    # "stackfet" | "driver_ext" | "ic_only"
    structure_type: str = "stackfet"
    V_mosfet:       float = 1000.0  # V  — MOSFET voltage rating
    controller_ref: str   = ""      # e.g. "ICE2QR4565G"
    mosfet_ref:     str   = ""      # e.g. "IPW90R120C3"
    vds_on: float = 0.0             # voltage across the primary switch when it is on
    r_ds_on: float = 0.62          # ON resistance of the primary switch [Ohm]
    MOS_Eoss: float = 0.0
    MOS_r_th: float = 0.0
    MOS_ton: float = 0.0
    MOS_toff: float = 0.0

    # ========================================================
    # 4. PRE-DESIGN CHOICES 
    # ========================================================
    eta: float = 0.85              # Estimated efficiency of the converter
    D_max: float = 0.61            # maximum duty cycle
    f_sw: float = 132e3            # switching frequency [Hz]
    Krp: float = 1.0               # ripple factor (1 for DCM, <1 for CCM)

    # ========================================================
    # 5. PRE-DESIGN CHOICES (transformer specifications)
    # ========================================================
    B_max: float = 0.3092             # Maximum flux density in the core [T]
    J_max: float = 6.0             # Maximum current density in the winding [A/m^2]
    T_max: float = 100.0           # Maximum temperature rise in the transformer [°C]
    T_amb: float = 25.0            # Ambient temperature [°C]
    Ku: float = 0.4                # Window utilization factor
    
    # Variables dépendantes (initialisées à 0, calculées dans __post_init__)
    kb: float = 0.0                 # bobbin factor

    # ========================================================
    # 6. TRANSFORMER (user + computed)
    # ========================================================
    Np: float = 11.10               # primary turns
    Ns1: float = 1.0                # secondary turns 1
    Ns2: float = 0.0                # secondary turns 2
    Naux: float = 0.0               # auxiliary turns

    # Computed variables
    Lp: float = 0.0  
    Lp_real: float = 0.0  
    vor: float = 0.0                # reflected voltage on the primary side
    B_max_real: float = 0.0              # maximum flux density
    AeAw_calc: float = 0.0          # area product
    Np_Ns1: float = 0.0             # turns ratio primary to secondary 1
    Np_Ns2: float = 0.0             # turns ratio primary to secondary 2
    Np_Naux: float = 0.0            # turns ratio primary to auxiliary  
    lg: float = 0.0                 # air gap length
    Fringing: float = 0.0           # fringing flux factor

    # ========================================================
    # 7. FERRITE SELECTION
    # ========================================================        
    core_ref:    str   = ""     # e.g. "E25/13/7"
    Ae: float = 103.0                
    Aw: float = 25.0
    Ve: float = 3300.0
    le: float = 36.0
    Al: float = 629.0
    Wtfe: float = 0.0
    MTl: float = 7.0
    g: float = 21.0
    Pv: float = 0.0
    mu_core: float = 5000.0

    # Variable dépendante
    AeAw_real: float = 0.0

    lp: float = 0.0             # length of the primary coil
    ls1: float = 0.0            # length of the first secondary coil
    ls2: float = 0.0            # length of the second secondary coil
    laux: float = 0.0           # length of the auxiliary coil

    # ========================================================
    # 8. PRIMARY CURRENTS (computed)
    # ========================================================
    i_p_max: float = 0.0           # maximum primary current
    i_p_rms: float = 0.0           # RMS primary current
    i_p_avg: float = 0.0           # average primary current
    i_p_avg_on: float = 0.0        # average primary current when the switch is on
    delta_i_p: float = 0.0         # primary current ripple
    i_p_valley: float = 0.0        # primary current valley
    i_p_dc: float = 0.0            # DC component of the primary current
    i_p_ac: float = 0.0            # AC component of the primary current 

    # ========================================================
    # 9. SECONDARY CURRENTS (computed)
    # ========================================================   
    D_out: float = 0.0             # duty cycle of the secondary side
    D_m: float = 0.0               # duty cycle linked to dead time

    i_s1_max: float = 0.0           # maximum secondary current
    i_s1_rms: float = 0.0           # RMS secondary current
    i_s1_valley: float = 0.0        # secondary current valley
    delta_i_s1: float = 0.0         # secondary current ripple
    i_s1_dc: float = 0.0            # DC component of the secondary current
    i_s1_ac: float = 0.0            # AC component of the secondary current 
    i_out1: float = 0.0            # output current 1
    i_out2: float = 0.0            # output current 2
    i_aux: float = 0.0             # auxiliary output current   

    # ========================================================
    # 10. WIRE SELECTION (user + computed)
    # ========================================================
    Dp: float = 0.0                 # primary wire diameter
    Sp_eff: float = 0.0             # effective cross-sectional area of the primary wire
    strands_p: int = 0              # number of strands in the primary wire
    Ds1: float = 0.0                # secondary wire diameter 1
    Ss1_eff: float = 0.0            # effective cross-sectional area of the secondary wire 1
    strands_s1: int = 0             # number of strands in the secondary wire 1
    Ds2: float = 0.0                # secondary wire diameter 2
    Ss2_eff: float = 0.0            # effective cross-sectional area of the secondary wire 2
    strands_s2: int = 0             # number of strands in the secondary wire 2
    Daux: float = 0.0               # auxiliary wire diameter
    Saux_eff: float = 0.0           # effective cross-sectional area of the auxiliary wire
    strands_aux: int = 0            # number of strands in the auxiliary wire  

    delta_cm: float = 0.0           # skin depth in cm
    D_awg_max_: float = 0.0         # Maximum AWG diameter to avoid the skin effect
    s_w_: float = 0.0               # Bare wire section based on the skin effect (reference for the number of strands)
    Aw_used: float = 0.0            # Window area used for the winding
    fits_in_core: bool = False      # Does the total copper area fit within the core window area (Aw)?

    AWG_pri:     str   = ""
    AWG_sec:     str   = ""
    use_litz:    bool  = False

    # ========================================================
    # 11. LOSSES (computed) 
    # ========================================================
    rho_cu_20: float = 1.724e-8         # Ω·m — copper resistivity at 20°C
    rho_cu_100: float = 23e-6           # Ω·m — copper resistivity at 100°C
    mu_0: float = 4 * math.pi * 1e-7    # H/m — permeability of free space 
    mu_r_nonMagnetic: float = 1.0       # relative permeability of non-magnetic materials

    r_dc_p: float = 0.0                 # Ω — dc resistance of the primary coil
    r_dc_s1: float = 0.0                # Ω — dc resistance of the secondary coil 1
    r_dc_s2: float = 0.0                # Ω — dc resistance of the secondary coil 2
    r_dc_aux: float = 0.0               # Ω — dc resistance of the auxiliary coil

    r_ac_p: float = 0.0                 # Ω — ac resistance of the primary coil
    r_ac_s1: float = 0.0                # Ω — ac resistance of the secondary coil 1
    r_ac_s2: float = 0.0                # Ω — ac resistance of the secondary coil 2
    r_ac_aux: float = 0.0               # Ω — ac resistance of the auxiliary coil

    # Dowell coefficients based on the diameters, the frequencies and the layers
    K_ac_p: float = 0.0                 # Coefficient of the ac resistance of the primary coil
    K_ac_s1: float = 0.0                # Coefficient of the ac resistance of the secondary coil 1
    K_ac_s2: float = 0.0                # Coefficient of the ac resistance of the secondary coil 2
    K_ac_aux: float = 0.0               # Coefficient of the ac resistance of the auxiliary coil

    # Core losses
    delta_B_dcm: float = 0.0            # Wb/m² — flux density in DCM
    delta_B_ccm: float = 0.0            # Wb/m² — flux density in DCM
    B_ac: float = 0.0                   
    k: float = 0.0                      # Core loss coefficient
    alpha: float = 0.0                  # Core loss exponent for frequency
    beta: float = 0.0                   # Core loss exponent for flux density
    Pfe: float = 0.0                    # W — core losses
    
    # Copper losses
    P_cu_p: float = 0.0                 # W — primary copper losses 
    P_cu_s1: float = 0.0                # W — secondary copper losses 1
    P_cu_s2: float = 0.0                # W — secondary copper losses 2
    P_cu_aux: float = 0.0               # W — auxiliary copper losses
    P_cu_total: float = 0.0             # W — total copper losses

    # MOSFET losses
    P_sw:float = 0.0                    # W — switching losses (MOSFET)
    P_cond: float = 0.0                 # W — conduction losses (MOSFET)
    P_coss: float = 0.0                 # W — Coss losses (MOSFET)
    P_sw_off: float = 0.0               # W — Switching losses - turn off (MOSFET)
    P_sw_on: float = 0.0                # W — Switching losses - turn on (MOSFET)
    P_mosfet: float = 0.0               # W - Total losses of the MOSFET
    MOS_Tj: float = 0.0                 # °C - Junction temperature (<150°C)
    
    # Diodes losses
    P_diode:     float = 0.0            # W — output diode losses

    # Capacitors losses
    P_c_out1: float = 0.0
    P_c_out2: float = 0.0
    P_c_bulk: float = 0.0

    P_total_loss:float = 0.0            # W — total estimated losses
    eta_actual:  float = 0.0            # — — actual efficiency estimate

    # ========================================================
    # 12. SNUBBER (user + computed) 
    # ========================================================
    V_clamp:     float = 0.0    # V  — clamp voltage
    C_snub:      float = 0.0    # nF — snubber capacitor
    R_snub:      float = 0.0    # kΩ — snubber resistor
    P_snub:      float = 0.0    # W  — snubber dissipation
    V_spike_est: float = 0.0    # V  — estimated spike without snubber
    L_leak:      float = 0.0    # µH — estimated leakage inductance

    # ========================================================
    # 13. OUTPUT STAGE (user + computed) 
    # ========================================================
    v_F: float = 0.7                # V  — output diode forward voltage
    I_diode_avg: float = 0.0        # A  — average diode current
    diode_ref:   str   = ""
    C_out1:       float = 0.0       # µF — output capacitor 1
    C_out1_esr:   float = 0.0       # mΩ — output cap ESR 1
    delta_Vout1:    float = 0.0     # %  — output voltage ripple 1
    C_out2:       float = 0.0       # µF — output capacitor 2
    C_out2_esr:   float = 0.0       # mΩ — output cap ESR 2
    delta_Vout2:    float = 0.0     # %  — output voltage ripple 2

    has_postfilter: bool = False
    L_pf:        float = 0.0    # µH — post-filter inductance
    C_pf:        float = 0.0    # µF — post-filter capacitor

    # ========================================================
    # DATASHEET PARAMETERS
    # ========================================================
    cap_ESR: float = 0.0 
  
    def __post_init__(self):
            """
            This method runs automatically after the object is created.
            It is used to calculate variables that depend on other variables.
            """
            self.kb = 1 / self.Ku
            self.AeAw_real = self.Ae * self.Aw
            self.signals = DesignStateSignals()
    
    def notify(self, section: str = "all"):
        """
        Emit the appropriate signal after a section's values change.
        Also always emits any_changed for global listeners (e.g. status bar).
        """
        sig_map = {
            "input_specs":   self.signals.input_specs_changed,
            "input_stage":   self.signals.input_stage_changed,
            "structure":     self.signals.structure_changed,
            "transformer":   self.signals.transformer_changed,
            "transformer_recap": self.signals.transformer_recap_changed,
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
    def from_dict(cls, d: dict) -> "FlybackState":
        """Restore from a plain dict (loaded from JSON project file)."""
        import dataclasses
        fields = {f.name for f in dataclasses.fields(cls)}
        filtered = {k: v for k, v in d.items() if k in fields}
        return cls(**filtered)

@dataclass
class FlybackResults:
    """This class serves solely as a memory (internal database).
        It stores the results (what the calculation engine calculates)."""

    # ========================================================
    # 1. INPUT SPECIFICATIONS (user input)
    # ========================================================
    
    # ========================================================
    # 2. INPUT STAGE
    # ========================================================
    delta_v_bulk_calc: float = 0.25     # Maximum voltage ripple allowed on the bulk capacitor
    v_bulk_min_calc: float = 0.0        # minimum bulk voltage based on the voltage drop across a capacitor
    v_bulk_min_nH_calc: float = 0.0     # minimum bulk voltage based on the voltage drop across a capacitor with hold-up
    c_bulk_calc: float = 0.0            # Input bulk capacitor [F]
    c_bulk_std: float = 0.0             # Standard input bulk capacitor [F]
    delta_T_calc: float = 0.0         
    t_d_calc: float = 0.0               # discharge time of the bulk capacitor
    t_d_nH_calc: float = 0.0            # discharge time of the bulk capacitor without hold-up  
    t_c_calc: float = 0.0               # charge time of the bulk capacitor

    # ========================================================
    # 3. SWITCHING STRUCTURE
    # ========================================================
    vds_on_calc: float = 0.0             # voltage across the primary switch when it is on

    # ========================================================
    # 4. PRE-DESIGN CHOICES 
    # ========================================================

    # ========================================================
    # 5. PRE-DESIGN CHOICES (transformer specifications)
    # ========================================================

    # ========================================================
    # 6. TRANSFORMER 
    # ========================================================
    Np_calc: float = 11.10               # primary turns
    Ns1_calc: float = 1.0                # secondary turns 1
    Ns2_calc: float = 0.0                # secondary turns 2
    Naux_calc: float = 0.0               # auxiliary turns

    AeAw_calc: float = 0.0               # effective cross section area times window area

    Lp_calc: float = 0.0                 # inductance  
    Lp_real_calc: float = 0.0            # inductance real
    vor_calc: float = 0.0                # reflected voltage on the primary side
    B_max_real_calc: float = 0.0         # flux density
    Np_Ns1_calc: float = 0.0             # turns ratio primary to secondary 1
    Np_Ns2_calc: float = 0.0             # turns ratio primary to secondary 2
    Np_Naux_calc: float = 0.0            # turns ratio primary to auxiliary  
    lg_calc: float = 0.0                 # air gap length
    Fringing_calc: float = 0.0           # fringing flux factor

    # ========================================================
    # 7. FERRITE SELECTION
    # ======================================================== 

    # ========================================================
    # 8. PRIMARY CURRENTS
    # ========================================================
    i_p_max_calc: float = 0.0           # maximum primary current
    i_p_rms_calc: float = 0.0           # RMS primary current
    i_p_avg_calc: float = 0.0           # average primary current
    i_p_avg_on_calc: float = 0.0        # average primary current when the switch is on
    delta_i_p_calc: float = 0.0         # primary current ripple
    i_p_valley_calc: float = 0.0        # primary current valley
    i_p_dc_calc: float = 0.0            # DC component of the primary current
    i_p_ac_calc: float = 0.0            # AC component of the primary current

    # ========================================================
    # 9. SECONDARY CURRENTS
    # ========================================================   
    D_out_calc: float = 0.0             # duty cycle of the secondary side
    D_m_calc: float = 0.0               # duty cycle linked to dead time

    i_s_max_calc: float = 0.0           # maximum secondary current
    i_s_rms_calc: float = 0.0           # RMS secondary current
    i_out1_calc: float = 0.0            # output current 1
    i_out2_calc: float = 0.0            # output current 2
    i_aux_calc: float = 0.0             # auxiliary output current   

    # ========================================================
    # 10. WIRE SELECTION
    # ========================================================
    Dp_calc: float = 0.0                 # primary wire diameter
    Sp_eff_calc: float = 0.0             # effective cross-sectional area of the primary wire
    strands_p_calc: int = 0              # number of strands in the primary wire
    Ds1_calc: float = 0.0                # secondary wire diameter 1
    Ss1_eff_calc: float = 0.0            # effective cross-sectional area of the secondary wire 1
    strands_s1_calc: int = 0             # number of strands in the secondary wire 1
    Ds2_calc: float = 0.0                # secondary wire diameter 2
    Ss2_eff_calc: float = 0.0            # effective cross-sectional area of the secondary wire 2
    strands_s2_calc: int = 0             # number of strands in the secondary wire 2
    Daux_calc: float = 0.0               # auxiliary wire diameter
    Saux_eff_calc: float = 0.0           # effective cross-sectional area of the auxiliary wire
    strands_aux_calc: int = 0            # number of strands in the auxiliary wire

    D_awg_max_calc: float = 0.0          # Maximum AWG diameter to avoid the skin effect
    s_w_calc: float = 0.0                # Bare wire section based on the skin effect (reference for the number of strands)
    Aw_used_calc: float = 0.0            # Window area used for the winding
    fits_in_core_calc: bool = False      # Does the total copper area fit within the core window area (Aw)?

    AWG_pri_calc:     str   = ""
    AWG_sec_calc:     str   = ""
    use_litz:    bool  = False

    # ========================================================
    # 11. LOSSES 
    # ========================================================
    P_sw_calc:float = 0.0                    # W — switching losses (MOSFET)
    P_cond_calc: float = 0.0                 # W — conduction losses (MOSFET)
    P_diode_calc:     float = 0.0            # W — output diode losses

    Pfe_calc: float = 0.0                    # W — core losses
    P_cu_p_calc: float = 0.0                 # W — primary copper losses 
    P_cu_s1_calc: float = 0.0                # W — secondary copper losses 1
    P_cu_s2_calc: float = 0.0                # W — secondary copper losses 2
    P_cu_aux_calc: float = 0.0               # W — auxiliary copper losses

    P_total_loss_calc: float = 0.0            # W — total estimated losses
    eta_actual_calc: float = 0.0            # — — actual efficiency estimate

    # ========================================================
    # 12. SNUBBER 
    # ========================================================
    V_clamp_calc:     float = 0.0    # V  — clamp voltage
    C_snub_calc:      float = 0.0    # nF — snubber capacitor
    R_snub_calc:      float = 0.0    # kΩ — snubber resistor
    P_snub_calc:      float = 0.0    # W  — snubber dissipation
    V_spike_est_calc: float = 0.0    # V  — estimated spike without snubber
    L_leak_calc:      float = 0.0    # µH — estimated leakage inductance

    # ========================================================
    # 13. OUTPUT STAGE
    # ========================================================


    # ========================================================
    # DATASHEET PARAMETERS
    # ========================================================
    r_ds_on: float = 0.62          # ON resistance of the primary switch [Ohm]
  
    def __post_init__(self):
            """
            This method runs automatically after the object is created.
            It is used to calculate variables that depend on other variables.
            """
            self.signals = DesignStateSignals()

# ==========================================
# 2. LE SYSTÈME DE SIGNAUX (L'alarme)
# ==========================================
class DesignStateSignals(QObject):
    """Qt signals emitted when DesignState sections change."""
    input_specs_changed   = pyqtSignal()
    input_stage_changed   = pyqtSignal()
    structure_changed     = pyqtSignal()
    transformer_changed   = pyqtSignal()
    transformer_recap_changed = pyqtSignal()
    wire_sections_changed = pyqtSignal()
    losses_changed        = pyqtSignal()
    snubber_changed       = pyqtSignal()
    output_stage_changed  = pyqtSignal()
    any_changed           = pyqtSignal()
    state_changed         = pyqtSignal()

# ==========================================
# 3. LA MÉMOIRE GLOBALE (Le conteneur)
# ==========================================
class DesignStates: 
    def __init__(self):
        self.specs = FlybackState()
        self.results = FlybackResults()
        self.signals = DesignStateSignals()
    
        
