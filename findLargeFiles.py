import os
import fnmatch

# 100MB = 100 * 1024 * 1024 bytes
SIZE_LIMIT = 100 * 1024 * 1024


def read_gitignore(gitignore_path):
    ignore_patterns = []
    try:
        with open(gitignore_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.append(line)
    except FileNotFoundError:
        print(f"Error: Cannot find '{gitignore_path}'")
    return ignore_patterns


# According to the .gitignore, remove the ignored ones from our list
def is_ignored(file_path, ignore_patterns):
    normalized_path = os.path.relpath(file_path).replace(os.sep, '/')
    for pattern in ignore_patterns:
        if pattern.endswith('/'):
            pattern = pattern[:-1]
            if normalized_path.startswith(pattern + '/'):
                return True
        elif fnmatch.fnmatch(normalized_path, pattern):
            return True
    return False


def is_hidden(file_path):
    # remove the dot ones like '.git'
    return os.path.basename(file_path).startswith('.')


def find_large_files(directory, ignore_patterns):
    large_files = []

    for root, dirs, files in os.walk(directory):
        # Remove directories that are ignored and hidden directories
        dirs[:] = [d for d in dirs if
                   not (is_ignored(os.path.join(root, d), ignore_patterns) or is_hidden(os.path.join(root, d)))]

        for file in files:
            file_path = os.path.join(root, file)

            # remove the hidden ones
            if not (is_ignored(file_path, ignore_patterns) or is_hidden(file_path)):
                try:
                    file_size = os.path.getsize(file_path)
                    if file_size > SIZE_LIMIT:
                        large_files.append(file_path)
                except OSError as e:
                    print(f"Cannot access {file_path}: {e}")

    return large_files


# According to lfs tracklist, write the file needed to be added.
def write_lfs_tracklist(large_files, output_file):
    with open(output_file, 'w') as f:
        for file in large_files:
            relative_path = os.path.relpath(file)
            f.write(f"{relative_path}\n")


def main():
    directory = os.getcwd() # Get the current working directory
    gitignore_path = os.path.join(directory, '.gitignore')
    ignore_patterns = read_gitignore(gitignore_path)

    if not ignore_patterns:
        print("We did not find .gitignore file, please configure it first.")
        return

    large_files = find_large_files(directory, ignore_patterns)

    if large_files:
        print(f"Found {len(large_files)} file(s) more than 100MB.")
        for file in large_files:
            print(file)
        output_file = os.path.join(directory, 'PyRecommend.txt')
        write_lfs_tracklist(large_files, output_file)
        print(f"PyRecommend File {output_file} summoned successfully.")
    else:
        print("There is no file more than 100MB.")


if __name__ == "__main__":
    main()
