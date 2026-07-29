"""
CalcEngine : fonctions de calcul pures pour les etapes 1 et 2.

Chaque fonction reproduit fidelement une formule du classeur Excel fourni
(feuille "Design DCM"). La reference de cellule d'origine est rappelee en
commentaire pour pouvoir auditer la correspondance calcul <-> classeur.

Aucune fonction ici ne touche a l'interface graphique : entree = donnees,
sortie = donnees. C'est ce qui permet de les tester unitairement et de les
reutiliser telles quelles pour generer, plus tard, les netlists LTSpice.
"""

import math
from typing import List

from app.models.design_state import (
    InputSpecs,
    InputStageResults,
    BulkCapIteration,
)

MAX_BULK_CAP_ITERATIONS = 8
BULK_CAP_CONVERGENCE_TOL_UF = 1e-4  # µF


def compute_power_balance(specs: InputSpecs) -> tuple[float, float]:
    """Pout,Sigma (B18) et Pin (B19)."""
    pout_sum = sum(specs.output_powers())                 # B18 = B14+B11+B8
    pin = pout_sum / (specs.eta_pct / 100.0)               # B19 = B18/(F3/100)
    return pout_sum, pin


def compute_vin_extremes(specs: InputSpecs) -> tuple[float, float]:
    """Vin,min (B20) et Vin,max (B21)."""
    vin_min = math.sqrt(2) * specs.vac_min                 # B20
    vin_max = math.sqrt(2) * specs.vac_max                 # B21
    return vin_min, vin_max


def _bulk_cap_iteration_0(specs: InputSpecs, pout_sum: float, vin_min: float) -> BulkCapIteration:
    """Premiere passe (B26:B32), amorcee sur une hypothese d'ondulation, sans Ic,avg.

    Note : le classeur utilise Pout,Sigma (B18) ici, pas Pin (B19) -- le
    (F3/100) au denominateur joue deja le role du rendement."""
    vripple0 = vin_min * (specs.delta_vc_in_pct / 100.0)               # B26
    vbulk_min0 = vin_min - vripple0                                    # B27
    delta_t = math.asin(vbulk_min0 / vin_min) / (2 * math.pi * specs.freq_line)     # B28
    t_c0 = (1.0 / (4 * specs.freq_line)) - delta_t                     # B29
    t_dh0 = ((1 + 2 * specs.nh) / (2 * specs.freq_line)) - t_c0        # B30
    eta = specs.eta_pct / 100.0
    cbulk0_f = (2 * pout_sum * t_dh0) / (eta * (vin_min ** 2 - vbulk_min0 ** 2))  # B31
    return BulkCapIteration(
        index=0,
        vbulk_min=vbulk_min0,
        ic_avg=float("nan"),
        t_conduction=t_c0,
        t_hold=t_dh0,
        cbulk_f=cbulk0_f,
        cbulk_uf=cbulk0_f * 1e6,
    )


def _bulk_cap_next_iteration(
    specs: InputSpecs,
    pout_sum: float,
    pin: float,
    vin_min: float,
    vin_max: float,
    previous: BulkCapIteration,
    index: int,
) -> BulkCapIteration:
    """Reproduit le motif B33:B38 (et son renouvellement B33bis... dans le classeur),
    generalise pour converger au-dela des deux passes manuelles du fichier Excel.

    Toutes ces grandeurs (B33, B34, B37) utilisent Pout,Sigma (B18) au
    numerateur, jamais Pin (B19) -- le facteur eta est deja au denominateur
    de chaque formule du classeur."""
    eta = specs.eta_pct / 100.0
    w = 2 * math.pi * specs.freq_line

    vbulk_min = math.sqrt(
        2 * specs.vac_min ** 2
        - (2 * pout_sum * previous.t_hold) / (eta * previous.cbulk_f)
    )                                                                   # B33
    ic_avg = pout_sum / (eta * vbulk_min)                               # B34
    t_c = (1.0 / w) * (
        math.acos(ic_avg / (vin_max * previous.cbulk_f * w))
        - math.asin(vbulk_min / vin_min)
    )                                                                   # B35
    t_dh = (1.0 / (2 * specs.freq_line)) + (specs.nh / specs.freq_line) - t_c   # B36
    cbulk_f = (2 * pout_sum * t_dh) / (eta * (vin_min ** 2 - vbulk_min ** 2))   # B37

    return BulkCapIteration(
        index=index,
        vbulk_min=vbulk_min,
        ic_avg=ic_avg,
        t_conduction=t_c,
        t_hold=t_dh,
        cbulk_f=cbulk_f,
        cbulk_uf=cbulk_f * 1e6,
    )


def size_bulk_capacitor(
    specs: InputSpecs,
    pout_sum: float,
    pin: float,
    vin_min: float,
    vin_max: float,
    max_iterations: int = MAX_BULK_CAP_ITERATIONS,
    tol_uf: float = BULK_CAP_CONVERGENCE_TOL_UF,
) -> tuple[List[BulkCapIteration], bool]:
    """
    Dimensionnement iteratif du condensateur de bulk par la methode du
    hold-up time (B26:B38 du classeur). Le fichier Excel s'arrete apres deux
    passes manuelles ; ici la boucle continue jusqu'a convergence de Cbulk
    (ou jusqu'a max_iterations), ce qui est la generalisation naturelle de
    la meme methode pour l'app.
    """
    iterations = [_bulk_cap_iteration_0(specs, pout_sum, vin_min)]
    converged = False

    for i in range(1, max_iterations + 1):
        nxt = _bulk_cap_next_iteration(
            specs, pout_sum, pin, vin_min, vin_max, iterations[-1], i
        )
        iterations.append(nxt)
        if abs(nxt.cbulk_uf - iterations[-2].cbulk_uf) < tol_uf:
            converged = True
            break

    return iterations, converged


def run_input_stage(specs: InputSpecs) -> InputStageResults:
    """Point d'entree unique pour l'etape 2, appele par le controleur."""
    pout_sum, pin = compute_power_balance(specs)
    vin_min, vin_max = compute_vin_extremes(specs)
    iterations, converged = size_bulk_capacitor(specs, pout_sum, pin, vin_min, vin_max)

    return InputStageResults(
        pout_sum=pout_sum,
        pin=pin,
        vin_min=vin_min,
        vin_max=vin_max,
        iterations=iterations,
        converged=converged,
    )
