import os.path
import sys
from pathlib import Path
from shutil import copyfile


def _eprint(*args, **kwargs):
    """ Prints to stderr """
    print(*args, file=sys.stderr, **kwargs)


def _lines_to_list(path):
    """
    Reads file from at the specified path and creates a list which contains
    lines from the file, without a newline.
    """
    with open(path, 'r') as f:
        return f.read().splitlines()


def _is_ignored(path):
    """
    Checks whether the specified path is ignored within the Mbed compilation.
    In details, takes the .mbedignore file in the path and checks whether it
    contains a line with string '*'.
    """
    mbedignore_path = os.path.join(path, '.mbedignore')
    if not Path(mbedignore_path).is_file():
        return False
    with open(mbedignore_path) as f:
        lines = f.read().splitlines()
    return '*' in lines


def _is_extra_newline_necessary(file):
    """
    Returns True if in the specific file, at the specified path (parameter
    file is a path to the file) an extra newline shall be added when writing
    a line to it. Sometimes there is no newline at the end of the file
    so this function checks that.
    """
    if not Path(file).is_file() or os.path.getsize(file) == 0:
        return False
    with open(file, 'rb+') as f:
        f.seek(-1, os.SEEK_END)
        last_character = f.read()
    return not last_character == b'\r' and not last_character == b'\n'


def _make_ignored(path):
    """
    Disable the path from the mbed compilation.
    Effectively it puts a line with string '*' in the .mbedignore file in the
    specified path.
    """
    mbedignore_path = os.path.join(path, '.mbedignore')
    string_to_append = '*\n' if not _is_extra_newline_necessary(
        mbedignore_path) else '\n*\n'
    with open(mbedignore_path, 'a') as f:
        f.write(string_to_append)


def _lines_to_set(path):
    """
    Converts lines from the file in the specified path to set of strings
    which are lines in the file. Returns empty set when file doesn't exist.
    """
    out = set()
    if Path(path).is_file():
        with open(path) as f:
            out = set(f.read().splitlines())
    return out


def _get_file_difference(left_file_path, right_file_path):
    """
    Returns a pair which is a difference between two files. The left return
    value are lines which are only present in the left file, the right return
    value are lines which are only present in the right file.
    """
    left = _lines_to_set(left_file_path)
    right = _lines_to_set(right_file_path)
    only_in_left = left.difference(right)
    only_in_right = right.difference(left)
    return only_in_left, only_in_right


def _make_unignored(path):
    """
    Include the specified path in Mbed compilation.
    Performs opposite action to _make_ignored function.
    """
    mbedignore_path = os.path.join(path, '.mbedignore')
    lines = _lines_to_list(mbedignore_path)
    lines.remove('*')
    if len(lines) == 0:
        Path(mbedignore_path).unlink()
    else:
        with open(mbedignore_path, 'w') as f:
            for line in lines:
                f.write(line + '\n')


def _ignore_paths(framework_path, rel_paths_to_ignore):
    """ Ignore specific paths in the Mbed compilation """
    for rel_path_to_ignore in rel_paths_to_ignore:
            # Prevent from adding multiple lines with '*' in the .mbedignore file
        path_to_ignore = os.path.join(
            framework_path, rel_path_to_ignore)
        if not _is_ignored(path_to_ignore):
            _make_ignored(path_to_ignore)


def _unignore_paths(framework_path, rel_paths_to_unignore):
    """ Include specific paths in the Mbed compilation """
    for rel_path_to_unignore in rel_paths_to_unignore:
        path_to_unignore = os.path.join(
            framework_path, rel_path_to_unignore)
        if _is_ignored(path_to_unignore):
            _make_unignored(path_to_unignore)


def _print_usage():
    print("\nUSAGE:\n\t<path to .mbedignore> "
          "<path to mbed-os framework in the PlatformioIO root directory>")
    print("\nEXAMPLE:\n\tpython3 mbedignore.py "
          "/home/user/Workspace/SomePioProject/.mbedignore "
          "/home/user/.platformio/packages/framework-mbed")


def _print_usage_and_exit():
    _print_usage()
    exit()


def apply(mbedignore_path, framework_path):
    """
    Apply rules related to ignoring paths in the mbed-os framework.

    Parameters:
    mbedignore_path (string): Path to .mbedignore file.
    framework_path (string): Path to mbed-os framework used by PlatformIO.

    This function will take the .mbedignore file in the path specified as the
    first parameter and will ignore them in the Mbed compilation within the
    PlatformIO ecosystem.

    The .mbedignore shall contain the paths to be ignored relatively from the
    framework's root directory, so the example content may be:
    features/cryptocell
    features/nfc

    This function will keep track of the previously ignored paths. This is done
    to be flexible when working with different projects which have different
    .mbedignore files.

    """
    # Perform sanitization
    if not Path(mbedignore_path).is_file():
        _eprint("\nERROR: Input .mbedignore is not a file.")
        _print_usage_and_exit()
    if not Path(framework_path).is_dir():
        _eprint(
            "\nERROR: The specified path to the mbed-os framework "
            "is not a directory.")
        _print_usage_and_exit()

    # The previous .mbedignore used by this program was put in the
    # mbed-os framework's root directory.
    previous_mbedignore_path = os.path.join(framework_path, '.mbedignore')

    # If in the old file there are lines which are not present in the new file
    # then we must unignore the paths in those lines. If in the new file there
    # there are paths not present in the old file, then we must ignore those
    # paths.
    rel_paths_to_unignore, rel_paths_to_ignore = _get_file_difference(
        previous_mbedignore_path, mbedignore_path)

    _ignore_paths(framework_path, rel_paths_to_ignore)
    _unignore_paths(framework_path, rel_paths_to_unignore)

    # Overwrite the old .mbedignore with the new on in the mbed-os framework's
    # root directory to keep track which paths were ignored earlier, to know
    # which paths need to be 'unignored'
    copyfile(mbedignore_path, previous_mbedignore_path)


if __name__ == '__main__':
    # Execute only if run as a script
    if(len(sys.argv) != 3):
        _eprint("\nERROR: Wrong number of parameters")
        _print_usage_and_exit()
    apply(sys.argv[1], sys.argv[2])
