# database/database.py
import sys
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Loglama ayarları
logging.basicConfig(
    filename=os.path.join(os.getenv('APPDATA'), 'Library', 'app.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_base_dir():
    """PyInstaller ve normal çalıştırma için temel dizini döndür."""
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_db_path():
    """Veritabanı dosyasının yolunu döndür."""
    # AppData dizinini al
    appdata_dir = os.path.join(os.getenv('APPDATA'), 'Library')
    # AppData dizininde Library klasörü yoksa oluştur
    if not os.path.exists(appdata_dir):
        os.makedirs(appdata_dir)
    # Veritabanı dosyasını AppData dizinine yerleştir
    db_path = os.path.join(appdata_dir, 'library.db')
    
    # Eğer AppData'da veritabanı dosyası yoksa, varsayılan konumdan kopyala
    default_db_path = os.path.join(get_base_dir(), 'library.db')
    if not os.path.exists(db_path) and os.path.exists(default_db_path):
        import shutil
        shutil.copy(default_db_path, db_path)
    
    return db_path

# Veritabanı yolunu oluştur
DB_PATH = get_db_path()

# Veritabanı dosyasının varlığını kontrol et
if not os.path.exists(DB_PATH):
    logging.warning(f"Veritabanı bulunamadı: {DB_PATH}. Yeni bir veritabanı oluşturulacak.")

try:
    # SQLite veritabanına bağlantı
    engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logging.info("Veritabanı bağlantısı başarılı.")
except Exception as e:
    logging.error(f"Veritabanı bağlantı hatası: {e}")
    sys.exit(1)