# WEBP_CBZ
Python utility to automatically parse, group, and compile messy manga chapter folders with .webp files into sorted .cbz volumes
Here is the complete `README.md` file formatted in a single code block. You can just click the **"Copy"** button in the top corner of the block and paste it directly into your GitHub repository.


# Manga CBZ Compiler


## Features

* **Smart Parsing:** Extracts chapter numbers (even decimals like `18.5`) from messy folder names.
* **Auto-Grouping:** Bundles chapters into volumes based on customizable limits.
* **Perfect Sorting:** Uses natural sorting so `Page 2` comes before `Page 10`.
* **Zero Dependencies:** Uses only built-in Python libraries. No `pip install` required.

## Expected Directory Structure

Your input directory should contain folders representing individual chapters. The script will ignore any non-directory files in the root.

```text
Manga_Name/
  ├── Ch. 1 - The Beginning/
  │    ├── 1.webp
  │    ├── 2.webp
  ├── Chapter 2/
  ├── Ch 10.5 - Extra/
````

## Getting Started

### Prerequisites

  * **Python 3.6** or higher.

### Installation & Usage

1.  Clone the repository or download the script:
    ```bash
    git clone [https://github.com/yourusername/manga-cbz-compiler.git](https://github.com/yourusername/manga-cbz-compiler.git)
    ```
2.  Open the script in your preferred text editor.
3.  Update the paths in the **CONFIG** section to match your local environment:
    ```python
    INPUT_DIR = Path(r"C:/path/to/your/messy/chapters")
    OUTPUT_DIR = Path(r"C:/path/to/save/finished/volumes")
    TEMP_DIR = Path(r"C:/path/to/temp/processing/folder")
    ```
4.  Run the script:
    ```bash
    python compiler.py
    ```

## Configuration

### Customizing Volume Sizes

By default, the script groups chapters based on predefined thresholds. To change how many chapters go into a volume, simply adjust the `thresholds` list in the code:

```python
# The numbers represent the maximum chapter limit for that volume.
# Vol 1 is up to 9.9, Vol 2 up to 18.9, etc.
thresholds = [
    9.9, 18.9, 27.9, 36.9, 45.9, 54.9, 63.9, 
    73.9, 83.9, 93.9, 103.9, 113.9, 123.9, 133.9
]
```

## 📄 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

```
```
