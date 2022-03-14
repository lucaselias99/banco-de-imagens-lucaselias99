import os

FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")


def create_directories():
    for extension in ALLOWED_EXTENSIONS.split(","):
        path = f"{FILES_DIRECTORY}/{extension}"

        if not os.path.exists(path):
            os.makedirs(path)


create_directories()
