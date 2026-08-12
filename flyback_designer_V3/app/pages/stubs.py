"""
pages/stubs.py — Placeholder pages for every design stage not yet implemented.

Each stub shows its page title and a "coming soon" message.
Replace each class with a real implementation as the project develops.
"""

from PyQt6.QtWidgets import QLabel, QVBoxLayout
from PyQt6.QtCore    import Qt

from ..widgets.common import PageBase, SectionHeader, ResultRow, HLine


def _make_stub(title: str, description: str):
    """Factory that returns a minimal stub PageBase subclass."""

    class _StubPage(PageBase):
        def __init__(self, ds, res, parent=None):
            super().__init__(ds, res, title=title, parent=parent)

        def _build_ui(self):
            lbl = QLabel(description)
            lbl.setWordWrap(True)
            lbl.setStyleSheet("color: #888; font-style: italic; padding: 12px 0;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            self._content_layout.addWidget(lbl)

        def refresh(self):
            pass

    _StubPage.__name__ = title.replace(" ", "") + "Page"
    return _StubPage


# ------------------------------------------------------------------ #
# One stub per unimplemented page
# ------------------------------------------------------------------ #


StructurePage = _make_stub(
    "Switching structure",
    "Selection of the controller architecture:\n"
    "  • StackFET — 800 V controller IC + external 1000 V CoolMOS (e.g. Infineon ICE2QR / ICE5QR, ST VIPER35)\n"
    "  • Driver + external MOSFET\n"
    "  • Integrated controller (MOSFET on-chip)\n\n"
    "Helps compare V_DS rating, gate drive requirements, and BOM impact.",
)



WaveformsPage = _make_stub(
    "Current waveforms",
    "Time-domain plots of primary and secondary currents in DCM:\n"
    "  I_pk_pri, I_rms_pri, I_pk_sec, I_rms_sec, t_on, t_off, duty cycle D.\n\n"
    "Matplotlib chart showing one full switching period will be added here.",
)

WireSectionsPage = _make_stub(
    "Wire sections",
    "Wire cross-section calculation from RMS currents and current density J:\n"
    "  S_pri = I_rms_pri / J_pri  [mm²]  →  AWG / diameter\n"
    "  S_sec = I_rms_sec / J_sec  [mm²]  →  AWG / diameter\n\n"
    "Will include Litz wire option and skin-depth check at f_sw.",
)

LossesPage = _make_stub(
    "Losses",
    "Breakdown of estimated power losses:\n"
    "  • MOSFET switching losses (Coss, tr, tf)\n"
    "  • MOSFET conduction losses (Rds_on × I_rms²)\n"
    "  • Core losses (Steinmetz: P = k × f^α × B^β × Ve)\n"
    "  • Output diode losses (Vf × I_avg)\n\n"
    "Total loss budget and efficiency estimate η_actual.",
)

SnubberPage = _make_stub(
    "Snubber design",
    "RCD clamp snubber sizing for the primary-side voltage spike:\n"
    "  V_spike = V_bulk_max + n·V_out + ΔV_leakage\n"
    "  C_snub, R_snub, V_clamp, P_snub.\n\n"
    "Will include leakage inductance estimation from transformer geometry.",
)

OutputStagePage = _make_stub(
    "Output stage",
    "Sizing of the output rectification and filtering:\n"
    "  • Output diode: V_RRM = (V_bulk_max / n) + V_out, I_avg = I_out\n"
    "  • Output capacitor C_out [µF], ESR, ripple voltage ΔV\n"
    "  • Optional LC post-filter (L_pf, C_pf) for low-noise applications.",
)
