"""
pre_process.py

Pre-process your image dataset:
 1. Resize input images to a max dimension (default 1024px), preserving aspect ratio.
 2. Flatten and reorganize method result folders into a single `method_results/` directory under the output folder, naming each subfolder by joining nested method names and scale levels (e.g. `MethodA_scale_0.30`).
 3. Normalize result filenames to `<basename>_result<ext>` and resize them to match corresponding (resized) input sizes.

Usage:
    python pre_process.py \
        --input_folder input \
        --method_results method_results \
        --output_folder processed \
        --max_size 1024
"""
import os
import argparse
from PIL import Image


def compute_target_size(width, height, max_size):
    """
    Compute a new size so that the larger dimension is at most max_size,
    preserving aspect ratio.
    """
    if width > max_size or height > max_size:
        scale = min(max_size / width, max_size / height)
        return (int(width * scale), int(height * scale))
    return (width, height)


def process_input_images(input_folder, output_input_folder, max_size):
    os.makedirs(output_input_folder, exist_ok=True)
    size_dict = {}
    for fname in sorted(os.listdir(input_folder)):
        if not fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        src = os.path.join(input_folder, fname)
        with Image.open(src) as img:
            orig_size = img.size
            target_size = compute_target_size(orig_size[0], orig_size[1], max_size)
            if target_size != orig_size:
                img_proc = img.resize(target_size, Image.Resampling.LANCZOS)
                print(f"Resized input {fname}: {orig_size} → {target_size}")
            else:
                img_proc = img.copy()
                print(f"Input {fname} within limits, size {orig_size}")
            dst = os.path.join(output_input_folder, fname)
            img_proc.save(dst)
        base = os.path.splitext(fname)[0]
        size_dict[base] = target_size
    return size_dict


def process_method_results(method_results_folder, output_results_folder, size_dict):
    for root, _, files in os.walk(method_results_folder):
        for fname in files:
            if '_result' not in fname:
                continue
            rel = os.path.relpath(root, method_results_folder)
            parts = rel.split(os.sep)
            method_name = '_'.join(parts)
            out_dir = os.path.join(output_results_folder, method_name)
            os.makedirs(out_dir, exist_ok=True)

            base = fname.split('_result')[0]
            ext = os.path.splitext(fname)[1]
            new_fname = f"{base}_result{ext}"

            src = os.path.join(root, fname)
            dst = os.path.join(out_dir, new_fname)
            with Image.open(src) as img:
                target_size = size_dict.get(base)
                if target_size:
                    img_proc = img.resize(target_size, Image.Resampling.LANCZOS)
                    print(f"Resized result {fname}: → {target_size}")
                else:
                    img_proc = img.copy()
                    print(f"No input size for {base}, keeping original size {img.size}")
                img_proc.save(dst)


def main():
    parser = argparse.ArgumentParser(
        description="Pre-process inputs and method results into a flat, resized structure."
    )
    parser.add_argument('--input_folder', type=str, default='input',
                        help="Folder containing raw input images.")
    parser.add_argument('--method_results', type=str, default='method_results',
                        help="Original nested method_results parent folder.")
    parser.add_argument('--output_folder', type=str, default='processed',
                        help="Root output folder for processed data.")
    parser.add_argument('--max_size', type=int, default=1024,
                        help="Max dimension for resizing images.")
    args = parser.parse_args()

    out_input = os.path.join(args.output_folder, 'input')
    out_methods = os.path.join(args.output_folder, 'method_results')

    sizes = process_input_images(args.input_folder, out_input, args.max_size)
    process_method_results(args.method_results, out_methods, sizes)

if __name__ == '__main__':
    main()
