# utils/utils.py
from __future__ import annotations
from collections import defaultdict, Counter
import csv
import math
from typing import List, Dict
from classes.models import Student, TimeSlot, GroupRecord, UnplacedStudent

# Noms de colonnes du fichier d'entrée (ton CSV)
NAME_COL = "Nom des élèves"
CLASS_COL = "Classe"
CHOICE_COLS = [
    "Indiquez la première spécialité à laquelle vous voulez participer.",
    "Indiquez la deuxième spécialité à laquelle vous voulez participer.",
    "Indiquez la troisième spécialité à laquelle vous voulez participer.",
    "Indiquez la quatrième spécialité à laquelle vous voulez participer.",
    "Indiquez la cinquième spécialité à laquelle vous voulez participer.",
]

def load_students_from_csv(path: str, delimiter: str = ";") -> List[Student]:
    students: List[Student] = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=delimiter)

        # sécurité basique : vérifier les colonnes importantes
        for col in [NAME_COL, CLASS_COL, *CHOICE_COLS]:
            if col not in reader.fieldnames:
                raise ValueError(
                    f"Colonne manquante dans le fichier : {col}\n"
                    f"Colonnes trouvées : {reader.fieldnames}"
                )

        for row in reader:
            name = (row.get(NAME_COL) or "").strip()
            if not name:
                # ligne vide / anonyme => on skip (ex: ta 2de6 sans nom)
                continue

            classe = (row.get(CLASS_COL) or "").strip()

            choices = []
            for col in CHOICE_COLS:
                spe = (row.get(col) or "").strip()
                if spe:
                    choices.append(spe)

            students.append(Student(name=name, classe=classe, choices=choices))

    return students


def save_planning_per_student(
    path: str,
    students: List[Student],
    time_slots: List[TimeSlot],
    delimiter: str = ";",
) -> None:
    # Les en-têtes = Nom, Classe, puis les heures des créneaux
    fieldnames = ["Nom", "Classe"] + [ts.label for ts in time_slots]

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()

        for st in students:
            row = {"Nom": st.name, "Classe": st.classe}
            for ts in time_slots:
                assignment = st.assignments.get(ts.index)
                value = ""
                if assignment is not None:
                    value = f"{assignment.specialty} (g{assignment.group_index + 1})"
                # on utilise directement le label d'heure comme clé
                row[ts.label] = value
            writer.writerow(row)


def save_planning_per_group_formatted(
    path: str,
    group_records: List[GroupRecord],
    time_slots: List[TimeSlot],
    delimiter: str = ";",
) -> None:
    """
    Format bloc :

    Math g1 | 9h00-9h25 | 9h30-9h55 | ...
    1ere    |           |           | ...
    Term    |           |           | ...
    Salle   |           |           | ...
            |           |           | ...
            |  Eleve    |           | ...
    """

    from collections import defaultdict

    # spe -> group_index -> slot_index -> [ noms ]
    by_spe = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for r in group_records:
        by_spe[r.specialty][r.group_index][r.timeslot.index].append(r.student_name)

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=delimiter)

        for spe, groups_dict in sorted(by_spe.items()):
            max_group_idx = max(groups_dict.keys())

            for g in range(max_group_idx + 1):
                slots_dict = groups_dict.get(g, {})

                # 1) ligne titre
                header_row = [f"{spe} g{g+1}"] + [ts.label for ts in time_slots]
                writer.writerow(header_row)

                # 2) 1ere / Term / Salle : vides
                writer.writerow(["1ere"] + [""] * len(time_slots))
                writer.writerow(["Term"] + [""] * len(time_slots))
                writer.writerow(["Salle"] + [""] * len(time_slots))

                # 3) lignes élèves (une par ligne, sous les horaires)
                max_len = max((len(v) for v in slots_dict.values()), default=0)

                for i in range(max_len):
                    row = [""]
                    for ts in time_slots:
                        names_here = slots_dict.get(ts.index, [])
                        cell = names_here[i] if i < len(names_here) else ""
                        row.append(cell)
                    writer.writerow(row)

                writer.writerow([])  # espace entre groupes

            writer.writerow([])      # espace entre spé

def compute_groups_per_specialty(
    students: List[Student],
    time_slots: List[TimeSlot],
    min_per_slot_group: int,
    max_per_slot_group: int,
    max_groups_per_spe: int = 5,
) -> Dict[str, int]:
    """
    Calcule le nombre de groupes par spécialité pour respecter
    ~ min_per_slot_group et max_per_slot_group élèves PAR GROUPE ET PAR CRÉNEAU,
    autant que possible.
    """

    counts = Counter()
    for st in students:
        for spe in st.choices:
            counts[spe] += 1

    slot_count = len(time_slots)
    groups: Dict[str, int] = {}

    for spe, n in counts.items():
        if n == 0:
            continue

        # Au moins autant de groupes pour ne pas dépasser max_per_slot_group
        # N / (slot_count * G) <= max_per_slot_group
        min_groups = math.ceil(n / (slot_count * max_per_slot_group))

        # Au plus autant de groupes pour essayer d'avoir au moins min_per_slot_group
        if n >= min_per_slot_group:
            max_groups = max(1, n // (slot_count * min_per_slot_group))
        else:
            max_groups = 1

        max_groups = min(max_groups, max_groups_per_spe)

        if min_groups > max_groups:
            # Contraintes impossibles à satisfaire parfaitement
            g = min(min_groups, max_groups_per_spe)
            print(
                f"[WARN] Pour la spé {spe}, impossible d'avoir entre "
                f"{min_per_slot_group} et {max_per_slot_group} élèves par groupe/créneau "
                f"(n={n}). On ouvre {g} groupe(s)."
            )
        else:
            g = min_groups

        g = max(1, min(g, max_groups_per_spe))
        groups[spe] = g

    return groups


def save_unplaced_students(
    path: str,
    unplaced_students: List[UnplacedStudent],
    delimiter: str = ";",
) -> None:
    """
    Sauvegarde les élèves qui n'ont pas pu être placés dans un fichier CSV.
    
    Format: Nom, Classe, Spécialités demandées, Spécialité problématique, Raison
    """
    fieldnames = ["Nom", "Classe", "Spécialités demandées", "Spécialité problématique", "Raison"]
    
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        
        for unplaced in unplaced_students:
            choices_str = ", ".join(unplaced.student.choices) if unplaced.student.choices else "Aucune"
            writer.writerow({
                "Nom": unplaced.student.name,
                "Classe": unplaced.student.classe,
                "Spécialités demandées": choices_str,
                "Spécialité problématique": unplaced.failed_specialty,
                "Raison": unplaced.reason
            })
