'''
Aquest fitxer conté les 4 subfuncions principals que executen diverses
tasques:

-
'''
import pandas as pd
from extract_msg import Message
import zipfile as zf
import shutil
import os

def unzip(path_origen: str, path_dest: str):
    '''
    :param path_origen: Path de la carpeta d'origen del conjunt de
    dades original en format ZIP.
    :param path_dest: Path de la carpeta de destinació de les
    dades descomprimides.

    En aquest cas, aquesta funció no retornarà cap valor,
    doncs només executa una tasca concreta.
    '''

    with zf.ZipFile(path_origen, 'r') as zip_f:
        # Descomprimim tot el contingut del zip
        zip_f.extractall(path_dest)


def read_msg(file):
    '''
    :param file: Path de cadascun dels arxius generats en la
    iteració executada per la funció desplegament.

    :return: Retorna un diccionari amb l'assumpte (Subject) i el cos
    (Body) corresponents a cada missatge en format MSG i que
    formaran part de la llista de diccionaris.
    '''
    msg = Message(file)
    dicc = {'subj': msg.subject, 'body': msg.body}

    return dicc


def read_other_files(folder):
    '''
    :param folder: Path de la carpeta que conté els fitxers CSV
    amb dades complementàries.

    :return: Retorna un dataframe amb la relació de temes calssificats per
    barris i un diccionari amb la relació de codi de reunió amb
    la seva respectiva data de realització.
    '''
    ID_filename = "ID_Dates.csv"
    path_ID_file = os.path.join(folder, ID_filename)
    ID_Dates = pd.read_csv(path_ID_file)
    dicc_ID_Dates = ID_Dates.to_dict(orient='index')
    # Emprem el paràmetre "index" doncs conserva l'índex com claus del
    # diccionari de diccionaris resultant. V. doc. oficial:
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_dict.html
    # No val la pena convertir-ho en llista de diccionaris, tal i com es
    # podria fer amb una llista comprimida: https://stackoverflow.com/a/49248618
    barris_filename = "temes_barris.csv"
    path_temes_file = os.path.join(folder, barris_filename)
    temes_barris = pd.read_csv(path_temes_file)

    return dicc_ID_Dates, temes_barris


def remove(path_origen: str, path_folders: list):
    '''
    :param path: Path de la carpeta que conté les carpetes a
    eliminar.

    En aquest cas, aquesta funció no retornarà cap valor,
    doncs només executa una tasca concreta.
    '''

    for folder in path_folders:
        path_delete = path_origen + "/" + str(folder) + "/"
        # https://www.geeksforgeeks.org/python-os-path-isdir-method/
        if os.path.isdir(path_delete):
            shutil.rmtree(path_delete, ignore_errors=True)
            print(f"Els continguts de la carpeta {path_delete} s'han eliminat amb èxit.")
        else:
            print(f"Error: la carpeta {path_delete} no existeix.")


