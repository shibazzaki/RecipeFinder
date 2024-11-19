import os
from datetime import datetime
from flask import current_app

def backup_database():
    """Створює резервну копію бази даних."""
    db_path = current_app.config['SQLALCHEMY_DATABASE_URI'].replace("sqlite:///", "")
    backup_dir = os.path.join(os.getcwd(), "backups")
    os.makedirs(backup_dir, exist_ok=True)

    backup_file = os.path.join(backup_dir, f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.db")
    if os.path.exists(db_path):
        with open(db_path, 'rb') as db_file:
            with open(backup_file, 'wb') as backup:
                backup.write(db_file.read())
        print(f"Backup created at {backup_file}")
    else:
        print("Database file not found.")
