# P12 — Détection automatique de faux billets — ONCFM

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Pipeline](https://img.shields.io/badge/pipeline-production%20(.pkl)-2ea44f?style=flat-square)](#)

> Modèle de classification supervisée pour l'**ONCFM** (Organisation nationale de lutte contre le faux-monnayage) : distinguer vrais et faux billets à partir de **6 mesures géométriques**, livré sous forme d'un **pipeline de production sérialisé** et d'un script en ligne de commande.

---

## 🎯 Contexte & besoin métier

Une machine relève six dimensions sur chaque billet ; les contrefaçons présentent de légers écarts géométriques. L'ONCFM veut un algorithme fiable et **utilisable en production**. Arbitrage métier central : **un faux billet non détecté (faux négatif) est bien plus grave qu'un vrai billet contrôlé à tort** — la stratégie vise donc à maximiser le rappel sur les faux, sans dégénérer.

---

## 📦 Livrables

| Livrable | Fichier | Contenu |
|---|---|---|
| **Notebook d'analyse** | `DERVOUT_Corentin_1_notebook_analyse_072026.ipynb` | EDA, imputation, modélisation, sélection, calibration, interprétation |
| **Script de production** | `DERVOUT_Corentin_2_script_app_072026.py` | Application CLI (fichier CSV ou saisie manuelle) |
| **Présentation** | `DERVOUT_Corentin_3_support_presentation_072026.pptx` | Support de soutenance |

*(Le pipeline sérialisé `pipeline_final.pkl` et le module `oncfm_model.py` — composants personnalisés — sont produits par le notebook et requis par le script.)*

---

## 🗂️ Données

**1 500 billets** (1 000 vrais / 500 faux, soit 66,7 % / 33,3 %), **6 variables** en mm : `diagonal`, `height_left`, `height_right`, `margin_low`, `margin_up`, `length`. Une seule variable présente **37 valeurs manquantes** (`margin_low`, 2,47 %).

---

## 🔍 Démarche

### 1. Contrôle qualité — vérifier plutôt que supposer
- **Doublons** : aucun.
- **Manquants — test du khi-deux d'indépendance** (χ² = 1,83 · **p = 0,176**) : l'absence de mesure est **indépendante de la nature du billet** → l'imputation n'introduira pas de biais de classe.
- **Aberrants** : aucune valeur physiquement absurde ; les billets « courts » sont conservés — *c'est précisément le signal d'une contrefaçon*.

### 2. Exploration — quantifier le pouvoir discriminant
Le **d de Cohen** (indépendant de l'équilibre des classes) hiérarchise les variables : **`length` (d = 3,41)** domine (les vrais sont ~1,57 mm plus longs), suivi de **`margin_low` (d = −2,66)** (marge inférieure plus large chez les faux). Une ACP 2D montre **deux nuages largement séparés** : le problème est intrinsèquement facile, les modèles seront donc très proches — l'enjeu se joue sur une **zone de recouvrement étroite**.

### 3. Imputation — choisie par la mesure, pas par habitude
Par masquage contrôlé sur le train et comparaison du **RMSE de reconstruction** : la **régression linéaire (`IterativeImputer`) l'emporte à 0,453 mm**, soit **‑29 % d'erreur vs la médiane** (0,635 mm). Constat éclairant : la RMSE de la moyenne (0,622) ≈ l'écart-type de `margin_low` (0,656) → **imputer par une constante revient quasiment au hasard**.

### 4. Modélisation — critère F‑bêta (β = 2)
Optimisation sur le **F‑bêta(2)** de la classe « faux » (le rappel pur est trivialement maximisable : tout classer « faux » donne un rappel de 1 mais un modèle inutile). GridSearchCV, 5 plis stratifiés. **Les trois modèles supervisés obtiennent exactement le même F‑bêta(2) = 0,983** (intervalles recouvrants) — aucun n'est mesurablement meilleur.

### 5. K-means — analysé, puis écarté pour une raison mesurée
Le cahier des charges demandait un k-means prédictif par centroïdes. La silhouette est maximale à **k = 2 (0,345)** : la séparation vrai/faux existe dans la seule géométrie (pureté 98,5 % par cluster). Mais le k-means est **écarté pour un défaut structurel quantifié** : en production, il ne produit que **2 valeurs de probabilité distinctes**, contre **1 047 pour la régression logistique** — or toute la stratégie repose sur le **réglage d'un seuil**, impossible avec des probabilités binaires.

### 6. Départage des modèles à égalité → régression logistique
Puisque les F‑bêta sont identiques, trois critères mesurables tranchent : **calibration (score de Brier)** — la régression logistique est la mieux calibrée (0,0084) car elle optimise la vraisemblance ; **granularité des probabilités** (la plus fine) ; et **interprétabilité** — indispensable pour un organisme public qui doit expliquer ses décisions. *(Un test de sélection de variables confirme par ailleurs de conserver les 6 mesures : les retirer dégrade systématiquement le score.)*

### 7. Calibration du seuil — stable, pas ajusté sur le bruit
Le seuil est calibré sur les **probabilités hors-échantillon** (validation croisée sur le train, test fermé). Vérification de stabilité sur **15 découpages différents** : optimum médian 0,810, avec un **large plateau (0,535–0,865)** où le F‑bêta varie de moins de 0,002. **Seuil retenu : 0,80** — valeur ronde au centre du plateau, robuste au découpage.

---

## 📊 Résultats finaux (jeu de test, ouvert une seule fois)

| Indicateur | Valeur |
|---|---|
| Faux billets interceptés | **100 / 100** (0 faux négatif) |
| Vrais billets rejetés à tort | 4 / 200 |
| **Rappel (faux)** | **1,00** · Précision (faux) 0,96 |
| Accuracy globale | 0,987 |

> **Honnêteté statistique.** Observer 0 échec sur 100 faux **ne prouve pas** un taux nul : cela garantit seulement, à 95 % de confiance, un taux d'échec réel inférieur à ~3 %. Le README l'assume plutôt que d'annoncer « 100 % ».

**Interprétation croisée.** Les coefficients de la régression logistique (`length` : rapport de cotes ≈ 40 ; `margin_low` : 0,073) sont **confirmés par l'importance par permutation** (méthode indépendante) : `length` puis `margin_low` dominent. Les erreurs se concentrent dans une **zone d'incertitude étroite (42 billets sur 300)** — d'où une piste opérationnelle : un **circuit à trois niveaux** (vrai automatique / faux automatique / vérification manuelle) plutôt qu'une sortie binaire.

---

## 🏗️ Pipeline de production (6 étapes)

`ColumnValidator` (contrôle des 6 colonnes, ignore les colonnes en trop comme `id`, réordonne, force le numérique) → contrôle d'intégrité → **imputation (régression linéaire)** → standardisation → **régression logistique** → **seuil de décision 0,80**. L'ensemble est sérialisé en un seul objet (`pipeline_final.pkl`) ; les classes personnalisées vivent dans `oncfm_model.py` (source unique, importée par le notebook et le script — sans quoi `joblib.load()` échoue).

### Utilisation du script

```bash
# Analyser un fichier de billets
python DERVOUT_Corentin_2_script_app_072026.py billets_production.csv

# Saisie manuelle d'un billet
python DERVOUT_Corentin_2_script_app_072026.py

# Options : --export resultats.csv | --details | --seuil 0.9
```

Le séparateur CSV est **détecté automatiquement**, les colonnes en trop conservées pour l'affichage, les **mesures manquantes reconstruites** par le modèle, et chaque verdict est assorti d'une **probabilité et d'un niveau de confiance**.

---

## ⚠️ Limites & prochaines pistes

- Le taux de faux négatifs **ne peut pas être prouvé nul** sur 100 faux (borne à ~3 %).
- Le modèle exploite des **dimensions géométriques** : des contrefaçons dimensionnellement parfaites échapperaient à cette approche.
- Piste identifiée : **circuit à trois niveaux** exploitant la zone d'incertitude pour cibler le contrôle humain.

---

## 🧰 Compétences & outils

`Python` · `scikit-learn` · `Pandas` · `SciPy` — Contrôle qualité statistique (test d'indépendance des manquants, d de Cohen) · Benchmark objectif d'imputation · Modélisation supervisée et sélection par F‑bêta, **calibration (Brier)** et interprétabilité · Analyse non supervisée (k-means) et argumentaire de rejet · Calibration robuste du seuil de décision · **Pipeline de production sérialisé** et application CLI · Prévention du *data leakage* (fit sur train uniquement).

---

## 📁 Structure du dossier

```
P12 - Détection de faux billets (ONCFM)/
├── DERVOUT_Corentin_1_notebook_analyse_072026.ipynb   # analyse complète
├── DERVOUT_Corentin_2_script_app_072026.py            # application de production (CLI)
└── DERVOUT_Corentin_3_support_presentation_072026.pptx # support de soutenance
```

---

*Projet réalisé dans le cadre du parcours Data Analyst d'OpenClassrooms (titre RNCP niveau 6). Données fictives fournies dans le cadre de la formation.*
