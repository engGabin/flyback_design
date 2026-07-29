"""
tabs/formula_ref.py — Formula Reference tab.

Displays all design equations used in the tool, grouped by stage.
Uses QTextBrowser with rich HTML; Greek symbols are Unicode.
Can be extended to render LaTeX via a WebEngineView + MathJax if needed.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QLabel
from PyQt6.QtCore    import Qt
from PyQt6.QtGui     import QFont


FORMULA_HTML = """
<html>
<head>
<style>
  body  { font-family: 'Segoe UI', sans-serif; font-size: 13px;
          color: #2a2a2a; margin: 16px; }
  h2    { font-size: 14px; font-weight: 600; color: #1a3a5c;
          border-bottom: 1px solid #dde; padding-bottom: 4px; margin-top: 20px; }
  h3    { font-size: 12px; font-weight: 600; color: #444; margin: 10px 0 4px; }
  .eq   { font-family: 'Courier New', monospace; font-size: 12px;
          background: #f4f6fa; border-left: 3px solid #4a80c4;
          padding: 6px 10px; margin: 4px 0 8px; border-radius: 2px; }
  .note { font-size: 11px; color: #666; margin: 0 0 8px 12px; }
</style>
</head>
<body>

<h2>1 — Input specifications</h2>

<h3>Output current</h3>
<div class="eq">I_out = P_out / V_out</div>

<h3>Input power</h3>
<div class="eq">P_in = P_out / η</div>

<h3>Bulk voltage (peak of rectified AC)</h3>
<div class="eq">V_bulk_max = V_ac_max × √2</div>
<div class="eq">V_bulk_min = V_ac_min × √2</div>

<h2>2 — Input stage</h2>

<h3>Bulk capacitor — hold-up sizing</h3>
<div class="eq">C_in ≥ 2 × P_in × t_hold / (V_bulk_min² − V_end²)   [F]</div>
<div class="note">V_end = 0.9 × V_bulk_min (10 % droop assumption)</div>
<div class="note">t_hold = 10 ms (one half-period at 50 Hz)</div>

<h3>Capacitor voltage rating</h3>
<div class="eq">V_C_rated ≥ 1.15 × V_bulk_max</div>

<h3>Input RMS current (approximate)</h3>
<div class="eq">I_in_rms ≈ P_in / (V_ac_min × PF)    PF ≈ 0.9 without PFC</div>

<h2>3 — Switching structure (StackFET / DCM flyback)</h2>
<div class="note">No dedicated formulas — see architecture selection notes.</div>

<h2>4 — Transformer design (DCM)</h2>

<h3>Magnetising inductance</h3>
<div class="eq">L_mag = (V_bulk_min × D_max)² / (2 × P_in × f_sw)   [H]</div>

<h3>Turns ratio</h3>
<div class="eq">n = N_p / N_s = (V_bulk_min × D_max) / ((V_out + V_f) × (1 − D_max))</div>
<div class="note">V_f = output diode forward voltage (≈ 0.4–0.8 V for Schottky)</div>

<h3>Reflected output voltage</h3>
<div class="eq">V_OR = (V_out + V_f) × n</div>

<h3>Primary peak current</h3>
<div class="eq">I_pk_pri = V_bulk_min × D_max / (L_mag × f_sw)</div>

<h3>Primary turns (from core Ae and B_max)</h3>
<div class="eq">N_p = L_mag × I_pk_pri / (B_max × A_e)   [turns]</div>
<div class="note">B_max ≤ 0.25 T for ferrite (MnZn) to avoid saturation</div>

<h3>Secondary turns</h3>
<div class="eq">N_s = N_p / n</div>

<h2>5 — Current waveforms (DCM)</h2>

<h3>On-time</h3>
<div class="eq">t_on = D_max / f_sw</div>

<h3>Demagnetisation time</h3>
<div class="eq">t_off = L_mag × I_pk_pri / V_OR</div>

<h3>Primary RMS current</h3>
<div class="eq">I_rms_pri = I_pk_pri × √(D_max / 3)</div>

<h3>Secondary peak current</h3>
<div class="eq">I_pk_sec = I_pk_pri × n</div>

<h3>Secondary RMS current</h3>
<div class="eq">I_rms_sec = I_pk_sec × √(D_off / 3)    D_off = t_off × f_sw</div>

<h2>6 — Wire sections</h2>

<h3>Required cross-section</h3>
<div class="eq">S_pri = I_rms_pri / J_pri   [mm²]</div>
<div class="eq">S_sec = I_rms_sec / J_sec   [mm²]</div>
<div class="note">J = 3–6 A/mm² for forced-air cooling; 2–4 A/mm² for natural convection</div>

<h3>Skin depth</h3>
<div class="eq">δ = √(ρ / (π × f_sw × μ₀))   [m]</div>
<div class="note">For copper at 100 °C: δ ≈ 75 / √f_sw  [µm]  (f in Hz)</div>

<h2>7 — Losses</h2>

<h3>MOSFET switching losses</h3>
<div class="eq">P_sw = ½ × V_bulk × I_pk × (t_r + t_f) × f_sw</div>

<h3>MOSFET conduction losses</h3>
<div class="eq">P_cond = R_ds(on) × I_rms_pri²</div>

<h3>Core losses (Steinmetz)</h3>
<div class="eq">P_core = k × f_sw^α × B_max^β × V_e</div>
<div class="note">Typical MnZn ferrite: k≈1.5, α≈1.5, β≈2.5 (fit to datasheet Pcv curve)</div>

<h3>Output diode losses</h3>
<div class="eq">P_diode = V_f × I_out</div>

<h2>8 — RCD Snubber</h2>

<h3>Primary switch voltage without snubber</h3>
<div class="eq">V_DS_peak = V_bulk_max + V_OR + ΔV_spike</div>
<div class="note">ΔV_spike due to leakage inductance L_lk ringing with C_DS</div>

<h3>Clamp voltage target</h3>
<div class="eq">V_clamp = 1.3 × (V_bulk_max + V_OR)</div>

<h3>Snubber capacitor</h3>
<div class="eq">C_snub ≥ L_lk × I_pk² / (V_clamp − V_OR)²</div>

<h3>Snubber resistor</h3>
<div class="eq">R_snub = V_clamp² / P_snub   (P_snub ≈ ½ × L_lk × I_pk² × f_sw)</div>

<h2>9 — Output stage</h2>

<h3>Output diode voltage rating</h3>
<div class="eq">V_RRM ≥ 1.5 × (V_bulk_max / n + V_out)</div>

<h3>Output capacitor — ripple spec</h3>
<div class="eq">C_out ≥ I_out / (f_sw × ΔV_ripple)</div>

<h3>ESR ripple contribution</h3>
<div class="eq">ΔV_ESR = ESR × I_pk_sec</div>

</body>
</html>
"""


class FormulaRefTab(QWidget):
    """Scrollable HTML reference of all design equations."""

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)

        browser = QTextBrowser()
        browser.setOpenExternalLinks(False)
        browser.setHtml(FORMULA_HTML)
        lay.addWidget(browser)
