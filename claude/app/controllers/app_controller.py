"""
AppController : le C du MVC.

Il ne connait pas les widgets CustomTkinter en detail, seulement des
dictionnaires de valeurs en entree et des dataclasses en sortie. C'est ce
qui permettra, plus tard, d'appeler exactement les memes methodes depuis un
export de netlist ou un test automatise, sans dependre de l'interface.
"""

from dataclasses import replace

from app.models.calc_engine import run_input_stage
from app.models.design_state import DesignState, InputStageResults


class AppController:
    def __init__(self, state: DesignState | None = None):
        self.state = state or DesignState()

    def update_input_stage(self, raw_specs: dict) -> InputStageResults:
        """
        Recoit les valeurs brutes du formulaire Etape 1, met a jour
        DesignState.specs, relance CalcEngine, stocke et retourne le
        resultat pour l'etape 2.
        """
        self.state.specs = replace(self.state.specs, **raw_specs)
        self.state.input_stage = run_input_stage(self.state.specs)
        return self.state.input_stage
