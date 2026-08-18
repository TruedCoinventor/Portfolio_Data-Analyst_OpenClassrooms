# P7 — Tableau de bord dynamique Power BI — Sanitoral

[![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Power Query](https://img.shields.io/badge/Power%20Query-ETL-217346?style=flat-square)](#)
[![DAX](https://img.shields.io/badge/DAX-modèle%20en%20étoile-F2C811?style=flat-square)](#)

> Tableau de bord Power BI de pilotage d'un portefeuille de **projets IT & Marketing internationaux** pour **Sanitoral** (client ESN DATA) : suivre la performance et **identifier les écarts prévisionnel/réel** nécessitant l'intervention des directeurs.

---

## 🎯 Contexte & besoin métier

Sanitoral pilote un portefeuille de **104 projets** IT et Marketing à l'échelle mondiale, décomposés en **phases**, avec pour chacune un **prévisionnel** (coût, durée, livrables) et un **réel**. La direction manque d'une vision unifiée pour repérer les dérives. Le dashboard doit servir trois profils de décideurs, du plus stratégique au plus opérationnel.

### Cadrage — Product Strategy Canvas
Avant toute construction, un **Product Strategy Canvas** formalise le besoin en *user stories* par persona :

| Utilisateur | Besoins clés |
|---|---|
| **Directeur Général** | Synthèse globale de la santé du portefeuille · alerte dès qu'un projet **dépasse 15 % d'écart** · accès au détail d'un projet pour décider de sa poursuite ou de son arrêt |
| **Directeur Régional** | Filtrer sur sa région · comparer les pays de sa région · suivre l'**évolution temporelle** des écarts pour détecter les dégradations |
| **Directeur National** | Indicateurs de chaque projet de son pays · **détail par phase** pour localiser les dépassements · comparaison IT vs Marketing pour prioriser |

---

## 📦 Livrable

| Livrable | Fichier | Contenu |
|---|---|---|
| **Tableau de bord** | `Dervout_Corentin_1_tableau-de-bord_202602.pbix` | Modèle de données, requêtes Power Query, mesures DAX et 6 pages interactives |

> Le `.pbix` n'est pas prévisualisable sur GitHub : il s'ouvre dans **Power BI Desktop** pour inspection complète (modèle, DAX, Power Query). Le modèle de données et le Product Strategy Canvas sont **intégrés en capture dans la page *Guide*** du rapport pour un aperçu sans installation.

---

## 🗂️ Données & modélisation

Source : classeur Excel **Sanitoral** (prévisionnel, réels, localisations, profils pays, types de projet).

**Modèle en étoile** organisé autour de la table de faits **`Projects_Plans`** (prévisionnel par projet × phase), reliée à :

- trois tables de **réels** — `Actual_Costs`, `Actual_Durations`, `Actual_Delivrables` — jointes via une **clé composite `Project_ID_Phase`** (grain projet × phase) ;
- les dimensions `Project_Types`, `Projects_Locations` → `Country_Profiles` (Pays, Région, type de pays) ;
- une **table Calendrier dédiée** (`Calendar` : Date, Mois, Trimestre, Année) alimentant les analyses temporelles ;
- une table **`_Measures`** dédiée regroupant toute la logique DAX.

---

## 🧮 Mesures DAX (30+)

Une bibliothèque de mesures structurée sur **trois axes d'écart** — Coût, Durée, Livrables :

- **Totaux** : `Total_Planned_*` et `Total_Actual_*` pour chaque axe ;
- **Écarts** : `Gap_Cost/Duration/Deliverable` (valeur) et `Percent_Gap_*` (pourcentage) ;
- **Écart composite** : `Composite_Gap` synthétisant les trois axes ;
- **Niveaux d'alerte** : `Alert_Level` (global) et par axe (`Alert_Level_Cost/Duration/Deliverable`), avec une **classification à 4 niveaux** — High / Medium / Low / Zero — plus fine qu'un simple seuil binaire ;
- **Comptages & parts** : `Num_Projects`, `Num_High/Medium/Low/Zero_Alert_Projects` et les `Percent_*` associés ;
- **Insight dynamique** : `Insight_Gap`, une mesure de narration automatique.

---

## 📄 Les 6 pages (design « 6 G »)

Le rapport suit une progression du global au détaillé, avec une navigation par boutons et **4 filtres croisés persistants** (Type de projet / Région / Pays / ID projet) :

| Page | Rôle |
|---|---|
| **Global** | Cartes KPI Planned / Actual / écart valeur / % écart pour Coût, Durée, Livrables · donut *Alert level* · carte *% High Alert Projects by Country* · deux courbes d'évolution temporelle (part et nombre) |
| **Gap** | Écarts en % **par phase** (projets IT vs Marketing), écarts par type de projet (coût, durée, livrables), table détaillée |
| **Geo** | Carte *Composite Gap by Country*, écarts par pays et par type de pays |
| **Grid** | Table de données détaillée (exploration libre) |
| **Granular** | Vue projet par projet (cartes + table + graphique), drill vers le détail |
| **Guide** | Capture du modèle + Product Strategy Canvas + **procédure de mise à jour des données** pas à pas |

---

## 🧭 Ce que le dashboard permet de lire

Grâce à l'écart composite et aux niveaux d'alerte, le décideur localise en quelques clics **où se concentrent les dérives** : sur quel **axe** (coût, durée ou livrables), quelle **phase**, quel **type de projet** (IT vs Marketing) et quel **pays**. Les courbes temporelles distinguent une dégradation durable d'un incident ponctuel.

> 💡 *Insight à mettre en avant en soutenance : la conclusion principale que révèle votre dashboard (ex. l'axe qui concentre les alertes, la phase ou le type de projet le plus en dérive).*

---

## 🤝 Posture de consultant

Deux éléments incarnent la posture attendue :
- le **Product Strategy Canvas** en amont, qui ancre chaque visuel dans un besoin utilisateur réel ;
- la **page *Guide*** avec une procédure de rafraîchissement claire (ré-exporter le classeur Sanitoral à structure identique → remplacer le fichier source → *Actualiser* → vérifier la cohérence lignes/colonnes), qui rend les équipes **autonomes** sur la maintenance de l'outil.

---

## ⚠️ Limites & prochaines pistes

- Le seuil d'alerte est fixé à **15 %** : le rendre **paramétrable** par l'utilisateur augmenterait la finesse d'analyse.
- La qualité du suivi dépend de la **régularité de l'export Sanitoral** ; une connexion directe (base ou API) supprimerait l'étape manuelle.
- Un **cumul historique** au-delà de la fenêtre fournie renforcerait les analyses de tendance.

---

## 🧰 Compétences & outils

`Power BI` · `Power Query (ETL)` · `DAX` · `Excel` — Cadrage produit (Product Strategy Canvas, user stories) · Modélisation en étoile (table de faits, dimensions, table calendrier, clé composite) · Bibliothèque de mesures DAX (écarts multi-axes, alertes à seuils, insight dynamique) · Dataviz interactive (cartes, Gantt, courbes, filtres croisés) · UX/UI et documentation de prise en main.

---

## 📁 Structure du dossier

```
P7 - Tableau de bord Power BI (Sanitoral)/
└── Dervout_Corentin_1_tableau-de-bord_202602.pbix   # rapport Power BI (modèle, DAX, 6 pages)
```

---

*Projet réalisé dans le cadre du parcours Data Analyst d'OpenClassrooms (titre RNCP niveau 6). Données fictives fournies dans le cadre de la formation.*
