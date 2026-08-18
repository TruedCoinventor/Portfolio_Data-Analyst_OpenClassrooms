# P5 — Base de données immobilière avec SQL — DATAImmo (Laplace Immo)

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Modélisation](https://img.shields.io/badge/modélisation-3NF-336791?style=flat-square)](#)
[![RGPD](https://img.shields.io/badge/conformité-RGPD-2ea44f?style=flat-square)](#)

> Conception et exploitation d'une base de données PostgreSQL **normalisée (3NF)** des transactions immobilières françaises, pour le réseau d'agences **Laplace Immo** — de la modélisation à 12 requêtes d'analyse du marché.

---

## 🎯 Contexte & besoin métier

**Laplace Immo**, réseau national d'agences, veut se démarquer en **prévoyant mieux le prix de vente des biens**. Dans le cadre du projet interne **DATAImmo**, la CTO Clara Daucourt confie la construction du socle de données : **enrichir la base** avec les données géographiques et de population, **garantir la conformité RGPD**, puis **analyser le marché** pour aider les agences régionales. Ce socle propre et documenté est le préalable à un futur modèle prédictif.

---

## 📦 Livrables

| Livrable | Fichier | Contenu |
|---|---|---|
| **Dictionnaire des données** | `Dervout_Corentin_1_dictionnaire_de_donnees_202512.xlsx` | Une feuille par table (Région, Département, Commune, Bien, Vente) + lexique |
| **Support de présentation** | `Dervout_Corentin_2_support_presentation_202512.pptx` | Contexte, RGPD, dictionnaire, schéma, BDD chargée, 12 requêtes et résultats |

---

## 🗂️ Données

Trois sources publiques (open data), croisées :

- **DVF** (Demandes de Valeurs Foncières, data.gouv) — transactions, **1er semestre 2020**
- **INSEE** — population par commune
- **Référentiel géographique** (data.gouv) — communes, départements, régions

---

## 🔍 Démarche

### 1. Dictionnaire des données
Pour chaque table : code, signification, type, longueur, nature (élémentaire / concaténé / calculé), règle de gestion et règle de calcul — en s'appuyant sur le template fourni et la notice descriptive du DVF.

### 2. Modélisation normalisée (3NF)
Schéma relationnel à **5 tables** en troisième forme normale, avec une chaîne hiérarchique claire :

```
Region ──< Departement ──< Commune ──< Bien ──< Vente
```

Choix de conception notables :
- **Clé concaténée** `code_commune_insee` (code département + code commune, 6 caractères) comme clé de la commune — car un code département seul n'identifie pas une commune de façon unique.
- **Enrichissement** de la commune par la `population_totale` (INSEE) et rattachement à `Département` puis `Région`.
- Attributs `type_local` / `type_de_voie` **conservés en colonnes** de `Bien` plutôt qu'externalisés — modèle resserré mais cohérent avec le besoin.

### 3. Sauvegarde & conformité RGPD
**Minimisation** : les noms d'acquéreurs ne sont pas intégrés à la base cible. **Stratégie de rafraîchissement** : réimport de la nouvelle version semestrielle du DVF, qui purge « automatiquement » les données ayant dépassé les seuils de conservation RGPD.

### 4. Création & chargement (PostgreSQL)
Import des fichiers bruts dans des tables de préparation, puis transformation vers le schéma cible avec clés primaires/étrangères. Contrôle du chargement par requêtes (ex. **34 991 communes** chargées).

### 5. Requêtage — analyse du marché
12 requêtes mobilisant jointures multi-tables (jusqu'à 5), agrégats, `GROUP BY`/`HAVING`, **CTE (`WITH`)**, sous-requêtes, **window functions** et alias de lisibilité.

---

## 📊 Résultats — les 12 requêtes (DVF, S1 2020)

| # | Question métier | Résultat clé |
|---|---|---|
| 1 | Appartements vendus (S1 2020) | **31 378** |
| 2 | Ventes d'appartements par région | **Île-de-France 13 995** (loin devant PACA 3 649, ARA 3 253) |
| 3 | Répartition des ventes par nombre de pièces | proportions par nb de pièces |
| 4 | Top 10 départements par prix/m² | **Paris 12 052,82 €/m²**, Hauts-de-Seine 7 219, Val-de-Marne 5 343 |
| 5 | Prix moyen/m² d'une maison en Île-de-France | **3 745,09 €/m²** |
| 6 | Top 10 appartements les plus chers | avec région et surface |
| 7 | Évolution des ventes T1 → T2 2020 | **+3,68 %** (CTE) |
| 8 | Classement des régions, prix/m² appart. > 4 pièces | agrégation multi-critères |
| 9 | Communes avec ≥ 50 ventes au T1 | filtrage sur agrégat (`HAVING`) |
| 10 | Écart de prix/m² entre 2 et 3 pièces | **-12,40 %** (le m² d'un 3-pièces est moins cher) |
| 11 | Top 3 communes par valeur foncière (dép. 6, 13, 33, 59, 69) | classement partitionné |
| 12 | Top 20 communes par transactions/1000 hab (> 10 000 hab) | **Paris 2e 5,84**, Paris 1er, Arcachon, La Baule… |

**Lecture transversale.** Le marché est **très concentré sur l'Île-de-France** (près de 14 000 ventes d'appartements sur le semestre, de loin la première région) et **Paris écrase les prix** (12 053 €/m², ~67 % au-dessus du 2e département). Le **prix au m² décroît avec la taille** (un 3-pièces est ~12 % moins cher au m² qu'un 2-pièces). La **rotation** est la plus forte dans le Paris central et les communes littorales prisées (Arcachon, La Baule, Roquebrune). Enfin, malgré le contexte du 1er semestre 2020, les ventes progressent légèrement du T1 au T2 (+3,7 %).

---

## ⚠️ Limites & prochaines pistes

- Le périmètre se limite au **1er semestre 2020** : une profondeur pluriannuelle permettrait d'analyser les tendances et la saisonnalité.
- Les prix/m² s'appuient sur la **surface Carrez** (appartements) : la comparaison maisons/appartements demande de la prudence méthodologique.
- Le socle est prêt pour la suite logique du projet DATAImmo : **alimenter un modèle de prédiction** du prix de vente.

---

## 🧰 Compétences & outils

`PostgreSQL` · `Power Architect / modélisation` · `Excel` — Modélisation relationnelle 3NF (dictionnaire, MCD/MLD/MPD, clés concaténées) · Gouvernance et **conformité RGPD** (minimisation, stratégie de sauvegarde) · ETL et contrôle d'intégrité · SQL avancé (jointures multi-tables, CTE, window functions, filtres sur agrégats) · Restitution orientée métier.

---

## 📁 Structure du dossier

```
P5 - Base de données immobilière (DATAImmo)/
├── Dervout_Corentin_1_dictionnaire_de_donnees_202512.xlsx   # dictionnaire (5 tables + lexique)
└── Dervout_Corentin_2_support_presentation_202512.pptx      # contexte, schéma, BDD, 12 requêtes
```

---

*Projet réalisé dans le cadre du parcours Data Analyst d'OpenClassrooms (titre RNCP niveau 6). Données publiques (DVF, INSEE, data.gouv), noms d'acquéreurs exclus par conformité RGPD.*
