# main.py
from classes.models import TimeSlot
from classes.planner import Planner
from utils.utils import (
    load_students_from_csv,
    save_planning_per_student,
    save_planning_per_group_formatted,
    compute_groups_per_specialty,
)

# --- Configuration métier ---

TIME_SLOTS = [
    TimeSlot(0, "09:00-09:25"),
    TimeSlot(1, "09:30-09:55"),
    TimeSlot(2, "10:05-10:30"),
    TimeSlot(3, "10:35-11:00"),
    TimeSlot(4, "11:00-11:25"),
]


def main() -> None:
    input_path = input("Chemin du fichier CSV d'entrée : ").strip()
    if not input_path:
        print("Aucun fichier fourni, arrêt.")
        return
    
    def ask_int(prompt: str, default: int) -> int:
        while True:
            val = input(f"{prompt} (défaut={default}) : ").strip()
            if val == "":
                return default
            try:
                num = int(val)
                if num > 0:
                    return num
                print("Veuillez entrer un nombre entier positif.")
            except ValueError:
                print("Valeur invalide, entrez un entier.")

    MAX_GROUPS_PER_SPECIALTY = ask_int("Nombre max de groupes par spécialité", 6)
    MIN_STUDENTS_PER_GROUP = ask_int("Nombre min d'élèves par groupe", 5)
    MAX_STUDENTS_PER_GROUP = ask_int("Nombre max d'élèves par groupe", 8)

    print("Chargement des élèves...")
    students = load_students_from_csv(input_path)
    print(f"{len(students)} élèves chargés.")

    groups_per_spe = compute_groups_per_specialty(
        students,
        TIME_SLOTS,
        MIN_STUDENTS_PER_GROUP,
        MAX_STUDENTS_PER_GROUP,
        MAX_GROUPS_PER_SPECIALTY,
    )

    print("Groupes par spécialité :")
    for spe, g in groups_per_spe.items():
        print(f"  - {spe}: {g} groupe(s)")

    planner = Planner(
        time_slots=TIME_SLOTS,
        groups_per_specialty=groups_per_spe,
        max_per_group=MAX_STUDENTS_PER_GROUP,
    )

    print("Répartition en cours...")
    planner.plan(students)
    print("Répartition terminée.")

    out_students = input("Chemin de sortie pour le planning PAR ÉLÈVE (.csv) : ").strip()
    if out_students:
        save_planning_per_student(out_students, students, TIME_SLOTS)
        print(f"Planning par élève enregistré dans {out_students}")

    out_groups = input("Chemin de sortie pour le planning PAR GROUPE (.csv) : ").strip()
    if out_groups:
        save_planning_per_group_formatted(
            out_groups,
            planner.group_records,
            TIME_SLOTS,
        )
        print(f"Planning par groupe enregistré dans {out_groups}")

    print("Terminé.")

if __name__ == "__main__":
    main()
