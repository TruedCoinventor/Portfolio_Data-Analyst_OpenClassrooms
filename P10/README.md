# P10 — Tableau de bord d'accès à l'eau potable — DWFA

[![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Power Query](https://img.shields.io/badge/Power%20Query%20(M)-100%25%20du%20prétraitement-217346?style=flat-square)](#)
[![DAX](https://img.shields.io/badge/DAX-modèle%20en%20étoile-F2C811?style=flat-square)](#)

> Tableau de bord Power BI d'aide à la décision pour **DWFA** (*Drinking Water For All*, ONG) : identifier et **prioriser les pays** à cibler selon trois domaines d'intervention, en croisant accès à l'eau, mortalité, démographie et stabilité politique (2000-2018).

---

## 🎯 Contexte & besoin métier

DWFA accompagne les pays pour améliorer l'accès à l'eau potable. Le tableau de bord doit **identifier les pays les plus en difficulté** et orienter les efforts selon les **trois domaines d'expertise** de l'ONG, du global au particulier (vues mondiale → continentale → nationale) :

| Domaine | Objectif | Critère de ciblage |
|---|---|---|
| **1 · Création de services** | Déployer de nouvelles infrastructures | Accès à l'eau le plus faible |
| **2 · Modernisation** | Améliorer la qualité des services existants | Bon accès de base, mais faible qualité |
| **3 · Consulting** | Accompagner les administrations publiques | Administration stable, politique perfectible |

---

## 📦 Livrables

| Livrable | Fichier | Contenu |
|---|---|---|
| **Tableau de bord** | `Dervout_Corentin_2_dashboard_072026.pbix` | Prétraitement (Power Query), modèle, mesures et 3 vues |
| **Présentation** | `Dervout_Corentin_1_présentation_072026.pptx` | Contexte, prétraitement, blueprint, choix d'outil, recommandations |

> Le `.pbix` n'est pas prévisualisable sur GitHub : il s'ouvre dans **Power BI Desktop** pour inspection complète (Power Query, modèle, mesures).

---

## 🗂️ Données

**5 fichiers CSV · 194 pays · période 2000-2018**, sources **OMS et FAO** : accès à l'eau potable (de base et *safely managed*), mortalité liée à l'eau insalubre (**2016 uniquement**), population rurale et urbaine, stabilité politique — chaque indicateur suivi année par année.

---

## 🔍 Démarche

### 1. Prétraitement — 100 % dans Power BI (Power Query / M)
Choix distinctif et assumé : **tout le nettoyage et les transformations sont réalisés dans Power Query, sans aucun outil externe** — le fichier `.pbix` est **autonome et reproductible** tel quel. Concrètement : **pivots** (les granularités passent en colonnes), **jointures des 5 fichiers**, typage et nettoyage, puis création de **champs calculés** — part de population sans accès (complément à 100 %), part urbaine, stabilité moyenne par pays, et un **indice d'efficacité de la politique publique** (indicateur composite). Gestion des cas particuliers : mortalité limitée à 2016, exclusion des territoires hors périmètre des 194 pays.

### 2. Modélisation — étoile à dimensions conformes
Deux **dimensions partagées** — un **Calendrier** (2000-2018) et une table **Région** (pays · continent) — filtrent l'ensemble des tables de faits (accès à l'eau, population, mortalité, stabilité politique, efficacité gouvernementale). Ce choix garantit la **cohérence des trois vues**, de meilleures performances, et **absorbe proprement les couvertures temporelles différentes** (la mortalité n'existe que pour 2016, sans créer d'incohérence).

### 3. Blueprint — cadrage avant construction
Un **blueprint** formalise, pour chacune des trois vues, la chaîne **besoin utilisateur → indicateurs → visualisation retenue** : **12 besoins** couvrant les trois domaines, garantissant que chaque graphique répond à une exigence précise.

### 4. Choix de l'outil justifié
**Power BI retenu plutôt que Tableau** : compétence déjà acquise (opérationnel immédiatement, livraison plus rapide et moins risquée), Power Query pour tout le prétraitement, modélisation en étoile et mesures DAX, Desktop gratuit. Tableau écarté (temps d'apprentissage pour un résultat équivalent).

---

## 📄 Les 3 vues

Filtres communs (continent, pays, année, **curseur de stabilité politique**) et navigateur de pages :

| Vue | Contenu |
|---|---|
| **Monde** | Cartes KPI (accès à l'eau, mortalité /100k, population) · carte choroplèthe · niveau de service par continent (barres 100 %) · évolution de l'accès 2000-2017 · accès basique rural vs urbain |
| **Continent** | Carte + trois nuages de points : **opportunités de création d'infrastructures** (Domaine 1), **opportunités de consulting** (Domaine 3), **accès basique vs qualité** (Domaine 2) |
| **Pays** | Diagnostic complet : évolution de l'accès et de la population, **donuts niveau de service** (global / urbain / rural : sans accès · basique · *safely managed*) |

---

## 🎯 Résultats — les pays à cibler par domaine

Sortie directement actionnable de l'analyse :

- **Domaine 1 — Création** (accès le plus faible) : **Tchad 39 %**, Soudan du Sud 41 %, Éthiopie 41 %, RD Congo 43 %, Niger 50 %.
- **Domaine 2 — Modernisation** (bon accès de base / faible qualité) : **Laos 82/16 %**, Népal 89/27 %, Bhoutan 97/36 %, Mongolie 83/24 %, Mexique 99/43 %.
- **Domaine 3 — Consulting** (administration stable, politique perfectible) : **Bénin, Zambie, Lesotho, Mozambique, Malawi**.

*Listes indicatives issues des données 2016-2017, à affiner avec les équipes terrain.*

---

## ⚠️ Limites & prochaines pistes

- **Mortalité WASH disponible pour 2016 seulement** : pas de suivi temporel sur cet indicateur (absorbé par le modèle).
- L'accès *safely managed* comporte de nombreuses **valeurs manquantes** selon la granularité.
- L'**indice d'efficacité** est un composite construit pour ce projet, à interpréter avec précaution.
- **Prochaines étapes** identifiées : finalisation de l'**accessibilité** (textes alternatifs, ordre de tabulation) puis publication.

---

## 🧰 Compétences & outils

`Power BI` · `Power Query (M)` · `DAX` — Prétraitement complet intégré (pivots, jointures multi-sources, champs calculés, indicateur composite) · Modélisation en étoile à dimensions conformes · Cadrage produit (blueprint besoin → indicateur → visualisation) · Dataviz décisionnelle multi-échelles (carte, scatter, donuts) · Justification des choix d'outil · Recommandations opérationnelles par domaine.

---

## 📁 Structure du dossier

```
P10 - Tableau de bord accès à l'eau (DWFA)/
├── Dervout_Corentin_2_dashboard_072026.pbix     # rapport Power BI (Power Query, modèle, 3 vues)
└── Dervout_Corentin_1_présentation_072026.pptx  # support de restitution
```

---

*Projet réalisé dans le cadre du parcours Data Analyst d'OpenClassrooms (titre RNCP niveau 6). Données publiques OMS / FAO / Banque Mondiale.*
