# classes/planner.py
from __future__ import annotations
from typing import List, Optional, Dict
from classes.models import TimeSlot, Student, Assignment, GroupRecord, UnplacedStudent


class Planner:
    """
    Responsable de la répartition des élèves dans les créneaux / groupes.

    - groups_per_specialty: dict "spe" -> nb de groupes (salles) pour cette spé
    - max_per_group: capacité max par groupe (ici 8)
    """

    def __init__(
        self,
        time_slots: List[TimeSlot],
        groups_per_specialty: Dict[str, int],
        max_per_group: Optional[int] = None,
    ) -> None:
        self.time_slots = time_slots
        self.groups_per_specialty = groups_per_specialty
        self.max_per_group = max_per_group

        # spe -> [ [count_group0, ..., groupN], ... par créneau ]
        self._group_counts: Dict[str, List[List[int]]] = {}

        self.group_records: List[GroupRecord] = []
        self.unplaced_students: List[UnplacedStudent] = []

    # --- internes -----------------------------------------------------------

    def _get_counts_for_specialty(self, spe: str) -> List[List[int]]:
        if spe not in self._group_counts:
            nb_groups = self.groups_per_specialty.get(spe, 1)
            self._group_counts[spe] = [
                [0] * nb_groups for _ in range(len(self.time_slots))
            ]
        return self._group_counts[spe]

    # --- API principale -----------------------------------------------------

    def plan(self, students: List[Student]) -> None:
        num_slots = len(self.time_slots)

        for student in students:
            if len(student.choices) > num_slots:
                reason = f"A {len(student.choices)} vœux pour {num_slots} créneaux disponibles"
                self.unplaced_students.append(
                    UnplacedStudent(
                        student=student,
                        failed_specialty="N/A",
                        reason=reason
                    )
                )
                continue

            used_slots = set()
            placement_failed = False

            for spe in student.choices:
                counts_for_spe = self._get_counts_for_specialty(spe)
                nb_groups = len(counts_for_spe[0])

                candidates = []
                for slot_idx in range(num_slots):
                    if slot_idx in used_slots:
                        continue

                    for group_idx in range(nb_groups):
                        current_count = counts_for_spe[slot_idx][group_idx]
                        if (
                            self.max_per_group is not None
                            and current_count >= self.max_per_group
                        ):
                            continue

                        candidates.append((current_count, slot_idx, group_idx))

                if not candidates:
                    reason = "Tous les créneaux/groupes sont pleins ou incompatibles"
                    self.unplaced_students.append(
                        UnplacedStudent(
                            student=student,
                            failed_specialty=spe,
                            reason=reason
                        )
                    )
                    placement_failed = True
                    break

                # on choisit la case la moins remplie
                candidates.sort(key=lambda x: x[0])
                _, chosen_slot_idx, chosen_group_idx = candidates[0]

                counts_for_spe[chosen_slot_idx][chosen_group_idx] += 1
                used_slots.add(chosen_slot_idx)

                ts = self.time_slots[chosen_slot_idx]
                assignment = Assignment(
                    specialty=spe,
                    timeslot=ts,
                    group_index=chosen_group_idx,
                )
                student.add_assignment(assignment)

                self.group_records.append(
                    GroupRecord(
                        specialty=spe,
                        timeslot=ts,
                        group_index=chosen_group_idx,
                        student_name=student.name,
                        classe=student.classe,
                    )
                )
            
            # Si le placement a échoué, annuler toutes les affectations de cet élève
            if placement_failed:
                # Retirer les enregistrements de groupe de cet élève
                self.group_records = [
                    gr for gr in self.group_records
                    if gr.student_name != student.name
                ]
                # Réinitialiser les compteurs pour cet élève
                for assignment in student.assignments.values():
                    counts = self._get_counts_for_specialty(assignment.specialty)
                    counts[assignment.timeslot.index][assignment.group_index] -= 1
                # Vider les affectations de l'élève
                student.assignments.clear()
