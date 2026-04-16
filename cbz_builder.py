import os
import re
import shutil
import zipfile
from pathlib import Path

# ================= CONFIG =================
# Note: Ensure these paths use forward slashes (/) or raw strings (r"")
INPUT_DIR = Path(r"C:/Users/Owner/Downloads/JAM/Downloads/Assassination_Classroom")
OUTPUT_DIR = Path(r"C:/Users/Owner/Downloads/JAM/Downloads/Assassination_Classroom_cbz")
TEMP_DIR = Path(r"C:/Users/Owner/Downloads/temp_cbz")

# ================= HELPERS =================


def extract_chapter_number(folder_name: str) -> float:
    """
    Smart extraction that handles messy names.
    Matches: "Chapter. 7.2", "Ch 18 - title", "Ch-27.5"
    """
    # Looks for Ch/Chapter, ignores optional punctuation, and grabs the number
    match = re.search(
        r"(?:Ch(?:apter)?[\s\.\-]*?)(\d+\.?\d*)", folder_name, re.IGNORECASE
    )
    if match:
        return float(match.group(1))

    # Fallback: Just find the first number in the string
    fallback = re.search(r"(\d+\.?\d*)", folder_name)
    if fallback:
        return float(fallback.group(1))

    return -1.0


def volume_from_chapter(ch: float) -> int:
    """
    Groups chapters into volumes based on maximum chapter limits.
    """
    if ch < 0:
        return 999

    # Upper limits for each volume (Vol 1 is up to 9.9, Vol 2 up to 18.9, etc.)
    thresholds = [
        9.9,
        18.9,
        27.9,
        36.9,
        45.9,
        54.9,
        63.9,
        73.9,
        83.9,
        93.9,
        103.9,
        113.9,
        123.9,
        133.9,
    ]

    for i, limit in enumerate(thresholds, 1):
        if ch <= limit:
            return i

    return 99  # For anything above chapter 133.9


def natural_sort_key(s):
    """Ensures Page 2 comes before Page 10."""
    return [
        float(text) if text.isdigit() else text.lower()
        for text in re.split(r"(\d+)", s)
    ]


# ================= MAIN SCRIPT =================

# 1. Clean up old temp folders
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Index Chapters
chapters = []
for folder in os.listdir(INPUT_DIR):
    full_path = os.path.join(INPUT_DIR, folder)
    if not os.path.isdir(full_path):
        continue

    chap_num = extract_chapter_number(folder)
    if chap_num == -1:
        print(f"Skipping unknown folder: {folder}")
        continue

    chapters.append((chap_num, folder, full_path))

# Sort by actual numerical value (Fixes Chapter 10 coming before Chapter 2)
chapters.sort(key=lambda x: x[0])
print(f"Found {len(chapters)} valid chapters.\n")

# 3. Group into Volumes
volumes = {}
for chap_num, folder, path in chapters:
    vol = volume_from_chapter(chap_num)
    if vol not in volumes:
        volumes[vol] = []
    volumes[vol].append((chap_num, folder, path))

# 4. Build CBZ Files
for vol, items in volumes.items():
    vol_folder = os.path.join(TEMP_DIR, f"Vol_{vol}")
    os.makedirs(vol_folder, exist_ok=True)

    print(f"Building Volume {vol}...")

    for chap_num, folder, path in items:
        # Get images and sort them NATURALLY
        images = [
            f for f in os.listdir(path) if f.lower().endswith((".webp", ".jpg", ".png"))
        ]
        images.sort(key=natural_sort_key)

        for i, img in enumerate(images, 1):
            src = os.path.join(path, img)

            # Zero-pad chapter and page numbers for perfect e-reader sorting
            # Example: Ch00010.5_Page0001.webp
            new_name = f"Ch{chap_num:05.1f}_Page{i:04d}{Path(img).suffix}"
            dst = os.path.join(vol_folder, new_name)

            shutil.copy2(src, dst)

    # ZIP → CBZ
    cbz_path = os.path.join(OUTPUT_DIR, f"Vol_{vol}.cbz")
    with zipfile.ZipFile(cbz_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(vol_folder):
            for f in sorted(files):
                full = os.path.join(root, f)
                arc = os.path.relpath(full, vol_folder)
                zipf.write(full, arc)

    print(f" -> Created {cbz_path}")

# Clean up temp folder when finished
shutil.rmtree(TEMP_DIR)
print("\nDONE ✔")
