"""
Textes des info-bulles ('?'), regroupes par cle logique.

Garder ce dictionnaire separe de la vue permet d'y injecter, au fil des
prochains livrables, des extraits reformules de la documentation technique
de l'utilisateur sans toucher au code des widgets.
"""

TECH_NOTES: dict[str, str] = {
    "vac_range": (
        "Plage de tension secteur universelle (85-528 Vac). Couvre le 110 Vac "
        "et le 400/480 Vac triphase redresse, frequent en environnement "
        "industriel. C'est cette plage large qui contraint la plupart des "
        "choix de conception en aval (Dmax, StackFET, snubber...)."
    ),
    "eta": (
        "Rendement estime de bout en bout. Sert uniquement a dimensionner Pin "
        "a partir de Pout ; il sera affine une fois les pertes calculees a "
        "l'etape 9. Une valeur optimiste ici sous-dimensionne le condensateur "
        "de bulk et le transformateur."
    ),
    "delta_vc_in": (
        "Ondulation basse frequence admise sur le bus DC, exprimee en % de "
        "Vin,min. Elle fixe l'hypothese de depart Vbulk,min,0 = Vin,min x "
        "(1 - ondulation) avant que la boucle de convergence ne l'affine."
    ),
    "nh": (
        "Nombre de demi-alternances secteur perdues a couvrir (tenue au "
        "hold-up). Nh = 1 couvre une coupure de secteur d'une demi-periode ; "
        "augmenter Nh alourdit directement le condensateur de bulk requis."
    ),
    "bulk_cap_method": (
        "Le condensateur de bulk est dimensionne par iterations successives : "
        "on estime Vbulk,min, on en deduit le temps de conduction du pont "
        "puis le temps de maintien (hold-up), ce qui donne un Cbulk ; on "
        "reinjecte ce Cbulk pour recalculer Vbulk,min, et ainsi de suite "
        "jusqu'a stabilisation. Le classeur Excel d'origine s'arrete a deux "
        "passes manuelles ; cette application boucle jusqu'a convergence."
    ),
}
