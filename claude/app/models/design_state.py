"""
Modele central de l'application (M du MVC).

DesignState regroupe l'etat complet d'un design flyback, etape par etape.
Chaque etape a sa propre dataclass de SAISIES (ce que l'utilisateur choisit)
et, quand cela a du sens, une dataclass de RESULTATS (ce que CalcEngine
calcule). Les etapes 3 a 10 ne sont pas encore implementees dans ce livrable
mais leurs dataclasses sont deja posees pour que le reste de l'application
s'y raccorde sans refonte de l'architecture.

Regle de conception : DesignState ne contient JAMAIS de logique de calcul.
Les calculs vivent exclusivement dans calc_engine.py (fonctions pures,
testables independamment de toute interface graphique).
"""

from dataclasses import dataclass, field, fields
from typing import Optional


@dataclass
class InputSpecs:
    """Etape 1 : Specifications d'entree (feuille Excel 'Design DCM', cellules B3:B16)."""

    vac_min: float = 85.0        # B3 - Tension secteur minimale [V]
    vac_max: float = 528.0       # B4 - Tension secteur maximale [V]
    freq_line: float = 50.0      # B5 - Frequence reseau [Hz]

    vout1: float = 12.0          # B6 - Tension de sortie principale [V]
    iout1: float = 0.583333      # B7 (= B8/B6 dans le classeur ; ici on le rend editable) [A]
    pout1: float = 7.0           # B8 - Puissance de sortie principale [W]

    vout2: Optional[float] = None   # B9
    iout2: Optional[float] = None   # B10
    pout2: Optional[float] = None   # B11

    vaux: Optional[float] = None    # B12
    iaux: Optional[float] = None    # B13
    paux: Optional[float] = None    # B14

    delta_vc_in_pct: float = 25.0   # B15 - Ondulation admissible du bus DC [%]
    nh: int = 1                     # B16 - Nombre de demi-alternances perdues (hold-up)

    eta_pct: float = 85.0           # F3 - Rendement estime [%]

    def output_powers(self) -> list[float]:
        """Retourne toutes les puissances de sortie renseignees (0 si vide)."""
        return [self.pout1 or 0.0, self.pout2 or 0.0, self.paux or 0.0]


@dataclass
class BulkCapIteration:
    """Une iteration du dimensionnement du condensateur de bulk (B26:B38)."""

    index: int
    vbulk_min: float          # V
    ic_avg: float             # A (absent a l'iteration 0)
    t_conduction: float       # s  (t_c)
    t_hold: float             # s  (t_d_h)
    cbulk_f: float            # F
    cbulk_uf: float           # µF


@dataclass
class InputStageResults:
    """Etape 2 : Etage d'entree - pont redresseur + condensateur de bulk."""

    pout_sum: float = 0.0      # B18
    pin: float = 0.0           # B19
    vin_min: float = 0.0       # B20 = sqrt(2) * Vac,min
    vin_max: float = 0.0       # B21 = sqrt(2) * Vac,max

    iterations: list[BulkCapIteration] = field(default_factory=list)
    converged: bool = False

    @property
    def cbulk_uf_final(self) -> Optional[float]:
        return self.iterations[-1].cbulk_uf if self.iterations else None

    @property
    def vbulk_min_final(self) -> Optional[float]:
        return self.iterations[-1].vbulk_min if self.iterations else None

    @property
    def vbulk_max(self) -> float:
        # Le bus continu monte jusqu'au sommet de la tension secteur max redressee.
        return self.vin_max


@dataclass
class DesignChoices:
    """Etape 3 (a venir) : Dmax, f_sw, Krp — laisse ici pour reference future."""

    dmax: float = 0.61
    f_sw: float = 132000.0
    krp: float = 1.0


@dataclass
class DesignState:
    """Etat complet du projet, transmis entre les vues via le controleur."""

    specs: InputSpecs = field(default_factory=InputSpecs)
    input_stage: InputStageResults = field(default_factory=InputStageResults)
    choices: DesignChoices = field(default_factory=DesignChoices)
    # Etapes 4 a 10 : topologie, controleur/transfo, magnetiques, snubber,
    # sortie, pertes, routage -- a ajouter au fil des prochains livrables,
    # chacune sous forme d'une dataclass dediee suivant le meme patron.
