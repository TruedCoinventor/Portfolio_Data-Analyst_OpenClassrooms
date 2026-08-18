# P3 — Requêter une base de données avec SQL — Assurance habitation

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![DBeaver](https://img.shields.io/badge/DBeaver-382923?style=flat-square&logo=dbeaver&logoColor=white)](https://dbeaver.io/)
[![Power Architect](https://img.shields.io/badge/SQL%20Power%20Architect-modélisation-FF6B35?style=flat-square)](#)

> Conception d'une base de données relationnelle à partir de deux fichiers CSV bruts (contrats d'assurance habitation en France), chargement sous PostgreSQL, et exploitation par 12 requêtes SQL répondant à des questions métier.

---

## 🎯 Contexte & besoin métier

Projet d'entraînement aux **fondamentaux SQL** : à partir de données fictives d'une compagnie d'**assurance habitation** (~30 000 contrats couvrant le territoire français), il s'agit de passer de fichiers plats à une base de données fiable, puis d'en extraire des réponses exploitables. La chaîne complète est couverte : **comprendre les données → les modéliser → garantir leur qualité → les interroger**.

---

## 📦 Livrables

| Livrable | Fichier | Contenu |
|---|---|---|
| **Document technique** | `Dervout_Corentin_1_document-technique_20251210.pdf` | Dictionnaire des données, méthodologie de typage, correction des anomalies, schéma relationnel, DDL |
| **Liste des requêtes** | `Dervout_Corentin_2_liste_20251210.docx` | Les 12 requêtes SQL et leurs résultats |
| **Support méthodologie** | `Dervout_Corentin_3_méthodologie_20251210.pdf` | Présentation de la démarche (exploration → schéma → BDD → requêtage) |
| **Grille d'auto-évaluation** | `Dervout_Corentin_4_grille_20251210.pdf` | Auto-évaluation du projet (artefact de formation) |

---

## 🗂️ Données

Deux fichiers CSV sources :

- **`Contrat.csv`** — 1 ligne par contrat : identifiant, adresse du logement assuré, surface, type de bien, type d'occupation, formule, valeur déclarée, prix de cotisation mensuel.
- **`Region.csv`** — référentiel géographique : code commune, région, académie, département, commune.

La clé de jointure est `Code_dep_code_commune` (concaténation code département + code commune), clé primaire de `Region` et clé étrangère de `Contrat`.

---

## 🔍 Démarche

### 1. Dictionnaire des données & typage
Construction d'un dictionnaire décrivant chaque colonne. Règles de typage explicites : `INT` pour les colonnes strictement numériques (hors zéro initial significatif), `VARCHAR` dès la présence de caractères. **Dimensionnement des `VARCHAR` mesuré objectivement** : application de `LEN` puis `MAX` sous Excel (sur une **copie** des fichiers, pour ne pas altérer les sources) afin de fixer la taille réelle de chaque champ.

### 2. Contrôle qualité & décision sur les anomalies
Détection d'**incohérences dans `Code_dep_code_commune`** côté Contrat : des codes DOM à 5 chiffres (97460, 97434, 97470) alors que les codes en 97x doivent en compter 6. Après vérification à la source sans correction fiable possible, **9 contrats aberrants ont été retirés** (IDs 128054, 128056, 128059, 128061, 128064, 128068, 128070, 128077, 128082) — un arbitrage assumé : *supprimer une donnée non corrigeable de façon fiable plutôt que d'introduire une valeur inventée*. Analyse en parallèle des colonnes à cellules vides pour décider des contraintes `NOT NULL`.

### 3. Modélisation & création de la base
Schéma relationnel sous **SQL Power Architect** reprenant fidèlement le dictionnaire ; relation entre les deux tables supprimée puis recréée pour garantir une configuration correcte ; export du DDL via *Forward SQL*. Base créée sous **PostgreSQL**, tables générées à partir du DDL exporté, puis import des données.

**État final chargé :** table `contrat` = **30 326 lignes** (30 335 − 9 anomalies), table `region` = **38 916 lignes**.

### 4. Requêtage
12 requêtes couvrant progressivement `WHERE`, `DISTINCT`, `COUNT`/`AVG`, `GROUP BY`/`HAVING`, `ORDER BY`/`LIMIT` et jointures (`INNER JOIN`) — chacune interprétée, pas seulement exécutée.

---

## 📊 Résultats — les 12 requêtes

| # | Question métier | Résultat clé |
|---|---|---|
| 1 | Contrats + surface pour le CP 92100 | 98 contrats, surfaces majoritairement 50–100 m² |
| 2 | Régions présentes | 19 régions dans le référentiel |
| 3 | Nombre de résidences principales | 25 612 contrats |
| 4 | Top 5 des plus grandes surfaces | jusqu'à 815 m² (contrat 104211) |
| 5 | Cotisation mensuelle moyenne | **19,33 €** |
| 6 | Répartition par valeur déclarée | 0–25 k€ : 22 712 · 25–50 k€ : 6 814 · 50–100 k€ : 696 · 100 k€+ : 104 |
| 7 | Formules « Intégral » en Pays de la Loire | 589 contrats |
| 8 | Maisons du département 71 (type + formule) | tendance nette « résidence principale » |
| 9 | Surface moyenne à Paris | ~51,8 m² |
| 10 | Top 10 départements par cotisation moyenne | Paris en tête (~36,4 €, ~40 % de plus que le 2ᵉ) |
| 11 | Communes ≥ 150 contrats | 20 communes, dont 13 dans Paris / bassin parisien |
| 12 | Contrats par région | 16 régions couvertes ; **l'Île-de-France ≈ 47 %** des contrats |

**Lecture transversale.** Deux signaux ressortent nettement : une **très forte concentration géographique** autour de l'Île-de-France et du bassin parisien (visible en requêtes 10, 11 et 12), et un **portefeuille positionné sur des valeurs de biens plutôt basses** (près de 4× plus de contrats dans la tranche la plus basse que dans la suivante). Autrement dit, si seulement 16 des 19 régions sont représentées, le poids de l'IDF structure à lui seul le portefeuille.

---

## ⚠️ Limites & prochaines pistes

- Les 9 lignes supprimées auraient pu être **récupérées par un croisement avec un référentiel officiel des codes communes** (INSEE) plutôt qu'écartées — piste d'amélioration côté qualité.
- Les requêtes restent **descriptives** ; un approfondissement (croisements formule × valeur × région, indicateurs de risque) donnerait une vraie lecture actuarielle.
- La concentration IDF mériterait d'être rapportée à la **population assurable** pour distinguer un biais de collecte d'une réalité de marché.

---

## 🧰 Compétences & outils

`PostgreSQL` · `DBeaver` · `SQL Power Architect` · `Excel` — Modélisation relationnelle (dictionnaire de données, schéma, clés PK/FK & intégrité référentielle) · Contrôle qualité et décisions de nettoyage documentées · SQL d'analyse (jointures, agrégats, filtres sur agrégats) · Restitution méthodologique.

---

## 📁 Structure du dossier

```
P3 - Requêter une BDD avec SQL/
├── Dervout_Corentin_1_document-technique_20251210.pdf   # dictionnaire, anomalies, schéma, DDL
├── Dervout_Corentin_2_liste_20251210.docx               # 12 requêtes + résultats
├── Dervout_Corentin_3_méthodologie_20251210.pdf         # support de présentation
└── Dervout_Corentin_4_grille_20251210.pdf               # grille d'auto-évaluation
```

---

*Projet réalisé dans le cadre du parcours Data Analyst d'OpenClassrooms (titre RNCP niveau 6). Données fictives fournies dans le cadre de la formation.*
