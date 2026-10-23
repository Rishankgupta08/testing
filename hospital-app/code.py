import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class HospitalManagementApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management Application")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.patient_frame = tk.Frame(self.notebook)
        self.doctor_frame = tk.Frame(self.notebook)
        self.appointment_frame = tk.Frame(self.notebook)
        self.billing_frame = tk.Frame(self.notebook)

        self.notebook.add(self.patient_frame, text="Patient")
        self.notebook.add(self.doctor_frame, text="Doctor")
        self.notebook.add(self.appointment_frame, text="Appointment")
        self.notebook.add(self.billing_frame, text="Billing")

        self.patient_widgets()
        self.doctor_widgets()
        self.appointment_widgets()
        self.billing_widgets()

        self.conn = sqlite3.connect("hospital.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                contact TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY,
                name TEXT,
                specialty TEXT,
                contact TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY,
                patient_id INTEGER,
                doctor_id INTEGER,
                date TEXT,
                time TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY,
                patient_id INTEGER,
                amount REAL,
                date TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        """)

        self.conn.commit()

    def patient_widgets(self):
        tk.Label(self.patient_frame, text="Patient Name").grid(row=0, column=0)
        tk.Label(self.patient_frame, text="Age").grid(row=1, column=0)
        tk.Label(self.patient_frame, text="Contact").grid(row=2, column=0)

        self.patient_name = tk.Entry(self.patient_frame)
        self.patient_age = tk.Entry(self.patient_frame)
        self.patient_contact = tk.Entry(self.patient_frame)

        self.patient_name.grid(row=0, column=1)
        self.patient_age.grid(row=1, column=1)
        self.patient_contact.grid(row=2, column=1)

        tk.Button(self.patient_frame, text="Add Patient", command=self.add_patient).grid(row=3, column=0, columnspan=2)

        self.patient_list = tk.Listbox(self.patient_frame)
        self.patient_list.grid(row=4, column=0, columnspan=2)

        tk.Button(self.patient_frame, text="View Patients", command=self.view_patients).grid(row=5, column=0, columnspan=2)

    def doctor_widgets(self):
        tk.Label(self.doctor_frame, text="Doctor Name").grid(row=0, column=0)
        tk.Label(self.doctor_frame, text="Specialty").grid(row=1, column=0)
        tk.Label(self.doctor_frame, text="Contact").grid(row=2, column=0)

        self.doctor_name = tk.Entry(self.doctor_frame)
        self.doctor_specialty = tk.Entry(self.doctor_frame)
        self.doctor_contact = tk.Entry(self.doctor_frame)

        self.doctor_name.grid(row=0, column=1)
        self.doctor_specialty.grid(row=1, column=1)
        self.doctor_contact.grid(row=2, column=1)

        tk.Button(self.doctor_frame, text="Add Doctor", command=self.add_doctor).grid(row=3, column=0, columnspan=2)

        self.doctor_list = tk.Listbox(self.doctor_frame)
        self.doctor_list.grid(row=4, column=0, columnspan=2)

        tk.Button(self.doctor_frame, text="View Doctors", command=self.view_doctors).grid(row=5, column=0, columnspan=2)

    def appointment_widgets(self):
        tk.Label(self.appointment_frame, text="Patient ID").grid(row=0, column=0)
        tk.Label(self.appointment_frame, text="Doctor ID").grid(row=1, column=0)
        tk.Label(self.appointment_frame, text="Date").grid(row=2, column=0)
        tk.Label(self.appointment_frame, text="Time").grid(row=3, column=0)

        self.appointment_patient_id = tk.Entry(self.appointment_frame)
        self.appointment_doctor_id = tk.Entry(self.appointment_frame)
        self.appointment_date = tk.Entry(self.appointment_frame)
        self.appointment_time = tk.Entry(self.appointment_frame)

        self.appointment_patient_id.grid(row=0, column=1)
        self.appointment_doctor_id.grid(row=1, column=1)
        self.appointment_date.grid(row=2, column=1)
        self.appointment_time.grid(row=3, column=1)

        tk.Button(self.appointment_frame, text="Add Appointment", command=self.add_appointment).grid(row=4, column=0, columnspan=2)

        self.appointment_list = tk.Listbox(self.appointment_frame)
        self.appointment_list.grid(row=5, column=0, columnspan=2)

        tk.Button(self.appointment_frame, text="View Appointments", command=self.view_appointments).grid(row=6, column=0, columnspan=2)

    def billing_widgets(self):
        tk.Label(self.billing_frame, text="Patient ID").grid(row=0, column=0)
        tk.Label(self.billing_frame, text="Amount").grid(row=1, column=0)
        tk.Label(self.billing_frame, text="Date").grid(row=2, column=0)

        self.billing_patient_id = tk.Entry(self.billing_frame)
        self.billing_amount = tk.Entry(self.billing_frame)
        self.billing_date = tk.Entry(self.billing_frame)

        self.billing_patient_id.grid(row=0, column=1)
        self.billing_amount.grid(row=1, column=1)
        self.billing_date.grid(row=2, column=1)

        tk.Button(self.billing_frame, text="Add Bill", command=self.add_bill).grid(row=3, column=0, columnspan=2)

        self.billing_list = tk.Listbox(self.billing_frame)
        self.billing_list.grid(row=4, column=0, columnspan=2)

        tk.Button(self.billing_frame, text="View Bills", command=self.view_bills).grid(row=5, column=0, columnspan=2)

    def add_patient(self):
        self.cursor.execute("INSERT INTO patients (name, age, contact) VALUES (?, ?, ?)",
                            (self.patient_name.get(), self.patient_age.get(), self.patient_contact.get()))
        self.conn.commit()
        self.patient_name.delete(0, tk.END)
        self.patient_age.delete(0, tk.END)
        self.patient_contact.delete(0, tk.END)

    def view_patients(self):
        self.patient_list.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM patients")
        patients = self.cursor.fetchall()
        for patient in patients:
            self.patient_list.insert(tk.END, patient)

    def add_doctor(self):
        self.cursor.execute("INSERT INTO doctors (name, specialty, contact) VALUES (?, ?, ?)",
                            (self.doctor_name.get(), self.doctor_specialty.get(), self.doctor_contact.get()))
        self.conn.commit()
        self.doctor_name.delete(0, tk.END)
        self.doctor_specialty.delete(0, tk.END)
        self.doctor_contact.delete(0, tk.END)

    def view_doctors(self):
        self.doctor_list.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM doctors")
        doctors = self.cursor.fetchall()
        for doctor in doctors:
            self.doctor_list.insert(tk.END, doctor)

    def add_appointment(self):
        self.cursor.execute("INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (?, ?, ?, ?)",
                            (self.appointment_patient_id.get(), self.appointment_doctor_id.get(), self.appointment_date.get(), self.appointment_time.get()))
        self.conn.commit()
        self.appointment_patient_id.delete(0, tk.END)
        self.appointment_doctor_id.delete(0, tk.END)
        self.appointment_date.delete(0, tk.END)
        self.appointment_time.delete(0, tk.END)

    def view_appointments(self):
        self.appointment_list.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM appointments")
        appointments = self.cursor.fetchall()
        for appointment in appointments:
            self.appointment_list.insert(tk.END, appointment)

    def add_bill(self):
        self.cursor.execute("INSERT INTO bills (patient_id, amount, date) VALUES (?, ?, ?)",
                            (self.billing_patient_id.get(), self.billing_amount.get(), self.billing_date.get()))
        self.conn.commit()
        self.billing_patient_id.delete(0, tk.END)
        self.billing_amount.delete(0, tk.END)
        self.billing_date.delete(0, tk.END)

    def view_bills(self):
        self.billing_list.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM bills")
        bills = self.cursor.fetchall()
        for bill in bills:
            self.billing_list.insert(tk.END, bill)

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementApplication(root)
    root.mainloop()