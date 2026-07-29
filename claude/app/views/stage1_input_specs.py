"""
Vue de l'etape 1 (Specifications d'entree) et de l'etape 2 (Etage d'entree).

Cette vue ne calcule rien elle-meme : elle lit les champs, transmet les
valeurs saisies au controleur, et affiche ce que le controleur lui renvoie
depuis CalcEngine. C'est le seul sens de communication (Vue -> Controleur
-> Modele -> Controleur -> Vue), conforme au MVC demande.
"""

from typing import TYPE_CHECKING

import customtkinter as ctk

from app.docs.technical_notes import TECH_NOTES
from app.views.widgets.labeled_field import LabeledField
from app.views.widgets.tooltip import HelpButton

if TYPE_CHECKING:
    from app.controllers.app_controller import AppController


class Stage1View(ctk.CTkFrame):
    """Etape 1 & 2 : Specifications d'entree + Etage d'entree (pont + Cbulk)."""

    def __init__(self, master, controller: "AppController", **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.grid_columnconfigure((0, 1), weight=1, uniform="col")

        self._build_specs_panel()
        self._build_results_panel()

    # ------------------------------------------------------------------ #
    # Panneau de saisie : Etape 1 - Specifications d'entree
    # ------------------------------------------------------------------ #
    def _build_specs_panel(self) -> None:
        panel = ctk.CTkFrame(self, corner_radius=12)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)

        ctk.CTkLabel(
            panel, text="Etape 1 - Specifications d'entree",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(anchor="w", padx=16, pady=(16, 12))

        specs = self.controller.state.specs

        self.field_vac_min = self._add_field(
            panel, "Vac,min", "V", specs.vac_min, help_key="vac_range"
        )
        self.field_vac_max = self._add_field(panel, "Vac,max", "V", specs.vac_max)
        self.field_freq = self._add_field(panel, "Frequence reseau", "Hz", specs.freq_line)

        self._add_separator(panel)

        self.field_vout1 = self._add_field(panel, "Vout1", "V", specs.vout1)
        self.field_pout1 = self._add_field(panel, "Pout1", "W", specs.pout1)

        self._add_separator(panel)

        self.field_eta = self._add_field(
            panel, "Rendement estime (\u03b7)", "%", specs.eta_pct, help_key="eta"
        )
        self.field_delta_vc = self._add_field(
            panel, "Ondulation bus \u0394Vc(in)", "%", specs.delta_vc_in_pct,
            help_key="delta_vc_in",
        )
        self.field_nh = self._add_field(
            panel, "Demi-alternances Nh", "-", specs.nh, help_key="nh"
        )

        ctk.CTkButton(
            panel, text="Calculer l'etage d'entree", command=self._on_compute
        ).pack(anchor="w", padx=16, pady=(20, 16))

    def _add_field(self, panel, label, unit, initial, help_key: str | None = None):
        field = LabeledField(
            panel,
            label=label,
            unit=unit,
            initial_value=f"{initial:g}" if initial is not None else "",
            help_text=TECH_NOTES.get(help_key) if help_key else None,
        )
        field.pack(anchor="w", padx=16, pady=4)
        return field

    def _add_separator(self, panel) -> None:
        ctk.CTkFrame(panel, height=1, fg_color=("gray80", "gray30")).pack(
            fill="x", padx=16, pady=10
        )

    # ------------------------------------------------------------------ #
    # Panneau de resultats : Etape 2 - Etage d'entree
    # ------------------------------------------------------------------ #
    def _build_results_panel(self) -> None:
        panel = ctk.CTkFrame(self, corner_radius=12)
        panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)

        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(anchor="w", fill="x", padx=16, pady=(16, 12))
        ctk.CTkLabel(
            header, text="Etape 2 - Etage d'entree",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(side="left")
        HelpButton(header, TECH_NOTES["bulk_cap_method"]).pack(side="left", padx=(8, 0))

        self.result_labels: dict[str, ctk.CTkLabel] = {}
        for key, text in [
            ("pout_sum", "Pout,\u03a3"),
            ("pin", "Pin"),
            ("vin_min", "Vin,min"),
            ("vin_max", "Vin,max"),
            ("vbulk_min", "Vbulk,min (converge)"),
            ("vbulk_max", "Vbulk,max"),
            ("cbulk", "Cbulk requis"),
            ("iterations", "Iterations jusqu'a convergence"),
        ]:
            row = ctk.CTkFrame(panel, fg_color="transparent")
            row.pack(anchor="w", fill="x", padx=16, pady=3)
            ctk.CTkLabel(row, text=text, width=200, anchor="w").pack(side="left")
            value_label = ctk.CTkLabel(row, text="\u2014", anchor="w", text_color=("gray20", "gray80"))
            value_label.pack(side="left")
            self.result_labels[key] = value_label

        self.status_label = ctk.CTkLabel(
            panel, text="", text_color=("#b03030", "#e08080"), wraplength=320, justify="left"
        )
        self.status_label.pack(anchor="w", padx=16, pady=(16, 16))

    # ------------------------------------------------------------------ #
    def _on_compute(self) -> None:
        raw = {
            "vac_min": self.field_vac_min.get_float(),
            "vac_max": self.field_vac_max.get_float(),
            "freq_line": self.field_freq.get_float(),
            "vout1": self.field_vout1.get_float(),
            "pout1": self.field_pout1.get_float(),
            "eta_pct": self.field_eta.get_float(),
            "delta_vc_in_pct": self.field_delta_vc.get_float(),
            "nh": self.field_nh.get_float(),
        }

        missing = [k for k, v in raw.items() if v is None]
        if missing:
            self.status_label.configure(
                text=f"Champs invalides ou vides : {', '.join(missing)}"
            )
            return

        self.status_label.configure(text="")
        results = self.controller.update_input_stage(raw)
        self._render_results(results)

    def _render_results(self, results) -> None:
        self.result_labels["pout_sum"].configure(text=f"{results.pout_sum:.3f} W")
        self.result_labels["pin"].configure(text=f"{results.pin:.3f} W")
        self.result_labels["vin_min"].configure(text=f"{results.vin_min:.3f} V")
        self.result_labels["vin_max"].configure(text=f"{results.vin_max:.3f} V")
        self.result_labels["vbulk_min"].configure(
            text=f"{results.vbulk_min_final:.3f} V" if results.vbulk_min_final else "\u2014"
        )
        self.result_labels["vbulk_max"].configure(text=f"{results.vbulk_max:.3f} V")
        self.result_labels["cbulk"].configure(
            text=f"{results.cbulk_uf_final:.3f} \u00b5F" if results.cbulk_uf_final else "\u2014"
        )
        n_iter = len(results.iterations) - 1  # -1 : l'iteration 0 est l'amorce, pas une convergence
        conv_text = f"{n_iter}" + ("" if results.converged else " (non converge)")
        self.result_labels["iterations"].configure(text=conv_text)
