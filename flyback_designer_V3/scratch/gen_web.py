def latex_wrap(content, note=None):
    html = f'''
<div class="eq">
  \\[
  \\begin{{aligned}}
  {content}
  \\end{{aligned}}
  \\]
</div>
'''
    if note:
        html += f'<div class="note">{note}</div>\n'
    return html

html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
  <script id="MathJax-script" async
          src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
  </script>
  <style>
    body  {{ font-family: 'Segoe UI', sans-serif; font-size: 14px;
            color: #F0EBD8; margin: 16px; background-color: #0D1321; }}
    h2    {{ font-size: 16px; font-weight: bold; color: #748CAB;
            border-bottom: 2px solid #3E5C76; padding-bottom: 6px; margin-top: 24px; }}
    h3    {{ font-size: 14px; font-weight: bold; color: #A9BECD; margin: 12px 0 6px; }}
    .note {{ font-size: 12px; color: #8FACC0; font-style: italic; margin: 0 0 10px 14px; }}
    .eq   {{ background: #273A56; border-left: 4px solid #748CAB;
            padding: 2px 16px; margin: 6px 0 12px; border-radius: 4px; overflow-x: auto; }}
    mjx-container {{ margin: 0 !important; padding: 10px 0 !important; }}
  </style>
</head>
<body>
"""

html += "<h2>1 — Input Power (calc_inputPower)</h2>\n"
html += latex_wrap(r"""P_{out,total} &= P_{out1} + P_{out2} + P_{aux} \\
P_{in} &= \frac{P_{out,total}}{\eta} \\
I_{out1} &= \frac{P_{out1}}{V_{out1}} \\
I_{out2} &= \frac{P_{out2}}{V_{out2}} \\
I_{aux} &= \frac{P_{aux}}{V_{aux}} \\
V_{in,min} &= V_{ac,min}\sqrt{2} \\
V_{in,max} &= V_{ac,max}\sqrt{2}""")

html += "<h2>2 — Bulk Capacitor (calc_bulkCapacitance)</h2>\n"
html += latex_wrap(r"""V_{ripple} &= V_{in,min}\,\Delta V_{bulk} \\
V_{bulk} &= V_{in,min} - V_{ripple} \\
\Delta T &= \frac{\arcsin\!\left(\dfrac{V_{bulk,min}}{V_{in,min}}\right)}{2\pi f_{L}} \\
t_c &= \frac{1}{4 f_{L}} - \Delta t \\
t_d &= \frac{1}{2 f_{L}} - t_c \\
t_{d,nH} &= \frac{1+2N_h}{2 f_{L}} - t_c \\
C_{bulk} &= \frac{2\,P_{out,total}\,t_{d,nH}}{\eta\left(V_{in,min}^{2} - V_{bulk}^{2}\right)} \\
V_{bulk,min,nH} &= \sqrt{2\,V_{ac,min}^{2} - \frac{2\,P_{out,total}\,t_{d,nH}}{\eta\, C_{bulk}}} \\
V_{bulk,min} &= \sqrt{2\,V_{ac,min}^{2} - \frac{2\,P_{out,total}\,t_{d}}{\eta\, C_{bulk}}}""")

html += "<h2>3 — Preliminary Sizing of the Transformer (calc_preDesign_transformer)</h2>\n"
html += latex_wrap(r"""V_{OR} &= \frac{D_{max}\,V_{bulk,min}}{1 - D_{max}} \\
V_{DS,on} &= \frac{V_{bulk,min} + V_{OR}}{1 + \dfrac{V_{bulk,min}\,V_{OR}}{R_{DS,on}\,P_{in}}} \\
\frac{N_p}{N_{s1}} &= \frac{V_{OR}}{V_{out1} + V_F} \\
D_{out} &= \frac{\left(V_{bulk,min} - V_{DS,on}\right) D_{max}}{V_{OR}} \\
D_m &= D_{max} - D_{out} \\
L_p &= \frac{\left(V_{bulk,min} - V_{DS,on}\right)^{2} D_{max}^{2}}{P_{in}\, f_{sw}\, K_{rp}}\left(1 - \frac{K_{rp}}{2}\right)""")

html += "<h3>Primary Current Estimations:</h3>\n"
html += latex_wrap(r"""I_{p,avg} &= \frac{P_{out,total}}{\eta\, V_{bulk,min}} \\
I_{p,avg,on} &= \frac{P_{out,total}}{V_{bulk,min}\,\eta\,D_{max}} \\
I_{p,max} &= \frac{P_{in}}{V_{bulk,min}\,D_{max}\left(1 - \dfrac{K_{rp}}{2}\right)} \\
I_{p,rms} &= I_{p,max}\sqrt{D_{max}\left(\frac{K_{rp}^{2}}{3} - K_{rp} + 1\right)} \\
\Delta I_p &= I_{p,max}\,K_{rp} \\
I_{p,valley} &= I_{p,max} - \Delta I_p \\
I_{p,dc} &= \frac{D_{max}\,I_{p,max}}{2} \\
I_{p,ac} &= \sqrt{I_{p,rms}^{2} - I_{p,dc}^{2}}""")

html += "<h3>Secondary Current Estimations:</h3>\n"
html += latex_wrap(r"""I_{s,max} &= \frac{2\,I_{out1}}{D_{out}\left(2 - K_{rp}\right)} \\
I_{s,rms} &= I_{s,max}\sqrt{D_{out}\left(\frac{K_{rp}^{2}}{3} - K_{rp} + 1\right)} \\
I_{s,avg} &= I_{out}""")

html += "<h3>Area Product:</h3>\n"
html += latex_wrap(r"""A_eA_w = L_p\,\frac{I_{p,max}}{B_{max}}\,k_b\left(\frac{I_{p,rms}}{J_{max}} + \frac{I_{s,rms}}{J_{max}\,\dfrac{N_p}{N_{s1}}}\right)""")

html += "<h2>4 — Transformer (calc_transformer)</h2>\n"
html += latex_wrap(r"""N_{P} &= \sqrt{\frac{L_p}{A_l \cdot 10^{-9}}} \\
l_g\ [\mathrm{m}] &= \frac{4\pi \cdot 10^{-7}\,N_{p,int}^{2}\,A_e \cdot 10^{-6}}{L_p} - \frac{l_e \cdot 10^{-3}}{\mu_{core}} \\
l_g\ [\mathrm{mm}] &= l_g\ [\mathrm{m}] \cdot 10^{3} \\
F_{ringing} &= 1 + \frac{l_g\ [\mathrm{m}]}{\sqrt{A_e \cdot 10^{-6}}}\,\ln\!\left(\frac{2g\cdot 10^{-3}}{l_g\ [\mathrm{m}]}\right) \\
N_{np} &= \sqrt{\frac{L_p\, l_g\ [\mathrm{m}]\cdot 10^{7}}{4\pi\, A_e \cdot 10^{-6}\, F_{ringing}}} \\
L_{p,real} &= N_p^{2}\, A_l \cdot 10^{-9} \\
B_{max,real} &= \frac{L_{p,real}\, I_{p,max}}{N_p\, A_e \cdot 10^{-6}} \\
N_{s1} &= \frac{N_p}{N_p/N_{s1}} \\
N_{s2} &= \frac{N_p\left(V_{out2}+V_F\right)\left(1 - D_{max} - D_m\right)}{V_{bulk,min}\,D_{max}} \\
N_{aux} &= \frac{N_p\left(V_{aux}+V_F\right)\left(1 - D_{max} - D_m\right)}{V_{bulk,min}\,D_{max}}""")

html += "<h2>5 — Final Flyback State (calc_flybackState)</h2>\n"
html += "<h3>Voltages:</h3>\n"
html += latex_wrap(r"""V_{OR} &= \frac{N_p}{N_{s1}}\left(V_{out1} + V_F\right) \\
V_{DS,on} &= \frac{V_{bulk,min} + V_{OR}}{1 + \dfrac{V_{bulk,min}\,V_{OR}}{R_{DS,on}\,P_{in}}}""")

html += "<h3>Primary Currents:</h3>\n"
html += latex_wrap(r"""I_{p,avg} &= \frac{P_{out,total}}{V_{bulk,min}\,\eta} \\
I_{p,avg,on} &= \frac{P_{out,total}}{V_{bulk,min}\,\eta\,D_{max}} \\
\Delta I_p &= \frac{V_{bulk,min}\,D_{max}}{L_{p,real}\,f_{sw}} \\
I_{p,max} &= I_{p,avg,on} + \frac{\Delta I_p}{2} \\
I_{p,rms} &= \sqrt{\left(3\,I_{p,avg}^{2} + \left(\frac{\Delta I_p}{2}\right)^{2}\right)\frac{D_{max}}{3}} \\
I_{p,valley} &= I_{p,max} - \Delta I_p \\
I_{p,dc} &= \frac{D_{max}\,I_{p,max}}{2} \\
I_{p,ac} &= \sqrt{I_{p,rms}^{2} - I_{p,dc}^{2}}""")

html += r"<h3>Duty Cycle and Secondary Current (subscript $k \in \{1,2\}$):</h3>\n"
html += latex_wrap(r"""D_{out} &= \frac{\left(V_{bulk,min} - V_{DS,on}\right) D_{max}}{V_{OR}} \\
D_m &= 1 - D_{max} - D_{out} \\
I_{sk,max} &= \frac{2\,I_{outk}}{D_{out}\left(2 - K_{rp}\right)} \\
I_{sk,rms} &= I_{sk,max}\sqrt{D_{out}\left(\frac{K_{rp}^{2}}{3} - K_{rp} + 1\right)} \\
I_{sk,valley} &= I_{sk,max}\left(1 - K_{rp}\right) \\
\Delta I_{sk} &= I_{sk,max} - I_{sk,valley} \\
I_{sk,dc} &= I_{outk} \\
I_{sk,ac} &= \sqrt{I_{sk,rms}^{2} - I_{sk,dc}^{2}}""")

html += "<h3>Transformer:</h3>\n"
html += latex_wrap(r"""l_g\ [\mathrm{m}] &= \frac{4\pi\cdot 10^{-7}\,N_p^{2}\,A_e\cdot 10^{-6}}{L_{p,real}} - \frac{l_e\cdot 10^{-3}}{\mu_{core}} \\
l_g\ [\mathrm{mm}] &= l_g\ [\mathrm{m}]\cdot 10^{3} \\
F_{ringing} &= 1 + \frac{l_g\ [\mathrm{m}]}{\sqrt{A_e\cdot 10^{-6}}}\,\ln\!\left(\frac{2g\cdot 10^{-3}}{l_g\ [\mathrm{m}]}\right) \\
B_{max,real} &= \frac{L_{p,real}\, I_{p,max}}{N_p\, A_e\cdot 10^{-6}} \\
A_eA_w &= L_{p,real}\,\frac{I_{p,max}}{B_{max,real}}\,k_b\left(\frac{I_{p,rms}}{J_{max}} + \frac{I_{s1,rms}}{J_{max}\,\dfrac{N_p}{N_{s1}}}\right)""")

html += "<h3>Winding lengths:</h3>\n"
html += latex_wrap(r"""l_p &= N_p\, l_e \\
l_{s1} &= N_{s1}\, l_e \\
l_{s2} &= N_{s2}\, l_e \\
l_{aux} &= N_{aux}\, l_e""")

html += "<h2>6 — Wire Diameter (calc_wire_sections)</h2>\n"
html += latex_wrap(r"""\delta\ [\mathrm{cm}] &= \frac{6.62}{\sqrt{f_{sw}}} \\
\delta\ [\mathrm{mm}] &= 10\,\delta\ [\mathrm{cm}] \\
D_{AWG,max} &= 2\,\delta\ [\mathrm{mm}] \\
S_w &= \frac{\pi\, D_{AWG,max}^{2}}{4}""")

html += r"<h3>For every winding $x \in \{p, s1, s2\}$ (theoretical effective section):</h3>\n"
html += latex_wrap(r"""S_{x,eff} &= \frac{I_{x,rms}}{J_{max}} \\
D_x &= \sqrt{\frac{4\,S_{x,eff}}{\pi}} \\
n_{strands,x} &= \left\lceil \frac{S_{x,eff}}{S_w} \right\rceil""")

html += r"<h3>Actual cross-sections based on the selected diameter, for $x \in \{p, s1, s2, aux\}$:</h3>\n"
html += latex_wrap(r"""S_{x,eff} &= \pi\left(\frac{D_x}{2}\right)^{2} \\
n_{strands,x} &= \left\lceil \frac{S_{x,eff}}{S_w} \right\rceil""")

html += "<h2>7 — Checking the Filling of the Roll-Up Window (check_core_window_fit)</h2>\n"
html += latex_wrap(r"""A_{w,used} &= \left(N_p S_{p,eff} + N_{s1} S_{s1,eff} + N_{s2} S_{s2,eff} + N_{aux} S_{aux,eff}\right) k_b \\
\text{fits\_in\_core} &= \left(A_{w,used} \le A_w\right)""")

html += "<h2>8 — Core and Copper Losses (calc_pfe_losses)</h2>\n"
html += latex_wrap(r"""\delta_{20} &= 100\sqrt{\frac{\rho_{Cu,20}}{\pi\, f_{sw}\, \mu_0\, \mu_{r,nonmag}}} \\
\delta_{100} &= 100\sqrt{\frac{\rho_{Cu,100}}{\pi\, f_{sw}\, \mu_0\, \mu_{r,nonmag}}}""")

html += r"<h3>Diameter to skin depth ratio, for $x \in \{p, s1, s2, aux\}$:</h3>\n"
html += latex_wrap(r"""Q_x = \frac{D_x}{\delta_{100}}""")

html += r"<h3>DC and AC resistances (Dowell coefficients), for $x \in \{p, s1, s2, aux\}$:</h3>\n"
html += latex_wrap(r"""R_{dc,x} &= \frac{\rho_{Cu,100}\, MT_l\, N_x}{S_{x,eff}} \\
R_{ac,x} &= R_{dc,x}\, K_{ac,x}""")

html += r"<h3>Copper losses, for $x \in \{p, s1, s2, aux\}$:</h3>\n"
html += latex_wrap(r"""P_{Cu,x} &= R_{dc,x}\, I_{x,dc}^{2} + R_{ac,x}\, I_{x,ac}^{2} \\
P_{Cu,total} &= P_{Cu,p} + P_{Cu,s1} + P_{Cu,s2} + P_{Cu,aux}""")

html += "<h3>Core losses:</h3>\n"
html += latex_wrap(r"""\Delta B_{DCM} &= \frac{L_{p,real}\, I_{p,max}}{N_p\, A_e\cdot 10^{-6}} \\
\Delta B_{CCM} &= \frac{L_{p,real}\, I_{p,max}\, K_{rp}}{N_p\, A_e\cdot 10^{-6}} \\
B_{ac} &= \frac{\Delta B}{2} \\
P_{fe} &= k\, f_{sw}^{\alpha}\, B_{ac}^{\beta}\, V_e""")

html += """
</body>
</html>
"""

python_content = f'''"""
tabs/formula_ref_web.py — Formula Reference tab using WebEngine + MathJax.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView

FORMULA_HTML_WEB = r"""{html}"""

class FormulaRefTabWeb(QWidget):
    """Scrollable HTML reference of all design equations rendered with MathJax."""

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)

        self.browser = QWebEngineView()
        self.browser.setHtml(FORMULA_HTML_WEB)
        lay.addWidget(self.browser)
'''

with open(r"app\tabs\formula_ref_web.py", "w", encoding="utf-8") as f:
    f.write(python_content)

print("Created formula_ref_web.py")
