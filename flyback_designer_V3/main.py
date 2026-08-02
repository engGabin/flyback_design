import sys
from PyQt6.QtWidgets import QApplication
from flyback_designer_V3.models.flyback_states import FlybackState
from flyback_designer_V2.models.calc_engine import recalc_all

class FlybackController:
    """
    LE CONTRÔLEUR (MVC)
    Il fait le lien entre la fenêtre (Vue) et les mathématiques (Modèle).
    """
    def __init__(self):
        # 1. Création de la mémoire (Le Modèle)
        self.state = FlybackState()
        
        # 2. Création de l'application graphique (La Vue)
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion") # Applique un thème moderne par défaut
        self.window = MainWindow(self.state)
        
        # 3. Connexion des événements (Le Câblage)
        # Quand on clique sur le bouton "Appliquer" de l'étape 1, ça lance notre fonction 'on_step1_apply'
        self.window.page_step1.btn_apply.clicked.connect(self.on_step1_apply)
        
    def on_step1_apply(self):
        """Fonction déclenchée par le bouton de l'étape 1."""
        print("\n--- Lancement des calculs ---")
        
        # A. On lit les valeurs tapées à l'écran et on les met dans la mémoire
        page = self.window.page_step1
        self.state.specs.vac_min = page.inp_vac_min.value
        self.state.specs.vac_max = page.inp_vac_max.value
        self.state.specs.vout = page.inp_vout.value
        self.state.specs.pout = page.inp_pout.value
        self.state.specs.eta = page.inp_eta.value
        self.state.specs.f_line = page.inp_fline.value
        
        # B. On lance la grosse calculatrice (calc_engine.py)
        recalc_all(self.state)
        
        # C. Mise à jour de l'interface (Cases grises de résultat)
        page.update_results()
        
        # D. On affiche le résultat de l'étape 2 (Calculs en arrière-plan) dans la console Python pour vérifier !
        print(f"Puissance d'entrée : {self.state.specs.pin:.2f} W")
        print(f"Vbulk Maximum      : {self.state.specs.vbulk_max:.2f} V")
        print(f"Vbulk Minimum      : {self.state.specs.vbulk_min:.2f} V")
        print("-----------------------------\n")

    def run(self):
        """Affiche la fenêtre et lance la boucle de l'application."""
        self.window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    # Démarre tout
    controller = FlybackController()
    controller.run()