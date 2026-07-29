# Flyback Designer

Application desktop (CustomTkinter) destinee a remplacer le classeur Excel
de dimensionnement d'alimentations Flyback. Ce premier livrable couvre
l'architecture generale du projet et les etapes 1-2 (Specifications
d'entree + Etage d'entree / condensateur de bulk).

## Lancer l'application

```bash
pip install -r requirements.txt
python main.py
```

## Architecture (MVC)

```
flyback_designer/
├── main.py                          # point d'entree
├── app/
│   ├── models/
│   │   ├── design_state.py          # dataclasses d'etat (M) : InputSpecs,
│   │   │                            #   InputStageResults, DesignChoices, DesignState
│   │   └── calc_engine.py           # fonctions de calcul PURES, sans UI
│   ├── views/
│   │   ├── main_window.py           # fenetre principale + navigation par etapes
│   │   ├── stage1_input_specs.py    # vue Etape 1 & 2
│   │   └── widgets/
│   │       ├── labeled_field.py     # champ "label + saisie + unite + (?)"
│   │       └── tooltip.py           # bouton d'aide contextuelle
│   ├── controllers/
│   │   └── app_controller.py        # relie vue <-> modele/calc_engine (C)
│   └── docs/
│       └── technical_notes.py       # textes des info-bulles techniques
```

**Flux de donnees** : la vue lit les champs -> `AppController` construit un
`dict` de valeurs brutes -> `CalcEngine` (fonctions pures) fait tous les
calculs -> le resultat (dataclass) remonte au controleur -> la vue l'affiche.
Aucune formule n'est ecrite dans les widgets ; cela permet de reutiliser
`calc_engine.py` tel quel plus tard pour l'export de netlist LTSpice/PSpice
ou pour des tests unitaires, sans toucher a l'interface.

## Correspondance avec le classeur Excel

Chaque fonction de `calc_engine.py` porte en commentaire la cellule Excel
d'origine (feuille "Design DCM"). Point d'attention decouvert pendant
l'implementation : les formules de dimensionnement du condensateur de bulk
(B31, B33, B34, B37) utilisent **Pout,Sigma (B18)**, pas **Pin (B19)** — le
facteur de rendement `eta` (F3/100) est deja au denominateur de chacune de
ces formules. Utiliser Pin y aurait introduit un double comptage du
rendement ; ce point a ete verifie en reproduisant numeriquement les
valeurs du classeur (Pout1=7 W, eta=85 %, Vac=85-528 V, delta_Vc(in)=25 %,
Nh=1) :

| Grandeur | Classeur Excel | App (converge) |
|---|---|---|
| Vin,min | 120.208153 V | 120.208153 V |
| Vin,max | 746.704761 V | 746.704761 V |
| Vbulk,min | 90.156115 V | 90.156115 V |
| Cbulk (apres 2 iterations manuelles) | 72.211073 µF | 72.211073 µF |

L'application boucle au-dela des deux passes manuelles du classeur jusqu'a
convergence de Cbulk (< 1e-4 µF), ou 8 iterations maximum.

## Prochaines etapes (non couvertes par ce livrable)

- Etape 3 : choix de Dmax / f_sw / Krp (dataclass `DesignChoices` deja posee)
- Etape 4 : selection de topologie (VIPER/TinySwitch integre, discret, StackFET)
- Etape 5 : base de donnees interne controleurs/transformateurs (feuilles
  `Configs_Transfo-Controleur` et `Devices Selection` du classeur, deja
  analysees pour la correspondance des colonnes VIPER26HD / VIPER25LDTR /
  VIPER35HDTR / TNY287DG-TL / AP3981D2-13)
- Etape 6 : magnetiques (Bmax, J, Ku, AeAw) — formules identifiees en
  colonnes J/N/R de "Design DCM"
- Etape 7 : snubber RCD / R2CD / TVS — feuille "Design Snubber" et
  "Snubber_NOC119" deja cartographiees (Rsn, Csn, Vrwm, Vc, Ptvs...)
- Etape 8-10 : sortie, pertes/thermique, routage
- Generation de netlist LTSpice/PSpice a partir de `DesignState`
