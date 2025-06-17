# filepath: /image-gallery-generator/image-gallery-generator/src/html_gallery.py
# Generate an HTML gallery of input images and method outputs,
# flexibly matching result filenames with any scale suffix and configurable columns per row.

import os
import argparse


def get_input_images(input_folder):
    """Return a sorted list of image filenames in the given folder."""
    return sorted([f for f in os.listdir(input_folder)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))])


def load_captions(captions_folder, image_filename):
    """Load caption from the corresponding .txt file in the captions folder."""
    caption_file = os.path.join(
        captions_folder,
        os.path.splitext(image_filename)[0] + '_caption.txt'
    )
    try:
        with open(caption_file, 'r') as cf:
            return cf.read().strip()
    except FileNotFoundError:
        return "No caption available"


def get_method_folders(method_results_folder):
    """Return a sorted list of subdirectory paths under the given folder."""
    return sorted(
        os.path.join(method_results_folder, d)
        for d in os.listdir(method_results_folder)
        if os.path.isdir(os.path.join(method_results_folder, d))
    )


def generate_html(input_images, input_folder, captions_folder,
                  method_folders, html_filename, images_per_row):
    """Generate an HTML gallery with fixed-size images in rows of `images_per_row`,
    matching result files by basename plus any suffix before '_result'."""
    with open(html_filename, 'w') as f:
        f.write("<html>\n<head>\n<title>Image Gallery</title>\n")
        f.write("<style>\n")
        f.write(f".image-group {{ border: 2px solid #333; margin-bottom: 20px; padding: 10px; }}\n")
        f.write(f".gallery-row {{ display: grid; grid-template-columns: repeat({images_per_row}, 1fr); gap: 10px; margin-bottom: 10px; }}\n")
        f.write(".gallery-item { text-align: center; border: 1px solid #ccc; padding: 5px; }\n")
        f.write(".gallery-item img { width: 100%; height: auto; }\n")
        f.write("</style>\n</head>\n<body>\n")

        for image in input_images:
            caption_text = load_captions(captions_folder, image)
            image_items = []

            input_path = os.path.join(input_folder, image).replace(os.sep, '/')
            image_items.append((input_path, "Input Image"))

            base, ext = os.path.splitext(image)
            for folder in method_folders:
                # Look for any result file that starts with the base name, regardless of extension
                candidates = [fn for fn in os.listdir(folder)
                              if fn.startswith(base) and '_result.' in fn]  # Changed this line
                if candidates:
                    sel = candidates[0]
                    method_path = os.path.join(folder, sel).replace(os.sep, '/')
                    label = os.path.basename(folder)
                    image_items.append((method_path, label))
                else:
                    image_items.append((None, None))

            while len(image_items) % images_per_row != 0:
                image_items.append((None, None))

            f.write("<div class='image-group'>\n")
            f.write("<div class='gallery-row'>\n")
            for src, label in image_items:
                if src is None:
                    f.write("<div class='gallery-item'></div>\n")
                else:
                    f.write("<div class='gallery-item'>\n")
                    f.write(f"<img src='{src}' alt='{label}'/>\n")
                    f.write(f"<div>{label}</div>\n")
                    f.write("</div>\n")
            f.write("</div>\n")
            f.write(f"<p>{caption_text}</p>\n")
            f.write("</div>\n")

        f.write("</body>\n</html>")

    print(f"HTML file generated: {html_filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate an HTML gallery for input images and method outputs"
    )
    parser.add_argument('--input_folder', type=str, default='input',
                        help="Folder containing input images.")
    parser.add_argument('--captions_folder', type=str, default='replies',
                        help="Folder containing caption files.")
    parser.add_argument('--method_results', type=str, default='method_results',
                        help="Folder containing method result subdirs.")
    parser.add_argument('--html_output', type=str, default='gallery.html',
                        help="Output HTML filename.")
    parser.add_argument('--images_per_row', type=int, default=4,
                        help="Number of images per row in the gallery.")
    args = parser.parse_args()

    inputs = get_input_images(args.input_folder)
    if not inputs:
        print("No input images found. Exiting.")
        return

    methods = get_method_folders(args.method_results)
    if not methods:
        print(f"No method result directories in '{args.method_results}'. Exiting.")
        return

    generate_html(inputs, args.input_folder,
                  args.captions_folder, methods,
                  args.html_output, args.images_per_row)


if __name__ == '__main__':
    main()