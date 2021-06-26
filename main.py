import concurrent.futures
import copy
import os
import os.path

mod_info_preset = """
version="3.*.*"
tags={
    "Gameplay"
}
name="MOD_FOLDER_NAME"
supported_version="3.*.*"
path="mod/MOD_FOLDER_NAME"
"""


def delete_if_mod_info_file(dir_entry):
    if dir_entry.is_file() and ".mod" in dir_entry.name:
        os.remove(dir_entry.path)


def delete_mod_info_file_recursive(dir_entry):
    if dir_entry.is_file():
        delete_if_mod_info_file(dir_entry)
        return
    elif dir_entry.is_dir():
        with os.scandir(dir_entry) as next_dir_entries:
            for next_dir_entry in next_dir_entries:
                delete_mod_info_file_recursive(next_dir_entry)


def delete_mod_info_file_thread_recursive(dir_entry):
    with concurrent.futures.ThreadPoolExecutor() as executor_service:
        with os.scandir(dir_entry) as next_dir_entries:
            for next_dir_entry in next_dir_entries:
                executor_service.submit(delete_mod_info_file_recursive, next_dir_entry)


def make_mod_info(select_folder_name):
    mode_info = copy.copy(mod_info_preset)
    mode_info = mode_info.replace("MOD_FOLDER_NAME", select_folder_name)
    return mode_info


def make_mod_info_files(select_path):
    with os.scandir(select_path) as mod_folder_entries:
        for mod_folder_entry in mod_folder_entries:
            if mod_folder_entry.is_dir():
                mode_info = make_mod_info(mod_folder_entry.name)
                mode_info_file_path = os.path.join(select_path, mod_folder_entry.name + ".mod")
                with open(mode_info_file_path, 'w') as f:
                    f.write(mode_info)


if __name__ == '__main__':
    path = "./"
    delete_mod_info_file_thread_recursive(path)
    make_mod_info_files(path)
