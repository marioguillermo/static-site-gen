import os
import shutil


def copy_static_to_public(source='static', destination='public'):
    # Step 1: Delete all contents of the destination directory
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print(f"Cleared destination directory: {destination}")

    # Step 2: Recreate the empty destination directory
    os.makedirs(destination, exist_ok=True)

    # Step 3: Recursive copy
    def recursive_copy(src, dest):
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dest_path = os.path.join(dest, item)

            if os.path.isdir(src_path):
                os.makedirs(dest_path, exist_ok=True)
                recursive_copy(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)
                print(f"Copied: {src_path} -> {dest_path}")

    # Start the recursive copy
    recursive_copy(source, destination)


if __name__ == '__main__':
    copy_static_to_public()
