# database/models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

try:
    from .database import Base
except ImportError as e:
    print(f"Veritabanı modülü yükleme hatası: {e}")
    import sys
    sys.exit(1)

class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_number = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    student_class = Column(String, nullable=False)
    email = Column(String, nullable=False)
    
    borrowed_books = relationship("Borrowed", back_populates="student")

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    category = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_quantity = Column(Integer, nullable=False)
    
    borrowed_books = relationship("Borrowed", back_populates="book")

class Borrowed(Base):
    __tablename__ = 'borrowed'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    borrow_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    
    student = relationship("Students", back_populates="borrowed_books")
    book = relationship("Book", back_populates="borrowed_books")