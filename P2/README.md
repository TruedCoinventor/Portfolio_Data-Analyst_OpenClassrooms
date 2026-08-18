# P2 — Analyse des ventes e-commerce — Le Grand Marché

[![Excel](https://img.shields.io/badge/Excel-dashboard-217346?style=flat-square&logo=microsoft-excel&logoColor=white)](#)
[![PowerPoint](https://img.shields.io/badge/PowerPoint-rapport%20mensuel-B7472A?style=flat-square&logo=microsoftpowerpoint&logoColor=white)](#)
[![Storytelling](https://img.shields.io/badge/compétence-storytelling%20data-blue?style=flat-square)](#)

> Rapport marketing mensuel et tableau de bord des clients affiliés pour **Le Grand Marché**, une enseigne de grande distribution en ligne (nourriture, biens de consommation, high-tech). Objectif : expliquer une baisse du chiffre d'affaires malgré une explosion des ventes, et projeter la tendance à venir.

---

## 🎯 Contexte & besoin métier

Dans le rôle d'un Data Analyst au service Marketing du Grand Marché, deux demandes internes convergent vers le rapport mensuel présenté à la direction :

- **Frédéric (Directeur Marketing)** veut comprendre, graphiques à l'appui, **d'où vient la baisse du chiffre d'affaires** et **comment la situation va évoluer**, dans un format court et accessible à un public non-technique — avec une **suggestion d'axe stratégique**.
- **Pauline (pôle Marketing)** a besoin d'aide pour **compléter une trame de tableau de bord** sur les **clients affiliés** du mois de février, qui lui servira de support de présentation.

L'enjeu métier de fond : l'entreprise a **arrêté le segment high-tech** l'année précédente pour se recentrer sur la nourriture et les biens de consommation. Il faut mesurer l'effet de ce virage et sécuriser la trajectoire du CA.

---

## 📦 Livrables

| Livrable | Fichier | Contenu |
|---|---|---|
| **Rapport mensuel** | `Dervout_Corentin_1_rapport_mensuel_20251201.pptx` | 5 graphiques sélectionnés + narration + axe stratégique (1 graphique / slide) |
| **Tableau de bord clients affiliés** | `Dervout_Corentin_2_clients_affilies_20251201.xlsx` | Synthèse mensuelle, tableau croisé client × catégorie, 5 infographies, données brutes |

---

## 🗂️ Données

- **Rapport mensuel :** indicateurs généraux du site sur ~1 an (ventes, CA, panier, visites, taux de conversion, temps passé avant achat), ventilés par catégorie *(nourriture, biens de consommation, high-tech)*.
- **Clients affiliés :** **660 transactions** de février (ID client, temps d'achat, montant, catégorie), plus l'historique de CA mensuel par catégorie de septembre à février.
- **Limites :** granularité mensuelle sur le volet général (peu de recul pour un lissage saisonnier) ; le périmètre « clients affiliés » ne couvre qu'**un seul mois**, ce qui limite les conclusions temporelles sur ce sous-ensemble.

> **Note méthodologique.** Les graphiques du rapport mensuel étaient **fournis pré-générés** (banque de visualisations issue d'un script). La compétence démontrée ici n'est pas la production de code mais la **lecture critique** : sélectionner les 5 graphiques les plus pertinents parmi ceux disponibles, les **interpréter** et en tirer un **récit** pour un public non-technique. Le tableau de bord Excel, lui, a été **construit à partir des données brutes**.

---

## 🔍 Démarche

**Volet 1 — Rapport mensuel (restitution direction)**
Sélection de 5 graphiques répondant aux demandes de Frédéric, réorganisés en un fil narratif ; application des bonnes pratiques d'accessibilité (choix des couleurs, contraste, titres porteurs de message) ; un seul graphique par slide ; adaptation du discours à un auditoire non-initié.

**Volet 2 — Tableau de bord clients affiliés (Excel)**
Structuration de la trame en trois onglets : un **tableau de bord** de synthèse (CA mensuel par catégorie, segmentation par temps d'achat, 5 infographies), un **tableau croisé dynamique client × catégorie**, et les **données brutes** de février. Calcul d'indicateurs (CA par catégorie, top 10 clients, panier vs temps passé).

---

## 📊 Résultats & lecture

**1. Une baisse du CA qui contraste avec une explosion du volume de ventes.**
Les ventes accélèrent fortement à partir d'octobre, de façon quasi exponentielle dès décembre ; le CA progresse d'abord puis recule en janvier. Le découplage volume/valeur est le cœur du sujet.

**2. La cause : le basculement de catalogue.**
La ventilation par catégorie l'explique à elle seule : les biens de consommation se maintiennent, la nourriture progresse régulièrement, tandis que le high-tech (panier élevé) décline **jusqu'à disparaître** — conséquence de l'arrêt du segment. La montée en volume de la nourriture (panier plus faible) ne compense pas encore la perte de valeur du high-tech : le repli du CA apparaît comme un **effet de transition**, appelé à se résorber le mois suivant.

**3. Un trafic qui explose mais ne convertit pas.**
Les visites augmentent encore plus vite que les ventes, sans impact proportionnel : le **taux de conversion diminue nettement** sur la période. La variabilité du temps passé avant achat s'accroît fortement — la médiane baisse (cœur de clientèle habitué au site), mais l'étalement révèle des **nouveaux visiteurs « perdus »** qui n'aboutissent pas.

**4. Côté clients affiliés (février) :** CA total de **12 058,95 €**, dont **7 441 €** en nourriture et **4 617 €** en biens de consommation (high-tech déjà à zéro). La segmentation par durée est parlante : les sessions **> 9 min 30** génèrent **7 577 €** sur 91 transactions, contre **1 563 €** pour les sessions **< 4 min** (47 transactions) — le temps d'engagement est fortement corrélé à la valeur du panier.

---

## 💡 Axe stratégique proposé

Le vrai gisement n'est pas la baisse (transitoire) du CA, mais le **potentiel inexploité du trafic** : une audience en forte croissance qui ne se transforme pas en ventes. La recommandation est d'investiguer deux leviers, à confier aux équipes concernées :

- **SEO / acquisition** — vérifier que le trafic attiré correspond bien à la nouvelle stratégie (nourriture / biens de consommation) plutôt qu'à des visiteurs non intéressés ;
- **UX / design du site** — réduire la friction pour les nouveaux visiteurs qui ne trouvent pas ce qu'ils cherchent, afin de convertir ce trafic supplémentaire.

---

## ⚠️ Limites & prochaines pistes

- Le diagnostic « effet de transition » sur le CA mérite d'être **confirmé sur les mois suivants** (le rapport projette une compensation, non encore observée).
- La chute du taux de conversion pointe une faiblesse SEO **ou** UX : **distinguer les deux** nécessite des données complémentaires (sources de trafic, parcours, taux de rebond par page).
- Le volet clients affiliés gagnerait à être **suivi sur plusieurs mois** pour distinguer tendance et effet ponctuel.

---

## 🧰 Compétences & outils

`Excel (TCD, graphiques)` · `PowerPoint` · Lecture critique et sélection de visualisations · Storytelling data · Bonnes pratiques d'accessibilité · Restitution à un public non-technique · Posture de conseil (recommandation stratégique)

---

## 📁 Structure du dossier

```
P2 - Analyse des ventes e-commerce/
├── Dervout_Corentin_1_rapport_mensuel_20251201.pptx    # rapport mensuel (5 graphiques + storytelling)
└── Dervout_Corentin_2_clients_affilies_20251201.xlsx   # tableau de bord clients affiliés
```

---

*Projet réalisé dans le cadre du parcours Data Analyst d'OpenClassrooms (titre RNCP niveau 6). Données fictives fournies dans le cadre de la formation.*
