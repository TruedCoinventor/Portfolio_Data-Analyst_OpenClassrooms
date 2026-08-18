<!--
  Note : vérifiez que les noms de dossiers de votre repo correspondent aux libellés
  du tableau des projets (les liens sont des ancres internes, donc robustes).
-->

# Portfolio Data Analyst — Corentin Dervout

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![SQL](https://img.shields.io/badge/SQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![dbt](https://img.shields.io/badge/dbt-FF694B?style=flat-square&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=flat-square&logo=snowflake&logoColor=white)](https://www.snowflake.com/)

> **Data Analyst — profil hybride développement & data, en route vers l'ingénierie de l'IA.**
> 3 ans d'expérience en développement logiciel (dont de l'intégration de modèles d'IA), désormais outillé de bout en bout sur la donnée : de la modélisation SQL au machine learning, jusqu'à la mise en production.

Bienvenue sur mon portfolio. Vous y trouverez une **sélection hiérarchisée** de projets réalisés dans le cadre du parcours **Data Analyst (titre RNCP 37837, niveau 6) d'OpenClassrooms** — parcours préparatoire officiel au titre **Développeur en Intelligence Artificielle (RNCP 37827)**. Chaque projet est documenté comme une **preuve de compétence**.

Chaque projet suit la même logique de lecture, pensée pour un recruteur ou un client :

> **Contexte / besoin métier → Données → Démarche → Résultats → Impact & recommandations**

Le détail complet de chaque projet (données, choix méthodologiques, limites, pistes) se trouve dans le `README` de son dossier.

---

## 🧭 Ma posture

J'aborde chaque mission en **consultant**, avec un réflexe d'ingénieur hérité du développement :

- **Je pars du besoin métier**, pas de l'outil : je reformule la question et je cadre le livrable attendu (Product Strategy Canvas, blueprint, cahier des charges selon les projets).
- **J'assume et je justifie mes choix** : chaque méthode (test statistique, algorithme, seuil) est argumentée, et ses **limites** sont explicitées — y compris quand cela conduit à écarter une option.
- **Je pense « production »** : code reproductible, pipelines testés, artefacts déployables (un pipeline sérialisé et un script CLI au P12, un projet dbt testé au P8).
- **Je rends l'analyse actionnable** et je facilite la prise en main : recommandations claires, dashboards lisibles, procédures de mise à jour et mini-formations pour rendre les équipes autonomes.

---

## 🧰 Stack & Outils

| Domaine | Outils & bibliothèques |
|---|---|
| **Langages** | Python · SQL · R |
| **Manipulation & analyse** | Pandas · NumPy · SciPy · statsmodels |
| **Visualisation** | Matplotlib · Seaborn · Plotly · Power BI (DAX, Power Query) · Streamlit |
| **Machine Learning** | Scikit-learn (ACP, clustering, classification, régression) |
| **Data Engineering** | dbt · Snowflake · PostgreSQL |
| **Dev & production** | Git · Docker · API REST · Linux · LLMs (prompt engineering) |
| **Méthodes** | Statistiques inférentielles · Modélisation relationnelle & en étoile · RGPD · Agile/SAFe |

---

## 🔭 Veille métier & technologique

Rester à jour fait partie du métier : ma veille alimente directement mes choix d'outils et de méthodes. **Thématiques suivies** : écosystème Python data (pandas, scikit-learn), Business Intelligence (Power BI, dbt), qualité et gouvernance des données, méthodes statistiques et ML, IA générative.

| Type de source | Exemples suivis |
|---|---|
| Références techniques | Documentations officielles (scikit-learn, pandas, dbt, Power BI), notes de version |
| Qualité des données | Pandera, Great Expectations |
| Données & institutions | INSEE · data.gouv.fr · FAO · Banque Mondiale · OMS |
| Communautés & pratique | Kaggle · Stack Overflow · communautés data |

**De la veille aux décisions — quelques arbitrages concrets tirés de mes projets :**
- **P13** — comparaison sourcée **KMeans / Ward / DBSCAN** (choix par silhouette) et **Pandera vs Great Expectations** pour la qualité de données (Pandera retenu, Great Expectations écarté pour sur-ingénierie) ;
- **P10** — **Power BI plutôt que Tableau**, arbitrage justifié (compétence acquise, Power Query, coût) ;
- **P12** — choix du modèle final par **calibration et reproductibilité**, pas seulement par la performance brute ;
- **P4** — seuil calorique de référence **fixé à 2 600 kcal, sourcé** (document FAO) plutôt qu'un chiffre par défaut.

---

## 📁 Projets

> Les projets sont classés **par compétence, du plus avancé au plus fondamental** — une douzaine de preuves couvrant l'ensemble du cycle de la donnée.

| # | Projet | Compétence clé | Stack |
|---|--------|----------------|-------|
| [P12](#p12--détection-de-faux-billets) | Détection de faux billets | Machine Learning supervisé | Python · scikit-learn |
| [P11](#p11--étude-de-marché-à-lexport) | Étude de marché à l'export | ACP · Clustering | Python · scikit-learn |
| [P13](#p13--projet-data-augmenté-par-lia) | Segmentation catalogue (P6 + IA) | Clustering · conduite de projet | Python · scikit-learn |
| [P8](#p8--analyse-sociodémographique-avec-dbt) | Pipeline sociodémographique | Data Engineering (dbt) | dbt · Snowflake |
| [P9](#p9--analyse-des-ventes-dune-librairie) | Analyse des ventes librairie | Statistiques inférentielles | Python · SciPy |
| [P6](#p6--optimisation-des-données-dune-boutique) | Optimisation données boutique | Nettoyage & KPI métier | Python · Pandas |
| [P4](#p4--étude-de-sécurité-alimentaire-fao) | Sécurité alimentaire mondiale | EDA & santé publique | Python · Pandas |
| [P5](#p5--base-de-données-immobilière) | Base immobilière | Modélisation SQL (3NF) | PostgreSQL |
| [P3](#p3--base-de-données-dassurance) | Base d'assurance | Fondamentaux SQL | PostgreSQL |
| [P7](#p7--tableau-de-bord-de-pilotage-de-projets) | Dashboard pilotage projets | Power BI (DAX, étoile) | Power BI |
| [P10](#p10--tableau-de-bord-daccès-à-leau-potable) | Dashboard accès à l'eau | Power BI (Power Query) | Power BI |
| [P2](#p2--analyse-des-ventes-e-commerce) | Reporting de performance | Storytelling data | Excel |

---

### 🤖 Machine Learning & modélisation

#### P12 — Détection de faux billets
Classer vrais/faux billets à partir de 6 mesures géométriques, pour l'ONCFM.
**Démarche :** contrôle qualité statistique (test du χ² sur les manquants, d de Cohen), benchmark d'imputation, comparaison de modèles arbitrée par la **calibration** et l'interprétabilité, seuil de décision calibré et validé sur 15 découpages.
`Python · scikit-learn`
> 💡 Régression logistique calibrée (seuil 0,80) livrée en **pipeline de production + script CLI** : **100 % des faux billets interceptés** (0 faux négatif) sur le jeu de test.

#### P11 — Étude de marché à l'export
Identifier les marchés cibles pour l'export de poulet bio (La Poule qui Chante), sur 127 pays et 17 indicateurs.
**Démarche :** consolidation de 8 sources (FAO, Banque Mondiale), harmonisation ISO3, **ACP** (5 composantes), **clustering** CAH + K-means comparés par ARI (0,65), score composite pondéré avec garde-fou de matérialité.
`Python · scikit-learn`
> 💡 La recommandation robuste n'est pas un pays mais **deux familles** — hubs ultra-premium (Belgique, Pays-Bas, Luxembourg…) et marchés développés premium — avec la nuance honnête des **plateformes de réexport**.

#### P13 — Projet data augmenté par l'IA
Faire passer l'analyse descriptive du P6 à une **segmentation multivariée automatisée** du catalogue BottleNeck.
**Démarche :** cahier des charges, veille sourcée, prévention du *data leakage*, arbitrage de deux variantes (silhouette + ARI), conduite de projet (backlog, risques) et **usage critique et documenté de l'IA**.
`Python · scikit-learn`
> 💡 L'ajout de la **rotation de stock** révèle un segment invisible à l'œil nu : **32 produits en « stock dormant »** (chers, peu rentables, stockés > 1 an), à déstocker en priorité.

---

### 🏗️ Data Engineering & pipelines

#### P8 — Analyse sociodémographique avec dbt
Comparer le profil des étudiants Data d'OpenClassrooms à la population française (INSEE).
**Démarche :** pipeline **dbt** en architecture médaillon (Bronze → Silver → Gold) sur Snowflake, référentiels INSEE versionnés en *seeds*, ~34 tests de qualité dont un **test de réconciliation**.
`dbt · Snowflake · Python`
> 💡 Le **« piège du non-renseigné »** : la féminisation apparente (18 %→31 %) est un **artefact de collecte** (le NR chute de 42 %→7 %) ; hors NR, la part des femmes est stable (~30-33 %).

---

### 🐍 Analyse de données (Python)

#### P9 — Analyse des ventes d'une librairie
Comprendre le comportement d'achat d'une librairie en ligne (Lapage) sur 24 mois (687 k transactions).
**Démarche :** KPIs et séries temporelles, concentration (Lorenz/Gini), puis **tests statistiques agrégés au niveau client** (Chi², Spearman, Kruskal-Wallis) pour éviter la pseudo-réplication.
`Python · Pandas · SciPy`
> 💡 Le **genre n'a aucune influence** ; c'est l'**âge** qui segmente (corrélation âge/panier ρ = −0,70) → 3 profils : jeunes (panier élevé), adultes, seniors (fidèles mais petits paniers).

#### P6 — Optimisation des données d'une boutique
Consolider et fiabiliser les données d'un caviste (BottleNeck) à partir de 3 sources hétérogènes (ERP, web, liaison).
**Démarche :** audit qualité, corrections documentées, fusion et décomposition des non-correspondances, indicateurs métier (CA, Pareto, marge, rotation de stock).
`Python · Pandas`
> 💡 Point de vigilance identifié : le **Champagne** cumule stock élevé, **marge la plus faible (35 %)** et rotation jusqu'à **31 mois** — plus d'un demi-million d'euros immobilisés.

#### P4 — Étude de sécurité alimentaire (FAO)
Analyser la disponibilité alimentaire mondiale et la sous-nutrition (données FAO, 2017).
**Démarche :** nettoyage et harmonisation multi-sources, indicateurs de capacité nourricière, étude de cas ciblée.
`Python · Pandas`
> 💡 Même avec un seuil exigeant de **2 600 kcal sourcé**, la production couvre les besoins (~107 %) : la faim est un problème de **répartition**, pas de production (illustré par le paradoxe du manioc thaïlandais).

---

### 🗄️ SQL & bases de données

#### P5 — Base de données immobilière
Concevoir et exploiter une base des transactions immobilières françaises (DVF) pour Laplace Immo.
**Démarche :** modélisation **3NF** (5 tables, clé concaténée), conformité RGPD (stratégie de réimport semestriel), chargement PostgreSQL, 12 requêtes d'analyse.
`PostgreSQL`
> 💡 Marché **ultra-concentré** : l'Île-de-France pèse ~47 % des ventes et **Paris atteint 12 053 €/m²**, ~67 % au-dessus du 2ᵉ département.

#### P3 — Base de données d'assurance
Modéliser et interroger une base de contrats d'assurance habitation.
**Démarche :** dictionnaire de données, dimensionnement objectif des champs, contrôle qualité, base PostgreSQL, 12 requêtes SQL interprétées.
`PostgreSQL`
> 💡 **Décision de qualité assumée** : suppression de 9 contrats aux codes DOM incohérents plutôt que d'inventer des valeurs ; lecture d'ensemble = forte concentration Île-de-France.

---

### 📊 Business Intelligence (Power BI)

#### P7 — Tableau de bord de pilotage de projets
Piloter un portefeuille de projets IT & Marketing internationaux (Sanitoral).
**Démarche :** cadrage par **Product Strategy Canvas**, modèle en étoile, **30+ mesures DAX** (écarts multi-axes, alerte à 4 niveaux), 6 pages interactives.
`Power BI · DAX`
> 💡 Posture consultant : une page **Guide** avec procédure de rafraîchissement rend les équipes autonomes sur la maintenance de l'outil.

#### P10 — Tableau de bord d'accès à l'eau potable
Aider une ONG (DWFA) à cibler ses pays prioritaires (données OMS/FAO, 194 pays).
**Démarche :** **tout le prétraitement en Power Query (M), sans Python** — fichier autonome ; modèle en étoile à dimensions conformes ; 3 vues (Monde / Continent / Pays).
`Power BI · Power Query`
> 💡 Recommandations **par domaine d'intervention** : création (Tchad 39 %…), modernisation (Laos 82/16 %…), consulting (Bénin, Zambie…).

---

### 📈 Reporting & storytelling

#### P2 — Analyse des ventes e-commerce
Produire un rapport de performance mensuel exploitable par la direction marketing (Le Grand Marché).
**Démarche :** sélection et interprétation de graphiques, storytelling data, recommandation d'axe stratégique.
`Excel · PowerPoint`
> 💡 La baisse du CA est **transitoire** (bascule high-tech → nourriture) ; le vrai levier est le **trafic qui explose sans convertir** — un potentiel inexploité.

---

## 🎓 À propos

Développeur de formation (Master SUPINFO, DUT GEII), j'ai **3 ans d'expérience en développement** — dont une alternance de 2 ans chez **Inetum** où j'ai notamment développé des scripts Python d'anonymisation RGPD **en lien avec l'équipe IA du client**, des **API REST** d'intégration de modèles, et des requêtes SQL complexes sur PostgreSQL.

Je consolide aujourd'hui ce socle par une **spécialisation Data Analyst** (titre RNCP 37837), tremplin officiel vers le titre **Développeur en Intelligence Artificielle (RNCP 37827)**. Mon objectif : une **alternance de Développeur IA (Sept. 2026 – Sept. 2027)**. Ce double profil dev + data me permet d'aller de l'analyse jusqu'à des solutions **fiables, testées et déployables**.

*Tous les projets présentés ici sont réalisés dans le cadre de la formation ; les données sont fictives ou issues de l'open data.*

---

## 📬 Contact

- 💼 [LinkedIn](https://fr.linkedin.com/in/corentin-dervout-392a93139)
- 💻 [GitHub](https://github.com/TruedCoinventor)
- 📨 c.dervout@gmail.com
