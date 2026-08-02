# =======================================================
# File : calc_engine.py
# Author : Gabin SBAFFI
# Date : 2026-07-29
# Description : this file is the calculation engine of the flyback designer application.
# =======================================================

import math
from models.flyback_states import *

def calc_inputPower(state: FlybackState):
    """Calculates the input power based on the output power and efficiency.
    Arguments: FlybackState (flyback object with parameters)
    Returns: 
        State -> p_out_total, p_in, i_out1, i_out2, i_aux, v_in_min, v_in_max
    """

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

def calc_bulkCapacitance(result: FlybackResults, state: FlybackState):
    """Calculates the bulk capacitance and related parameters based on the input voltage and output power.
    Arguments: FlybackResults (store results)- FlybackState (flyback object with parameters)
    Returns: 
        Results -> c_bulk_calc, v_bulk_min_calc
        State -> NONE
    """

    v_ripple = state.v_in_min * state.delta_v_bulk
    v_bulk = state.v_in_min - v_ripple
    result.delta_T_calc = math.asin(v_bulk / state.v_in_min) / (2 * math.pi * state.f_line)
    result.t_c_calc = 1 / (4 * state.f_line) - result.delta_T_calc
    result.t_d_calc = 1 / (2 * state.f_line) - result.t_c_calc
    result.t_d_nH_calc = ((1 + 2 * state.Nh)/(2 * state.f_line)) - result.t_c_calc
    
    result.c_bulk_calc = (2 * state.p_out_total * result.t_d_nH_calc) / (state.eta * (state.v_in_min**2 - v_bulk**2))

    voltage_part = 2 * (state.vac_min**2)
    discharge_part = (2 * state.p_out_total * result.t_d_nH_calc) / (state.eta * result.c_bulk_calc)
    if voltage_part >= discharge_part:
        result.v_bulk_min_nH_calc = math.sqrt(voltage_part - discharge_part)
    else:
        result.v_bulk_min_nH_calc = 0.0
        return print(f"Erreur de calcul")
        # Error

    voltage_part2 = 2 * (state.vac_min**2)
    discharge_part2 = (2 * state.p_out_total * result.t_d_calc) / (state.eta * result.c_bulk_calc)
    if voltage_part2 >= discharge_part2:
        result.v_bulk_min_calc = math.sqrt(voltage_part2 - discharge_part2)
    else:
        result.v_bulk_min_calc = 0.0
        return print(f"Erreur de calcul")
        # Error

def calc_preDesign_transformer(state: FlybackState, result: FlybackResults):
    """Calculates the pre-design parameters for the transformer (Lp, Np/Ns, Vor, ...)
    Arguments: FlybackResults (store results)- FlybackState (flyback object with parameters)
    Returns: 
        Results -> vor_calc, vds_on_calc, Lp_calc, Np_Ns1_calc, D_out_calc, D_m_calc
                    i_p_(calc), i_s_(calc)
        State -> v_bulk_min
    """
    voltage_part = 2 * (state.vac_min**2)
    discharge_part = (2 * state.p_out_total * result.t_d_nH_calc) / (state.eta * state.c_bulk)
    if voltage_part >= discharge_part:
        state.v_bulk_min_nH = math.sqrt(voltage_part - discharge_part)
    else:
        result.v_bulk_min_nH = 0.0
        return print(f"Erreur de calcul")
        # Error

    voltage_part2 = 2 * (state.vac_min**2)
    discharge_part2 = (2 * state.p_out_total * result.t_d_calc) / (state.eta * state.c_bulk)
    if voltage_part2 >= discharge_part2:
        state.v_bulk_min = math.sqrt(voltage_part2 - discharge_part2)
    else:
        result.v_bulk_min = 0.0
        return print(f"Erreur de calcul")
        # Error
        
    result.vor_calc = (state.D_max * state.v_bulk_min)/(1 - state.D_max)
    result.vds_on_calc = (state.v_bulk_min + result.vor_calc)/(1 + (state.v_bulk_min * result.vor_calc)/
                                                               (state.r_ds_on * state.p_in))
    result.Np_Ns1_calc = result.vor_calc / (state.v_out1 + state.v_F)
    result.D_out_calc = ((state.v_bulk_min - result.vds_on_calc) * state.D_max) / (result.vor_calc)
    result.D_m_calc = state.D_max - result.D_out_calc 

    result.Lp_calc = ((((state.v_bulk_min - result.vds_on_calc)**2 * state.D_max**2) / 
                    (state.p_in * state.f_sw * state.Krp))) * (1 - state.Krp/2)
    result.AeAw_calc = result.Lp_calc * (result.i_p_max_calc / state.B_max) * state.kb * (
            (result.i_p_rms_calc / state.J_max) + (result.i_s_rms_calc / (state.J_max * result.Np_Ns1_calc)))

    #---------------------------------------------------------
    # First current estimations 
    #---------------------------------------------------------
    result.i_p_avg_calc = state.p_out_total / (state.v_bulk_min * state.eta)
    result.i_p_avg_on_calc = state.p_out_total / (state.v_bulk_min * state.eta * state.D_max)
    result.i_p_max_calc = state.p_in / ((state.v_bulk_min * state.D_max)*(1 - state.Krp/2))
    result.i_p_rms_calc = result.i_p_max_calc * math.sqrt(state.D_max*(state.Krp**2 /3 - state.Krp + 1))   
    result.delta_i_p_calc = result.i_p_max_calc * state.Krp
    result.i_p_valley_calc = result.i_p_max_calc - result.delta_i_p_calc
    result.i_p_dc_calc = state.D_max * result.i_p_max_calc/2
    result.i_p_ac_calc = math.sqrt(result.i_p_rms_calc**2 - result.i_p_dc_calc**2)

    result.i_s_max_calc = (2 * state.i_out1)/(result.D_out_calc * (2 - state.Krp))
    result.i_s_rms_calc = result.i_s_max_calc * math.sqrt(result.D_out_calc * (state.Krp**2 /3 - state.Krp + 1))

def calc_transformer(state: FlybackState, result: FlybackResults):
    """Calculates the transformer parameters based on the pre-design calculations and the flyback state.
        Arguments: FlybackResults (store results)- FlybackState (flyback object with parameters)
        Returns: 
            Results -> lg_calc, Fringing_calc, Np_calc, Lp_real_calc, B_max_calc, Ns1_calc, Ns2_calc, Naux_calc
            State -> NONE
        """
    Np_intermediate = math.sqrt(result.Lp_calc/(state.Al * 1e-9))
    lg_mm = ((4*math.pi * 1e-7 * Np_intermediate**2 * state.Ae *1e-6) / result.Lp_calc) - (
        (state.le*1e-3)/state.mu_core) #[m]
    result.lg_calc = lg_mm * 1e3 #[mm]
    result.Fringing_calc = 1 + (lg_mm / (math.sqrt(state.Ae*1e-6))) * math.log((2*state.g*1e-3) / lg_mm)
    result.Np_calc = math.sqrt((result.Lp_calc * lg_mm *1e7) / (4 * math.pi * state.Ae * 1e-6 * result.Fringing_calc))
    
    result.Lp_real_calc = result.Np_calc**2 * state.Al * 1e-9

    result.B_max_calc = (result.Lp_real_calc * result.i_p_max_calc) / (result.Np_calc * state.Ae * 1e-6)
   
    result.Ns1_calc = result.Np_calc / result.Np_Ns1_calc
    result.Ns2_calc = (result.Np_calc * (state.v_out2 + state.v_F) * (1 - state.D_max - result.D_m_calc)) / (
        state.v_bulk_min * state.D_max)
    result.Naux_calc = (result.Np_calc * (state.v_aux + state.v_F) * (1 - state.D_max - result.D_m_calc)) / (
        state.v_bulk_min * state.D_max) 

def calc_flybackState(state: FlybackState, result: FlybackResults):
    """Calculates the final flyback state based on the inputs and choices previously made.
    Arguments: FlybackResults (store results)- FlybackState (flyback object with parameters)
    Returns: 
        Results -> NONE
        State -> lg, B_max, lp, ls1, ls2, laux 
                    i_p, i_s, i_aux, v_or, Np_Ns1, Np_Ns2, Np_Naux, Ns1_Naux 
    """

    state.Lp_real = state.Np**2 * state.Al * 1e-9

    state.i_p_avg = state.p_out_total / (state.v_bulk_min * state.eta) 
    state.i_p_avg_on = state.p_out_total / (state.v_bulk_min * state.eta * state.D_max)
    state.delta_i_p = (state.v_bulk_min * state.D_max)/(state.Lp_real * state.f_sw)
    state.i_p_max = state.i_p_avg_on + state.delta_i_p/2
    state.i_p_rms = math.sqrt((3*state.i_p_avg**2 + (state.delta_i_p/2)**2)*(state.D_max/3))
    state.i_p_valley = state.i_p_max - state.delta_i_p

    lg_mm = ((4*math.pi * 1e-7 * state.Np**2 * state.Ae *1e-6) / state.Lp_real) - (
            (state.le*1e-3)/state.mu_core) #[m]
    state.lg = lg_mm * 1e3 #[mm]
    state.Fringing = 1 + (lg_mm / (math.sqrt(state.Ae*1e-6))) * math.log((2*state.g*1e-3) / lg_mm)
    state.B_max_real = (state.Lp_real * state.i_p_max) / (state.Np * state.Ae * 1e-6)

    state.vor = state.Np_Ns1 * (state.v_out1 + state.v_F)
    state.vds_on = (state.v_bulk_min + state.vor)/(1 + (state.v_bulk_min * state.vor)/
                                                         (state.r_ds_on * state.p_in))
    state.D_out = ((state.v_bulk_min - state.vds_on) * state.D_max) / (state.vor)
    state.D_m = 1- state.D_max - state.D_out

def calc_wire_sections(state: FlybackState, result: FlybackResults):
    """Calculates the different wire diameters, sections and number of strands required for primary, secondary and auxiliary windings, 
            taking into account the skin effect.
            Checks if the total windings fit in the core window area (Aw).
    Arguments: FlybackResults (store results) - FlybackState (parameters)
    Returns: 
        Results -> D_awg_max_calc, s_w_calc, S(p,s1,s2,aux)_eff_calc, D(p,s1,s2,aux)_calc, strands_(p,s1,s2,aux)_calc
        State -> delta_cm
    """
    # ---------------------------------------------------------
    # 1. Skin depth calculation
    # ---------------------------------------------------------
    # for copper: delta = 6.62 / sqrt(f_sw) [en cm]
    state.delta_cm = 6.62 / math.sqrt(state.f_sw)
    delta_mm = state.delta_cm * 10.0
    
    # Diamètre AWG max pour éviter l'effet de peau
    result.D_awg_max_calc = 2 * delta_mm
    result.s_w_calc = (math.pi * (result.D_awg_max_calc**2)) / 4.0

    # ---------------------------------------------------------
    # 2. Primary
    # ---------------------------------------------------------
    result.Sp_eff_calc = state.i_p_rms / state.J_max
    result.Dp_calc = math.sqrt((4 * result.Sp_eff_calc) / math.pi)
    result.strands_p_calc = math.ceil(result.Sp_eff_calc / result.s_w_calc)

    # ---------------------------------------------------------
    # 3. Secondary 1
    # ---------------------------------------------------------
    result.Ss1_eff_calc = state.i_s_rms / state.J_max
    result.Ds1_calc = math.sqrt((4 * result.Ss1_eff_calc) / math.pi)
    result.strands_s1_calc = math.ceil(result.Ss1_eff_calc / result.s_w_calc)

    # ---------------------------------------------------------
    # 4. Secondary 2
    # ---------------------------------------------------------
    result.Ss2_eff_calc = state.i_s_rms / state.J_max
    result.Ds2_calc = math.sqrt((4 * result.Ss2_eff_calc) / math.pi)
    result.strands_s2_calc = math.ceil(result.Ss2_eff_calc / result.s_w_calc)

    # ---------------------------------------------------------
    # 5. Auxiliary
    # ---------------------------------------------------------
    # It is often assumed that the auxiliary current is low (e.g., controller power supply)
    i_aux_rms = state.i_aux * math.sqrt(state.D_max) if hasattr(state, 'i_aux') else 0.1
    result.Saux_eff_calc = i_aux_rms / state.J_max
    if result.Saux_eff_calc > 0:
        result.Daux_calc = math.sqrt((4 * result.Saux_eff_calc) / math.pi)
        result.strands_aux_calc = math.ceil(result.Saux_eff_calc / result.s_w_calc)
    else:
        result.Daux_calc = 0.0
        result.strands_aux_calc = 1
    if result.strands_aux_calc == 0: result.strands_aux_calc = 1

def check_core_window_fit(state: FlybackState, result: FlybackResults):
    """Checks if the total copper area of the windings fits within the core window area (Aw).
    Arguments: FlybackResults (store results) - FlybackState (parameters)
    Returns: 
        Results -> Aw_calc, fits_in_core
        State -> NONE
    """  
    # On calcule la surface totale de cuivre théorique
    result.Aw_used_calc = (state.Np * result.Sp_eff_calc + 
                         state.Ns1 * result.Ss1_eff_calc + 
                         state.Ns2 * result.Ss2_eff_calc +
                         state.Naux * result.Saux_eff_calc) * state.kb
    
    # Check if the total copper area fits within the core window area (Aw)
    result.fits_in_core_calc = result.Aw_used_calc <= state.Aw 