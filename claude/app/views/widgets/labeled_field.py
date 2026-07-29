"""
LabeledField : ligne standard "Label [entree] unite (?)" utilisee dans
tous les formulaires de saisie de l'application.
"""

from typing import Callable, Optional

import customtkinter as ctk

from app.views.widgets.tooltip import HelpButton


class LabeledField(ctk.CTkFrame):
    def __init__(
        self,
        master,
        label: str,
        unit: str = "",
        initial_value: str = "",
        help_text: Optional[str] = None,
        on_change: Optional[Callable[[str], None]] = None,
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text=label, width=140, anchor="w").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )

        self.var = ctk.StringVar(value=initial_value)
        self.entry = ctk.CTkEntry(self, textvariable=self.var, width=110)
        self.entry.grid(row=0, column=1, sticky="w")

        if unit:
            ctk.CTkLabel(self, text=unit, width=40, anchor="w").grid(
                row=0, column=2, sticky="w", padx=(6, 0)
            )

        if help_text:
            HelpButton(self, help_text).grid(row=0, column=3, padx=(8, 0))

        if on_change:
            self.var.trace_add("write", lambda *_: on_change(self.var.get()))

    def get_float(self) -> Optional[float]:
        raw = self.var.get().strip().replace(",", ".")
        if not raw:
            return None
        try:
            return float(raw)
        except ValueError:
            return None

    def set_value(self, value) -> None:
        self.var.set("" if value is None else f"{value:g}")
