# Desenvolva suas rotas aqui
from flask import Flask, request
from app.kenzie.image import (
    upload_images,
    get_files,
    get_specif_files,
    download_specific_image,
    download_images,
)
from http import HTTPStatus
import os

MAX_CONTENT_LENGTH = os.getenv("MAX_CONTENT_LENGTH")
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(MAX_CONTENT_LENGTH) * 1024 * 1024


@app.post("/upload")
def upload():
    files = request.files
    for file in files.values():
        try:
            upload_images(file)
        except FileExistsError:
            return {"msg": "Nome de arquivo já existente"}, HTTPStatus.CONFLICT
        except FileNotFoundError:
            return {"msg": "Extensão não suportada"}, HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    return {"msg": "Arquivo enviado com sucesso"}, HTTPStatus.CREATED


@app.errorhandler(413)
def big_file(error):
    return {
        "msg": f"Arquivo ultrapassou {MAX_CONTENT_LENGTH} MB"
    }, HTTPStatus.REQUEST_ENTITY_TOO_LARGE


@app.get("/files")
def list_files():
    return get_files(), HTTPStatus.OK


@app.get("/files/<extension>")
def list_files_by_extension(extension):
    try:
        return get_specif_files(extension), HTTPStatus.OK
    except FileNotFoundError:
        return {"msg": "Formato de extensão não suportada"}, HTTPStatus.NOT_FOUND


@app.get("/download/<file_name>")
def download(file_name):
    try:
        return download_specific_image(file_name), HTTPStatus.OK
    except FileNotFoundError:
        return {"msg": "Arquivo não encontrado"}, HTTPStatus.NOT_FOUND
    except IndexError:
        return {"msg": "Nome de arquivo inválido"}, HTTPStatus.NOT_FOUND


@app.get("/download-zip")
def download_dir_as_zip():
    file_extension = request.args.get("file_extension")
    compression_ratio = request.args.get("compression_ratio", 6)
    if not file_extension:
        return download_images(file_extension, compression_ratio, True), HTTPStatus.OK

    return download_images(file_extension, compression_ratio, False), HTTPStatus.OK
