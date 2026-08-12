from models.snubber_state import SnubberState, SnubberResults

def calc_snubber(state: SnubberState, result: SnubberResults):
    """
    Calculates the snubber components based on the data provided by the user.
    """
    result.sn_vor = (state.sn_Np / state.sn_Ns) * (state.sn_Vout + state.sn_v_F) # [V]
    result.v_sn = state.k_cl * result.sn_vor
    result.p_sn = 0.5 * state.sn_Llk * state.sn_i_p_max**2 * state.sn_f_sw * (
        result.v_sn/(result.v_sn - result.sn_vor)
    )
    result.r_sn = (result.v_sn**2)/(result.p_sn) *1e-3 # [kΩ]
    result.c_sn = result.v_sn / (state.delta_v_sn * result.r_sn*1e3 * state.sn_f_sw) *1e9 # [nF]
    result.v_clamp = result.v_sn
    result.v_rwm = state.k_Vwm * result.sn_vor # [V]
    
