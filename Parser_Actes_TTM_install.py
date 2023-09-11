'''
Script per automatitzar la instal·lació del programa
Parser Emails de la Taula Tècnica de Mobilitat del Districte.
'''

import zipfile as zf
import os
import glob



def unzip(path_src: str, path_dest: str):
    '''
    :param path_src: Path de la carpeta d'origen del conjunt de
    dades original en format ZIP.
    :param path_dest: Path de la carpeta de destinació de les
    dades descomprimides.
    En aquest cas, aquesta funció no retornarà cap valor,
    doncs només executa una tasca concreta.
    '''

    with zf.ZipFile(path_src, 'r') as zip_f:
        # Descomprimim tot el contingut del zip
        zip_f.extractall(path_dest)

def desplegament(path: list):
    '''
    En primer lloc, definim la funció desplegament per crear la
    estructura de subcarpetes en la carpeta data i traslladar
    el conjunt de dades original a la carpeta "0_dades_no_processades".

    :param path: Llista de nom de les carpeta arrel on organitzarem les dades.
    V. més detalls en el comentari corresponent en main.
    :return: No retorna cap valor doncs només s'executen tasques.
    '''

    for p in path:
        # Com sabem que el darrer objecte en la llista correspon a la nova
        # subcarpeta figures que ha de crear-se en la nova carpeta reports,
        # introduïm una sentència iterativa en que realitzi una execució
        # lleument diferent amb el darrer objecte de la llista.
        full_path = PATH + p + "/"
        os.makedirs(full_path, exist_ok=True)

    
    for fin in glob.glob(PATH + "*.zip"):
        unzip(fin, PATH)

    return

PATH = 'parser_actes_ttm/'
PATH_2 = ['data', 'reports']
subcarpetes = desplegament(PATH_2)



