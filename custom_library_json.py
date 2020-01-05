import sys
import filecmp
from os import path
from shutil import copyfile


def apply(env, path_to_directory_with_custom_library_json, library_name):
    """
    Copies the library.json from the path:

    <project_root_directory>/<path_to_directory_with_custom_library_json>/
    <library_name>/library.json

    to the place in the PIO build directory where the library is downloaded.

    Takes the map with environmental variables from PIO as the first argument
    (obtained with 'Import("env")' and the accessible with 'env' variable).
    """

    root_dir = env['PROJECT_DIR']
    pio_env = env['PIOENV']
    libdeps_dir = env['PROJECT_LIBDEPS_DIR']

    library_json_src_path = path.join(
        root_dir,
        path_to_directory_with_custom_library_json,
        library_name,
        'library.json')

    library_json_dst_path = path.join(
        libdeps_dir, pio_env, library_name, 'library.json')

    if not path.exists(path.dirname(library_json_dst_path)):
        print("The library {} is not found in the building directory".format(
            library_name), file=sys.stderr)
    else:
        if not path.exists(library_json_dst_path) or \
           not filecmp.cmp(library_json_src_path, library_json_dst_path):
            print("Overwriting library.json in {}".format(library_name))
            copyfile(library_json_src_path, library_json_dst_path)
