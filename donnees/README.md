# Données et statut des résultats

- `addition_entiere.csv`, `addition_flottante.csv`, `multiplication.csv` : valeurs reprises du rapport original fourni par Maxime, cohérentes avec les tableaux du rapport précédent. Estimations Quartus Vectorless ; les rapports individuels de toutes les variantes ne sont pas disponibles. Les fréquences absentes restent vides.
- `filtre_quartus.csv` : synthèse de l'archive TP1_EXO2 du 29 septembre 2026 ; Power Analyzer, confiance Low, sans activité de simulation, interfaces non entièrement contraintes. La fréquence est demandée, pas un débit validé.
- `mesures_brutes.csv` : quatre instantanés photographiés du testeur UM25C. Les étiquettes `sw0` d'origine sont conservées pour la traçabilité. L'interprétation retenue dans le rapport est celle des niveaux haut et bas autour du courant d'environ 0,6 A validé par l'enseignante. Aucune énergie propre au filtre n'est déduite de leur différence.
- `energies_operateurs.csv` et `synthese_calculs.json` : produits par le script de calcul. Les énergies par opération supposent un résultat valide par cycle en régime établi.
- `debits_filtre.csv` : fréquences utiles minimales théoriques, sans suppression vidéo, pour une IP à un pixel par cycle.

Le courant arrondi de référence donne environ 3 W sous 5 V, puis 50,4 mJ par trame par calcul nominal, présenté comme **environ 50 mJ** dans la conclusion. La valeur conditionnelle de 0,5043 mJ/image du filtre isolé suppose 100 MHz réellement atteints et une activité conforme à l'estimation ; ce n'est pas une mesure.

Les valeurs brutes n'ont pas été ajustées pour obtenir une conclusion. Aucune mesure de parallélisme ni d'implantation sans DSP n'est ajoutée artificiellement.
