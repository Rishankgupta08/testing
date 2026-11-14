from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class Patient:
    id: int
    name: str
    birth_date: date

    def age(self) -> int:
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

class Hospital:
    def __init__(self, name: str):
        self.name = name
        self.patients: List[Patient] = []

    def admit_patient(self, patient: Patient) -> None:
        self.patients.append(patient)

    def discharge_patient(self, patient_id: int) -> bool:
        for i, p in enumerate(self.patients):
            if p.id == patient_id:
                del self.patients[i]
                return True
        return False

    def list_patients(self) -> List[Patient]:
        return self.patients

if __name__ == "__main__":
    hospital = Hospital("General Hospital")
    p1 = Patient(id=1, name="John Doe", birth_date=date(1990, 5, 15))
    hospital.admit_patient(p1)
    print(f"Admitted patients: {[p.name for p in hospital.list_patients()]}")