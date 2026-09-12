import os
from db_manager import DatabaseManager

def create_all_tables(db_manager):
    """
    Create all necessary tables for the application using DatabaseManager instance.
    
    Args:
        db_manager: An initialized DatabaseManager instance
    """
    # טבלת לקוחות כוללת שם משתמש, סיסמה מוצפנת וסטטוס חיבור
    db_manager.create_table(
        "clients",
        "(client_id VARCHAR(255) PRIMARY KEY, "
        "password_hash VARCHAR(256) NOT NULL, "
        "client_ip VARCHAR(50), "
        "client_port INT, "
        "last_seen DATETIME, "
        "ddos_status BOOLEAN DEFAULT FALSE, "
        "total_sent_media INT DEFAULT 0, "
        "is_connected BOOLEAN DEFAULT FALSE)"
    )
    
    # טבלת מדיה מפוענחת
    db_manager.create_table(
        "decrypted_media",
        "(id INT AUTO_INCREMENT PRIMARY KEY, "
        "user_id VARCHAR(255), "
        "media_type_id INT, "
        "path_to_decrypted_media VARCHAR(255))"
    )
    
    # טבלת תפריט מדיה
    db_manager.create_table(
        "media_menu",
        "(id_media INT PRIMARY KEY, "
        "image_path VARCHAR(255), "
        "audio_path VARCHAR(255), "
        "video_path VARCHAR(255))"
    )

def populate_media_menu(db_manager):
    """
    Populate the media_menu table with predefined data using relative paths.
    
    Args:
        db_manager: An initialized DatabaseManager instance
    """
    # שימוש בנתיבים יחסיים במקום נתיבים קשיחים במחשב ספציפי
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    predefined_media = [
        (1, os.path.join("JPG", "Ransom.jpg"), None, None),
        (2, os.path.join("JPG", "cover1_image.jpg"), None, None),
        (3, None, None, os.path.join("MP4", "video.mp4"))
    ]

    existing_rows = db_manager.get_all_rows("media_menu")
    if not existing_rows:
        for media in predefined_media:
            db_manager.insert_row(
                "media_menu",
                "(id_media, image_path, audio_path, video_path)",
                "(%s, %s, %s, %s)",
                media
            )
        print("Media menu populated successfully.")