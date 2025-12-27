# gui_main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import webbrowser

from classes.models import TimeSlot
from classes.planner import Planner
from utils.utils import (
    load_students_from_csv,
    save_planning_per_student,
    save_planning_per_group_formatted,
    compute_groups_per_specialty,
    save_unplaced_students,
)


class ContactWindow(tk.Toplevel):
    """Fenêtre de contact pour suggestions et améliorations"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Contact")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Centrer la fenêtre
        self.transient(parent)
        
        self._build_ui()
    
    def _build_ui(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title_label = tk.Label(
            main_frame,
            text="📧 Contactez-moi",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Message d'introduction
        intro_text = (
            "Vous avez des suggestions d'améliorations, des bugs à signaler "
            "ou des questions sur le logiciel ?\n\n"
            "N'hésitez pas à me contacter !"
        )
        intro_label = tk.Label(
            main_frame,
            text=intro_text,
            font=("Arial", 10),
            justify="center",
            wraplength=450
        )
        intro_label.pack(pady=(0, 30))
        
        # Frame des informations de contact
        contact_frame = ttk.LabelFrame(main_frame, text="Informations de contact")
        contact_frame.pack(fill="x", pady=10)
        
        # Email
        email_frame = ttk.Frame(contact_frame)
        email_frame.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(
            email_frame,
            text="📧 Email :",
            font=("Arial", 10, "bold")
        ).pack(side="left")
        
        email_link = tk.Label(
            email_frame,
            text="yvan.kerdanet@example.com",
            font=("Arial", 10),
            foreground="blue",
            cursor="hand2"
        )
        email_link.pack(side="left", padx=(10, 0))
        email_link.bind("<Button-1>", lambda e: self.open_email())
        
        # GitHub
        github_frame = ttk.Frame(contact_frame)
        github_frame.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(
            github_frame,
            text="🐙 GitHub :",
            font=("Arial", 10, "bold")
        ).pack(side="left")
        
        github_link = tk.Label(
            github_frame,
            text="github.com/KerdanetYvan",
            font=("Arial", 10),
            foreground="blue",
            cursor="hand2"
        )
        github_link.pack(side="left", padx=(10, 0))
        github_link.bind("<Button-1>", lambda e: self.open_github())
        
        # Repository
        repo_frame = ttk.Frame(contact_frame)
        repo_frame.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(
            repo_frame,
            text="📦 Repository :",
            font=("Arial", 10, "bold")
        ).pack(side="left")
        
        repo_link = tk.Label(
            repo_frame,
            text="Ouvrir le dépôt GitHub",
            font=("Arial", 10),
            foreground="blue",
            cursor="hand2"
        )
        repo_link.pack(side="left", padx=(10, 0))
        repo_link.bind("<Button-1>", lambda e: self.open_repo())
        
        # Note
        note_text = (
            "💡 Pour signaler un bug ou proposer une amélioration,\n"
            "vous pouvez également créer une issue sur GitHub."
        )
        note_label = tk.Label(
            main_frame,
            text=note_text,
            font=("Arial", 9),
            foreground="gray",
            justify="center"
        )
        note_label.pack(pady=(20, 0))
        
        # Bouton fermer
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(
            button_frame,
            text="Fermer",
            command=self.destroy
        ).pack()
    
    def open_email(self):
        """Ouvrir le client email par défaut"""
        email = "kerdanety@gmail.com"
        subject = "Planification des Spécialités - Contact"
        webbrowser.open(f"mailto:{email}?subject={subject}")
    
    def open_github(self):
        """Ouvrir le profil GitHub"""
        webbrowser.open("https://github.com/KerdanetYvan")
    
    def open_repo(self):
        """Ouvrir le repository GitHub du projet"""
        webbrowser.open("https://github.com/KerdanetYvan/planification_spe")


class HelpWindow(tk.Toplevel):
    """Fenêtre d'aide expliquant le fonctionnement du logiciel"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Comment ça marche ?")
        self.geometry("700x600")
        self.resizable(True, True)
        
        # Centrer la fenêtre
        self.transient(parent)
        
        self._build_ui()
    
    def _build_ui(self):
        # Frame principal avec scrollbar
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Zone de texte avec scrollbar
        text_widget = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=("Arial", 10),
            padx=10,
            pady=10
        )
        text_widget.pack(fill="both", expand=True)
        
        # Contenu de l'aide
        help_text = """GUIDE D'UTILISATION - Planification des Spécialités

═══════════════════════════════════════════════════════════════

1. PRÉSENTATION

Ce logiciel permet de répartir automatiquement les élèves dans des groupes de spécialités en fonction de leurs choix, tout en respectant des contraintes de taille de groupe et de nombre de créneaux horaires.


2. PRÉREQUIS - FORMAT DU FICHIER CSV

Le fichier d'entrée doit être un fichier CSV (valeurs séparées par des virgules ou points-virgules) avec les colonnes suivantes :

┌─────────────────────────────────────────────────────────┐
│  Nom  │  Prénom  │  Spécialité 1  │  Spécialité 2  │...│
├─────────────────────────────────────────────────────────┤
│ Dupont │  Marie   │     Maths      │      PC        │...│
│ Martin │  Pierre  │     SVT        │    HGGSP       │...│
│  ...   │   ...    │      ...       │      ...       │...│
└─────────────────────────────────────────────────────────┘

IMPORTANT :
• La première ligne doit contenir les en-têtes de colonnes
• Les colonnes "Nom" et "Prénom" sont obligatoires
• Les colonnes de spécialités peuvent avoir n'importe quel nom (ex: "Spé 1", "Choix 1", etc.)
• Chaque élève doit avoir au moins une spécialité renseignée
• Le séparateur peut être une virgule (,) ou un point-virgule (;)


3. ÉTAPES D'UTILISATION

Étape 1 : Sélectionner le fichier CSV
   → Cliquez sur "Parcourir..." et sélectionnez votre fichier d'élèves

Étape 2 : Configurer les paramètres
   • Min. élèves par groupe/créneau : Nombre minimum d'élèves dans un groupe
   • Max. élèves par groupe/créneau : Nombre maximum d'élèves dans un groupe
   • Max. groupes par spécialité : Nombre maximum de créneaux pour chaque spécialité

Étape 3 : Générer les plannings
   → Cliquez sur "Générer les plannings"
   → Une fenêtre de résultats s'affichera avec un résumé

Étape 4 : Enregistrer les résultats
   Vous pouvez enregistrer au choix :
   • Planning par élève : Liste de tous les élèves avec leurs créneaux attribués
   • Planning par groupe : Liste des élèves pour chaque groupe de spécialité
   • Élèves non placés : Si certains élèves n'ont pas pu être placés


4. EXEMPLES DE PARAMÈTRES

Configuration petite classe (120-150 élèves) :
   • Min : 8 élèves
   • Max : 12 élèves
   • Max groupes : 3-4

Configuration grande classe (200+ élèves) :
   • Min : 10 élèves
   • Max : 15 élèves
   • Max groupes : 5-6


5. CONSEILS

✓ Vérifiez que votre fichier CSV est bien formaté avant de l'importer
✓ Adaptez les paramètres en fonction du nombre d'élèves total
✓ Si des élèves ne peuvent pas être placés, essayez d'ajuster les paramètres
✓ Sauvegardez tous les fichiers générés pour référence


6. EN CAS DE PROBLÈME

• "Aucun élève trouvé" → Vérifiez le format de votre CSV
• "Élèves non placés" → Augmentez le max. groupes par spécialité ou ajustez les tailles min/max
• Erreur de lecture → Vérifiez l'encodage du fichier (UTF-8 recommandé)


═══════════════════════════════════════════════════════════════

Pour toute question ou assistance, contactez l'auteur à cette adresse : kerdanety@gmail.com ou via ce site internet : kerdanetyvan.fr

© 2025 Yvan KERDANET
"""
        
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")  # Lecture seule
        
        # Bouton fermer
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Fermer",
            command=self.destroy
        ).pack(side="right")


class ResultsWindow(tk.Toplevel):
    """Fenêtre de résultats avec options d'export"""
    
    def __init__(self, parent, students, planner, time_slots, min_group=5, max_group=8, max_groups_per_spe=5):
        super().__init__(parent)
        
        self.students = students
        self.planner = planner
        self.time_slots = time_slots
        self.min_group = min_group
        self.max_group = max_group
        self.max_groups_per_spe = max_groups_per_spe
        
        self.title("Résultats de la planification")
        
        # Hauteur dynamique selon s'il y a des élèves non placés
        height = 650 if planner.unplaced_students else 420
        self.geometry(f"600x{height}")
        self.resizable(False, False)
        
        # Centrer la fenêtre
        self.transient(parent)
        self.grab_set()
        
        self._build_ui()
        
    def _build_ui(self):
        padding = {"padx": 10, "pady": 5}
        
        # Frame de résumé
        summary_frame = ttk.LabelFrame(self, text="Résumé")
        summary_frame.pack(fill="x", padx=10, pady=10)
        
        num_placed = len(self.students) - len(self.planner.unplaced_students)
        total_students = len(self.students)
        
        ttk.Label(
            summary_frame, 
            text=f"✓ Génération terminée avec succès",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", **padding)
        
        ttk.Label(summary_frame, text="Élèves placés :").grid(
            row=1, column=0, sticky="w", **padding
        )
        ttk.Label(
            summary_frame, 
            text=f"{num_placed} / {total_students}",
            font=("Arial", 9, "bold")
        ).grid(row=1, column=1, sticky="w", **padding)
        
        if self.planner.unplaced_students:
            ttk.Label(summary_frame, text="Élèves non placés :").grid(
                row=2, column=0, sticky="w", **padding
            )
            # Utiliser tk.Label pour pouvoir mettre du texte en rouge
            label_unplaced = tk.Label(
                summary_frame, 
                text=f"{len(self.planner.unplaced_students)}",
                font=("Arial", 9, "bold"),
                foreground="red"
            )
            label_unplaced.grid(row=2, column=1, sticky="w", **padding)
        
        # Frame de conseils si élèves non placés
        if self.planner.unplaced_students:
            advice_frame = ttk.LabelFrame(self, text="💡 Conseils pour améliorer la répartition")
            advice_frame.pack(fill="x", padx=10, pady=10)
            
            advice_text = self._generate_advice()
            
            advice_label = tk.Label(
                advice_frame,
                text=advice_text,
                font=("Arial", 9),
                justify="left",
                wraplength=560,
                foreground="#1a5490"
            )
            advice_label.pack(anchor="w", **padding)
        
        # Frame d'export
        export_frame = ttk.LabelFrame(self, text="Enregistrer les résultats")
        export_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Export par élève
        student_frame = ttk.Frame(export_frame)
        student_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(
            student_frame, 
            text="Planning par élève",
            font=("Arial", 9, "bold")
        ).pack(anchor="w")
        
        ttk.Label(
            student_frame,
            text="Liste tous les élèves avec leurs créneaux de spécialités attribués.",
            foreground="gray"
        ).pack(anchor="w")
        
        ttk.Button(
            student_frame,
            text="Enregistrer sous...",
            command=self.save_per_student
        ).pack(anchor="w", pady=(5, 0))
        
        ttk.Separator(export_frame, orient="horizontal").pack(fill="x", padx=10, pady=5)
        
        # Export par groupe
        group_frame = ttk.Frame(export_frame)
        group_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(
            group_frame,
            text="Planning par groupe",
            font=("Arial", 9, "bold")
        ).pack(anchor="w")
        
        ttk.Label(
            group_frame,
            text="Affiche pour chaque spécialité et créneau la liste des élèves du groupe.",
            foreground="gray"
        ).pack(anchor="w")
        
        ttk.Button(
            group_frame,
            text="Enregistrer sous...",
            command=self.save_per_group
        ).pack(anchor="w", pady=(5, 0))
        
        # Export élèves non placés (si nécessaire)
        if self.planner.unplaced_students:
            ttk.Separator(export_frame, orient="horizontal").pack(fill="x", padx=10, pady=5)
            
            unplaced_frame = ttk.Frame(export_frame)
            unplaced_frame.pack(fill="x", padx=10, pady=10)
            
            # Utiliser tk.Label pour pouvoir mettre du texte en rouge
            tk.Label(
                unplaced_frame,
                text="Élèves non placés",
                font=("Arial", 9, "bold"),
                foreground="red"
            ).pack(anchor="w")
            
            ttk.Label(
                unplaced_frame,
                text=f"Liste des {len(self.planner.unplaced_students)} élève(s) qui n'ont pas pu être placés."
            ).pack(anchor="w")
            
            ttk.Button(
                unplaced_frame,
                text="Enregistrer sous...",
                command=self.save_unplaced
            ).pack(anchor="w", pady=(5, 0))
        
        # Bouton fermer
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(
            button_frame,
            text="Fermer",
            command=self.destroy
        ).pack(side="right")
    
    def _generate_advice(self):
        """Génère des conseils personnalisés pour améliorer la répartition"""
        num_unplaced = len(self.planner.unplaced_students)
        total_students = len(self.students)
        
        # Calculer des suggestions
        suggestions = []
        
        # Suggestion 1: Augmenter le max par groupe
        new_max = self.max_group + 2
        suggestions.append(f"• Augmenter le max. élèves par groupe à {new_max}")
        
        # Suggestion 2: Augmenter le nombre de groupes si pas déjà élevé
        if self.max_groups_per_spe < len(self.time_slots):
            new_max_groups = min(self.max_groups_per_spe + 1, len(self.time_slots))
            suggestions.append(f"• Augmenter le max. groupes par spécialité à {new_max_groups}")
        
        # Suggestion 3: Diminuer le min si pas trop bas
        if self.min_group > 3:
            new_min = max(3, self.min_group - 1)
            suggestions.append(f"• Diminuer le min. élèves par groupe à {new_min}")
        
        advice = f"Pour placer les {num_unplaced} élève(s) restant(s), vous pouvez essayer de :\n\n"
        advice += "\n".join(suggestions)
        advice += "\n\nRecommandation : Privilégiez d'abord l'augmentation du nombre de groupes pour maintenir des effectifs raisonnables."
        
        return advice
    
    def save_per_student(self):
        """Enregistrer le planning par élève"""
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Enregistrer le planning par élève",
            defaultextension=".csv",
            filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")],
        )
        
        if file_path:
            try:
                save_planning_per_student(file_path, self.students, self.time_slots)
                messagebox.showinfo(
                    "Succès",
                    "Le planning par élève a été enregistré avec succès.",
                    parent=self
                )
            except Exception as e:
                messagebox.showerror(
                    "Erreur",
                    f"Erreur lors de l'enregistrement :\n{str(e)}",
                    parent=self
                )
    
    def save_per_group(self):
        """Enregistrer le planning par groupe"""
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Enregistrer le planning par groupe",
            defaultextension=".csv",
            filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")],
        )
        
        if file_path:
            try:
                save_planning_per_group_formatted(
                    file_path,
                    self.planner.group_records,
                    self.time_slots,
                )
                messagebox.showinfo(
                    "Succès",
                    "Le planning par groupe a été enregistré avec succès.",
                    parent=self
                )
            except Exception as e:
                messagebox.showerror(
                    "Erreur",
                    f"Erreur lors de l'enregistrement :\n{str(e)}",
                    parent=self
                )
    
    def save_unplaced(self):
        """Enregistrer la liste des élèves non placés"""
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Enregistrer les élèves non placés",
            defaultextension=".csv",
            filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")],
        )
        
        if file_path:
            try:
                save_unplaced_students(file_path, self.planner.unplaced_students)
                messagebox.showinfo(
                    "Succès",
                    "La liste des élèves non placés a été enregistrée avec succès.",
                    parent=self
                )
            except Exception as e:
                messagebox.showerror(
                    "Erreur",
                    f"Erreur lors de l'enregistrement :\n{str(e)}",
                    parent=self
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
        self.geometry("650x300")
        self.resizable(False, False)

        self.input_path = tk.StringVar()
        self.min_group_var = tk.StringVar(value="5")
        self.max_group_var = tk.StringVar(value="8")
        self.max_groups_per_spe_var = tk.StringVar(value="5")
        self.status_var = tk.StringVar(value="En attente de fichier CSV...")

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
            text="❓ Comment ça marche ?",
            command=self.show_help
        ).pack(side="left")
        
        ttk.Button(
            action_frame,
            text="📧 Contact",
            command=self.show_contact
        ).pack(side="left", padx=(5, 0))

        ttk.Button(
            action_frame,
            text="Générer les plannings",
            command=self.run_planning,
        ).pack(side="right")

        # Copyright
        copyright_label = tk.Label(
            self,
            text="© 2025 Yvan KERDANET",
            font=("Arial", 8),
            foreground="gray"
        )
        copyright_label.pack(side="bottom", pady=(0, 2))

        # Barre de statut
        status_bar = ttk.Label(self, textvariable=self.status_var, anchor="w")
        status_bar.pack(fill="x", side="bottom", padx=5, pady=5)

    # --- Actions ----------------------------------------------------

    def show_help(self):
        """Afficher la fenêtre d'aide"""
        HelpWindow(self)
    
    def show_contact(self):
        """Afficher la fenêtre de contact"""
        ContactWindow(self)

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

        # 6. Ouvrir la fenêtre de résultats
        self.status_var.set("Terminé.")
        ResultsWindow(self, students, planner, TIME_SLOTS, min_group, max_group, max_groups_per_spe)


if __name__ == "__main__":
    app = PlanningApp()
    app.mainloop()
