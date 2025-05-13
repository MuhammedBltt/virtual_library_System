# ui/main_window.py
import sys
import os
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import re
import shutil

try:
    from database import models
except ImportError as e:
    print(f"Veritabanı modülü yükleme hatası: {e}")
    sys.exit(1)

class MainWindow(ctk.CTk):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.title("Advanced School Library System")
        self.geometry("1000x700")
        
        # Tema ayarları
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Ana çerçeve
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Başlık
        ctk.CTkLabel(self.main_frame, text="Advanced School Library System", font=("Helvetica", 20, "bold")).pack(pady=10)
        
        # Sekmeler
        self.notebook = ctk.CTkTabview(self.main_frame)
        self.notebook.pack(fill="both", expand=True, pady=10)
        
        self.books_tab = self.notebook.add("Books")
        self.students_tab = self.notebook.add("Students")
        self.borrow_tab = self.notebook.add("Borrow/Return")
        self.reports_tab = self.notebook.add("Reports")
        self.settings_tab = self.notebook.add("Settings")
        
        # Sekmeleri kur
        self.setup_books_tab()
        self.setup_students_tab()
        self.setup_borrow_tab()
        self.setup_reports_tab()
        self.setup_settings_tab()
    
    def setup_books_tab(self):
        # Arama çubuğu
        search_frame = ctk.CTkFrame(self.books_tab)
        search_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(search_frame, text="Search Books:").pack(side="left")
        self.book_search_var = ctk.StringVar()
        ctk.CTkEntry(search_frame, textvariable=self.book_search_var).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Search", command=self.search_books).pack(side="left")
        
        # Kitap ekleme/düzenleme
        add_frame = ctk.CTkFrame(self.books_tab)
        add_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(add_frame, text="Title:").grid(row=0, column=0, padx=5)
        self.book_title_var = ctk.StringVar()
        ctk.CTkEntry(add_frame, textvariable=self.book_title_var).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(add_frame, text="Author:").grid(row=0, column=2, padx=5)
        self.book_author_var = ctk.StringVar()
        ctk.CTkEntry(add_frame, textvariable=self.book_author_var).grid(row=0, column=3, padx=5)
        ctk.CTkLabel(add_frame, text="Category:").grid(row=0, column=4, padx=5)
        self.book_category_var = ctk.StringVar()
        ctk.CTkEntry(add_frame, textvariable=self.book_category_var).grid(row=0, column=5, padx=5)
        ctk.CTkLabel(add_frame, text="Quantity:").grid(row=0, column=6, padx=5)
        self.book_quantity_var = ctk.StringVar()
        ctk.CTkEntry(add_frame, textvariable=self.book_quantity_var).grid(row=0, column=7, padx=5)
        ctk.CTkButton(add_frame, text="Add Book", command=self.add_book).grid(row=0, column=8, padx=5)
        
        # Kitap listesi
        self.book_tree = ttk.Treeview(self.books_tab, columns=("ID", "Title", "Author", "Category", "Quantity", "Total"), show="headings")
        self.book_tree.heading("ID", text="ID")
        self.book_tree.heading("Title", text="Title")
        self.book_tree.heading("Author", text="Author")
        self.book_tree.heading("Category", text="Category")
        self.book_tree.heading("Quantity", text="Available")
        self.book_tree.heading("Total", text="Total")
        self.book_tree.pack(fill="both", expand=True, pady=10)
        self.book_tree.bind("<Double-1>", self.edit_book)
        ctk.CTkButton(self.books_tab, text="Delete Selected", command=self.delete_book).pack(pady=5)
        self.refresh_books()
    
    def setup_students_tab(self):
        # Arama çubuğu
        search_frame = ctk.CTkFrame(self.students_tab)
        search_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(search_frame, text="Search Students:").pack(side="left")
        self.student_search_var = ctk.StringVar()
        ctk.CTkEntry(search_frame, textvariable=self.student_search_var).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Search", command=self.search_students).pack(side="left")
        
        # Öğrenci ekleme
        add_frame = ctk.CTkFrame(self.students_tab)
        add_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(add_frame, text="Student Number:").grid(row=0, column=0, padx=5)
        self.student_number_var = ctk.StringVar()
        ctk.CTkEntry(add_frame, textvariable=self.student_number_var).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(add_frame, text="Name:").grid(row=0, column=2, padx=5)
        self.student_name_var = ctk.StringVar()
        ctk.CTkEntry(add_frame, textvariable=self.student_name_var).grid(row=0, column=3, padx=5)
        ctk.CTkLabel(add_frame, text="Class:").grid(row=0, column=4, padx=5)
        self.student_class_var = ctk.StringVar()
        ctk.CTkEntry(add_frame, textvariable=self.student_class_var).grid(row=0, column=5, padx=5)
        ctk.CTkLabel(add_frame, text="Email:").grid(row=0, column=6, padx=5)
        self.student_email_var = ctk.StringVar()
        ctk.CTkEntry(add_frame, textvariable=self.student_email_var).grid(row=0, column=7, padx=5)
        ctk.CTkButton(add_frame, text="Add Student", command=self.add_student).grid(row=0, column=8, padx=5)
        
        # Öğrenci listesi
        self.student_tree = ttk.Treeview(self.students_tab, columns=("ID", "Number", "Name", "Class", "Email"), show="headings")
        self.student_tree.heading("ID", text="ID")
        self.student_tree.heading("Number", text="Student Number")
        self.student_tree.heading("Name", text="Name")
        self.student_tree.heading("Class", text="Class")
        self.student_tree.heading("Email", text="Email")
        self.student_tree.pack(fill="both", expand=True, pady=10)
        self.student_tree.bind("<Double-1>", self.edit_student)
        ctk.CTkButton(self.students_tab, text="Delete Selected", command=self.delete_student).pack(pady=5)
        self.refresh_students()
    
    def setup_borrow_tab(self):
        # Ödünç alma
        borrow_frame = ctk.CTkFrame(self.borrow_tab)
        borrow_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(borrow_frame, text="Student ID:").grid(row=0, column=0, padx=5)
        self.borrow_student_id_var = ctk.StringVar()
        ctk.CTkEntry(borrow_frame, textvariable=self.borrow_student_id_var).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(borrow_frame, text="Book ID:").grid(row=0, column=2, padx=5)
        self.borrow_book_id_var = ctk.StringVar()
        ctk.CTkEntry(borrow_frame, textvariable=self.borrow_book_id_var).grid(row=0, column=3, padx=5)
        ctk.CTkButton(borrow_frame, text="Borrow Book", command=self.borrow_book).grid(row=0, column=4, padx=5)
        
        # İade etme
        return_frame = ctk.CTkFrame(self.borrow_tab)
        return_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(return_frame, text="Borrow ID:").grid(row=0, column=0, padx=5)
        self.return_borrow_id_var = ctk.StringVar()
        ctk.CTkEntry(return_frame, textvariable=self.return_borrow_id_var).grid(row=0, column=1, padx=5)
        ctk.CTkButton(return_frame, text="Return Book", command=self.return_book).grid(row=0, column=2, padx=5)
        
        # Ödünç alma listesi
        self.borrow_tree = ttk.Treeview(self.borrow_tab, columns=("ID", "Student", "Book", "Borrow Date", "Due Date", "Return Date", "Fine"), show="headings")
        self.borrow_tree.heading("ID", text="ID")
        self.borrow_tree.heading("Student", text="Student")
        self.borrow_tree.heading("Book", text="Book")
        self.borrow_tree.heading("Borrow Date", text="Borrow Date")
        self.borrow_tree.heading("Due Date", text="Due Date")
        self.borrow_tree.heading("Return Date", text="Return Date")
        self.borrow_tree.heading("Fine", text="Fine")
        self.borrow_tree.pack(fill="both", expand=True, pady=10)
        self.refresh_borrows()
    
    def setup_reports_tab(self):
        # Rapor seçenekleri
        report_frame = ctk.CTkFrame(self.reports_tab)
        report_frame.pack(fill="x", pady=5)
        ctk.CTkButton(report_frame, text="Most Borrowed Books", command=self.report_most_borrowed).pack(side="left", padx=5)
        ctk.CTkButton(report_frame, text="Overdue Books", command=self.report_overdue).pack(side="left", padx=5)
        ctk.CTkButton(report_frame, text="Popular Categories", command=self.report_popular_categories).pack(side="left", padx=5)
        
        # Rapor çıktısı
        self.report_text = ctk.CTkTextbox(self.reports_tab, height=400)
        self.report_text.pack(fill="both", expand=True, pady=10)
    
    def setup_settings_tab(self):
        # Tema değiştirme
        theme_frame = ctk.CTkFrame(self.settings_tab)
        theme_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(theme_frame, text="Theme:").pack(side="left")
        self.theme_var = ctk.StringVar(value="light")
        ctk.CTkOptionMenu(theme_frame, values=["light", "dark"], variable=self.theme_var, command=self.change_theme).pack(side="left", padx=5)
        
        # Veritabanı yedekleme
        backup_frame = ctk.CTkFrame(self.settings_tab)
        backup_frame.pack(fill="x", pady=5)
        ctk.CTkButton(backup_frame, text="Backup Database", command=self.backup_database).pack(side="left", padx=5)
        ctk.CTkButton(backup_frame, text="Restore Database", command=self.restore_database).pack(side="left", padx=5)
    
    def add_book(self):
        title = self.book_title_var.get().strip()
        author = self.book_author_var.get().strip()
        category = self.book_category_var.get().strip()
        quantity = self.book_quantity_var.get().strip()
        
        if not all([title, author, category, quantity]):
            messagebox.showerror("Error", "All fields are required!")
            return
        if not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Error", "Quantity must be a positive number!")
            return
        
        try:
            book = models.Book(title=title, author=author, category=category, quantity=int(quantity), total_quantity=int(quantity))
            self.session.add(book)
            self.session.commit()
            self.refresh_books()
            self.clear_book_fields()
            messagebox.showinfo("Success", "Book added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {str(e)}")
    
    def edit_book(self, event):
        selected = self.book_tree.selection()
        if not selected:
            return
        book_id = self.book_tree.item(selected)["values"][0]
        book = self.session.query(models.Book).filter_by(id=book_id).first()
        
        self.book_title_var.set(book.title)
        self.book_author_var.set(book.author)
        self.book_category_var.set(book.category)
        self.book_quantity_var.set(str(book.quantity))
        
        def save_edit():
            title = self.book_title_var.get().strip()
            author = self.book_author_var.get().strip()
            category = self.book_category_var.get().strip()
            quantity = self.book_quantity_var.get().strip()
            
            if not all([title, author, category, quantity]):
                messagebox.showerror("Error", "All fields are required!")
                return
            if not quantity.isdigit() or int(quantity) <= 0:
                messagebox.showerror("Error", "Quantity must be a positive number!")
                return
            
            try:
                book.title = title
                book.author = author
                book.category = category
                book.quantity = int(quantity)
                book.total_quantity = int(quantity) + len([b for b in book.borrowed_books if not b.return_date])
                self.session.commit()
                self.refresh_books()
                self.clear_book_fields()
                messagebox.showinfo("Success", "Book updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update book: {str(e)}")
        
        add_frame = self.books_tab.winfo_children()[1]
        add_frame.winfo_children()[-1].configure(text="Update Book", command=save_edit)
    
    def delete_book(self):
        selected = self.book_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a book to delete!")
            return
        book_id = self.book_tree.item(selected)["values"][0]
        book = self.session.query(models.Book).filter_by(id=book_id).first()
        if book.borrowed_books:
            messagebox.showerror("Error", "Cannot delete book with active borrows!")
            return
        try:
            self.session.delete(book)
            self.session.commit()
            self.refresh_books()
            messagebox.showinfo("Success", "Book deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete book: {str(e)}")
    
    def search_books(self):
        query = self.book_search_var.get().strip().lower()
        self.book_tree.delete(*self.book_tree.get_children())
        try:
            books = self.session.query(models.Book).all()
            for book in books:
                if query in book.title.lower() or query in book.author.lower() or query in book.category.lower():
                    self.book_tree.insert("", "end", values=(book.id, book.title, book.author, book.category, book.quantity, book.total_quantity))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search books: {str(e)}")
    
    def add_student(self):
        number = self.student_number_var.get().strip()
        name = self.student_name_var.get().strip()
        student_class = self.student_class_var.get().strip()
        email = self.student_email_var.get().strip()
        
        if not all([number, name, student_class, email]):
            messagebox.showerror("Error", "All fields are required!")
            return
        if not number.isdigit():
            messagebox.showerror("Error", "Student number must be a number!")
            return
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return
        
        try:
            student = models.Students(student_number=int(number), name=name, student_class=student_class, email=email)
            self.session.add(student)
            self.session.commit()
            self.refresh_students()
            self.clear_student_fields()
            messagebox.showinfo("Success", "Student added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")
    
    def edit_student(self, event):
        selected = self.student_tree.selection()
        if not selected:
            return
        student_id = self.student_tree.item(selected)["values"][0]
        student = self.session.query(models.Students).filter_by(id=student_id).first()
        
        self.student_number_var.set(str(student.student_number))
        self.student_name_var.set(student.name)
        self.student_class_var.set(student.student_class)
        self.student_email_var.set(student.email)
        
        def save_edit():
            number = self.student_number_var.get().strip()
            name = self.student_name_var.get().strip()
            student_class = self.student_class_var.get().strip()
            email = self.student_email_var.get().strip()
            
            if not all([number, name, student_class, email]):
                messagebox.showerror("Error", "All fields are required!")
                return
            if not number.isdigit():
                messagebox.showerror("Error", "Student number must be a number!")
                return
            if not self.validate_email(email):
                messagebox.showerror("Error", "Invalid email format!")
                return
            
            try:
                student.student_number = int(number)
                student.name = name
                student.student_class = student_class
                student.email = email
                self.session.commit()
                self.refresh_students()
                self.clear_student_fields()
                messagebox.showinfo("Success", "Student updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update student: {str(e)}")
        
        add_frame = self.students_tab.winfo_children()[1]
        add_frame.winfo_children()[-1].configure(text="Update Student", command=save_edit)
    
    def delete_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a student to delete!")
            return
        student_id = self.student_tree.item(selected)["values"][0]
        student = self.session.query(models.Students).filter_by(id=student_id).first()
        if student.borrowed_books:
            messagebox.showerror("Error", "Cannot delete student with active borrows!")
            return
        try:
            self.session.delete(student)
            self.session.commit()
            self.refresh_students()
            messagebox.showinfo("Success", "Student deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
    
    def search_students(self):
        query = self.student_search_var.get().strip().lower()
        self.student_tree.delete(*self.student_tree.get_children())
        try:
            students = self.session.query(models.Students).all()
            for student in students:
                if query in str(student.student_number) or query in student.name.lower() or query in student.student_class.lower() or query in student.email.lower():
                    self.student_tree.insert("", "end", values=(student.id, student.student_number, student.name, student.student_class, student.email))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search students: {str(e)}")
    
    def borrow_book(self):
        student_id = self.borrow_student_id_var.get().strip()
        book_id = self.borrow_book_id_var.get().strip()
        
        if not all([student_id, book_id]):
            messagebox.showerror("Error", "Student ID and Book ID are required!")
            return
        if not (student_id.isdigit() and book_id.isdigit()):
            messagebox.showerror("Error", "IDs must be numbers!")
            return
        
        try:
            student = self.session.query(models.Students).filter_by(id=int(student_id)).first()
            book = self.session.query(models.Book).filter_by(id=int(book_id)).first()
            
            if not student or not book:
                messagebox.showerror("Error", "Invalid Student ID or Book ID!")
                return
            if book.quantity <= 0:
                messagebox.showerror("Error", "No copies available!")
                return
            
            borrow = models.Borrowed(student_id=int(student_id), book_id=int(book_id), borrow_date=datetime.now(), due_date=datetime.now() + timedelta(days=7))
            book.quantity -= 1
            self.session.add(borrow)
            self.session.commit()
            self.refresh_borrows()
            self.refresh_books()
            self.borrow_student_id_var.set("")
            self.borrow_book_id_var.set("")
            messagebox.showinfo("Success", "Book borrowed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to borrow book: {str(e)}")
    
    def return_book(self):
        borrow_id = self.return_borrow_id_var.get().strip()
        
        if not borrow_id:
            messagebox.showerror("Error", "Borrow ID is required!")
            return
        if not borrow_id.isdigit():
            messagebox.showerror("Error", "Borrow ID must be a number!")
            return
        
        try:
            borrow = self.session.query(models.Borrowed).filter_by(id=int(borrow_id)).first()
            if not borrow:
                messagebox.showerror("Error", "Invalid Borrow ID!")
                return
            if borrow.return_date:
                messagebox.showerror("Error", "Book already returned!")
                return
            
            borrow.return_date = datetime.now()
            book = self.session.query(models.Book).filter_by(id=borrow.book_id).first()
            book.quantity += 1
            self.session.commit()
            self.refresh_borrows()
            self.refresh_books()
            self.return_borrow_id_var.set("")
            messagebox.showinfo("Success", "Book returned successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {str(e)}")
    
    def report_most_borrowed(self):
        try:
            self.report_text.delete("0.0", "end")
            books = self.session.query(models.Book).all()
            borrow_counts = [(book, len(book.borrowed_books)) for book in books]
            borrow_counts.sort(key=lambda x: x[1], reverse=True)
            self.report_text.insert("0.0", "Most Borrowed Books:\n\n")
            for book, count in borrow_counts[:5]:
                self.report_text.insert("end", f"{book.title} by {book.author}: {count} borrows\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def report_overdue(self):
        try:
            self.report_text.delete("0.0", "end")
            borrows = self.session.query(models.Borrowed).filter(models.Borrowed.return_date.is_(None)).all()
            self.report_text.insert("0.0", "Overdue Books:\n\n")
            for borrow in borrows:
                if borrow.due_date < datetime.now():
                    student = self.session.query(models.Students).filter_by(id=borrow.student_id).first()
                    book = self.session.query(models.Book).filter_by(id=borrow.book_id).first()
                    days_late = (datetime.now() - borrow.due_date).days
                    fine = days_late * 1  # 1 TL/gün
                    self.report_text.insert("end", f"ID: {borrow.id}, Student: {student.name}, Book: {book.title}, Days Late: {days_late}, Fine: {fine} TL\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def report_popular_categories(self):
        try:
            self.report_text.delete("0.0", "end")
            books = self.session.query(models.Book).all()
            category_counts = {}
            for book in books:
                category_counts[book.category] = category_counts.get(book.category, 0) + len(book.borrowed_books)
            category_counts = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
            self.report_text.insert("0.0", "Popular Categories:\n\n")
            for category, count in category_counts[:5]:
                self.report_text.insert("end", f"{category}: {count} borrows\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def change_theme(self, theme):
        try:
            ctk.set_appearance_mode(theme)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change theme: {str(e)}")
    
    def backup_database(self):
        try:
            if hasattr(sys, '_MEIPASS'):
                base_dir = os.path.dirname(sys.executable)
            else:
                base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            
            db_path = os.path.join(base_dir, 'library.db')
            backup_path = os.path.join(base_dir, f"library_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
            
            if not os.path.exists(db_path):
                messagebox.showerror("Error", "Database file not found!")
                return
                
            shutil.copy(db_path, backup_path)
            messagebox.showinfo("Success", "Database backed up successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")
    
    def restore_database(self):
        messagebox.showinfo("Info", "Please select a backup file manually and replace library.db.")
    
    def validate_email(self, email):
        try:
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            return bool(re.match(pattern, email))
        except Exception as e:
            messagebox.showerror("Error", f"Email validation failed: {str(e)}")
            return False
    
    def clear_book_fields(self):
        self.book_title_var.set("")
        self.book_author_var.set("")
        self.book_category_var.set("")
        self.book_quantity_var.set("")
        add_frame = self.books_tab.winfo_children()[1]
        add_frame.winfo_children()[-1].configure(text="Add Book", command=self.add_book)
    
    def clear_student_fields(self):
        self.student_number_var.set("")
        self.student_name_var.set("")
        self.student_class_var.set("")
        self.student_email_var.set("")
        add_frame = self.students_tab.winfo_children()[1]
        add_frame.winfo_children()[-1].configure(text="Add Student", command=self.add_student)
    
    def refresh_books(self):
        try:
            self.book_tree.delete(*self.book_tree.get_children())
            books = self.session.query(models.Book).all()
            for book in books:
                self.book_tree.insert("", "end", values=(book.id, book.title, book.author, book.category, book.quantity, book.total_quantity))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh books: {str(e)}")
    
    def refresh_students(self):
        try:
            self.student_tree.delete(*self.student_tree.get_children())
            students = self.session.query(models.Students).all()
            for student in students:
                self.student_tree.insert("", "end", values=(student.id, student.student_number, student.name, student.student_class, student.email))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh students: {str(e)}")
    
    def refresh_borrows(self):
        try:
            self.borrow_tree.delete(*self.borrow_tree.get_children())
            borrows = self.session.query(models.Borrowed).all()
            for borrow in borrows:
                student = self.session.query(models.Students).filter_by(id=borrow.student_id).first()
                book = self.session.query(models.Book).filter_by(id=borrow.book_id).first()
                if student and book:  # None kontrolü
                    return_date = borrow.return_date or "Not Returned"
                    fine = self.calculate_fine(borrow)
                    self.borrow_tree.insert("", "end", values=(borrow.id, student.name, book.title, borrow.borrow_date, borrow.due_date, return_date, f"{fine} TL"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh borrows: {str(e)}")
    
    def calculate_fine(self, borrow):
        try:
            if borrow.return_date or borrow.due_date > datetime.now():
                return 0
            days_late = (datetime.now() - borrow.due_date).days
            return days_late * 1  # 1 TL/gün
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate fine: {str(e)}")
            return 0