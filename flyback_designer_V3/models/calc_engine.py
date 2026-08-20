# =======================================================
# File : calc_engine.py
# Author : Gabin SBAFFI
# Date : 2026-07-29
# Description : this file is the calculation engine of the flyback designer application.
# =======================================================

import math
from models.flyback_states import *

def get_standard_value(val: float) -> float:
    """Returns the next standard E12 value greater than or equal to `val`.
    Works for any magnitude (pF, nF, µF, F, Ohms, etc.)."""
    if val <= 0:
        return 0.0
    
    e12_series = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2, 10.0]
    
    # Extract the base 10 exponent
    exponent = math.floor(math.log10(val))
    # Get the mantissa (value between 1.0 and 9.999...)
    mantissa = val / (10**exponent)
    
    # Find the next E12 value
    for std in e12_series:
        # We use a small tolerance (1e-6) for floating point precision issues
        if std >= mantissa - 1e-6:
            return std * (10**exponent)
            
    return e12_series[-1] * (10**exponent)

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
    result.c_bulk_std = get_standard_value(result.c_bulk_calc)

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
    if state.c_bulk == 0:
        state.v_bulk_min = 0.0
        state.v_bulk_min_nH = 0.0
        return print(f"Erreur de calcul")
    else:
        voltage_part = 2 * (state.vac_min**2)
        discharge_part = (2 * state.p_out_total * result.t_d_nH_calc) / (state.eta * state.c_bulk)
        if voltage_part >= discharge_part:
            state.v_bulk_min_nH = math.sqrt(voltage_part - discharge_part)
        else:
            state.v_bulk_min_nH = 0.0
            return print(f"Erreur de calcul")

        voltage_part2 = 2 * (state.vac_min**2)
        discharge_part2 = (2 * state.p_out_total * result.t_d_calc) / (state.eta * state.c_bulk)
        if voltage_part2 >= discharge_part2:
            state.v_bulk_min = math.sqrt(voltage_part2 - discharge_part2)
        else:
            state.v_bulk_min = 0.0
            return print(f"Erreur de calcul")
        
    result.vor_calc = (state.D_max * state.v_bulk_min)/(1 - state.D_max)
    result.vds_on_calc = (state.v_bulk_min + result.vor_calc)/(1 + (state.v_bulk_min * result.vor_calc)/
                                                               (state.r_ds_on * state.p_in))
    result.Np_Ns1_calc = result.vor_calc / (state.v_out1 + state.v_F)
    result.D_out_calc = ((state.v_bulk_min - result.vds_on_calc) * state.D_max) / (result.vor_calc)
    result.D_m_calc = state.D_max - result.D_out_calc 

    result.Lp_calc = ((((state.v_bulk_min - result.vds_on_calc)**2 * state.D_max**2) / 
                    (state.p_in * state.f_sw * state.Krp))) * (1 - state.Krp/2)

    #---------------------------------------------------------
    # Primary current estimations 
    #---------------------------------------------------------
    result.i_p_avg_calc = state.p_out_total / (state.v_bulk_min * state.eta)
    result.i_p_avg_on_calc = state.p_out_total / (state.v_bulk_min * state.eta * state.D_max)
    result.i_p_max_calc = state.p_in / ((state.v_bulk_min * state.D_max)*(1 - state.Krp/2))
    result.i_p_rms_calc = result.i_p_max_calc * math.sqrt(state.D_max*(state.Krp**2 /3 - state.Krp + 1))   
    result.delta_i_p_calc = result.i_p_max_calc * state.Krp
    result.i_p_valley_calc = result.i_p_max_calc - result.delta_i_p_calc
    result.i_p_dc_calc = state.D_max * result.i_p_max_calc/2
    result.i_p_ac_calc = math.sqrt(result.i_p_rms_calc**2 - result.i_p_dc_calc**2)

    #---------------------------------------------------------
    # Secondary current estimations 
    #---------------------------------------------------------
    result.i_s_max_calc = (2 * state.i_out1)/(result.D_out_calc * (2 - state.Krp))
    result.i_s_rms_calc = result.i_s_max_calc * math.sqrt(result.D_out_calc * (state.Krp**2 /3 - state.Krp + 1))

    #---------------------------------------------------------
    # Area product estimations 
    #---------------------------------------------------------
    result.AeAw_calc = result.Lp_calc * (result.i_p_max_calc / state.B_max) * state.kb * (
            (result.i_p_rms_calc / state.J_max) + (result.i_s_rms_calc / (state.J_max * result.Np_Ns1_calc)))


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

    result.B_max_real_calc = (result.Lp_real_calc * result.i_p_max_calc) / (result.Np_calc * state.Ae * 1e-6)
   
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

    # ----------------------------------------------
    # Turns ratios
    # ----------------------------------------------    
    if state.Ns1 == 0:
        state.Np_Ns1 = 0
    else:
        state.Np_Ns1 = state.Np / state.Ns1
    if state.Ns2 == 0:
        state.Np_Ns2 = 0
    else:
        state.Np_Ns2 = state.Np / state.Ns2
    if state.Naux == 0:
        state.Np_Naux = 0
        state.Ns1_Naux = 0
    else:
        state.Np_Naux = state.Np / state.Naux
        state.Ns1_Naux = state.Ns1 / state.Naux

    #---------------------------------------------------------
    # Voltages estimations 
    #---------------------------------------------------------  
    state.vor = state.Np_Ns1 * (state.v_out1 + state.v_F)
    state.vds_on = (state.v_bulk_min + state.vor)/(1 + (state.v_bulk_min * state.vor)/
                                                         (state.r_ds_on * state.p_in))

    # ----------------------------------------------
    # Primary current estimations
    # ----------------------------------------------    
    state.i_p_avg = state.p_out_total / (state.v_bulk_min * state.eta) 
    state.i_p_avg_on = state.p_out_total / (state.v_bulk_min * state.eta * state.D_max)
    state.delta_i_p = (state.v_bulk_min * state.D_max)/(state.Lp_real * state.f_sw)
    state.i_p_max = state.i_p_avg_on + state.delta_i_p/2
    state.i_p_rms = math.sqrt((3*state.i_p_avg**2 + (state.delta_i_p/2)**2)*(state.D_max/3))
    state.i_p_valley = state.i_p_max - state.delta_i_p
    state.i_p_dc = state.D_max * (state.i_p_max/2)
    state.i_p_ac = math.sqrt(state.i_p_rms**2 - state.i_p_dc**2)

    #---------------------------------------------------------
    # Secondary current estimations 
    #---------------------------------------------------------
    state.D_out = ((state.v_bulk_min - state.vds_on) * state.D_max) / (state.vor)
    state.D_m = 1- state.D_max - state.D_out
    state.i_s1_max = (2 * state.i_out1)/(state.D_out * (2 - state.Krp))
    state.i_s1_rms = state.i_s1_max * math.sqrt(state.D_out * (state.Krp**2 /3 - state.Krp + 1))
    state.i_s1_valley = state.i_s1_max * (1-state.Krp)
    state.delta_i_s1 = state.i_s1_max - state.i_s1_valley
    state.i_s1_dc = state.i_out1
    state.i_s1_ac = math.sqrt(state.i_s1_rms**2 - state.i_s1_dc**2)

    state.i_s2_max = (2 * state.i_out2)/(state.D_out * (2 - state.Krp))
    state.i_s2_rms = state.i_s2_max * math.sqrt(state.D_out * (state.Krp**2 /3 - state.Krp + 1))
    state.i_s2_valley = state.i_s2_max * (1-state.Krp)
    state.delta_i_s2 = state.i_s2_max - state.i_s2_valley
    state.i_s2_dc = state.i_out2
    state.i_s2_ac = math.sqrt(state.i_s2_rms**2 - state.i_s2_dc**2)

    #---------------------------------------------------------
    # Auxiliary current estimations 
    #---------------------------------------------------------
    # state.i_aux_max = (state.v_bulk_min - state.vds_on)/state.Laux * state.D_m
    # state.i_aux_rms = state.i_s1_rms
    # state.i_aux_valley = state.i_s1_valley
    # state.delta_i_aux = state.delta_i_s1
    # state.i_aux_dc = state.i_out1
    # state.i_aux_ac = math.sqrt(state.i_aux_rms**2 - state.i_aux_dc**2)
    
    #---------------------------------------------------------
    # Transformer calculations 
    #---------------------------------------------------------
    lg_mm = ((4*math.pi * 1e-7 * state.Np**2 * state.Ae *1e-6) / state.Lp_real) - (
            (state.le*1e-3)/state.mu_core) #[m]
    state.lg = lg_mm * 1e3 #[mm]
    state.Fringing = 1 + (lg_mm / (math.sqrt(state.Ae*1e-6))) * math.log((2*state.g*1e-3) / lg_mm)
    state.B_max_real = (state.Lp_real * state.i_p_max) / (state.Np * state.Ae * 1e-6)

    state.AeAw_calc = state.Lp_real * (state.i_p_max / state.B_max_real) * state.kb * (
            (state.i_p_rms / state.J_max) + (state.i_s1_rms / (state.J_max * state.Np_Ns1)))
    
    #---------------------------------------------------------
    # Lengths of windings
    #---------------------------------------------------------
    state.lp = state.Np * state.le # [mm]
    state.ls1 = state.Ns1 * state.le # [mm]
    state.ls2 = state.Ns2 * state.le # [mm]
    state.laux = state.Naux * state.le # [mm]   
    

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
    result.Ss1_eff_calc = state.i_s1_rms / state.J_max
    result.Ds1_calc = math.sqrt((4 * result.Ss1_eff_calc) / math.pi)
    result.strands_s1_calc = math.ceil(result.Ss1_eff_calc / result.s_w_calc)

    # ---------------------------------------------------------
    # 4. Secondary 2
    # ---------------------------------------------------------
    result.Ss2_eff_calc = state.i_s2_rms / state.J_max
    result.Ds2_calc = math.sqrt((4 * result.Ss2_eff_calc) / math.pi)
    result.strands_s2_calc = math.ceil(result.Ss2_eff_calc / result.s_w_calc)

    # ---------------------------------------------------------
    # 5. Auxiliary
    # ---------------------------------------------------------
    # It is often assumed that the auxiliary current is low (e.g., controller power supply)
    # i_aux_rms = state.i_aux * math.sqrt(state.D_max) if hasattr(state, 'i_aux') else 0.1
    # result.Saux_eff_calc = i_aux_rms / state.J_max
    # if result.Saux_eff_calc > 0:
    #     result.Daux_calc = math.sqrt((4 * result.Saux_eff_calc) / math.pi)
    #     result.strands_aux_calc = math.ceil(result.Saux_eff_calc / result.s_w_calc)
    # else:
    #     result.Daux_calc = 0.0
    #     result.strands_aux_calc = 1
    # if result.strands_aux_calc == 0: result.strands_aux_calc = 1

    # ---------------------------------------------------------
    # 6. Actual Wire Sections (based on chosen diameter)
    # --------------------------------------------------------- 
    if state.Dp > 0:
        state.Sp_eff = math.pi * (state.Dp/2)**2
        state.strands_p = math.ceil(state.Sp_eff/result.s_w_calc)
    else: 
        state.Sp_eff = 0
        state.strands_p = 1
    if state.Ds1 > 0:
        state.Ss1_eff = math.pi * (state.Ds1/2)**2
        state.strands_s1 = math.ceil(state.Ss1_eff/result.s_w_calc)
    else: 
        state.Ss1_eff = 0
        state.strands_s1 = 1
    if state.Ds2 > 0:
        state.Ss2_eff = math.pi * (state.Ds2/2)**2
        state.strands_s2 = math.ceil(state.Ss2_eff/result.s_w_calc)
    else: 
        state.Ss2_eff = 0
        state.strands_s2 = 1
    if state.Daux > 0:
        state.Saux_eff = math.pi * (state.Daux/2)**2
        state.strands_aux = math.ceil(state.Saux_eff/result.s_w_calc)
    else: 
        state.Saux_eff = 0
        state.strands_aux = 1


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

def calc_output_capacitance(state: FlybackState, result: FlybackResults):
    """Calculates the output capacitance value.
    Arguments: FlybackResults (store results) - FlybackState (parameters)
    Returns: 
        Results -> C_out1, C_out2
        State -> NONE
    """
    if state.i_out1 == 0 or state.delta_Vout1 == 0 or state.v_out1 == 0 or state.f_sw == 0 or state.i_s1_max == 0:
        result.C_out1 = 0
        result.C_out1_esr = 0
    else:
        result.C_out1 = 10 * (state.D_max * state.i_out1) / (state.delta_Vout1/100 * state.v_out1 * state.f_sw)
        result.C_out1_esr = (state.delta_Vout1/100) * (state.v_out1/state.i_s1_max)
    if state.i_out2 == 0 or state.delta_Vout2 ==0 or state.v_out2 == 0 or state.f_sw == 0 or state.i_s2_max == 0:
        result.C_out2 = 0
        result.C_out2_esr = 0
    else:
        result.C_out2 = 10 * (state.D_max * state.i_out2) / (state.delta_Vout2/100 * state.v_out2 * state.f_sw)
        result.C_out2_esr = (state.delta_Vout2/100) * (state.v_out2/state.i_s2_max)    
    

def calc_output_voltages(state: FlybackState, result: FlybackResults):
    """Calculates the output voltage ripple of the flyback converter.
    Arguments: FlybackResults (store results) - FlybackState (parameters)
    Returns: 
        Results -> NONE
        State -> ripple_v1_calc, ripple_v2_calc
    """
    state.ripple_v1_calc = (state.i_s1_max * state.C_out1_esr) + ((state.i_out1 * state.D_max) / (state.C_out1 * state.f_sw))
    state.ripple_v2_calc = (state.i_s2_max * state.C_out2_esr) + ((state.i_out2 * state.D_max) / (state.C_out2 * state.f_sw))
   

def calc_pfe_losses(state: FlybackState, result: FlybackResults):
    """Calculates the core losses in the transformer.
    Arguments: FlybackResults (store results) - FlybackState (parameters)
    Returns: 
        Results -> 
        State -> 
    """
    
    delta_20 = 100 * math.sqrt(state.rho_cu_20 / (math.pi * state.f_sw * state.mu_0 * state.mu_r_nonMagnetic))
    delta_100 = 100 * math.sqrt(state.rho_cu_100 / (math.pi * state.f_sw * state.mu_0 * state.mu_r_nonMagnetic))
    
    Q_p = state.Dp/delta_100
    Q_s1 = state.Ds1/delta_100
    Q_s2 = state.Ds2/delta_100
    Q_aux = state.Daux/delta_100

    # -----------------------------------------------
    # DC resistances
    # -----------------------------------------------
    state.r_dc_p = (state.rho_cu_100 * state.MTl * state.Np) / state.Sp_eff
    state.r_dc_s1 = (state.rho_cu_100 * state.MTl * state.Ns1) / state.Ss1_eff
    state.r_dc_s2 = (state.rho_cu_100 * state.MTl * state.Ns2) / state.Ss2_eff
    state.r_dc_aux = (state.rho_cu_100 * state.MTl * state.Naux) / state.Saux_eff

    # -----------------------------------------------
    # AC resistance coefficients (Dowell's coefficients)
    # -----------------------------------------------
    state.r_ac_p = state.r_dc_p * state.K_ac_p
    state.r_ac_s1 = state.r_dc_s1 * state.K_ac_s1
    state.r_ac_s2 = state.r_dc_s2 * state.K_ac_s2
    state.r_ac_aux = state.r_dc_aux * state.K_ac_aux

    # -----------------------------------------------
    # Winding copper losses
    # -----------------------------------------------
    state.P_cu_p = (state.r_dc_p * state.i_p_dc**2) + (state.r_ac_p * state.i_p_ac**2)
    state.P_cu_s1 = (state.r_dc_s1 * state.i_s1_dc**2) + (state.r_ac_s1 * state.i_s1_ac**2)
    state.P_cu_s2 = (state.r_dc_s2 * state.i_s2_dc**2) + (state.r_ac_s2 * state.i_s2_ac**2)
    state.P_cu_aux = (state.r_dc_aux * state.i_aux_dc**2) + (state.r_ac_aux * state.i_aux_ac**2)
    state.P_cu_total = state.P_cu_p + state.P_cu_s1 + state.P_cu_s2 + state.P_cu_aux

    # -----------------------------------------------
    # Core losses
    # -----------------------------------------------
    state.delta_B_dcm =(state.Lp_real * state.i_p_max) / (state.Np * state.Ae*1e-6)
    state.delta_B_ccm =(state.Lp_real * state.i_p_max * state.Krp) / (state.Np * state.Ae*1e-6)
    state.B_ac = state.delta_B/2
    state.Pfe = state.k * state.f_sw**state.alpha * state.B_ac**state.beta * state.Ve



def calc_mosfet_losses(state: FlybackState, result: FlybackResults, type: str="MOSFET"):
    """Calculates the MOSFET losses in the flyback converter.
    Arguments: FlybackResults (store results) - FlybackState (parameters)
    Returns: 
        Results -> NONE
        State -> P_cond, P_coss, P_sw_off, P_sw_on, P_mosfet
        Returns -> String message indicating missing parameters or success
    """
    
    missing = []
    
    if type == "MOSFET":
        rds_on = state.r_ds_on
        MOS_toff = state.MOS_toff
        MOS_ton = state.MOS_ton
        MOS_Eoss = state.MOS_Eoss
        MOS_coss = state.MOS_coss
        if rds_on == 0: missing.append("Rds(on)")
        if MOS_toff == 0: missing.append("t_off")
        if MOS_ton == 0: missing.append("t_on")
        if MOS_Eoss == 0 and MOS_coss == 0: missing.append("Eoss or Coss")
    elif type == "IC":
        rds_on = state.ctr_r_ds_on
        MOS_toff = state.ctr_toff
        MOS_ton = state.ctr_ton
        MOS_Eoss = state.ctr_Eoss
        MOS_coss = state.ctr_coss
        if rds_on == 0: missing.append("Rds(on)")
        if MOS_toff == 0: missing.append("t_off")
        if MOS_ton == 0: missing.append("t_on")
        if MOS_Eoss == 0 and MOS_coss == 0: missing.append("Eoss or Coss")
    else: 
        raise ValueError("Invalid component type")
    
    if state.i_p_rms == 0: missing.append("Primary RMS current (i_p_rms)")
    if state.f_sw == 0: missing.append("Switching frequency (f_sw)")
    if state.i_p_max == 0: missing.append("Peak primary current (i_p_max)")
    
    vds_on = state.v_bulk_min 
    vds_off = state.v_in_max + state.vor + (state.vor * 1.5)
    i_off = state.i_p_max 
    i_on = state.i_p_valley 
    
    P_cond = rds_on * state.i_p_rms**2
    P_sw_off = 1/2 * vds_off * i_off * state.f_sw * MOS_toff
    P_sw_on = 1/2 * vds_on * i_on * state.f_sw * MOS_ton
    
    if MOS_Eoss != 0:
        P_coss = MOS_Eoss * state.f_sw
    elif MOS_coss != 0 and MOS_Eoss == 0:
        P_coss = 1/2 * MOS_coss * vds_off**2 * state.f_sw
    else:
        P_coss = 0
    
    if type == "MOSFET":
        state.P_cond = P_cond
        state.P_sw_on = P_sw_on
        state.P_sw_off = P_sw_off
        state.P_sw = P_sw_on + P_sw_off
        state.P_coss = P_coss
        state.P_mosfet = P_cond + P_sw_on + P_sw_off + P_coss
    elif type == "IC":
        state.P_cond_ctr = P_cond
        state.P_sw_on_ctr = P_sw_on
        state.P_sw_off_ctr = P_sw_off
        state.P_sw_ctr = P_sw_on + P_sw_off
        state.P_coss_ctr = P_coss
        state.P_ctr = P_cond + P_sw_on + P_sw_off + P_coss

    if missing:
        return f"Calculations performed, but the following values are missing for {type}:\n- " + "\n- ".join(missing)
    else:
        return f"All OK: No missing values for {type} losses calculations."


def calc_diode_losses(diode: str, type: str, state: FlybackState, result: FlybackResults):
    """Calculates the diode losses in the flyback converter.
    Arguments: FlybackResults (store results) - FlybackState (parameters)
    Returns: 
        Results -> 
        State -> 
    """
    if diode == "D_out1":
        v_F = state.V_F1
        r_d = state.r_d1
        i_s_rms = state.i_s1_rms
        i_out = state.i_out1
        v_rev = state.v_out1 + state.v_in_max * (state.Ns1/state.Np)
        Q_rr = state.Qrr_d1
        Cj = state.Cj_d1
    elif diode == "D_out2":
        v_F = state.V_F2
        r_d = state.r_d2
        i_s_rms = state.i_s2_rms
        i_out = state.i_out2
        v_rev = state.v_out2 + state.v_in_max * (state.Ns2/state.Np)
        Q_rr = state.Qrr_d2
        Cj = state.Cj_d2
    else: 
        raise ValueError("Diode not recognized")

    missing = []
    if v_F == 0: missing.append("V_F")
    if r_d == 0: missing.append("r_d")
    if i_s_rms == 0: missing.append("i_s_rms")
    if i_out == 0: missing.append("i_out")
    if v_rev == 0: missing.append("v_rev")
    if type == "Standard" and Q_rr == 0: missing.append("Q_rr")
    if type == "Ultra-fast" and Q_rr == 0: missing.append("Q_rr")
    if type == "Schottky" and Cj == 0: missing.append("Cj")

    P_cond = v_F * i_out + r_d * i_s_rms
    if type == "Schottky": P_sw = 1/2 * Cj * v_rev**2 * state.f_sw
    elif type == "Ultra-fast": P_sw = Q_rr * v_rev * state.f_sw
    elif type == "Standard": P_sw = Q_rr * v_rev * state.f_sw 
    else: raise ValueError("Diode type not recognized")
    
    P_diode = P_cond + P_sw

    if diode == "D_out1":
        state.P_cond_diode1 = P_cond
        state.P_sw_diode1 = P_sw
        state.P_diode1 = P_diode
    elif diode == "D_out2":
        state.P_cond_diode2 = P_cond
        state.P_sw_diode2 = P_sw
        state.P_diode2 = P_diode

    if missing:
        return f"Calculations performed, but the following values are missing for {diode}:\n- " + "\n- ".join(missing)
    else:
        return f"All OK: No missing values for {diode} losses calculations."


def calc_capacitor_losses(capa: str, state: FlybackState, result: FlybackResults):
    """Calculates the capacitor losses in the flyback converter.
    Arguments: FlybackResults (store results) - FlybackState (parameters)
    Returns: 
        Results -> 
        State -> 
    """
    if capa == "C1_out1":
        C_esr = getattr(state, "C1_out1_ESR", 0.0)
        i_c_rms = state.i_s1_ac
    elif capa == "C2_out1":
        C_esr = getattr(state, "C2_out1_ESR", 0.0)
        i_c_rms = state.i_s1_ac
    elif capa == "C1_out2":
        C_esr = getattr(state, "C1_out2_ESR", 0.0)
        i_c_rms = state.i_s2_ac
    elif capa == "C2_out2":
        C_esr = getattr(state, "C2_out2_ESR", 0.0)
        i_c_rms = state.i_s2_ac
    elif capa == "C_bulk":
        C_esr = state.C_bulk_esr
        i_in_avg = state.p_out_total / (state.eta * state.v_in_min)
        i_c_rms = math.sqrt(state.i_p_rms**2 - i_in_avg**2)
    elif capa == "C_snubber":
        C_esr = state.C_snub_esr
        ts = (state.L_leak * state.i_p_max) / (state.V_clamp - state.vor)
        i_c_rms = state.i_p_max * math.sqrt((ts * state.f_sw) / (3))
    else:
        raise ValueError("Capacitor not recognized")

    missing = []
    if C_esr == 0:
        missing.append("C_esr (Equivalent Series Resistance)")
    if i_c_rms == 0:
        missing.append("RMS Current (i_c_rms)")

    P_capa = C_esr * i_c_rms**2

    if capa == "C1_out1":
        state.P_c1_out1 = P_capa
    elif capa == "C2_out1":
        state.P_c2_out1 = P_capa
    elif capa == "C1_out2":
        state.P_c1_out2 = P_capa
    elif capa == "C2_out2":
        state.P_c2_out2 = P_capa
    elif capa == "C_bulk":
        state.P_c_bulk = P_capa
    elif capa == "C_snubber":
        setattr(state, "P_snubber", P_capa)

    if missing:
        return f"Calculations performed, but the following values are missing for {capa}:\n- " + "\n- ".join(missing)
    else:
        return f"All OK: No missing values for {capa} losses calculations."

def snubber_losses(state: FlybackState, result: FlybackResults):
    """Calculates the snubber losses in the flyback converter.
    Arguments: FlybackResults (store results) - FlybackState (parameters)
    Returns: 
        Results -> 
        State -> 
    """

    missing = []
    if state.L_leak == 0:
        missing.append("L_leak")
    if state.i_p_max == 0:
        missing.append("i_p_max")
    if state.f_sw == 0:
        missing.append("f_sw")
    if state.V_clamp == 0:
        missing.append("V_clamp")
    if state.vor == 0:
        missing.append("vor")

    if missing:
        raise ValueError("Unable to calculate snubber losses. Please provide: \n- " + "\n- ".join(missing))
    
    P_snubber = 1/2 * state.L_leak * state.i_p_max**2 * state.f_sw * (state.V_clamp / (state.V_clamp - state.vor))

    return P_snubber

    
    