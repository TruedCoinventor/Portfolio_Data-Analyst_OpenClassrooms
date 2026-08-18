# P9 — Analyse des ventes d'une librairie avec Python — Lapage

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=flat-square&logo=scipy&logoColor=white)](https://scipy.org)
[![statsmodels](https://img.shields.io/badge/statsmodels-séries%20temporelles-11557c?style=flat-square)](https://www.statsmodels.org)

> Analyse commerciale et comportementale d'une librairie en ligne (**Lapage**) sur 24 mois : indicateurs de ventes, séries temporelles, concentration du CA et **tests statistiques rigoureux** pour identifier des leviers de segmentation.

---

## 🎯 Contexte & besoin métier

Deux demandes complémentaires, à restituer au CODIR (dans le rôle de Sylvain) : **Annabelle** attend les **indicateurs de ventes** (KPIs, évolution du CA, top/flop), **Julie** attend une série de **corrélations statistiques** sur le comportement d'achat (âge, genre). Objectif : dégager des leviers concrets de segmentation et de ciblage marketing.

---

## 📦 Livrables

| Livrable | Fichier | Contenu |
|---|---|---|
| **Notebook** | `Dervout_Corentin_1_notebook_032026.ipynb` | Exploration, nettoyage, KPIs, séries temporelles, tests statistiques |
| **Présentation** | `Dervout_Corentin_1_support_032026.pptx` | Support CODIR (chiffres clés, corrélations, recommandations) |

---

## 🗂️ Données & préparation

Trois sources fusionnées : `products` (3 286 produits), `customers` (8 621 clients), `transactions` (**1 048 575 lignes brutes**). Après suppression de **361 041 lignes entièrement vides** et jointure : **687 534 transactions** sur **mars 2021 → février 2023 (24 mois)**.

Points de rigueur :
- **Validation croisée** du préfixe d'`id_prod` contre la catégorie (`0_/1_/2_` == categ : vérifié) ;
- **jointure *left* volontaire** pour conserver **21 produits jamais vendus** et **21 clients sans achat**, analysés à part ;
- calcul de l'**âge à la date de transaction** ;
- avant la partie statistique, **rechargement propre des données** pour éviter toute pollution par l'étape d'analyse.

---

## 📊 Indicateurs clés

| KPI | Valeur |
|---|---|
| Chiffre d'affaires (24 mois) | **12,03 M€** (≈ 501 k€/mois) |
| Transactions | 687 534 (≈ 28 600/mois) |
| Clients uniques | 8 600 · Produits vendus : 3 265 |
| Panier moyen (session) | **34,81 €** |
| Concentration (Gini) | **0,442** — Top 20 % des clients = **48 % du CA** |
| Part B2B | **7,4 %** (884 k€), portée par **4 clients** |

Analyses complémentaires : **moyenne mobile 3 mois** et **décomposition temporelle** (tendance / saisonnalité / résidus, `statsmodels`), **Pareto produits** (21 % des références = 80 % du CA), top/flop par CA, courbe de Lorenz.

**Insight catalogue.** La **Catégorie 2 ne pèse que 5,3 % des transactions mais 23 % du CA** (prix moyen ~76 €) ; la Catégorie 0 domine en volume (60 %) mais moins en valeur (37 %) ; la Catégorie 1 offre le meilleur équilibre. Les **4 clients B2B** (écart ×21 avec le 5ᵉ client) achètent de façon équilibrée sur les trois catégories, à l'inverse des B2C — un profil d'acheteurs institutionnels (bibliothèques, entreprises).

---

## 🔬 Démarche statistique

**Le choix méthodologique central : agréger les données au niveau du client avant tout test**, pour ne pas donner plus de poids aux clients actifs (pseudo-réplication) — et exclure les 4 B2B pour ne pas biaiser le segment B2C (640 734 transactions, 8 596 clients). Chaque test est ensuite choisi selon la nature des variables et un **test de normalité (Shapiro-Wilk)** : les variables étant toutes non normales, **Spearman** et **Kruskal-Wallis** sont retenus plutôt que leurs équivalents paramétriques.

| Relation | Test | Résultat | Conclusion |
|---|---|---|---|
| Genre × Catégorie dominante | Chi² | χ² = 4,90 · **p = 0,086** | **Aucun lien significatif** — le genre n'est pas un levier |
| Âge × CA total | Spearman | ρ = ‑0,18 | Faible négative — insuffisant |
| Âge × Fréquence d'achat | Spearman | ρ = +0,22 | Faible positive — insuffisant |
| Âge × Panier moyen | Spearman | **ρ = ‑0,70** | **Forte négative — levier clé** |
| Âge × Catégorie dominante | Kruskal-Wallis | p ≈ 0 | **Lien fort — segmentation par âge** |

> **Le genre, un faux levier — et pas de « mirage » statistique.** En raisonnant directement **au niveau du client** (catégorie dominante par client), le test du Chi² genre × catégorie ressort **non significatif (p = 0,086)** : le comportement d'achat ne dépend pas du genre. L'agrégation en amont évite l'écueil classique du Chi² sur des centaines de milliers de lignes, qui aurait produit un faux positif. À l'inverse, l'**âge × panier moyen** révèle une **corrélation forte (ρ = ‑0,70)** : plus le client est âgé, plus son panier est modeste.

---

## 👥 Trois profils clients par âge

| Profil | Âge moyen | Catégorie dominante | Comportement |
|---|---|---|---|
| 🧑 **Jeunes** | ~23 ans (σ = 4,3, très homogène) | Catégorie 2 | Panier élevé, achats peu fréquents |
| 👤 **Adultes** | ~43 ans | Catégorie 0 | Segment le plus large, comportement standard |
| 👴 **Seniors** | ~50 ans et + | Catégorie 1 | Très fidèles, mais paniers modestes |

---

## 💡 Recommandations

- **Segmenter par âge, pas par genre** : le genre n'a aucune influence, trois segments d'âge se dégagent nettement.
- **Faire de la Catégorie 2 un levier de croissance** : 5 % des transactions mais 23 % du CA, portée par les jeunes → développer l'offre et sa visibilité.
- **Mieux monétiser les seniors** (fidèles mais petits paniers) : cross-selling et **packs découverte** pour relever le panier moyen.
- **Sécuriser les 4 clients B2B** ; interroger les **21 produits jamais vendus** (rationalisation du catalogue) et **relancer les 21 clients inscrits sans achat**.

---

## ⚠️ Limites & prochaines pistes

- Les tests portent sur des **corrélations** (pas de causalité) ; l'âge explique le panier mais d'autres facteurs restent à explorer.
- L'agrégation au niveau client masque la **variabilité intra-client** dans le temps.
- La saisonnalité mériterait un historique plus long que 24 mois pour être confirmée.

---

## 🧰 Compétences & outils

`Python` · `Pandas` · `NumPy` · `SciPy` · `statsmodels` · `Matplotlib` — Nettoyage et fusion multi-sources · Feature engineering (âge, panier, fréquence) · Segmentation B2B/B2C par détection d'anomalie · Séries temporelles (moyenne mobile, décomposition) · Concentration (Lorenz/Gini) · **Statistiques inférentielles** (choix du test, normalité, Chi²/Spearman/Kruskal-Wallis) · Restitution et recommandations au CODIR.

*RGPD : travail sur identifiants pseudonymisés, aucune donnée nominative.*

---

## 📁 Structure du dossier

```
P9 - Analyse des ventes librairie (Lapage)/
├── Dervout_Corentin_1_notebook_032026.ipynb   # analyse complète (exécutée)
└── Dervout_Corentin_1_support_032026.pptx      # support de présentation CODIR
```

---

*Projet réalisé dans le cadre du parcours Data Analyst d'OpenClassrooms (titre RNCP niveau 6). Données fictives fournies dans le cadre de la formation.*
