# P11 — Étude de marché à l'export avec Python — La Poule qui Chante

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![ACP](https://img.shields.io/badge/ACP-clustering-orange?style=flat-square)](#)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)

> Étude de marché internationale pour **La Poule qui Chante** (producteur français de poulet **bio**) : sur 127 pays et 17 indicateurs, réduction dimensionnelle (**ACP**) et **segmentation** (CAH + K-means) pour identifier, sans a priori géographique, les meilleurs marchés à l'export.

---

## 🎯 Contexte & besoin métier

L'entreprise vend son poulet bio uniquement en France ; le marché domestique arrive à maturité et la direction (Patrick, au COMEX) veut **explorer l'export**. Mission : **identifier des groupes de pays à cibler** de façon objective, en s'appuyant sur des données économiques, alimentaires, politiques et logistiques — pas sur l'intuition.

---

## 📦 Livrables

| Livrable | Fichier | Contenu |
|---|---|---|
| **Notebook 1 — Préparation & EDA** | `Dervout_Corentin_1_preparation_nettoyage_analyse_exploratoire_072026.ipynb` | Collecte multi-sources, harmonisation ISO3, feature engineering, contrôles, exploration |
| **Notebook 2 — ACP & clustering** | `Dervout_Corentin_2_clustering_visualisations_072026.ipynb` | Standardisation, ACP, CAH vs K-means, scoring, recommandations |
| **Présentation** | `Dervout_Corentin_3_presentation_072026.pptx` | Support COMEX (méthode accessible + recommandations) |

---

## 🗂️ Données & préparation

**Année de référence 2017** (meilleure couverture inter-sources, avant la rupture COVID, première année de l'indicateur d'inabordabilité d'une alimentation saine). Croisement de **plusieurs sources ouvertes** : FAO (bilans alimentaires, sécurité alimentaire, commerce, **usage des terres → surface bio**, **coût d'une alimentation saine**) et Banque Mondiale (**gouvernance WGI, PIB PPA, logistique/douanes LPI, croissance**).

Points de rigueur distinctifs :
- **Harmonisation des pays par code ISO3** (via `pycountry` + appariement flou `thefuzz`), retrait des agrégats régionaux ;
- **valeurs manquantes traitées au cas par cas** (imputer seulement si justifiable — ex. PIB Chine depuis l'agrégat, surface bio non déclarée → 0 — sinon retirer le pays) ;
- **7 variables métier calculées**, dont un **taux de dépendance aux imports** défini comme imports ÷ *disponibilité intérieure* (rapport borné, dimensionnellement cohérent) ;
- **exclusion de la France** (pays hôte : on ne se cible pas soi-même) ;
- **contrôle automatisé des contraintes** → **127 pays complets, 17 variables, 0 valeur manquante, 94,2 % de la population mondiale couverte** ;
- **outliers conservés** (Chine, Inde, marchés ultra-premium… information business réelle, pas des erreurs).

---

## 🔬 Démarche analytique

### 1. ACP (sur données standardisées)
Centrage-réduction (Z-score) indispensable avant l'ACP pour éviter que la population ou la taille du marché n'écrasent les autres variables. **Critère de Kaiser + coude de l'éboulis → 5 composantes retenues (72,1 % de variance)** :
- **PC1 (~31 %)** — richesse / développement (PIB, gouvernance, efficacité douanière, urbanisation ; négativement l'inabordabilité alimentaire) ;
- **PC2 (~15 %)** — taille et dépendance du marché aux imports.

### 2. Clustering — dans l'espace ACP, deux méthodes confrontées
Le regroupement est fait **sur les coordonnées ACP** (décorrélées, débruitées) et non sur les données brutes. **CAH (Ward)** et **K-means** sont comparés via l'**Adjusted Rand Index (ARI = 0,653)** — accord fort sur le cœur des groupes. Le choix de **k = 5** est un compromis assumé : la silhouette favorise k = 2 (riches vs pauvres), trop grossier pour cibler ; **5 familles offrent la granularité utile au business**.

### 3. Scoring des cibles
Le clustering dit *où* sont les opportunités ; un **score composite pondéré** classe ensuite les pays premium selon les priorités d'un producteur bio haut de gamme, avec un **garde-fou de matérialité** (marché < 10 Md$ écarté) :

| Critère | Poids |
|---|---|
| PIB/habitant (pouvoir d'achat premium) | 30 % |
| Dépendance aux imports | 25 % |
| Prix moyen à l'import (positionnement premium) | 20 % |
| Maturité bio (part de l'agriculture bio) | 15 % |
| Efficacité douanière (LPI) | 10 % |

---

## 📊 Résultats — 5 familles de pays

| Famille | Nb | PIB/hab | Dépendance import | Exemples | Cible ? |
|---|---|---|---|---|---|
| **Hubs ultra-premium** | 7 | ~75 700 $ | très forte | Belgique, Pays-Bas, Luxembourg, Irlande, UAE, Malte, Danemark | ✅ **prioritaire** |
| **Développés premium** | 28 | ~47 800 $ | modérée | Autriche, Suisse, Allemagne, Suède, Norvège | ✅ **cœur de cible** |
| Intermédiaires autosuffisants | 41 | — | faible | gros consommateurs mais peu importateurs | ❌ |
| Géants | 3 | ~48 200 $ | quasi nulle | Chine, Inde, États-Unis | ❌ hors périmètre |
| Pauvres | 48 | ~7 000 $ | — | pouvoir d'achat insuffisant pour un premium | ❌ |

**Palmarès (score composite) :** 🥇 **Luxembourg (0,59)** · 🥈 **Pays-Bas (0,54)** · 🥉 **Belgique (0,52)** · Autriche (0,49)…

---

## 💡 Recommandation au COMEX

**La recommandation robuste n'est pas *un* pays, mais *deux familles* :**
- les **hubs ultra-premium** (Belgique, Pays-Bas, Luxembourg, Irlande, UAE…) — petits mais très riches et très importateurs, marché premium déjà installé ;
- les **marchés développés premium** (Autriche, Suisse, Allemagne, Suède…) — le cœur de cible, plus large.

*Nuance honnête assumée* : plusieurs hubs (Belgique, Pays-Bas, Luxembourg) sont d'abord des **plateformes de réexport** — leur très forte dépendance aux imports ne reflète pas seulement une consommation finale, ce qu'une prospection terrain devra affiner.

---

## ⚠️ Limites & prochaines pistes

- Données figées sur **2017** — à actualiser.
- Pas de prise en compte des **barrières tarifaires/sanitaires** ni des **coûts logistiques réels** (distance) à l'export.
- Les **hubs de réexport** demandent une validation de la demande finale.
- Chine, Inde et États-Unis justifieraient une **étude dédiée** hors périmètre d'un premier export.

---

## 🧰 Compétences & outils

`Python` · `Pandas` · `scikit-learn` · `Matplotlib` · `Seaborn` — Consolidation multi-sources et harmonisation ISO3 (appariement flou) · Feature engineering métier · Statistiques multivariées (**ACP**) · **Clustering** (CAH + K-means dans l'espace ACP, comparaison par ARI) · Scoring composite pondéré et garde-fou de matérialité · Esprit critique (outliers, réexport) · Restitution stratégique au COMEX.

---

## 📁 Structure du dossier

```
P11 - Étude de marché export (La Poule qui Chante)/
├── Dervout_Corentin_1_preparation_nettoyage_analyse_exploratoire_072026.ipynb  # collecte, nettoyage, EDA
├── Dervout_Corentin_2_clustering_visualisations_072026.ipynb                    # ACP, clustering, scoring
└── Dervout_Corentin_3_presentation_072026.pptx                                 # support COMEX
```

---

*Projet réalisé dans le cadre du parcours Data Analyst d'OpenClassrooms (titre RNCP niveau 6). Données publiques FAO / Banque Mondiale (2017).*
