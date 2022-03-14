# Desenvolva sua lógica de manipulação das imagens aqui
import os
from flask import send_file, send_from_directory
from werkzeug.datastructures import FileStorage

from app.kenzie import FILES_DIRECTORY


def upload_images(file: FileStorage):
    filename = file.filename
    extension = filename.split(".")[1]
    FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
    path = f"{FILES_DIRECTORY}/{extension}"
    if filename in os.listdir(path):

        raise FileExistsError

    file.save(f"{path}/{filename}")


def get_files():

    gif = os.listdir(f"{FILES_DIRECTORY}/gif")
    png = os.listdir(f"{FILES_DIRECTORY}/png")
    jpg = os.listdir(f"{FILES_DIRECTORY}/jpg")
    output = {"gif": gif, "png": png, "jpg": jpg}
    return output


def get_specif_files(extension):

    ext = os.listdir(f"{FILES_DIRECTORY}/{extension}")
    extension_name = ext[0].split(".")[1]

    return {f"{extension_name}": ext}


def download_specific_image(file):
    extension = file.split(".")[1]
    path = f".{FILES_DIRECTORY}/{extension}"
    if file in os.listdir(f"{FILES_DIRECTORY}/{extension}"):
        return send_from_directory(directory=path, path=file, as_attachment=True)
    raise FileNotFoundError


def download_images(file_extension, compression_ratio, bool: bool):
    if bool:
        filename = "images.zip"
        png_path = f"{FILES_DIRECTORY}/png"
        gif_path = f"{FILES_DIRECTORY}/gif"
        jpg_path = f"{FILES_DIRECTORY}/jpg"
        save_path = os.path.join("/tmp", filename)

        terminal = (
            f"zip -r -{compression_ratio} {save_path} {png_path} {jpg_path} {gif_path}"
        )
    else:
        filename = f"{file_extension}.zip"
        directory_path = os.path.join(FILES_DIRECTORY, file_extension)
        save_path = os.path.join("/tmp", filename)
        terminal = f"zip -r -j -{compression_ratio} {save_path} {directory_path}"

    if os.path.isfile(save_path):
        os.remove(save_path)
    os.system(terminal)
    return send_file(save_path, as_attachment=True)
