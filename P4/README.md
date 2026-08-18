# P4 — Étude de santé publique avec Python — Sécurité alimentaire mondiale (FAO)

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat-square)](https://matplotlib.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org)

> Étude de la sécurité alimentaire mondiale (2017) à partir de quatre jeux de données ouverts de la **FAO** : la planète produit-elle assez pour nourrir tout le monde, et si oui, pourquoi la sous-nutrition persiste-t-elle ?

---

## 🎯 Contexte & besoin métier

La faim reste un enjeu mondial majeur. À partir des données FAO (population, disponibilité alimentaire, aide alimentaire, sous-nutrition), l'étude vise à **analyser la disponibilité alimentaire mondiale et sa répartition**, à **identifier les déséquilibres entre production, consommation et sous-nutrition**, et à **mettre en évidence les limites structurelles** du système alimentaire mondial.

---

## 📦 Livrables

| Livrable | Fichier | Contenu |
|---|---|---|
| **Notebook** | `Dervout_Corentin_1_notebook_202601.ipynb` | Analyse complète : exploration, nettoyage, indicateurs, visualisations |
| **Notebook (PDF)** | `Dervout_Corentin_2_notebook-pdf_202601.pdf` | Export PDF pour consultation sans exécution |
| **Présentation** | `Dervout_Corentin_3_presentation_202601.pptx` | Support de soutenance (10 analyses + conclusion) |

---

## 🗂️ Données

Quatre jeux de données FAO (open data, agrégats pays/année — **aucune donnée personnelle, hors périmètre RGPD**) :

| Dataset | Volume | Contenu |
|---|---|---|
| `population.csv` | 1 416 lignes | Population par pays et par année |
| `dispo_alimentaire.csv` | 15 605 lignes × 18 col. | Bilan alimentaire détaillé par pays et produit (2017) |
| `aide_alimentaire.csv` | 1 475 lignes | Aide alimentaire reçue par pays et par année |
| `sous_nutrition.csv` | 1 218 lignes | Personnes en sous-nutrition (fenêtres triennales) |

---

## 🔍 Démarche

### 1. Découverte & ciblage
Appropriation des quatre sources, de leur structure et de leur contexte ; focalisation sur l'année **2017** (année couverte par le bilan de disponibilité).

### 2. Nettoyage & harmonisation
Remplacement des valeurs manquantes, **standardisation des unités** (population en unités réelles, quantités converties en kg, aide en kg), et **conversion des fenêtres triennales de sous-nutrition** (« 2012-2014 ») en année centrale pour permettre les jointures. Croisements clés : population × sous-nutrition et population × disponibilité alimentaire.

### 3. Choix méthodologique — un seuil calorique *sourcé*
Point central de l'analyse : le besoin calorique de référence a été fixé à **2 600 kcal/personne/jour**, justifié à partir d'un document FAO (moyenne d'un homme ~3 000 kcal et d'une femme ~2 200 kcal, en excluant les enfants dont les besoins sont moindres). *Ce choix, plus exigeant que les seuils souvent retenus (2 250–2 500 kcal), rend les estimations de capacité nourricière volontairement conservatrices — un parti pris assumé et documenté plutôt qu'un chiffre rond pris par défaut.*

### 4. Synthèse visuelle
Traduction de chaque indicateur en un graphique dédié (donut, barres, barres empilées, treemap, courbes d'évolution, tableaux stylés) au service d'un récit clair.

---

## 📊 Résultats

| # | Analyse | Résultat clé (base 2 600 kcal) |
|---|---|---|
| 1 | Sous-nutrition mondiale (2017) | **535,7 M** de personnes, soit **7,1 %** de la population |
| 2 | Capacité nourricière totale | **8,05 Md** de personnes nourrissables = **~107 %** des besoins |
| 3 | Capacité avec les végétaux seuls | **6,64 Md** = **~88 %** → insuffisant à eux seuls |
| 4 | Répartition de la disponibilité intérieure | Nourriture 49,5 % · Traitement 22,4 % · Animaux 13,2 % · Autres 8,8 % · Pertes 4,6 % · Semences 1,6 % |
| 5 | Usage des principales céréales | 42,8 % à l'humain, 36,3 % à l'animal (Riz/Millet/Blé → humain ; Orge/Avoine/Maïs → animal) |
| 6 | Top pays en sous-nutrition | Haïti (~48 %) et Corée du Nord (~47 %) : près d'**un habitant sur deux** |
| 7 | Aide alimentaire (2013-2016) | Syrie, Éthiopie, Yémen = **~40 %** de l'aide mondiale |
| 8 | Évolution de l'aide (top 5) | Besoin en baisse pour 4 pays sur 5 ; **hausse au Yémen** (guerre, blocus, crise) |
| 9 | Disponibilité par habitant | Pays du Nord ~1,5× le besoin ; les plus bas descendent à **~70 %** (Haïti) |
| 10 | Étude de cas — manioc en Thaïlande | **83,4 %** de la production exportée, **2,9 %** pour les locaux |

**Lecture transversale.** Même avec un seuil de besoin exigeant (2 600 kcal), la production mondiale **couvre les besoins de l'ensemble de la population (~107 %)**. La sous-nutrition n'est donc pas un problème de volume produit mais de **répartition, d'usage et d'accès** : une part importante de la disponibilité part vers l'alimentation animale, le traitement industriel et les pertes, et les écarts Nord/Sud sont massifs (du simple ~70 % du besoin au double). Nuance apportée par l'analyse végétale : les végétaux seuls ne couvriraient que ~88 % des besoins au seuil retenu — la structure du système (et pas seulement son volume) compte.

### 🇹🇭 Le paradoxe thaïlandais (cas d'étude)
La Thaïlande **exporte 83,4 % de sa production de manioc** et n'en consacre que **2,9 %** à sa population locale, pendant que **~9 % de ses habitants (~6,5 M)** sont en sous-nutrition — une illustration concrète que l'insécurité alimentaire tient à l'allocation des ressources, non à leur existence.

---

## ✅ Conclusion

La production alimentaire mondiale est **en théorie suffisante** pour nourrir convenablement la population. La sous-nutrition est donc **un problème d'accès et de répartition**. L'aide alimentaire n'apporte qu'une **réponse temporaire** aux urgences ; ce sont des **réformes structurelles** des systèmes alimentaires mondiaux qui permettraient d'agir sur les causes.

---

## ⚠️ Limites & prochaines pistes

- Le résultat de capacité nourricière est **sensible au seuil calorique** retenu : le documenter (comme fait ici à 2 600 kcal) est essentiel, et une **analyse de sensibilité** (2 400 / 2 500 / 2 700 kcal) renforcerait la robustesse.
- L'étude est **transversale (2017)** ; une lecture **pluriannuelle** de la disponibilité affinerait les tendances.
- Le remplacement systématique des valeurs manquantes par 0 est pragmatique mais **peut sous-estimer** certains agrégats — à documenter au cas par cas.

---

## 🧰 Compétences & outils

`Python` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn` · `Jupyter` — Exploration et nettoyage multi-sources · Jointures et création d'indicateurs métier · Choix méthodologiques sourcés · Data visualisation et storytelling pour un public non technique.

---

## 📁 Structure du dossier

```
P4 - Étude santé publique (FAO)/
├── Dervout_Corentin_1_notebook_202601.ipynb      # notebook complet (exécuté)
├── Dervout_Corentin_2_notebook-pdf_202601.pdf    # export PDF
└── Dervout_Corentin_3_presentation_202601.pptx   # support de soutenance
```

---

*Projet réalisé dans le cadre du parcours Data Analyst d'OpenClassrooms (titre RNCP niveau 6). Données FAO en open data.*
