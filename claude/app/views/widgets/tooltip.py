"""
HelpButton : petit bouton rond '?' qui affiche une info-bulle technique
au survol. Reutilise sur chaque etape de l'application.
"""

import customtkinter as ctk


class HelpButton(ctk.CTkFrame):
    """Bouton '?' + fenetre flottante affichant du texte au survol."""

    def __init__(self, master, text: str, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._text = text
        self._popup: ctk.CTkToplevel | None = None

        self.button = ctk.CTkButton(
            self,
            text="?",
            width=22,
            height=22,
            corner_radius=11,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("gray75", "gray30"),
            hover_color=("gray65", "gray40"),
        )
        self.button.pack()
        self.button.bind("<Enter>", self._show)
        self.button.bind("<Leave>", self._hide)

    def _show(self, _event=None):
        if self._popup is not None:
            return
        x = self.button.winfo_rootx() + 25
        y = self.button.winfo_rooty()

        self._popup = ctk.CTkToplevel(self)
        self._popup.wm_overrideredirect(True)
        self._popup.wm_geometry(f"+{x}+{y}")
        self._popup.attributes("-topmost", True)

        label = ctk.CTkLabel(
            self._popup,
            text=self._text,
            wraplength=320,
            justify="left",
            fg_color=("gray90", "gray20"),
            corner_radius=8,
            padx=10,
            pady=8,
        )
        label.pack()

    def _hide(self, _event=None):
        if self._popup is not None:
            self._popup.destroy()
            self._popup = None
