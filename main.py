"""
Select a folder.
The folder you select, every .jfif image will
be converted to a PNG and exported in a sub folder of this py file.
"""
import logging
import os
from typing import Iterable
from tkinter.filedialog import askdirectory

from PIL import Image
from PIL import UnidentifiedImageError


def check_allowed_suffix(filename: str, allowed_suffix: Iterable) -> bool:
    """Return true if filename is one of the formats in allowed_suffix.
    """
    for suffix in allowed_suffix:
        if filename[-len(suffix):] == suffix:
            return True
    else:
        return False


def collect_files_from_dir(import_folder_path: str, allowed_dir_names: list[str]) -> list[str]:
    """Return a list of filenames from a directory, and then
    only include images within the allowed formats.
    """
    arr = get_files(import_folder_path)
    # arr = os.listdir(import_folder_path)
    allowed_img_files = []
    for filename in arr:
        if check_allowed_suffix(filename, allowed_dir_names):
            allowed_img_files.append(filename)
    return allowed_img_files


def get_files(dir_path: str):
    """Function from https://stackoverflow.com/a/168580"""
    a = [s for s in os.listdir(dir_path)
         if os.path.isfile(os.path.join(dir_path, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dir_path, s)), reverse=True)
    return a


def create_new_dir(export_dir_name: str) -> None:
    """Create the export directory. If it already exists, do nothing.
    """
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, export_dir_name)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    else:
        logging.warning('export path already exists')


def remove_suffix(file_name: str) -> str:
    """Remove the suffix from the file name"""
    return file_name.split('.')[0]


def main() -> None:
    """Public static void main string args"""
    export_dir_name = 'export'
    img_formats = ['.webp', '.jfif']
    dire = askdirectory(title="WHAT FOLDER WOULD YOU LIKE TO TARGET?").replace('/', '\\')
    files = collect_files_from_dir(dire, img_formats)
    create_new_dir(export_dir_name)
    for i, img_file in enumerate(files):
        img_full_dir = dire + "\\" + img_file
        print(f'saving {img_file} as PNG')
        try:
            im = Image.open(img_full_dir).convert("RGBA")
            im.save(f"{export_dir_name}\\{i}_{remove_suffix(img_file)}.png", "png")
        except UnidentifiedImageError:
            logging.warning(f"Couldn't convert {img_file} for some reason")


if __name__ == '__main__':
    main()
