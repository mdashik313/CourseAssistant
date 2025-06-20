#!/usr/bin/python
import os
import subprocess

# Configs
include_ext = ["css"]  # Remove File Types
ignore_list = [".git", ".vscode", "placeholder"]  # Ignore Files/Folders from Scanning
curr_dir = os.getcwd()  # Current Directory
src_dir = curr_dir + '/static/css/src'
dist_dir = curr_dir + '/static/css/dist'


# Functions
def run_fast_scandir(src, ignore=[], inc_ext=[]):
    subfolders, files = [], []

    for f in os.scandir(src):
        if f.name not in ignore:
            if f.is_dir():
                subfolders.append(f.path)
            elif f.is_file():
                ext = f.name.split('.')[-1]
                if (ext != f.name) and (ext in inc_ext):
                    clean_path = f.path.replace(src_dir, '')
                    files.append(clean_path)

    for src in list(subfolders):
        sub_folders, f = run_fast_scandir(src, ignore, inc_ext)
        subfolders.extend(sub_folders)
        files.extend(f)
    return subfolders, files


def build_css(filename):
    filename = filename.replace('\\', '/')
    src_file = src_dir + filename
    dist_file = dist_dir + filename
    cmd = f'npx tailwindcss -i {src_file} -o {dist_file} --minify'
    subprocess.Popen(cmd, shell=True)


# Main
sf, file_list = run_fast_scandir(src_dir, ignore_list, include_ext)

for item in file_list:
    print(f"-> Building \"{item}\"")
    build_css(item)
