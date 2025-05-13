# ui/app.py
import sys
import os

# PyInstaller ile çalışırken dosya yollarını doğru şekilde yönet
if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

try:
    from database import models, database
    from ui.main_window import MainWindow
except ImportError as e:
    print(f"Modül yükleme hatası: {e}")
    print(f"sys.path: {sys.path}")
    sys.exit(1)

# Veritabanı ve modelleri oluştur
try:
    models.Base.metadata.create_all(bind=database.engine)
except Exception as e:
    print(f"Veritabanı oluşturma hatası: {e}")
    sys.exit(1)

# Veritabanı oturumu
try:
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=database.engine)
    session = Session()
except Exception as e:
    print(f"Oturum oluşturma hatası: {e}")
    sys.exit(1)

if __name__ == "__main__":
    try:
        app = MainWindow(session)
        app.mainloop()
    except Exception as e:
        print(f"Uygulama başlatma hatası: {e}")
        sys.exit(1)