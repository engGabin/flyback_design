# =======================================================
# File : test_calc_engine.py
# Description : Script de test pour valider les équations du Flyback
# =======================================================

import sys
import os

# 1. On trouve le chemin du dossier "tests" (là où est ce fichier)
current_dir = os.path.dirname(os.path.abspath(__file__))
# 2. On remonte d'un cran pour trouver la racine du projet (Design_Flyback_Application)
project_root = os.path.dirname(current_dir)
# 3. On remonte encore d'un cran pour trouver le dossier contenant flyback_designer_V3
parent_of_root = os.path.dirname(project_root)

# 4. On ajoute ces chemins à la mémoire de Python
sys.path.insert(0, project_root)
sys.path.insert(0, parent_of_root)

from flyback_designer_V3.models.flyback_states import *
from flyback_designer_V3.models.calc_engine import *

def lancer_test_complet():
    print("=== DÉBUT DU TEST DU MOTEUR FLYBACK ===\n")

    # 1. Initialisation des objets mémoires
    print("1. Initialisation de FlybackState et FlybackResults...")
    state = FlybackState()
    result = FlybackResults()
           
    # ---------------------------------------------------------
    # 2. TEST : calc_inputPower
    # ---------------------------------------------------------
    print("\n2. Test de 'calc_inputPower'...")
    calc_inputPower(state)
    print(f"   -> Puissance totale (p_out_total) : {state.p_out_total:.2f} W")
    print(f"   -> Puissance d'entrée (p_in)      : {state.p_in:.2f} W")
    print(f"   -> Tension AC min crête (V_in_min): {state.v_in_min:.2f} V")

    # ---------------------------------------------------------
    # 3. TEST : calc_bulkCapacitance
    # ---------------------------------------------------------
    print("\n3. Test de 'calc_bulkCapacitance'...")
    calc_bulkCapacitance(result, state)
    print(f"   -> C_bulk théorique calculé : {result.c_bulk_calc * 1e6:.2f} µF")
    print(f"   -> V_bulk_min théorique     : {result.v_bulk_min_calc:.2f} V")
    print(f"   -> V_bulk_min_nH théorique  : {result.v_bulk_min_nH_calc:.2f} V")

    # ---------------------------------------------------------
    # 4. TEST : calc_preDesign_transformer
    # ---------------------------------------------------------
    print("\n4. Test de 'calc_preDesign_transformer'...")
    # L'utilisateur choisit une capa standard (ex: 33µF) d'après le calcul précédent
    state.c_bulk = 72.5e-6 
    
    calc_preDesign_transformer(state, result)
    print(f"   -> V_bulk_min réel avec 23.5µF : {state.v_bulk_min:.2f} V")
    print(f"   -> V_bulk_min_nH réel avec 23.5µF : {state.v_bulk_min_nH:.2f} V")
    print(f"   -> Tension réfléchie (V_OR)  : {result.vor_calc:.2f} V")
    print(f"   -> Inductance Primaire (Lp)  : {result.Lp_calc * 1e6:.2f} µH")
    print(f"   -> Ratio de Spire (Np/Ns)    : {result.Np_Ns1_calc:.2f}")
    print(f"   -> Courant Crête (I_pk_max)  : {result.i_p_max_calc:.3f} A")

    # ---------------------------------------------------------
    # 5. TEST : calc_transformer
    # ---------------------------------------------------------
    print("\n5. Test de 'calc_transformer'...")
    calc_transformer(state, result)
    print(f"   -> Spires Primaire (Np)      : {result.Np_calc:.1f} tours")
    print(f"   -> Spires Secondaire (Ns1)   : {result.Ns1_calc:.1f} tours")
    print(f"   -> Inductance réelle (Lp)    : {result.Lp_real_calc * 1e6:.2f} µH")
    print(f"   -> Air Gap calculé (lg)      : {result.lg_calc:.2f} mm")

    print("\n=== FIN DU TEST ===")


if __name__ == "__main__":
    lancer_test_complet()