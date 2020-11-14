from pathlib import Path
#define the project root, independently from the local path of the user
def get_project_root() -> Path:
    return Path(__file__).parent.parent
