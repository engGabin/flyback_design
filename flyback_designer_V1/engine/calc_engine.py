"""
CalcEngine — pure-Python calculation stubs for every design stage.
Each function takes the DesignState, updates it in-place, and returns it.
Pages call these after user input; results propagate via DesignState.notify().

All formulas are documented with their source equation in comments.
"""

import math
from .design_state import DesignState


# ------------------------------------------------------------------ #
# 1 — Input stage
# ------------------------------------------------------------------ #

def calc_input_stage(ds: DesignState) -> DesignState:
    """
    Compute bulk voltage range and minimum input capacitor.

    Vbulk_max = Vac_max * sqrt(2)
    Vbulk_min = Vac_min * sqrt(2) - ΔV  (hold-up droop)
    Cin ≥ 2 * P_in * t_hold / (Vbulk_min² - Vbulk_min_target²)
    """
    ds.P_in = ds.P_out / max(ds.eta, 0.01)

    ds.V_bulk_max = ds.Vac_max * math.sqrt(2)
    ds.V_bulk_min = ds.Vac_min * math.sqrt(2)

    # Hold-up: capacitor must supply P_in for t_hold, down to 0.9*Vbulk_min
    V_end = 0.90 * ds.V_bulk_min
    delta_E = ds.P_in * ds.t_hold
    dV2 = ds.V_bulk_min ** 2 - V_end ** 2
    if dV2 > 0:
        ds.C_in = (2 * delta_E / dV2) * 1e6  # µF
    else:
        ds.C_in = 0.0

    ds.C_in_voltage = ds.V_bulk_max * 1.15  # 15 % margin
    ds.I_in_rms = ds.P_in / (ds.Vac_min * 0.9)  # rough estimate

    ds.notify("input_stage")
    return ds


# ------------------------------------------------------------------ #
# 4 — Transformer (DCM flyback)
# ------------------------------------------------------------------ #

def calc_transformer(ds: DesignState) -> DesignState:
    """
    DCM flyback magnetising inductance:

    L_mag = (Vbulk_min * D_max)² / (2 * P_in * f_sw)    [H]

    Peak primary current:
    I_pk = Vbulk_min * D_max / (L_mag * f_sw)

    Turns ratio:
    n = Np/Ns = (Vbulk_min * D_max) / ((V_out + V_diode) * (1 - D_max))
    """
    if ds.V_bulk_min <= 0 or ds.f_sw <= 0:
        return ds

    # Magnetising inductance
    num = (ds.V_bulk_min * ds.D_max) ** 2
    den = 2 * ds.P_in * ds.f_sw
    ds.L_mag = (num / den) * 1e3  # mH

    # Peak primary current
    ds.I_pk_pri = (ds.V_bulk_min * ds.D_max) / (ds.L_mag * 1e-3 * ds.f_sw)

    # Turns ratio
    V_sec = ds.V_out + ds.V_diode_fwd
    if V_sec > 0:
        ds.n = (ds.V_bulk_min * ds.D_max) / (V_sec * (1 - ds.D_max))
        ds.V_or = V_sec * ds.n

    # Primary turns (rough estimate from core Ae and B_max)
    if ds.A_e > 0:
        B_pk = 0.25  # T default
        ds.B_max = B_pk
        ds.N_p = math.ceil(
            (ds.L_mag * 1e-3 * ds.I_pk_pri) / (B_pk * ds.A_e * 1e-6)
        )
        ds.N_s = max(1, round(ds.N_p / ds.n)) if ds.n > 0 else 0

    ds.notify("transformer")
    return ds


# ------------------------------------------------------------------ #
# 5 — Waveforms
# ------------------------------------------------------------------ #

def calc_waveforms(ds: DesignState) -> DesignState:
    """
    DCM waveform parameters.

    t_on  = D_max / f_sw
    t_off = L_mag * I_pk / (V_or)     [demagnetisation time]

    I_rms_pri = I_pk * sqrt(D/3)
    I_rms_sec = I_pk_sec * sqrt(D_off/3)
    """
    if ds.L_mag <= 0 or ds.f_sw <= 0:
        return ds

    ds.t_on  = (ds.D_max / ds.f_sw) * 1e6   # µs
    L = ds.L_mag * 1e-3  # H

    if ds.V_or > 0:
        ds.t_off = (L * ds.I_pk_pri / ds.V_or) * 1e6  # µs
        D_off = (ds.t_off * 1e-6) * ds.f_sw
    else:
        ds.t_off  = 0.0
        D_off     = 0.0

    ds.D_actual  = ds.D_max
    ds.I_rms_pri = ds.I_pk_pri * math.sqrt(ds.D_actual / 3)

    if ds.n > 0:
        ds.I_pk_sec  = ds.I_pk_pri * ds.n
        ds.I_rms_sec = ds.I_pk_sec * math.sqrt(D_off / 3)

    ds.notify("waveforms")
    return ds


# ------------------------------------------------------------------ #
# 6 — Wire sections
# ------------------------------------------------------------------ #

def calc_wire_sections(ds: DesignState) -> DesignState:
    """
    Section = I_rms / J    [mm²]
    AWG lookup from cross-section.
    """
    if ds.J_pri > 0 and ds.I_rms_pri > 0:
        ds.S_pri_mm2 = ds.I_rms_pri / ds.J_pri
        ds.AWG_pri   = _mm2_to_awg(ds.S_pri_mm2)

    if ds.J_sec > 0 and ds.I_rms_sec > 0:
        ds.S_sec_mm2 = ds.I_rms_sec / ds.J_sec
        ds.AWG_sec   = _mm2_to_awg(ds.S_sec_mm2)

    ds.notify("wire_sections")
    return ds


def _mm2_to_awg(mm2: float) -> str:
    """Approximate AWG from cross-section in mm²."""
    awg_table = [
        (0.0507, "30"), (0.0804, "28"), (0.128, "26"), (0.205, "24"),
        (0.326, "22"), (0.518, "20"), (0.823, "18"), (1.31, "16"),
        (2.08, "14"),  (3.31, "12"),  (5.26, "10"),  (8.37,  "8"),
    ]
    for area, awg in awg_table:
        if mm2 <= area:
            return f"AWG {awg}"
    return "AWG <8"


# ------------------------------------------------------------------ #
# 7 — Losses (placeholder)
# ------------------------------------------------------------------ #

def calc_losses(ds: DesignState) -> DesignState:
    """Stub — will be filled with Coss, Rds_on, Steinmetz parameters."""
    # Rough estimate: 1 - eta fraction of P_in
    ds.P_total_loss = ds.P_in * (1 - ds.eta)
    ds.P_sw   = ds.P_total_loss * 0.40
    ds.P_cond = ds.P_total_loss * 0.30
    ds.P_core = ds.P_total_loss * 0.20
    ds.P_diode= ds.P_total_loss * 0.10
    ds.eta_actual = ds.P_out / max(ds.P_in, 0.001)
    ds.notify("losses")
    return ds


# ------------------------------------------------------------------ #
# 8 — Snubber (RCD)
# ------------------------------------------------------------------ #

def calc_snubber(ds: DesignState) -> DesignState:
    """
    RCD snubber sizing.
    V_spike ≈ n * V_out + V_bulk_max + V_leakage_spike
    V_clamp = 1.3 * (n * V_out + V_bulk_max)

    C_snub ≥ L_leak * I_pk² / (V_clamp - n*V_out - V_bulk_max)²
    R_snub = V_clamp² / (P_snub * 2) — losses split between R and forward voltage
    """
    V_reflected = ds.n * (ds.V_out + ds.V_diode_fwd) if ds.n > 0 else 0
    ds.V_spike_est = ds.V_bulk_max + V_reflected + 100  # rough estimate
    ds.V_clamp = 1.30 * (ds.V_bulk_max + V_reflected)

    delta_V = ds.V_clamp - V_reflected
    if delta_V > 0 and ds.L_leak > 0:
        L = ds.L_leak * 1e-6
        ds.C_snub = (L * ds.I_pk_pri ** 2 / delta_V ** 2) * 1e9  # nF

    # Snubber dissipation ≈ 0.5 * L_leak * I_pk² * f_sw
    if ds.L_leak > 0:
        ds.P_snub = 0.5 * (ds.L_leak * 1e-6) * ds.I_pk_pri ** 2 * ds.f_sw

    if ds.P_snub > 0 and ds.V_clamp > 0:
        ds.R_snub = (ds.V_clamp ** 2 / ds.P_snub) * 1e-3  # kΩ

    ds.notify("snubber")
    return ds


# ------------------------------------------------------------------ #
# 9 — Output stage
# ------------------------------------------------------------------ #

def calc_output_stage(ds: DesignState) -> DesignState:
    """
    Output capacitor from ripple spec:
    C_out = I_out / (f_sw * ΔV_ripple)

    Output diode average current = I_out.
    """
    target_ripple_V = ds.V_out * 0.01  # 1 % ripple target
    if ds.f_sw > 0:
        ds.C_out = (ds.I_out / (ds.f_sw * target_ripple_V)) * 1e6  # µF

    ds.V_ripple    = target_ripple_V * 1e3  # mV
    ds.I_diode_avg = ds.I_out
    ds.P_diode     = ds.V_diode_fwd * ds.I_out

    ds.notify("output_stage")
    return ds


# ------------------------------------------------------------------ #
# Full recalculation chain
# ------------------------------------------------------------------ #

def recalc_all(ds: DesignState) -> DesignState:
    """
    Run the complete design chain in dependency order.
    Called when input specs change.
    """
    calc_input_stage(ds)
    calc_transformer(ds)
    calc_waveforms(ds)
    calc_wire_sections(ds)
    calc_losses(ds)
    calc_snubber(ds)
    calc_output_stage(ds)
    return ds
