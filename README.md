# Image Gallery Generation Pipeline
![Sample HTML Gallery](sample_html.png)

**Image Gallery Generator** is a lightweight Python toolkit that transforms your raw images and algorithmic results into polished, responsive HTML galleries in just two steps. Whether you’re writing a paper, preparing a presentation, or sharing work online, this pipeline makes it effortless to showcase your results.

  * **Organize & Resize:** Automatically normalize nested folder structures and resize input images and their corresponding results to matching dimensions.
  * **Caption & Compare:** Overlay custom captions for each image pair, enabling clear side-by-side comparisons across different methods.
  * **Generate & Customize:** Produce a single, self-contained HTML file using a CSS grid. The layout, columns, and styling are all configurable—no front-end skills required.

### Use Cases in Research:

  * Quickly create side-by-side "before and after" examples for image processing tasks.
  * Build image galleries for your paper’s supplementary material or project website.
  * Standardize visualization workflows across multiple experiments and collaborators.

Transform hours of manual formatting into a reproducible, scriptable pipeline that lets you focus on your research.

## How It Works

### 1\. Pre-processing (`src/pre_process.py`)

  * Resizes oversized input images to a configurable maximum dimension.
  * Flattens and normalizes your nested `method_results/` into a standard folder structure.
  * Renames all result files to `<basename>_result.<ext>` and resizes them to match their corresponding input image.

### 2\. HTML Generation (`src/html_gallery.py`)

  * Scans the processed folders and your caption files (`<basename>.txt`).
  * Builds a responsive CSS-grid gallery with a configurable number of columns.
  * Outputs a single `gallery.html` file that you can open in any browser.

## 📋 Requirements

  * Python 3.7+
  * Pillow (for image resizing)
  * A virtual environment is recommended.

<!-- end list -->

```bash
# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install Pillow
```

## 🚀 Quick Start with Sample Data

Clone the repository and run the scripts with the included sample data.

```bash
# 1. Clone the repository
git clone https://github.com/Dominoer/image-gallery-generator.git
cd image-gallery-generator

# 2. Run the pre-processing step
python src/pre_process.py \
  --input_folder sample_data/input \
  --method_results sample_data/method_results \
  --output_folder processed \
  --max_size 1024

# 3. Generate the HTML gallery
python src/html_gallery.py \
  --input_folder processed/input \
  --captions_folder sample_data/captions \
  --method_results processed/method_results \
  --html_output gallery.html \
  --cols 4

# 4. Open gallery.html in your browser!
```

## 🔧 Directory Layout

The scripts expect the following directory structure for your raw data.

### Before Processing

```
project_root/
├── input/                  # Raw input images
│   ├── foo.jpg
│   └── bar.png
│
├── method_results/         # Your outputs, can be nested
│   ├── MethodA/
│   │   ├── scale_0.30/
│   │   │   ├── foo_scale_0.30_result.png
│   │   │   └── bar_scale_0.30_result.png
│   │   └── scale_0.50/
│   │       ├── foo_scale_0.50_result.png
│   │       └── bar_scale_0.50_result.png
│   └── MethodB/
│       └── SubMethodA/
│           └── scale_0.50/
│               ├── foo_result.png
│               └── bar_result.png
│
└── captions/               # One .txt file per image, matching the base name
    ├── foo.txt             # e.g., "Low-light denoising result"
    └── bar.txt             # e.g., "Texture transfer output"
```

### After Pre-processing

The `pre_process.py` script will create a clean, flattened `processed/` directory.

```
processed/
├── input/
│   ├── foo.jpg             # Resized if it was >1024px
│   └── bar.png
│
└── method_results/
    ├── MethodA_scale_0.30/
    │   ├── foo_result.png
    │   └── bar_result.png
    ├── MethodA_scale_0.50/
    │   ├── foo_result.png
    │   └── bar_result.png
    └── MethodB_SubMethodA_scale_0.50/
        ├── foo_result.png
        └── bar_result.png
```

## ⚙️ Usage Details

### 1\. Pre-processing

```bash
python src/pre_process.py \
  --input_folder path/to/your/inputs \
  --method_results path/to/your/results \
  --output_folder processed \
  --max_size 1024
```

  * `--input_folder`: Your raw `input/` images.
  * `--method_results`: Parent folder of all method subfolders.
  * `--output_folder`: Where the cleaned `processed/` directory will be created.
  * `--max_size`: Maximum width or height for resized images (default: 1024).

### 2\. HTML Gallery Generation

```bash
python src/html_gallery.py \
  --input_folder processed/input \
  --captions_folder path/to/your/captions \
  --method_results processed/method_results \
  --html_output gallery.html \
  --images_per_row 4
```

  * `--input_folder`: The processed input directory.
  * `--captions_folder`: Directory containing your `<basename>.txt` caption files.
  * `--method_results`: The processed, normalized method outputs directory.
  * `--html_output`: Output HTML filename (default: `gallery.html`).
  * `--images_per_row`: Number of columns in the CSS grid (default: 4).

## 🎨 Customization

  * **CSS Tweaks:** Edit the `<style>` block directly in `src/html_gallery.py`.
  * **Image Resolution:** Change the `--max_size` argument to control image dimensions.
  * **Gallery Layout:** Adjust `--images_per_row` for more or fewer columns.

## 📁 Sample Data

This repository includes sample data using public domain images from Unsplash:

  * `sample_data/input/`: 3 sample input images.
  * `sample_data/method_results/`: Simulated method outputs in a nested structure.
  * `sample_data/captions/`: Sample caption files.

## 🤝 Contributing

Contributions are welcome\! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
