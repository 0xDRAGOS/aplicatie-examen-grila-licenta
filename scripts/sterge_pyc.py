import os

def delete_pyc_and_pycache(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".pyc"):
                try:
                    os.remove(os.path.join(root, file))
                    print(f"Șters: {file}")
                except Exception as e:
                    print(f"Eroare la ștergerea {file}: {e}")
        for dir_name in dirs:
            if dir_name == "__pycache__":
                path = os.path.join(root, dir_name)
                try:
                    os.rmdir(path)
                    print(f"Șters folder: {path}")
                except Exception as e:
                    print(f"Eroare la ștergerea {path}: {e}")

if __name__ == "__main__":
    delete_pyc_and_pycache(".")
