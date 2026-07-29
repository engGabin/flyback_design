import math
from models.design_state import DesignState

def recalc_all(state: DesignState):
    """The pure calculation engine.
        It takes a "state" object as a parameter, reads its input values,
        applies Flyback's physical formulas, and updates the results."""

    # ---------------------------------------------------------
    # Electricals Calculation
    # ---------------------------------------------------------
    state.p_out_total = state.p_out1 + state.p_out2 + state.p_aux
    state.p_in = state.p_out_total / state.eta
    if state.v_out1 > 0:
        state.i_out1 = state.p_out1 / state.v_out1
    else:
        state.i_out1 = 0.0
    if state.v_out2 > 0:
        state.i_out2 = state.p_out2 / state.v_out2
    else:
        state.i_out2 = 0.0
    if state.v_aux > 0:
        state.i_aux = state.p_aux / state.v_aux
    else:
        state.i_aux = 0.0

    state.v_in_min = state.vac_min * math.sqrt(2)
    state.v_in_max = state.vac_max * math.sqrt(2)

    # ---------------------------------------------------------
    # Capacitor Bulk Calculation
    # ---------------------------------------------------------
    v_ripple = state.v_in_min * state.delta_v_bulk
    v_bulk = state.v_in_min - v_ripple
    delta_T = math.asin(v_bulk / state.v_in_min) / (2 * math.pi * state.f_line)
    t_c = 1 / (4 * state.f_line) - delta_T
    t_d = 1 / (2 * state.f_line) - t_c
    t_d_nH = ((1 + 2 * state.Nh)/(2 * state.f_line)) - t_c
    
    state.c_bulk_calc = (2 * state.p_out_total * t_d_nH) / (state.eta * (state.v_in_min**2 - v_bulk**2))

    voltage_part = 2 * (state.vac_min**2)
    discharge_part = (2 * state.p_out_total * t_d) / (state.eta * state.c_bulk)
    if voltage_part >= discharge_part:
        state.v_bulk_min = math.sqrt(voltage_part - discharge_part)
    else:
        state.v_bulk_min = 0.0
        # Error: the capacitor is too small to hold the charge

    # ---------------------------------------------------------
    # Pre-Design Calculation
    # ---------------------------------------------------------
    state.vor = (state.D_max * state.v_bulk_min)/(1 - state.D_max)
    state.vds_on = (state.v_bulk_min + state.vor)/(1 + (state.v_bulk_min * state.vor)/(state.r_ds_on * state.p_in))
    state.Lp_calc = ((((state.v_bulk_min - state.vds_on)**2 * state.D_max**2) / 
                    (state.p_in * state.f_sw * state.Krp))) * (1 - state.Krp/2)

    #---------------------------------------------------------
    # First current estimations 
    #---------------------------------------------------------
    state.Np_Ns1_calc = state.vor / (state.v_out1 + state.v_F)
    state.i_p_avg = state.p_out_total / (state.v_bulk_min * state.eta)
    state.i_p_avg_on = state.p_out_total / (state.v_bulk_min * state.eta * state.D_max)
    state.i_p_max = state.p_in / ((state.v_bulk_min * state.D_max)*(1 - state.Krp/2))
    state.i_p_rms = state.i_p_max * math.sqrt(state.D_max*(state.Krp**2 /3 - state.Krp + 1))   
    state.delta_i_p = state.i_p_max * state.Krp
    state.i_p_valley = state.i_p_max - state.delta_i_p
    state.i_p_dc = state.D_max * state.i_p_max/2
    state.i_p_ac = math.sqrt(state.i_p_rms**2 - state.i_p_dc**2)

    state.D_out = ((state.v_bulk_min - state.vds_on) * state.D_max) / (state.vor)
    state.i_s_max = (2 * state.i_out1)/(state.D_out * (2 - state.Krp))
    state.i_s_rms = state.i_s_max * math.sqrt(state.D_out * (state.Krp**2 /3 - state.Krp + 1))

    #---------------------------------------------------------
    # Transformer Calculation
    #---------------------------------------------------------
    state.AeAw_calc = state.Lp_calc * (state.i_p_max / state.B_max) * state.kb * (
        (state.i_p_rms / state.J_max) + (state.i_s_rms / (state.J_max * state.Np_Ns1_calc)))

    Np_intermediate = math.sqrt(state.Lp_calc/(state.Al * 1e-9))
    lg_mm = ((4*math.pi * 1e-7 * Np_intermediate**2 * state.Ae *1e-6) / state.Lp_calc) - (
        (state.le*1e-3)/state.mu_core) #[m]
    state.lg = lg_mm * 1e3 #[mm]
    state.Fringing = 1 + (lg_mm / (math.sqrt(state.Ae*1e-6))) * math.log((2*state.g*1e-3) / lg_mm)
    state.Np_calc = math.sqrt((state.Lp_calc * lg_mm *1e-7) / (4 * math.pi * state.Ae * state.Fringing))
    state.Lp_real = state.Np**2 * state.Al * 1e-9

    state.B_max_calc = (state.Lp_real * state.i_p_max) / (state.Np * state.Ae * 1e-6)

    #---------------------------------------------------------
    # Second Current Calculations
    #---------------------------------------------------------
    state.Lp = state.Lp_calc
    state.i_p_avg1 = state.i_p_avg 
    state.i_p_avg_on1 = state.i_p_avg_on
    state.delta_i_p1 = (state.v_bulk_min * state.D_max)/(state.Lp * state.f_sw)
    state.i_p_max1 = state.i_p_avg_on1 + state.delta_i_p1/2
    state.i_p_rms1 = math.sqrt((3*state.i_p_avg1**2 + (state.delta_i_p1/2)**2)*(state.D_max/3))
    state.i_p_valley1 = state.i_p_max1 - state.delta_i_p1    
