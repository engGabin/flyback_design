# =======================================================
# File : calculs_flyback.py
# Author : Gabin SBAFFI
# Date : 2026-07-28
# Description : this file contains the CalculateurFlyback class, which is responsible for performing calculations related to flyback converter design.
# =======================================================

# .\flybakc_designer_V2\tests\

import math

class CalculateurFlyback:
    def __init__(self):
        # ========================================================
        # 1. INPUT SPECIFICATIONS
        # ========================================================
        self.vac_min = 85.0         # Minimum AC input voltage [V]
        self.vac_max = 528.0        # Maximum AC input voltage [V]
        self.f_line = 50.0          # Line frequency [Hz]
        
        self.p_out1 = 7.0           # Output power 1 [W]
        self.v_out1 = 12.0          # Output voltage 1 [V]
        self.p_out2 = 0             # Output power 2 [W]
        self.v_out2 = 0             # Output voltage 2 [V]
        self.p_aux = 0              # Auxiliary output power [W]
        self.v_aux = 0              # Auxiliary output voltage [V]

        self.Nh = 1.0               # Number of Hold-Ups
        self.delta_v_bulk = 0.25    # Maximum voltage ripple allowed on the bulk capacitor
        
        # ========================================================
        # INPUT BULK CAPACITOR
        # ========================================================
        self.c_bulk = 23.5e-6       # Input bulk capacitor [F]

        # ========================================================
        # 2. PRE-DESIGN CHOICES (first estimations)
        # ========================================================
        self.eta = 0.85             # Estimated efficiency of the converter
        self.D_max = 0.61           # maximum duty cycle
        self.f_sw = 132e3           # switching frequency [Hz]
        self.Krp = 1                # ripple factor (1 for DCM, <1 for CCM)

        # ========================================================
        # 3. PRE-DESIGN CHOICES (transformer specifications)
        # ========================================================
        self.B_max = 0.2            # Maximum flux density in the core [T]
        self.J_max = 6              # Maximum current density in the winding [A/m^2]
        self.T_max = 100.0          # Maximum temperature rise in the transformer [°C]
        self.T_amb = 25.0           # Ambient temperature [°C]
        self.Ku = 0.4               # Window utilization factor
        self.kb = 1/self.Ku         # bobbin factor

        # ========================================================
        # 4. FERRITE SELECTION
        # ========================================================        
        self.Ae = 103               
        self.Aw = 25          
        self.AeAw_real = self.Ae*self.Aw
        self.Ve = 3300
        self.le = 36
        self.Al = 629
        self.Wtfe = 0
        self.MTl = 7
        self.g = 21
        self.Pv = 0.0
        self.mu_core = 5000  
        self.Lp = 0.0      

        # ========================================================
        # 5. NUMBER OF TURNS SELECTION
        # ========================================================
        self.Np = 11.10             # primary turns
        self.Ns1 = 1                # secondary turns 1
        self.Ns2 = 0                # secondary turns 2
        self.Naux = 0               # auxiliary turns   

        # ========================================================
        # DATASHEET PARAMETERS
        # ========================================================
        self.r_ds_on = 0.62        # ON resistance of the primary switch [Ohm]
        self.v_F = 0.7             # Forward voltage drop of the diode [V]

        # ========================================================
        # VARIABLES TO STORE CALCULATED RESULTS
        # ========================================================
        self.p_out_total = 0.0
        self.p_in = 0.0
        self.D_out = 0.0            # duty cycle of the secondary side
        self.D_m = 0.0              # duty cycle linked to dead time (current = 0)
        self.Lp_calc = 0.0          # primary inductance

        self.c_bulk_calc = 0.0      # calculated bulk capacitor value based on number of hold-up

        #---------------------------------------------------------
        # Voltages variables
        #---------------------------------------------------------
        self.v_in_max = 0.0         # maximum input voltage 
        self.v_in_min = 0.0         # minimum input voltage 
        self.v_bulk_min = 0.0       # minimum bulk voltage based on the voltage drop across a capacitor

        self.vor = 0.0              # reflected voltage on the primary side
        self.vds_on = 0.0           # voltage across the primary switch when it is on

        #---------------------------------------------------------
        # Currents variables
        #---------------------------------------------------------
        self.i_p_max = 0.0          # maximum primary current
        self.i_p_max1 = 0.0         
        self.i_p_rms = 0.0          # RMS primary current
        self.i_p_rms1 = 0.0
        self.i_p_avg = 0.0          # average primary current
        self.i_p_avg1 = 0.0
        self.i_p_avg_on = 0.0       # average primary current when the switch is on
        self.i_p_avg_on1 = 0.0
        self.delta_i_p = 0.0        # primary current ripple
        self.delta_i_p1 = 0.0
        self.i_p_valley = 0.0       # primary current valley
        self.i_p_valley1 = 0.0
        self.i_p_dc = 0.0           # DC component of the primary current
        self.i_p_dc1 = 0.0
        self.i_p_ac = 0.0           # AC component of the primary current
        self.i_p_ac1 = 0.0

        self.i_s_max = 0.0          # maximum secondary current
        self.i_s_max1 = 0.0
        self.i_s_rms = 0.0          # RMS secondary current
        self.i_s_rms1 = 0.0
        self.i_out1 = 0.0           # output current 1
        self.i_out2 = 0.0           # output current 2
        self.i_aux = 0.0            # auxiliary output current

        #---------------------------------------------------------
        # Transformer variables
        #---------------------------------------------------------
        self.AeAw_calc = 0.0        # product of the effective area and the window area
        self.Np_calc = 0.0          # primary turns
        self.Ns1_calc = 0.0         # secondary turns 1
        self.Ns2_calc = 0.0         # secondary turns 2
        self.Naux_calc = 0.0        # auxiliary turns
        self.Np_Ns1_calc = 0.0      # turns ratio primary to secondary 1
        self.Np_Ns2_calc = 0.0      # turns ratio primary to secondary 2
        self.Np_Naux_calc = 0.0     # turns ratio primary to auxiliary
        self.lg = 0.0               # air gap length
        self.Fringing = 0.0         # fringing flux factor
        self.Lp_real = 0.0          # real primary inductance
        self.B_max_calc = 0.0           # flux density

    def executer_calculs(self):
        """Executes the calculation chain step by step."""

        # ---------------------------------------------------------
        # Electricals Calculation
        # ---------------------------------------------------------
        self.p_out_total = self.p_out1 + self.p_out2 + self.p_aux
        self.p_in = self.p_out_total / self.eta
        if self.v_out1 > 0:
            self.i_out1 = self.p_out1 / self.v_out1
        else:
            self.i_out1 = 0.0
        if self.v_out2 > 0:
            self.i_out2 = self.p_out2 / self.v_out2
        else:
            self.i_out2 = 0.0
        if self.v_aux > 0:
            self.i_aux = self.p_aux / self.v_aux
        else:
            self.i_aux = 0.0

        self.v_in_min = self.vac_min * math.sqrt(2)
        self.v_in_max = self.vac_max * math.sqrt(2)

        # ---------------------------------------------------------
        # Capacitor Bulk Calculation
        # ---------------------------------------------------------
        v_ripple = self.v_in_min * self.delta_v_bulk
        v_bulk = self.v_in_min - v_ripple
        delta_T = math.asin(v_bulk / self.v_in_min) / (2 * math.pi * self.f_line)
        t_c = 1 / (4 * self.f_line) - delta_T
        t_d = 1 / (2 * self.f_line) - t_c
        t_d_nH = ((1 + 2 * self.Nh)/(2 * self.f_line)) - t_c
        
        self.c_bulk_calc = (2 * self.p_out_total * t_d_nH) / (self.eta * (self.v_in_min**2 - v_bulk**2))

        voltage_part = 2 * (self.vac_min**2)
        discharge_part = (2 * self.p_out_total * t_d) / (self.eta * self.c_bulk)
        if voltage_part >= discharge_part:
            self.v_bulk_min = math.sqrt(voltage_part - discharge_part)
        else:
            self.v_bulk_min = 0.0
            # Error: the capacitor is too small to hold the charge

        # ---------------------------------------------------------
        # Pre-Design Calculation
        # ---------------------------------------------------------
        self.vor = (self.D_max * self.v_bulk_min)/(1 - self.D_max)
        self.vds_on = (self.v_bulk_min + self.vor)/(1 + (self.v_bulk_min * self.vor)/(self.r_ds_on * self.p_in))
        self.Lp_calc = ((((self.v_bulk_min - self.vds_on)**2 * self.D_max**2) / 
                        (self.p_in * self.f_sw * self.Krp))) * (1 - self.Krp/2)

        #---------------------------------------------------------
        # First current estimations 
        #---------------------------------------------------------
        self.Np_Ns1_calc = self.vor / (self.v_out1 + self.v_F)
        self.i_p_avg = self.p_out_total / (self.v_bulk_min * self.eta)
        self.i_p_avg_on = self.p_out_total / (self.v_bulk_min * self.eta * self.D_max)
        self.i_p_max = self.p_in / ((self.v_bulk_min * self.D_max)*(1 - self.Krp/2))
        self.i_p_rms = self.i_p_max * math.sqrt(self.D_max*(self.Krp**2 /3 - self.Krp + 1))   
        self.delta_i_p = self.i_p_max * self.Krp
        self.i_p_valley = self.i_p_max - self.delta_i_p
        self.i_p_dc = self.D_max * self.i_p_max/2
        self.i_p_ac = math.sqrt(self.i_p_rms**2 - self.i_p_dc**2)

        self.D_out = ((self.v_bulk_min - self.vds_on) * self.D_max) / (self.vor)
        self.i_s_max = (2 * self.i_out1)/(self.D_out * (2 - self.Krp))
        self.i_s_rms = self.i_s_max * math.sqrt(self.D_out * (self.Krp**2 /3 - self.Krp + 1))

        #---------------------------------------------------------
        # Transformer Calculation
        #---------------------------------------------------------
        self.AeAw_calc = self.Lp_calc * (self.i_p_max / self.B_max) * self.kb * (
            (self.i_p_rms / self.J_max) + (self.i_s_rms / (self.J_max * self.Np_Ns1_calc)))

        Np_intermediate = math.sqrt(self.Lp_calc/(self.Al * 1e-9))
        lg_mm = ((4*math.pi * 1e-7 * Np_intermediate**2 * self.Ae *1e-6) / self.Lp_calc) - (
            (self.le*1e-3)/self.mu_core) #[m]
        self.lg = lg_mm * 1e3 #[mm]
        self.Fringing = 1 + (lg_mm / (math.sqrt(self.Ae*1e-6))) * math.log((2*self.g*1e-3) / lg_mm)
        self.Np_calc = math.sqrt((self.Lp_calc * lg_mm *1e-7) / (4 * math.pi * self.Ae * self.Fringing))
        self.Lp_real = self.Np**2 * self.Al * 1e-9

        self.B_max_calc = (self.Lp_real * self.i_p_max) / (self.Np * self.Ae * 1e-6)

        #---------------------------------------------------------
        # Second Current Calculations
        #---------------------------------------------------------
        self.Lp = self.Lp_calc
        self.i_p_avg1 = self.i_p_avg 
        self.i_p_avg_on1 = self.i_p_avg_on
        self.delta_i_p1 = (self.v_bulk_min * self.D_max)/(self.Lp * self.f_sw)
        self.i_p_max1 = self.i_p_avg_on1 + self.delta_i_p1/2
        self.i_p_rms1 = math.sqrt((3*self.i_p_avg1**2 + (self.delta_i_p1/2)**2)*(self.D_max/3))
        self.i_p_valley1 = self.i_p_max1 - self.delta_i_p1

        



    def afficher_resultats(self):
        """Displays the results properly in the console."""
        # print("=== RESULTS OF THE FLYBACK DESIGN ===")
        # print(f"Input Power (Pin) : {self.p_in:.2f} W")
        # print(f"Output Current (Iout1) : {self.i_out1:.3f} A")
        # print(f"Output Current (Iout2) : {self.i_out2:.3f} A")
        # print(f"Output Current (Iaux) : {self.i_aux:.3f} A")
        # print("-" * 40)
        # print(f"Maximum bulk Voltage : {self.v_in_max:.1f} V")
        # print(f"Minimum peak bulk Voltage : {self.v_in_min:.1f} V")
        # print(f"Minimum bulk Voltage : {self.v_bulk_min:.1f} V")
        # print(f"Calculated Bulk Capacitor : {self.c_bulk_calc*1e6:.2f} uF")
        # print(f"Reflected Voltage on Primary Side : {self.vor:.1f} V")
        # print(f"Voltage across Primary Switch when ON : {self.vds_on:.1f} V")
        # print(f"Primary Inductance : {self.Lp_calc*1e6:.2f} uH")
        # print("-" * 40)
        # print(f"Turns Ratio (Np/Ns1) : {self.Np_Ns1_calc:.2f}")
        # print(f"Average Primary Current : {self.i_p_avg:.3f} A")
        # print(f"Average Primary Current (ON) : {self.i_p_avg_on:.3f} A")
        # print(f"Maximum Primary Current : {self.i_p_max:.3f} A")
        # print(f"RMS Primary Current : {self.i_p_rms:.3f} A")
        # print(f"Current Ripple : {self.delta_i_p:.3f} A")
        # print(f"DC Primary Current : {self.i_p_dc:.3f} A")
        # print(f"AC Primary Current : {self.i_p_ac:.3f} A")
        # print("-" * 40)
        # print(f"Air Gap Length : {self.lg:.2f} mm")
        # print(f"Fringing Effect : {self.Fringing:.2f}")
        # print(f"Real Inductance : {self.Lp_real*1e6:.2f}")
        # print(f"Flux Density : {self.B_max_calc:.2f} mT")
        # print(f"Average Primary Current : {self.i_p_avg1:.3f} A")
        # print(f"Average Primary Current (ON) : {self.i_p_avg_on1:.3f} A")
        # print(f"Maximum Primary Current : {self.i_p_max1:.3f} A")
        # print(f"RMS Primary Current : {self.i_p_rms1:.3f} A")
        # print(f"Current Ripple : {self.delta_i_p1:.3f} A")  
        # print(f"Primary Current Valley : {self.i_p_valley1:.3f} A")      
        print("============================================")

# ========================================================
# LANCEMENT DU SCRIPT
# ========================================================
if __name__ == "__main__":
    # 1. On crée notre calculatrice
    mon_design = CalculateurFlyback()
    
    # 2. On peut modifier les valeurs par défaut ici si on le souhaite
    # mon_design.p_out = 20.0  # Test avec 20W par exemple
    
    # 3. On lance les calculs
    mon_design.executer_calculs()
    
    # 4. On affiche le résultat
    mon_design.afficher_resultats()