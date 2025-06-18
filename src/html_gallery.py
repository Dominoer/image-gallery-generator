# html_gallery.py
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
        os.path.splitext(image_filename)[0] + '_reply.txt'
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
                  method_folders, html_filename, cols):
    """Generate an HTML gallery with fixed-size images in rows of `cols`,
    matching result files by basename plus any suffix before '_result'."""
    with open(html_filename, 'w') as f:
        f.write("<html>\n<head>\n<title>Image Gallery</title>\n")
        f.write("<style>\n")
        # dynamic grid-template based on cols
        f.write(f".image-group {{ border: 2px solid #333; margin-bottom: 20px; padding: 10px; }}\n")
        f.write(f".gallery-row {{ display: grid; grid-template-columns: repeat({cols}, 1fr); gap: 10px; margin-bottom: 10px; }}\n")
        f.write(".gallery-item { text-align: center; border: 1px solid #ccc; padding: 5px; }\n")
        f.write(".gallery-item img { width: 100%; height: auto; }\n")
        f.write("</style>\n</head>\n<body>\n")

        for image in input_images:
            caption_text = load_captions(captions_folder, image)
            image_items = []

            # Input image first
            input_path = os.path.join(input_folder, image).replace(os.sep, '/')
            image_items.append((input_path, "Input Image"))

            base, ext = os.path.splitext(image)
            for folder in method_folders:
                # Look for exact match or match with scale suffix
                candidates = []
                for fn in os.listdir(folder):
                    if fn.endswith(f"_result{ext}"):
                        # Extract the base part before any suffix
                        result_base = fn.replace(f"_result{ext}", "")
                        # Check if it matches exactly or starts with base followed by underscore
                        if result_base == base or result_base.startswith(base + "_"):
                            candidates.append(fn)
                
                if candidates:
                    # Prefer exact match, otherwise take the first one
                    exact_match = f"{base}_result{ext}"
                    if exact_match in candidates:
                        sel = exact_match
                    else:
                        sel = candidates[0]
                    method_path = os.path.join(folder, sel).replace(os.sep, '/')
                    label = os.path.basename(folder)
                    image_items.append((method_path, label))
                else:
                    image_items.append((None, None))

            # pad to multiple of cols
            while len(image_items) % cols != 0:
                image_items.append((None, None))

            # write group
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
    parser.add_argument('--captions_folder', type=str, default='captions',
                        help="Folder containing caption files.")
    parser.add_argument('--method_results', type=str, default='method_results',
                        help="Folder containing method result subdirs.")
    parser.add_argument('--html_output', type=str, default='gallery.html',
                        help="Output HTML filename.")
    parser.add_argument('--cols', type=int, default=4,
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
                  args.html_output, args.cols)


if __name__ == '__main__':
    main()
