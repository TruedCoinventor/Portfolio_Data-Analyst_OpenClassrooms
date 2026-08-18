#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Détection automatique de faux billets : ONCFM
=============================================

Application de prédiction. Le modèle (régression logistique, seuil de décision
0,80) est chargé depuis ``pipeline_final.pkl``, produit par le notebook
d'analyse.

Deux modes d'utilisation :

    # 1. Analyse d'un fichier de billets
    python Nom_Prenom_2_script_app_072026.py billets_production.csv

    # 2. Saisie manuelle d'un billet
    python Nom_Prenom_2_script_app_072026.py

Options :

    --export resultats.csv   enregistre les résultats dans un fichier
    --details                affiche les mesures utilisées après imputation
    --seuil 0.9              remplace ponctuellement le seuil de décision

Le fichier d'entrée doit comporter les six colonnes ``diagonal``,
``height_left``, ``height_right``, ``margin_low``, ``margin_up`` et ``length``.
Le séparateur (virgule, point-virgule, tabulation) est détecté automatiquement,
les colonnes supplémentaires : telle une colonne ``id`` : sont conservées pour
l'affichage mais ignorées par le modèle, et l'ordre des colonnes est
indifférent.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Les composants personnalisés doivent être importables pour que joblib
# puisse reconstruire le pipeline sauvegardé.
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import joblib
    from oncfm_model import FEATURES
except ImportError as erreur:  # pragma: no cover
    print(f"Erreur : dépendance manquante ({erreur}).", file=sys.stderr)
    print("Installez les bibliothèques listées dans requirements.txt.", file=sys.stderr)
    sys.exit(1)


CHEMIN_MODELE = Path(__file__).resolve().parent / "pipeline_final.pkl"
LARGEUR = 66


# ----------------------------------------------------------------------
# Présentation
# ----------------------------------------------------------------------
def titre(texte: str) -> None:
    print("\n" + "=" * LARGEUR)
    print(f" {texte}")
    print("=" * LARGEUR)


def erreur_fatale(message: str, conseil: str = "") -> None:
    print(f"\n[ERREUR] {message}", file=sys.stderr)
    if conseil:
        print(f"         {conseil}", file=sys.stderr)
    sys.exit(1)


# ----------------------------------------------------------------------
# Chargement du modèle
# ----------------------------------------------------------------------
def charger_modele():
    if not CHEMIN_MODELE.exists():
        erreur_fatale(
            f"Modèle introuvable : {CHEMIN_MODELE}",
            "Exécutez le notebook d'analyse pour le régénérer.",
        )
    try:
        modele = joblib.load(CHEMIN_MODELE)
    except Exception as exc:
        erreur_fatale(
            f"Le modèle n'a pas pu être chargé ({type(exc).__name__} : {exc}).",
            "Vérifiez que les versions de scikit-learn correspondent "
            "(voir requirements.txt).",
        )
    return modele


# ----------------------------------------------------------------------
# Lecture des données
# ----------------------------------------------------------------------
def lire_fichier(chemin: str) -> pd.DataFrame:
    """Lit un CSV en détectant automatiquement son séparateur.

    Les fichiers de l'ONCFM circulent tantôt en point-virgule (export
    européen), tantôt en virgule. Deviner plutôt que supposer évite un échec
    au moment le plus gênant.
    """
    fichier = Path(chemin)
    if not fichier.exists():
        erreur_fatale(
            f"Fichier introuvable : {fichier}",
            "Vérifiez le chemin indiqué.",
        )

    donnees = None
    for arguments in (
        {"sep": None, "engine": "python"},          # détection automatique
        {"sep": ";", "decimal": ","},               # export européen
        {"sep": ";"},
        {"sep": ","},
        {"sep": "\t"},
    ):
        try:
            essai = pd.read_csv(fichier, **arguments)
        except Exception:
            continue
        if essai.shape[1] >= len(FEATURES):
            donnees = essai
            break

    if donnees is None:
        erreur_fatale(
            f"Impossible d'interpréter le fichier {fichier.name}.",
            "Formats acceptés : CSV séparé par virgule, point-virgule ou tabulation.",
        )

    if donnees.empty:
        erreur_fatale(f"Le fichier {fichier.name} ne contient aucune ligne.")

    donnees.columns = [str(c).strip() for c in donnees.columns]

    manquantes = [c for c in FEATURES if c not in donnees.columns]
    if manquantes:
        erreur_fatale(
            f"Colonnes absentes du fichier : {', '.join(manquantes)}.",
            f"Colonnes attendues : {', '.join(FEATURES)}. "
            f"Colonnes trouvées : {', '.join(donnees.columns)}.",
        )

    # Les nombres à virgule décimale sont convertis si nécessaire.
    # Le test porte sur le caractère numérique de la colonne plutôt que sur son
    # dtype exact : pandas 2 renvoie « object » là où pandas 3 renvoie « str ».
    for colonne in FEATURES:
        if not pd.api.types.is_numeric_dtype(donnees[colonne]):
            donnees[colonne] = pd.to_numeric(
                donnees[colonne].astype(str).str.strip().str.replace(",", ".", regex=False),
                errors="coerce",
            )

    print(f"Fichier lu       : {fichier.name}")
    print(f"Billets détectés : {len(donnees)}")

    incomplets = int(donnees[FEATURES].isna().any(axis=1).sum())
    if incomplets:
        print(
            f"Remarque         : {incomplets} billet(s) présentent une mesure "
            f"manquante,\n                   elle sera reconstruite par le modèle."
        )
    return donnees


def saisir_billet() -> pd.DataFrame:
    """Saisie interactive des six mesures d'un billet."""
    titre("SAISIE MANUELLE D'UN BILLET")
    print("Entrez les six mesures en millimètres.")
    print("Laissez vide si une mesure est indisponible ; elle sera estimée.")
    print("(Ctrl+C pour abandonner)\n")

    mesures: dict[str, float] = {}
    for colonne in FEATURES:
        while True:
            try:
                saisie = input(f"  {colonne:14s} : ").strip().replace(",", ".")
            except (KeyboardInterrupt, EOFError):
                print("\n\nSaisie interrompue.")
                sys.exit(0)

            if saisie == "":
                mesures[colonne] = np.nan
                break
            try:
                mesures[colonne] = float(saisie)
                break
            except ValueError:
                print("     Valeur non numérique. Exemple attendu : 112.83")

    if all(np.isnan(v) for v in mesures.values()):
        erreur_fatale("Aucune mesure fournie : impossible de prédire.")

    return pd.DataFrame([mesures])


# ----------------------------------------------------------------------
# Prédiction
# ----------------------------------------------------------------------
def predire(modele, donnees: pd.DataFrame, seuil: float | None = None) -> pd.DataFrame:
    """Applique le modèle et renvoie un tableau de résultats."""
    try:
        probabilites = modele.predict_genuine_proba(donnees)
    except ValueError as exc:
        erreur_fatale(str(exc))
    except Exception as exc:  # pragma: no cover
        erreur_fatale(f"Échec de la prédiction ({type(exc).__name__} : {exc}).")

    seuil_applique = modele.threshold if seuil is None else seuil
    authentique = probabilites >= seuil_applique

    # Identifiant du billet : colonne id si elle existe, numéro de ligne sinon
    if "id" in donnees.columns:
        identifiants = donnees["id"].astype(str).to_numpy()
    else:
        identifiants = np.array([f"billet_{i}" for i in range(1, len(donnees) + 1)])

    return pd.DataFrame({
        "id": identifiants,
        "is_genuine": authentique,
        "probabilite_authentique": probabilites.round(4),
        "verdict": np.where(authentique, "Vrai billet", "FAUX BILLET"),
        "confiance": np.where(
            np.maximum(probabilites, 1 - probabilites) >= 0.95, "élevée", "à vérifier"
        ),
    })


def afficher(resultats: pd.DataFrame, seuil: float, details: pd.DataFrame | None = None) -> None:
    titre("RÉSULTATS DE L'ANALYSE")
    print(f"{'Identifiant':<14}{'Verdict':<15}{'P(authentique)':>16}{'Confiance':>14}")
    print("-" * LARGEUR)

    for ligne in resultats.itertuples(index=False):
        marque = " " if ligne.is_genuine else ">"
        print(
            f"{marque}{ligne.id:<13}{ligne.verdict:<15}"
            f"{ligne.probabilite_authentique:>16.4f}{ligne.confiance:>14}"
        )

    total = len(resultats)
    vrais = int(resultats["is_genuine"].sum())
    faux = total - vrais
    douteux = int((resultats["confiance"] == "à vérifier").sum())

    titre("SYNTHÈSE")
    print(f"  Billets analysés        : {total}")
    print(f"  Vrais billets           : {vrais:3d}  ({vrais / total:.1%})")
    print(f"  Faux billets détectés   : {faux:3d}  ({faux / total:.1%})")
    print(f"\n  Seuil de décision       : {seuil:.2f}")
    print("  Un billet est déclaré authentique si P(authentique) >= seuil.")

    if douteux:
        print(
            f"\n  /!\\  {douteux} billet(s) en zone d'incertitude : "
            f"un contrôle manuel est recommandé."
        )

    if details is not None:
        titre("MESURES UTILISÉES (après reconstruction des valeurs manquantes)")
        print(details.round(3).to_string(index=False))


# ----------------------------------------------------------------------
# Point d'entrée
# ----------------------------------------------------------------------
def analyser_arguments() -> argparse.Namespace:
    analyseur = argparse.ArgumentParser(
        description="Détection automatique de faux billets : ONCFM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemples :\n"
            "  python %(prog)s billets_production.csv\n"
            "  python %(prog)s billets_production.csv --export resultats.csv\n"
            "  python %(prog)s          (saisie manuelle)\n"
        ),
    )
    analyseur.add_argument(
        "fichier", nargs="?",
        help="chemin du fichier CSV à analyser (sinon : saisie manuelle)",
    )
    analyseur.add_argument(
        "--export", metavar="SORTIE.CSV",
        help="enregistre les résultats dans un fichier CSV",
    )
    analyseur.add_argument(
        "--details", action="store_true",
        help="affiche les mesures utilisées après imputation",
    )
    analyseur.add_argument(
        "--seuil", type=float, default=None, metavar="VALEUR",
        help="remplace ponctuellement le seuil de décision (0 à 1)",
    )
    return analyseur.parse_args()


def main() -> None:
    arguments = analyser_arguments()

    if arguments.seuil is not None and not 0 < arguments.seuil < 1:
        erreur_fatale("Le seuil doit être strictement compris entre 0 et 1.")

    titre("ONCFM : DÉTECTION AUTOMATIQUE DE FAUX BILLETS")
    modele = charger_modele()
    seuil = modele.threshold if arguments.seuil is None else arguments.seuil
    print(f"Modèle chargé    : régression logistique, seuil {seuil:.2f}")

    if arguments.fichier:
        donnees = lire_fichier(arguments.fichier)
    else:
        donnees = saisir_billet()

    resultats = predire(modele, donnees, arguments.seuil)

    mesures = None
    if arguments.details:
        etapes = modele.estimator_
        transforme = donnees
        for nom, etape in etapes.steps[:-1]:
            transforme = etape.transform(transforme)
        mesures = pd.DataFrame(
            etapes.named_steps["imputation"].transform(
                etapes.named_steps["controle_integrite"].transform(
                    etapes.named_steps["validation_colonnes"].transform(donnees)
                )
            ),
            columns=FEATURES,
        )
        mesures.insert(0, "id", resultats["id"].to_numpy())

    afficher(resultats, seuil, mesures)

    if arguments.export:
        try:
            resultats.to_csv(arguments.export, index=False)
            print(f"\nRésultats enregistrés : {arguments.export}")
        except OSError as exc:
            erreur_fatale(f"Écriture impossible ({exc}).")

    print()


if __name__ == "__main__":
    main()
