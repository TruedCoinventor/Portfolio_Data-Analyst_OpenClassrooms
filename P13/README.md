# P13 — Projet data augmenté par l'IA — Segmentation du catalogue BottleNeck

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Clustering](https://img.shields.io/badge/ML-clustering%20non%20supervisé-orange?style=flat-square)](#)
[![IA](https://img.shields.io/badge/démarche-augmentée%20par%20l'IA-8A2BE2?style=flat-square)](#)

> Reprise du livrable **P6** (analyse descriptive du caviste **BottleNeck**) pour le faire passer d'un **constat univarié** à une **segmentation multivariée automatisée** par machine learning non supervisé — conduite comme un vrai projet outillé (cahier des charges, veille, arbitrages, gestion des risques) et **augmenté par un usage critique de l'IA**.

> 🔗 **Suite directe du [P6](../P6%20-%20Optimisation%20données%20boutique%20(BottleNeck)/)** : le P6 nettoie et fusionne les données (ERP / web / liaison) ; le P13 repart de son export consolidé `df_merge_bottleneck.xlsx` pour la modélisation.

---

## 🎯 Contexte & besoin métier

Le P6 répondait à un besoin de **constat** (prix, CA, stock, marge, variable par variable) mais ne disait pas *comment regrouper les produits* pour piloter le catalogue. Problématique reformulée :

> *« Peut-on regrouper automatiquement les produits en familles cohérentes — selon leur positionnement prix, leur volume de ventes et leur rotation de stock — pour orienter les décisions d'assortiment, de pricing et de gestion de stock ? »*

L'idée : laisser l'algorithme **révéler des familles de comportements** (que l'analyste interprète et nomme), chacune appelant une stratégie différenciée — sécuriser, piloter par le stock, déstocker.

---

## 📦 Livrables

| Livrable | Fichier | Contenu |
|---|---|---|
| **Notebook** | `Dervout_Corentin_1_projet_ameliore_082026.ipynb` | Préparation, feature engineering, comparaison de variantes, clustering, restitution |
| **Documentation** | `Dervout_Corentin_2_documentation_082026.md` | Cahier des charges, veille sourcée, démarche, gestion de projet, usage de l'IA |

---

## 🗂️ Données & périmètre

Source : **export consolidé du P6** (825 produits). Avant tout ML, les **régimes particuliers sont isolés par règle métier explicite** — un produit jamais vendu ou absent du site n'est pas « un produit qui vend peu », c'est un **état qualitatif distinct** :

| Règle | Volume |
|---|---|
| Hors site web (`total_sales` manquant) | 111 |
| Invendus (`total_sales == 0`) | 25 |
| **→ Cœur de catalogue (base du clustering)** | **689** |
| *Contrôle* | 111 + 25 + 689 = **825** ✅ |

*Périmètre exclu (assumé)* : pas de forecasting (snapshot d'octobre, aucune série temporelle), pas d'axe ancienneté (`post_date` absente de l'export).

---

## 🔭 Veille (extrait)

La veille, sourcée (doc. scikit-learn, Pandera…), compare les options sur chaque axe :

| Axe | Retenu | Comparé / écarté |
|---|---|---|
| Méthode de clustering | **KMeans** (meilleure silhouette) | Agglomératif/Ward (témoin de robustesse) · DBSCAN (écarté : paramétrage inadapté au faible volume) |
| Choix du nombre de clusters | **Silhouette + coude** (convergents) | — |
| Qualité de données (industrialisation future) | **Pandera** (léger, type-safe) | Great Expectations (écarté : sur-ingénierie pour un notebook) |

---

## 🔬 Démarche ML

### Choix des variables — avec prévention du *data leakage*
Axes retenus : **`price`** (positionnement), **`total_sales`** (volume), **`stock_mois`** (rotation = `stock_quantity / total_sales`).
- **`ca` exclu des features** : colinéaire (= `total_sales × price`), il ferait *fuiter* l'information des axes prix/ventes — conservé en lecture seule pour chiffrer le poids des segments.
- **`taux_marge` écarté des axes** : quasi-plat (75 % des produits entre 56,6 % et 66,3 %) → non discriminant, n'ajouterait que du bruit ; conservé pour qualifier les segments.

### Pré-traitement justifié par les distributions
`log1p` sur les variables à forte asymétrie à droite (`stock_mois` asym. 4,9, `price` 2,6…) pour éviter que les longues traînes n'écrasent les distances euclidiennes, puis `StandardScaler` (KMeans raisonne en distances).

### Comparaison de deux variantes → arbitrage multi-critères
| | Variante A (2 axes) | **Variante B (3 axes)** |
|---|---|---|
| Variables | prix, ventes | prix, ventes, **rotation de stock** |
| Meilleure silhouette (k=3) | 0,408 | **0,481** |
| Accord KMeans/Ward (ARI) | — | **0,788** |
| Apport | 3 paliers de prix | **révèle le stock dormant** |

**Décision : variante B, k = 3** (silhouette et coude convergents ; KMeans retenu, Ward gardé comme témoin — ARI 0,79 : les deux algorithmes voient la même structure). *L'ajout de la rotation de stock est l'apport central : il ne coûte rien et rend le modèle à la fois plus net et plus actionnable.*

---

## 📊 Résultats — 3 segments métier (+ invendus isolés)

| Segment | Volume | Profil (médianes) | Part du CA | Action |
|---|---|---|---|---|
| **Moteur de CA** | 413 | prix 16 € · stock 2,8 mois · marge 61 % | **48,5 %** | Socle à sécuriser (disponibilité) |
| **Premium** | 244 | prix 46 € · stock 1,6 mois · marge 61 % | **43,2 %** | Piloter par le stock, pas par le volume |
| **Stock dormant** | 32 | prix 61 € · **stock 16,5 mois** · marge 40 % | 8,3 % | Déstockage prioritaire (capital immobilisé) |
| *Invendus (isolés)* | 25 | `total_sales = 0` | — | Décision produit par produit |

**L'apport du ML.** Une segmentation intuitive sur le seul couple prix/ventes retrouve les segments évidents mais **masque le stock dormant** : ce sont ces **32 produits chers, peu rentables et stockés > 1 an** que la rotation de stock fait émerger. Le segment est **validé comme réel** (dispersion homogène : Q1 à 12 mois, médiane 16,5) et non un artefact d'outliers. Le ML apporte une frontière **reproductible, multivariée et scalable** là où l'analyse manuelle reste subjective.

---

## 🤖 Usage de l'IA dans la démarche

Un assistant IA a été mobilisé comme **outil de travail critique**, non comme source de réponses : brainstorming d'axes, aide au code (pipeline scikit-learn), et **relecture méthodologique** (détection de pièges). Chaque suggestion a été **validée ou redressée** — plusieurs explicitement **écartées** : piste d'ancienneté (colonne absente), variante à 4 axes intégrant la marge (silhouette dégradée à 0,393), inclusion de `ca` (data leakage). Les décisions finales relèvent d'un **jugement métier et statistique assumé par l'auteur**.

---

## 🗂️ Conduite de projet

Le projet est piloté comme un vrai projet data : **découpage en 7 lots**, **backlog priorisé** (user stories, charges, *definition of done*), **kanban**, **planning jalonné (Gantt)** et **registre des risques** — dont les principaux (*fuite de données*, *biais de distances sur données asymétriques*, *silhouette modeste*, *non-reproductibilité*) sont tracés avec leur parade. Une **mini-formation métier** (session 30 min + fiche 1 page + CSV segmenté) accompagne la restitution pour rendre les équipes autonomes sur la lecture des segments.

---

## ⚠️ Limites & prochaines pistes

- **Silhouette modeste (~0,48)** : le catalogue est un *continuum* plus qu'un ensemble de paquets nets → segments statistiquement modestes mais **métier-pertinents** (assumé).
- **Faible volume (689 produits)** : POC exploratoire, non déployable en l'état.
- **Snapshot sans dimension temporelle** : ni dynamique de ventes, ni ancienneté.
- **Industrialisation (backlog)** : validation automatisée via **Pandera** et recalcul périodique.

---

## 🧰 Compétences & outils

`Python` · `Pandas` · `scikit-learn` · `Matplotlib` — Cadrage (reformulation métier, critères d'acceptation) · **Veille technologique sourcée** · Feature engineering et **prévention du data leakage** · Clustering non supervisé (KMeans, Ward, silhouette/coude, ARI) · **Arbitrage multi-critères** de variantes · Reproductibilité (garde-fous `assert`, graine fixée) · **Usage critique et documenté de l'IA** · Gestion de projet (lots, backlog, risques, Gantt) · Restitution et **mini-formation métier**.

---

## 📁 Structure du dossier

```
P13 - Projet augmenté par l'IA (BottleNeck)/
├── Dervout_Corentin_1_projet_ameliore_082026.ipynb   # segmentation ML (notebook)
└── Dervout_Corentin_2_documentation_082026.md         # démarche, veille, gestion de projet, IA
```

---

*Projet réalisé dans le cadre du parcours Data Analyst d'OpenClassrooms (titre RNCP niveau 6). Volet technique du P13 (amélioration du P6). Données fictives fournies dans le cadre de la formation.*
