"""
MainWindow : fenetre principale avec navigation laterale par etapes.

Seule l'etape 1&2 (Stage1View) est implementee dans ce livrable. Les
etapes 3 a 10 apparaissent dans la barre laterale a titre de plan
d'ensemble et affichent un panneau "a venir" tant qu'elles ne sont pas
developpees -- ce qui permet de brancher chaque nouvelle etape sans
modifier la structure de navigation.
"""

import customtkinter as ctk

from app.controllers.app_controller import AppController
from app.views.stage1_input_specs import Stage1View

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

STAGES = [
    ("1-2", "Specs & Etage d'entree"),
    ("3", "Parametres de conception"),
    ("4", "Choix de la structure"),
    ("5", "Controleur & Transformateur"),
    ("6", "Design du transformateur"),
    ("7", "Snubber"),
    ("8", "Etage de sortie"),
    ("9", "Pertes & thermique"),
    ("10", "Routage & divers"),
]


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Flyback Designer")
        self.geometry("1180x720")
        self.minsize(980, 600)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.controller = AppController()

        self._build_sidebar()
        self._build_content_area()
        self._show_stage("1-2")

    def _build_sidebar(self) -> None:
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(
            sidebar, text="Flyback Designer",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", padx=20, pady=(24, 4))
        ctk.CTkLabel(
            sidebar, text="Alimentation a decoupage",
            font=ctk.CTkFont(size=12), text_color=("gray40", "gray60"),
        ).pack(anchor="w", padx=20, pady=(0, 20))

        self.stage_buttons: dict[str, ctk.CTkButton] = {}
        for key, label in STAGES:
            btn = ctk.CTkButton(
                sidebar,
                text=f"{key}. {label}",
                anchor="w",
                fg_color="transparent",
                command=lambda k=key: self._show_stage(k),
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.stage_buttons[key] = btn

    def _build_content_area(self) -> None:
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color=("gray95", "gray10"))
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.stage1_view = Stage1View(self.content, self.controller, fg_color="transparent")
        self.placeholder_view = self._build_placeholder()

    def _build_placeholder(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.content, fg_color="transparent")
        ctk.CTkLabel(
            frame,
            text="Cette etape n'est pas encore implementee dans cette version.",
            font=ctk.CTkFont(size=14),
            text_color=("gray40", "gray60"),
        ).pack(padx=20, pady=40)
        return frame

    def _show_stage(self, key: str) -> None:
        for k, btn in self.stage_buttons.items():
            btn.configure(fg_color=("gray80", "gray25") if k == key else "transparent")

        self.stage1_view.grid_forget()
        self.placeholder_view.grid_forget()

        if key == "1-2":
            self.stage1_view.grid(row=0, column=0, sticky="nsew")
        else:
            self.placeholder_view.grid(row=0, column=0, sticky="nsew")


def main() -> None:
    app = MainWindow()
    app.mainloop()
