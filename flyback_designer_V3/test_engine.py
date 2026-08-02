# =======================================================
# File : calc_engine.py
# Author : Gabin SBAFFI
# Date : 2026-07-31
# Description : this file is a test script to verify the functionality of the calculation engine linked to the design_state.py file.
# =======================================================

from flyback_designer_V3.models.flyback_states import FlybackState
from flyback_designer_V3.models.calc_engine import *

def tester_mon_moteur():
    print("=== DÉBUT DU TEST DU MOTEUR FLYBACK ===\n")

    # 1. Création de la 'mémoire' vierge
    print("1. Initialisation de la mémoire (DesignState)...")
    etat = FlybackState()
    print(f"   -> Valeurs par défaut : Pout = {etat.p_out1} W, C_bulk = {etat.c_bulk*1e6} µF")

    # 2. Premier calcul avec les valeurs par défaut
    print("\n2. Lancement des calculs (recalc_all)...")
    recalc_all(etat)
    print(f"   -> Résultat : V_bulk_min = {etat.v_bulk_min:.2f} V")

    # 3. On simule un utilisateur qui change une valeur
    print("\n3. Simulation d'un changement : Pout passe à 30 W et C_bulk à 10 µF...")
    etat.p_out1 = 30.0
    etat.c_bulk = 320e-6

    # 4. On recalcule
    print("\n4. Relance des calculs...")
    print(f"   -> Valeurs modifiées : Pout = {etat.p_out1} W, C_bulk = {etat.c_bulk*1e6} µF")
    recalc_all(etat)
    
    # 5. On vérifie le nouveau résultat
    if etat.v_bulk_min != 0.0:
        print(f"   -> Résultat : V_bulk_min = {etat.v_bulk_min:.2f} V")

    print("\n=== FIN DU TEST ===")

if __name__ == "__main__":
    tester_mon_moteur()