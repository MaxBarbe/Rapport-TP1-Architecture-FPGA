# Rapport TP1 Architecture multicores

**Maxime Barbe — Master 2 ESTel — Université Côte d'Azur**

Étude des opérateurs arithmétiques, du filtre vidéo et de la consommation d'une plateforme DE10-Nano.

- **[Lire le rapport PDF](pdf/Rapport_TP1_Maxime_Barbe.pdf)**
- **[Télécharger le projet LaTeX pour Overleaf](Rapport_TP1_Overleaf.zip)**
- [Source principale](main.tex), [images du rapport](images), [photos originales](photos), [données CSV](donnees).

## Contenu

Le rapport présente les estimations d'addition et de multiplication, l'architecture d'un filtre 3 × 3, les ressources FPGA et les observations sur carte. L'analyse du parallélisme, la comparaison DSP/éléments logiques et les calculs de débit du filtre distinguent explicitement les résultats disponibles des relations théoriques. Il ne revendique pas d'essais absents des archives.

Le courant retenu pour la plateforme est d'environ **0,6 A**, validé par l'enseignante. Sous 5 V, cela correspond à environ **3 W** et **50 mJ par trame** au débit nominal de 59,52 images/s. Les relevés du testeur montrent des niveaux haut et bas, sans isoler la consommation du filtre.

## Compiler le LaTeX

Importer le ZIP dans Overleaf en choisissant `main.tex`, ou depuis la racine :

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Autre possibilité : `tectonic main.tex`. Le PDF publié comporte **15 pages**, a été compilé avec Tectonic et vérifié visuellement.

## Reproduire les calculs

Python 3, sans dépendance supplémentaire :

```sh
python3 scripts/calculs.py
python3 scripts/calculs.py --check
```

La première commande produit les tableaux calculés ; la seconde vérifie qu'ils correspondent aux données versionnées. Le script ne relance pas Quartus et ne simule pas une activité absente.

## Traçabilité

Les fichiers CSV et leur [notice](donnees/README.md) précisent la provenance et le statut de chaque série. Les données historiques n'ont pas été remplacées par les calculs théoriques. Le code et les projets FPGA sont dans [le dépôt technique du TP](https://github.com/MaxBarbe/TP1-DE10-Nano-HDMI).

Une intelligence artificielle a été utilisée comme aide à la rédaction et à la reformulation du rapport, comme indiqué en conclusion.
