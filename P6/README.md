# P6 — Optimisation de la gestion des données d'une boutique — BottleNeck

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org)

> Consolidation et fiabilisation des données d'un caviste en ligne (**BottleNeck**, vins & spiritueux) à partir de trois systèmes hétérogènes — ERP, site web, table de liaison — puis analyse du catalogue, des ventes, des stocks et des marges.

---

## 🎯 Contexte & besoin métier

BottleNeck vend en ligne mais gère ses données dans des systèmes séparés : un **ERP** (prix, stock) et un **site web** e-commerce (ventes), reliés par une **table de liaison** manuelle. Objectif : réconcilier ces sources en un référentiel fiable, corriger les anomalies de saisie, et produire un **reporting exploitable** (chiffre d'affaires, marges, rotation des stocks) pour la direction.

> 🔗 Ce projet constitue la **base reprise et augmentée au P13** (segmentation ML du catalogue avec un usage encadré de l'IA) — les deux se lisent bien en miroir.

---

## 📦 Livrables

| Livrable | Fichier | Contenu |
|---|---|---|
| **Notebook** | `Dervout_Corentin_1_notebook_042026.ipynb` | EDA, nettoyage, fusion, analyses (prix, CA, stocks, marge, corrélations) |
| **Présentation** | `Dervout_Corentin_2_presentation_042026.pptx` | Synthèse de la démarche, résultats et plan d'action |

Le notebook exporte également le dataset consolidé (`df_merge_bottleneck.xlsx`) pour partage avec les équipes métier.

---

## 🗂️ Données

| Source | Volume | Contenu |
|---|---|---|
| `erp.xlsx` | 825 lignes × 6 col. | Prix, prix d'achat, stock, statut de stock |
| `web.xlsx` | 1 513 lignes × 29 col. | SKU, ventes, type de produit (données CMS) |
| `liaison.xlsx` | 825 lignes × 2 col. | Correspondance `product_id` ↔ `id_web` |

---

## 🔍 Démarche

### 1. Exploration & contrôle qualité
Audit systématique de chaque fichier (dimensions, types, valeurs manquantes, doublons) **avant toute correction**. Anomalies détectées et traitées :

- **3 prix négatifs** (‑20 €, ‑8 €, ‑9,1 €) ramenés en valeur absolue, avec recommandation d'un contrôle de saisie côté ERP ;
- **2 stocks négatifs** remis à zéro et `stock_status` recalculé depuis la quantité réelle (**4 incohérences** corrigées au total) ;
- **1 prix aberrant** repéré par comparaison : Champagne Egly-Ouriet à **12,65 €** au lieu de ~77 € — erreur de saisie confirmée ;
- côté web, **24 des 29 colonnes** supprimées (vides ou hors périmètre), 83 lignes vides et 2 produits sans SKU retirés → **714 produits** exploitables.

### 2. Fusion en deux temps
`ERP × Liaison` sur `product_id`, puis jointure avec `Web` sur `id_web = sku` (*left join*). Décomposition rigoureuse des non-correspondances : **111 articles sans données web = 91 produits jamais vendus en ligne + 20 « orphelins »** (présents dans la liaison mais absents du site — retrait ou erreur de référencement), dont **2 avec stock actif** = capital immobilisé non exploité.

### 3. Analyse univariée des prix & outliers
Prix moyen **32,28 €** (médiane 24,3 € ; max 225 €). Double détection d'outliers : **Z-score > 3** (17 articles, seuil 112 €) et **IQR ×1,5** (36 articles, soit **4,4 %**, seuil 83 €). Ces outliers sont **justifiés** : Cognac (~97 €), Champagne (~70 €) et Whisky (~66 €) sont structurellement plus chers que le Vin (~29 €), catégorie trop hétérogène pour un IQR global.

### 4. Analyses métier (CA, ventes, stocks, marge, corrélations)
Construction des indicateurs et lecture croisée (voir résultats).

---

## 📊 Résultats

| Indicateur | Résultat |
|---|---|
| Chiffre d'affaires (web) | **143 680 €** |
| Concentration du CA (Pareto) | **63 % des articles** font 80 % du CA → catalogue résilient |
| Quantités vendues | 5 751 bouteilles |
| Stock total | 17 822 bouteilles, **532 119 €** (prix de vente) / **298 628 €** (prix d'achat) |
| Taux de marge par catégorie | Cognac/Whisky ~82 % · Vin 61 % · **Champagne 35 %** |
| Corrélation prix ↔ ventes | **‑0,52** (négative modérée : les articles chers se vendent moins) |
| Corrélation stock ↔ ventes | **+0,44** (positive modérée : les best-sellers sont plus stockés) |
| Marges négatives | 4 articles, dont l'erreur Egly-Ouriet confirmée |

**Lecture transversale — le point de vigilance : le Champagne.** Le catalogue est sain dans l'ensemble (aucune dépendance à quelques références : il en faut 63 % pour faire 80 % du CA). Le vrai sujet est le **stock** : plus d'un demi-million d'euros immobilisés, et une catégorie qui cumule les trois signaux d'alerte — **stock élevé, marge la plus faible (35 %) et rotation atteignant 31 mois** : le Champagne. La corrélation prix/ventes de ‑0,52 confirme par ailleurs que toute hausse de prix se paie en volume.

---

## 💡 Plan d'action proposé

- **Fiabiliser l'ERP à la source** : contrôles de saisie (prix > 0, stock ≥ 0, cohérence `stock_status`).
- **Nettoyer la liaison** : corriger les 20 `id_web` orphelins et **remettre en vente les 2 produits à stock actif** non achetables en ligne.
- **Revoir l'approvisionnement du Champagne** (rotation jusqu'à 31 mois, marge à 35 %).
- **Unifier les référentiels produits** pour supprimer la table de liaison et automatiser le reporting via un outil de data visualisation.

---

## ⚠️ Limites & prochaines pistes

- La difficulté centrale du projet est de **distinguer les vraies erreurs des valeurs légitimement atypiques** (outliers de prix) — d'où l'importance des allers-retours métier.
- Les produits orphelins ne sont pas récupérables avec les seules données fournies : une **remontée métier** est nécessaire.
- Suite naturelle : **automatiser les contrôles qualité** (cf. P13) et bâtir une **dataviz interactive**.

---

## 🧰 Compétences & outils

`Python` · `Pandas` · `NumPy` · `Plotly` · `Seaborn` · `Jupyter` — Audit et nettoyage multi-sources · Jointures et gestion des non-correspondances · Détection d'outliers (Z-score, IQR) · Indicateurs métier (CA, Pareto, marge, valorisation et rotation de stock) · Analyse de corrélations · Restitution et recommandations opérationnelles.

*RGPD : les données manipulées (produits, prix, stocks) ne contiennent aucune donnée personnelle.*

---

## 📁 Structure du dossier

```
P6 - Optimisation données boutique (BottleNeck)/
├── Dervout_Corentin_1_notebook_042026.ipynb     # analyse complète (exécutée)
└── Dervout_Corentin_2_presentation_042026.pptx  # support de présentation
```

---

*Projet réalisé dans le cadre du parcours Data Analyst d'OpenClassrooms (titre RNCP niveau 6). Données fictives fournies dans le cadre de la formation.*
