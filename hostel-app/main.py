import tkinter as tk
from tkinter import ttk, messagebox

class HostelManagementApplication:
    def __init__(self, root):
        self.root = root
        self.root.title('Hostel Management Application')
        self.root.geometry('800x600')

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.student_frame = tk.Frame(self.notebook)
        self.room_frame = tk.Frame(self.notebook)
        self.fee_frame = tk.Frame(self.notebook)

        self.notebook.add(self.student_frame, text='Student Records')
        self.notebook.add(self.room_frame, text='Room Assignments')
        self.notebook.add(self.fee_frame, text='Fee Tracking')

        self.student_records()
        self.room_assignments()
        self.fee_tracking()

    def student_records(self):
        tk.Label(self.student_frame, text='Student ID').grid(row=0, column=0)
        tk.Label(self.student_frame, text='Name').grid(row=1, column=0)
        tk.Label(self.student_frame, text='Email').grid(row=2, column=0)

        self.student_id = tk.Entry(self.student_frame)
        self.student_name = tk.Entry(self.student_frame)
        self.student_email = tk.Entry(self.student_frame)

        self.student_id.grid(row=0, column=1)
        self.student_name.grid(row=1, column=1)
        self.student_email.grid(row=2, column=1)

        tk.Button(self.student_frame, text='Add Student', command=self.add_student).grid(row=3, column=0)
        tk.Button(self.student_frame, text='Update Student', command=self.update_student).grid(row=3, column=1)
        tk.Button(self.student_frame, text='Delete Student', command=self.delete_student).grid(row=3, column=2)

        self.student_tree = ttk.Treeview(self.student_frame)
        self.student_tree['columns'] = ('Student ID', 'Name', 'Email')

        self.student_tree.column('#0', width=0, stretch=tk.NO)
        self.student_tree.column('Student ID', anchor=tk.W, width=100)
        self.student_tree.column('Name', anchor=tk.W, width=100)
        self.student_tree.column('Email', anchor=tk.W, width=100)

        self.student_tree.heading('#0', text='', anchor=tk.W)
        self.student_tree.heading('Student ID', text='Student ID', anchor=tk.W)
        self.student_tree.heading('Name', text='Name', anchor=tk.W)
        self.student_tree.heading('Email', text='Email', anchor=tk.W)

        self.student_tree.grid(row=4, column=0, columnspan=3)

        self.students = []

    def room_assignments(self):
        tk.Label(self.room_frame, text='Room Number').grid(row=0, column=0)
        tk.Label(self.room_frame, text='Student ID').grid(row=1, column=0)

        self.room_number = tk.Entry(self.room_frame)
        self.room_student_id = tk.Entry(self.room_frame)

        self.room_number.grid(row=0, column=1)
        self.room_student_id.grid(row=1, column=1)

        tk.Button(self.room_frame, text='Assign Room', command=self.assign_room).grid(row=2, column=0)
        tk.Button(self.room_frame, text='Update Room', command=self.update_room).grid(row=2, column=1)
        tk.Button(self.room_frame, text='Delete Room', command=self.delete_room).grid(row=2, column=2)

        self.room_tree = ttk.Treeview(self.room_frame)
        self.room_tree['columns'] = ('Room Number', 'Student ID')

        self.room_tree.column('#0', width=0, stretch=tk.NO)
        self.room_tree.column('Room Number', anchor=tk.W, width=100)
        self.room_tree.column('Student ID', anchor=tk.W, width=100)

        self.room_tree.heading('#0', text='', anchor=tk.W)
        self.room_tree.heading('Room Number', text='Room Number', anchor=tk.W)
        self.room_tree.heading('Student ID', text='Student ID', anchor=tk.W)

        self.room_tree.grid(row=3, column=0, columnspan=3)

        self.rooms = []

    def fee_tracking(self):
        tk.Label(self.fee_frame, text='Student ID').grid(row=0, column=0)
        tk.Label(self.fee_frame, text='Fee Amount').grid(row=1, column=0)

        self.fee_student_id = tk.Entry(self.fee_frame)
        self.fee_amount = tk.Entry(self.fee_frame)

        self.fee_student_id.grid(row=0, column=1)
        self.fee_amount.grid(row=1, column=1)

        tk.Button(self.fee_frame, text='Add Fee', command=self.add_fee).grid(row=2, column=0)
        tk.Button(self.fee_frame, text='Update Fee', command=self.update_fee).grid(row=2, column=1)
        tk.Button(self.fee_frame, text='Delete Fee', command=self.delete_fee).grid(row=2, column=2)

        self.fee_tree = ttk.Treeview(self.fee_frame)
        self.fee_tree['columns'] = ('Student ID', 'Fee Amount')

        self.fee_tree.column('#0', width=0, stretch=tk.NO)
        self.fee_tree.column('Student ID', anchor=tk.W, width=100)
        self.fee_tree.column('Fee Amount', anchor=tk.W, width=100)

        self.fee_tree.heading('#0', text='', anchor=tk.W)
        self.fee_tree.heading('Student ID', text='Student ID', anchor=tk.W)
        self.fee_tree.heading('Fee Amount', text='Fee Amount', anchor=tk.W)

        self.fee_tree.grid(row=3, column=0, columnspan=3)

        self.fees = []

    def add_student(self):
        student_id = self.student_id.get()
        student_name = self.student_name.get()
        student_email = self.student_email.get()

        self.students.append({
            'Student ID': student_id,
            'Name': student_name,
            'Email': student_email
        })

        self.student_tree.insert('', 'end', values=(student_id, student_name, student_email))

        self.student_id.delete(0, tk.END)
        self.student_name.delete(0, tk.END)
        self.student_email.delete(0, tk.END)

    def update_student(self):
        selected = self.student_tree.focus()
        if selected:
            values = self.student_tree.item(selected, 'values')
            student_id = values[0]

            for student in self.students:
                if student['Student ID'] == student_id:
                    student['Name'] = self.student_name.get()
                    student['Email'] = self.student_email.get()

            self.student_tree.item(selected, values=(student_id, self.student_name.get(), self.student_email.get()))

            self.student_id.delete(0, tk.END)
            self.student_name.delete(0, tk.END)
            self.student_email.delete(0, tk.END)

    def delete_student(self):
        selected = self.student_tree.focus()
        if selected:
            values = self.student_tree.item(selected, 'values')
            student_id = values[0]

            for student in self.students:
                if student['Student ID'] == student_id:
                    self.students.remove(student)

            self.student_tree.delete(selected)

    def assign_room(self):
        room_number = self.room_number.get()
        student_id = self.room_student_id.get()

        self.rooms.append({
            'Room Number': room_number,
            'Student ID': student_id
        })

        self.room_tree.insert('', 'end', values=(room_number, student_id))

        self.room_number.delete(0, tk.END)
        self.room_student_id.delete(0, tk.END)

    def update_room(self):
        selected = self.room_tree.focus()
        if selected:
            values = self.room_tree.item(selected, 'values')
            room_number = values[0]

            for room in self.rooms:
                if room['Room Number'] == room_number:
                    room['Student ID'] = self.room_student_id.get()

            self.room_tree.item(selected, values=(room_number, self.room_student_id.get()))

            self.room_number.delete(0, tk.END)
            self.room_student_id.delete(0, tk.END)

    def delete_room(self):
        selected = self.room_tree.focus()
        if selected:
            values = self.room_tree.item(selected, 'values')
            room_number = values[0]

            for room in self.rooms:
                if room['Room Number'] == room_number:
                    self.rooms.remove(room)

            self.room_tree.delete(selected)

    def add_fee(self):
        student_id = self.fee_student_id.get()
        fee_amount = self.fee_amount.get()

        self.fees.append({
            'Student ID': student_id,
            'Fee Amount': fee_amount
        })

        self.fee_tree.insert('', 'end', values=(student_id, fee_amount))

        self.fee_student_id.delete(0, tk.END)
        self.fee_amount.delete(0, tk.END)

    def update_fee(self):
        selected = self.fee_tree.focus()
        if selected:
            values = self.fee_tree.item(selected, 'values')
            student_id = values[0]

            for fee in self.fees:
                if fee['Student ID'] == student_id:
                    fee['Fee Amount'] = self.fee_amount.get()

            self.fee_tree.item(selected, values=(student_id, self.fee_amount.get()))

            self.fee_student_id.delete(0, tk.END)
            self.fee_amount.delete(0, tk.END)

    def delete_fee(self):
        selected = self.fee_tree.focus()
        if selected:
            values = self.fee_tree.item(selected, 'values')
            student_id = values[0]

            for fee in self.fees:
                if fee['Student ID'] == student_id:
                    self.fees.remove(fee)

            self.fee_tree.delete(selected)

if __name__ == '__main__':
    root = tk.Tk()
    app = HostelManagementApplication(root)
    root.mainloop()