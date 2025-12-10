# gui_main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from classes.models import TimeSlot
from classes.planner import Planner
from utils.utils import (
    load_students_from_csv,
    save_planning_per_student,
    save_planning_per_group_formatted,
    compute_groups_per_specialty,
    save_unplaced_students,
)

# --- Config des créneaux (même chose que dans ton main actuel) ---

TIME_SLOTS = [
    TimeSlot(0, "09:00-09:25"),
    TimeSlot(1, "09:30-09:55"),
    TimeSlot(2, "10:05-10:30"),
    TimeSlot(3, "10:35-11:00"),
    TimeSlot(4, "11:00-11:25"),
]


class PlanningApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Planning des spécialités")
        self.geometry("650x260")
        self.resizable(False, False)

        self.input_path = tk.StringVar()
        self.min_group_var = tk.StringVar(value="5")
        self.max_group_var = tk.StringVar(value="8")
        self.max_groups_per_spe_var = tk.StringVar(value="5")
        self.status_var = tk.StringVar(value="Prêt.")

        self._build_ui()

    # --- UI ---------------------------------------------------------

    def _build_ui(self):
        padding = {"padx": 10, "pady": 5}

        # Frame fichier
        file_frame = ttk.LabelFrame(self, text="Fichier d'élèves")
        file_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(file_frame, text="CSV des choix de spécialités :").grid(
            row=0, column=0, sticky="w", **padding
        )

        path_entry = ttk.Entry(file_frame, textvariable=self.input_path, width=50)
        path_entry.grid(row=0, column=1, sticky="we", **padding)

        ttk.Button(
            file_frame,
            text="Parcourir...",
            command=self.browse_input_file,
        ).grid(row=0, column=2, **padding)

        file_frame.columnconfigure(1, weight=1)

        # Frame paramètres
        params_frame = ttk.LabelFrame(self, text="Paramètres de répartition")
        params_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(params_frame, text="Min. élèves par groupe/créneau :").grid(
            row=0, column=0, sticky="w", **padding
        )
        ttk.Entry(params_frame, textvariable=self.min_group_var, width=5).grid(
            row=0, column=1, sticky="w", **padding
        )

        ttk.Label(params_frame, text="Max. élèves par groupe/créneau :").grid(
            row=1, column=0, sticky="w", **padding
        )
        ttk.Entry(params_frame, textvariable=self.max_group_var, width=5).grid(
            row=1, column=1, sticky="w", **padding
        )

        ttk.Label(params_frame, text="Max. groupes par spécialité :").grid(
            row=2, column=0, sticky="w", **padding
        )
        ttk.Entry(params_frame, textvariable=self.max_groups_per_spe_var, width=5).grid(
            row=2, column=1, sticky="w", **padding
        )

        # Frame actions
        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(
            action_frame,
            text="Générer les plannings",
            command=self.run_planning,
        ).pack(side="right")

        # Barre de statut
        status_bar = ttk.Label(self, textvariable=self.status_var, anchor="w")
        status_bar.pack(fill="x", side="bottom", padx=5, pady=5)

    # --- Actions ----------------------------------------------------

    def browse_input_file(self):
        path = filedialog.askopenfilename(
            title="Choisir le fichier CSV d'entrée",
            filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")],
        )
        if path:
            self.input_path.set(path)

    def _parse_int(self, value_str: str, field_name: str):
        value_str = value_str.strip()
        if not value_str:
            raise ValueError(f"Le champ '{field_name}' est vide.")
        try:
            value = int(value_str)
        except ValueError:
            raise ValueError(f"Le champ '{field_name}' doit être un entier.")
        if value <= 0:
            raise ValueError(f"Le champ '{field_name}' doit être > 0.")
        return value

    def run_planning(self):
        # 1. Vérif fichier
        input_path = self.input_path.get().strip()
        if not input_path:
            messagebox.showwarning(
                "Fichier manquant",
                "Veuillez sélectionner un fichier CSV d'élèves.",
            )
            return

        # 2. Lecture des paramètres
        try:
            min_group = self._parse_int(
                self.min_group_var.get(), "Min. élèves par groupe/créneau"
            )
            max_group = self._parse_int(
                self.max_group_var.get(), "Max. élèves par groupe/créneau"
            )
            max_groups_per_spe = self._parse_int(
                self.max_groups_per_spe_var.get(), "Max. groupes par spécialité"
            )
        except ValueError as e:
            messagebox.showerror("Paramètre invalide", str(e))
            return

        if min_group > max_group:
            messagebox.showerror(
                "Paramètres incohérents",
                "Le minimum par groupe/créneau doit être inférieur ou égal au maximum.",
            )
            return

        self.status_var.set("Chargement des élèves...")
        self.update_idletasks()

        # 3. Charger les élèves
        try:
            students = load_students_from_csv(input_path)
        except Exception as e:
            messagebox.showerror("Erreur de lecture", str(e))
            self.status_var.set("Erreur de lecture du fichier.")
            return

        if not students:
            messagebox.showerror(
                "Aucun élève",
                "Le fichier ne contient aucun élève.",
            )
            self.status_var.set("Aucun élève.")
            return

        # 4. Calcul des groupes par spé
        from utils.utils import compute_groups_per_specialty  # si pas déjà importé en haut

        self.status_var.set("Calcul des groupes par spécialité...")
        self.update_idletasks()

        try:
            groups_per_spe = compute_groups_per_specialty(
                students,
                TIME_SLOTS,
                min_group,
                max_group,
                max_groups_per_spe,
            )
        except Exception as e:
            messagebox.showerror("Erreur de calcul des groupes", str(e))
            self.status_var.set("Erreur lors du calcul des groupes.")
            return

        # 5. Répartition
        self.status_var.set("Répartition des élèves...")
        self.update_idletasks()

        try:
            planner = Planner(
                time_slots=TIME_SLOTS,
                groups_per_specialty=groups_per_spe,
                max_per_group=max_group,
            )
            planner.plan(students)
        except Exception as e:
            messagebox.showerror("Erreur de répartition", str(e))
            self.status_var.set("Erreur lors de la répartition.")
            return

        # 5b. Gérer les élèves non placés
        if planner.unplaced_students:
            num_unplaced = len(planner.unplaced_students)
            response = messagebox.askyesno(
                "Élèves non placés",
                f"{num_unplaced} élève(s) n'ont pas pu être placés.\n"
                f"Voulez-vous sauvegarder la liste des élèves non placés ?",
            )
            
            if response:
                unplaced_file = filedialog.asksaveasfilename(
                    title="Enregistrer les élèves non placés",
                    defaultextension=".csv",
                    filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")],
                )
                
                if unplaced_file:
                    try:
                        save_unplaced_students(unplaced_file, planner.unplaced_students)
                    except Exception as e:
                        messagebox.showerror(
                            "Erreur d'enregistrement (élèves non placés)", str(e)
                        )

        # 6. Choix fichiers de sortie
        self.status_var.set("Choix du fichier de sortie (par élève)...")
        self.update_idletasks()

        out_students = filedialog.asksaveasfilename(
            title="Enregistrer le planning PAR ÉLÈVE",
            defaultextension=".csv",
            filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")],
        )

        if out_students:
            try:
                save_planning_per_student(out_students, students, TIME_SLOTS)
            except Exception as e:
                messagebox.showerror(
                    "Erreur d'enregistrement (par élève)", str(e)
                )
                self.status_var.set("Erreur à l'enregistrement (par élève).")
                return

        self.status_var.set("Choix du fichier de sortie (par groupe)...")
        self.update_idletasks()

        out_groups = filedialog.asksaveasfilename(
            title="Enregistrer le planning PAR GROUPE",
            defaultextension=".csv",
            filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")],
        )

        if out_groups:
            try:
                save_planning_per_group_formatted(
                    out_groups,
                    planner.group_records,
                    TIME_SLOTS,
                )
            except Exception as e:
                messagebox.showerror(
                    "Erreur d'enregistrement (par groupe)", str(e)
                )
                self.status_var.set("Erreur à l'enregistrement (par groupe).")
                return

        self.status_var.set("Terminé.")
        
        # Message de succès personnalisé selon s'il y a des élèves non placés
        if planner.unplaced_students:
            num_placed = len(students) - len(planner.unplaced_students)
            messagebox.showinfo(
                "Succès partiel",
                f"Les plannings ont été générés.\n"
                f"{num_placed} élèves placés sur {len(students)}.\n"
                f"{len(planner.unplaced_students)} élève(s) non placé(s).",
            )
        else:
            messagebox.showinfo(
                "Succès",
                "Les plannings ont été générés avec succès.\n"
                f"Tous les {len(students)} élèves ont été placés.",
            )


if __name__ == "__main__":
    app = PlanningApp()
    app.mainloop()
