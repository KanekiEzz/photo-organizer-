import os
import shutil
from datetime import datetime
import sys

# ============================
#   File Type Categories
# ============================
CATEGORIES = {
    "Photo": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "heic"],
    "Video": ["mp4", "mov", "avi", "mkv", "flv", "wmv"],
    "Document": ["pdf", "doc", "docx", "txt", "xlsx", "xls", "ppt", "pptx"],
    "Audio": ["mp3", "wav", "aac", "flac", "ogg"],
}

def get_category(filename):
    ext = filename.lower().split(".")[-1]
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


# ============================
#   ORGANIZER (RECURSIVE)
# ============================
def organize_files(source_folder):
    if not os.path.isdir(source_folder):
        print(f"❌ Path does not exist: {source_folder}")
        return

    for root, dirs, files in os.walk(source_folder):
        for filename in files:
            file_path = os.path.join(root, filename)

            if "Photo" in root or "Video" in root or "Document" in root or "Audio" in root or "Other" in root:
                continue

            if not os.path.isfile(file_path):
                continue

            stat = os.stat(file_path)
            modified = datetime.fromtimestamp(stat.st_mtime)

            year = str(modified.year)
            month = f"{modified.month:02d}"

            category = get_category(filename)

            target_dir = os.path.join(source_folder, category, year, month)
            os.makedirs(target_dir, mode=0o755, exist_ok=True)

            dest_path = os.path.join(target_dir, filename)

            if os.path.exists(dest_path):
                print(f"⚠️ Already exists, skipping: {filename}")
                continue

            shutil.move(file_path, dest_path)
            print(f"Moved: {filename} → {category}/{year}/{month}")

    print("✅ All files sorted successfully!")


# ============================
#           MAIN
# ============================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Missing path. Usage: python organize.py /data")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.isdir(path):
        print("❌ Invalid directory:", path)
        sys.exit(1)

    print("✔ Sorting files inside:", path)
    organize_files(path)
