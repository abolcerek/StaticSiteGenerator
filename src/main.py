import os
import shutil

def copy_static(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        return
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    def recursion(source_dir, dest_dir):
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)
        directories = os.listdir(source_dir)
        for file in directories:
            full_path = os.path.join(source_dir, file)
            print(f"copying {full_path} -> {dest_dir}")
            if os.path.isfile(full_path):
                shutil.copy(full_path, dest_dir)
            else:
                subdir = os.path.join(dest_dir, file)
                recursion(full_path, subdir)
    recursion(source_dir, dest_dir)

    
def main():
    copy_static("./static", "./public")
main()
