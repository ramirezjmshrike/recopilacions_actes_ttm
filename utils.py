'''
Aquest fitxer conté les 5 funcions principals que executen el programa:

- desplegament(): Executa les tasques per descomprimir i llegir els fitxers
                que conté la font de dades originals i retorna dues llistes
                de diccionaris amb dades de l'ordre del dia i actes de reunions.

- parsing_ttm(): Executa les tasques relatives a generar les variables de referència
                i descripció de cada tema en l'ordre del dia de cada reunió i també
                l'acord en l'acta corresponent.

- cleaning_dict(): Executa tasques de neteja de dades en les llistes de diccionaris.

- manipulacio(): Executa tasques de conversió de cada diccionari en DataFrame,
                concatenació (unió vertical) d'aquests, merge (unió horitzontal) amb
                la classificació de temes per barris a més de les tasques de neteja
                que és preferible realitzar en un DataFrame i creació de la variable
                "Ref. Tema i Reunió".

- output():     Executa les tasques per convertir el dataset ja processat en formats
                fàcils de compartir o adequats per fer-hi anàl·lisis o estudis
                específics.

En una futura versió es preveu implementar un paral·lelisme dins de la funció
# desplegament(). V. més detalls en el fitxer README.
'''
import pandas as pd
from datetime import date
from multiprocessing import cpu_count, Pool
import re
import glob
import os
import sys
from src.desplegament import unzip, read_msg, read_other_files, remove
from src.parsing import parsing_ttm
from src.cleaning import replace_continguts, sub_continguts, \
    cleaning_df, separar_paraules, replace_typos, sub_typos
from src.manipulacio import to_df, gen_ref_reunions

def desplegament(carpetes: list):
    '''
    :param carpetes: Llista de noms de carpetes amb les que
                    s'executaran diverses tasques.
    
    :return: Aquesta funció retorna els següents valors:
            - 
            - 
            - 
            - 
    '''  
    zipfiles = os.path.join(carpetes[0], "*.zip")

    for fin in glob.glob(zipfiles):
        unzip(fin, carpetes[0])

    # Filtrem els continguts de la carpeta origen de manera
    # que no enumeri en la llista els fitxers que també hi
    # siguin presents. Font: https://stackoverflow.com/a/72039309 
    folders = [name for name in os.listdir(carpetes[0]) if os.walk(name)]
    zips = ".zip"
    folders = [f for f in folders if all(z not in f for z in zips)]


    # En primer lloc, volem comprovar si la màquina que executa el
    # programa disposa d'una o més CPU. Per fer aquest avaluació
    # mitjançant la funció cpu_count ens inspirem en aquest exemple
    # del site StackOverflow: https://stackoverflow.com/a/1006337
    # En el cas de només disposar d'1 CPU, llavors realitzarem una
    # execució seqüencial.
    if cpu_count() == 1:
        for f in folders:
            msgfiles = os.path.join(carpetes[0], f, "*.msg")        
            list_dicc = [read_msg(fin) for fin in glob.glob(msgfiles)]

            subcarpeta = os.path.join(carpetes[0], f)
            files = read_other_files(subcarpeta)
    # En el cas de disposar-ne de 2 o més, llavors realitzarem un
    # paral·lelisme amb els disponibles.
    elif cpu_count() >= 2:
        # Per implementar un multiprocess per llegir fitxers, adaptem
        # aquesta proposta del site StackOverflow:
        # https://stackoverflow.com/a/36590187
        # En el cas de disposar de 2 CPU, s'obté una millora a 2'9 segons
        # en contrast als 3'9 segons de la execució seqüencial.

        for f in folders:
            msgfiles = os.path.join(carpetes[0], f, "*.msg")
            files = [fin for fin in glob.glob(msgfiles)]

            with Pool(processes=cpu_count()) as pool:
                list_dicc = pool.map(read_msg, files)

            subcarpeta = os.path.join(carpetes[0], f)
            files = read_other_files(subcarpeta)
       
    set_subj = set([d['subj'] for d in list_dicc])

    class NumberMSG_Exception(Exception):
        pass

    try:
        # Creem una excepció per que aturi el program i esborri els fitxers generats
        # en el cas que es detecti que no coincideix el nombre l'Ordres del dia amb
        # el d'Actes diferents:
        # https://stackoverflow.com/a/49953661
        # https://medium.com/@saadjamilakhtar/5-best-practices-for-python-exception-handling-5e53b876a20 
        if len(set_subj) % 2 != 0:
            print("Aquest error s'origina per que no coincideix el nombre de fitxers\n" \
                "MSG amb Ordres del dia amb els d'Actes de reunions. Comprova que:\n" \
                "1. Que el nombre total de fitxers sigui parell.\n" \
                "2. Si el nombre total de fitxers és parell, llavors que no hi hagi\n" \
                "algun fitxer duplicat per accident.")
            print(f"Detectem {len(list_dicc)} fitxers MSG " \
                f"i d'aquests {len(set_subj)} en són diferents.")
            raise NumberMSG_Exception("Error detectat en la carpeta de fitxers MSG.")      

    except NumberMSG_Exception:
        # Eliminem els continguts de la carpeta data:
        remove(carpetes[0], folders)
        # Finalitzem la execució del robot:
        sys.exit(1)
    
    else:
        # D'altra manera, continuem amb normalitat la execució del robot:
        reunions = files[0]
        barris = files[1]  
        
        print(f"Hem recopilat {len(list_dicc)} MSG i {len(files)} CSV en total.")

        # Eliminem els continguts de la carpeta data:
        remove(carpetes[0], folders)

        # I, llavors, creem la subcarpeta específica per les dades processades:
        full_path = os.path.join(carpetes[0], carpetes[1], "")
        os.makedirs(full_path, exist_ok=True)

        return list_dicc, reunions, barris, full_path


def parsing(list_msg: list, OdD_str: str, acta_str: str):
    '''
    :param list_msg: Llista de diccionaris que conté cadascun
    l'Assumpte i el cos principal de text de cada email.
    :param OdD_str: Literal necessari per construir el patró
    regex per diferenciar entre missatges que són Ordres del dia
    o Actes de reunions.
    :param acta_str: Literal necessari per construir el patró
    regex per diferenciar entre missatges que són Ordres del dia
    o Actes de reunions.
    :return: Retorn dues llistes de diccionaris d'emails d'Ordres
    del dia i Actes de reunions, respectivament.
    '''
    rgx_OdD = "^" + OdD_str
    rgx_Acta = "^" + acta_str
    patro = ["Descripció:", "Acords:"]

    col_name = ["Descripció Ordre del dia", "Acords"]

    ODs = [parsing_ttm(m,
                       col_name[0],
                       patro[0]) for m in list_msg if re.search(rgx_OdD,
                                                                m['subj'])]

    Actes = [parsing_ttm(m,
                         col_name[1],
                         patro[1]) for m in list_msg if re.search(rgx_Acta,
                                                                  m['subj'])]

    return ODs, Actes


def cleaning(dicc: dict, col_name: str, patrons: list):
    '''
    :param dicc: Diccionari amb els diversos camps dels emails ja parsejats.
    :param cols_names: Llista amb les etiquetes de columna de les variables
    on s'ha d'han executar les tasques de neteja del text.
    :param patrons: Llista amb cinc llistes patrons literals i regex a
    eliminar; actualment només es fa ús de quatre.

    :return: Diccionari amb els patrons ja suprimits.
    '''

    # Normalització i eliminació d'epígrafs innecessaris:
    cols_names = ["Descripció del tema", col_name]
    dicc = replace_continguts(dicc, cols_names, patrons[0])
    dicc = sub_continguts(dicc, cols_names, patrons[1])
    # Correció d'errors ortotipogràfics
    dicc = replace_typos(dicc, cols_names, patrons[2])
    dicc = sub_typos(dicc, cols_names, patrons[3])
    # Separació de potencials paraules amb altres paraules i els signes
    # de puntuació:
    dicc = separar_paraules(dicc, cols_names)

    return dicc


def manipulacio(ODs: list, Actes: list, buits: str, col: str, reunions: dict, barris):
    '''
    :param ODs: Llista de diccionaris amb les dades dels Ordres del dia
    de reunions.
    :param Actes: Llista de diccionaris amb les dades dels Ordres del dia
    de reunions.
    Variables globals: S'empren també com variables globals el diccionari
    amb diccionaris

    :return: DataFrame ja llest per convertir-lo en el format ja desitjat.
    '''

    df_ODs = to_df(ODs)
    df_Actes = to_df(Actes)

    # Variable global reunions convertida a llista de diccionaris:
    reunions_lst = [d for d in reunions.values()]

    # Definim els dos DataFrame en una llista per facilitar la iteració
    # de la funció que genera la nova columna "Ref. Tema i Reunió":
    df_lst = [df_ODs, df_Actes]  # Claus [0] i [1], respectivament.

    for df_i in df_lst:
        df_i = gen_ref_reunions(df_i, reunions_lst)

    # Reduïm el nombre de columnes de cada DataFrame prèviament al primer merge:
    df_lst[0] = df_ODs[['Ref. Tema i Reunió', 'Descripció Ordre del dia']]
    df_lst[1] = df_Actes[['Id', 'Ref. Tema i Reunió', 'Data de la reunió', 'Descripció del tema', 'Acords']]
    df_ = pd.merge(df_lst[0], df_lst[1], how='right', left_on=['Ref. Tema i Reunió'], right_on=['Ref. Tema i Reunió'])

    # Executem el merge amb el DataFrame dels temes classificats per barris i
    # eliminem la columna "Id" que ara ja és redundant:
    actes = pd.merge(barris, df_, how='right', left_on=['Id'], right_on=['Id'])
    actes = actes[['Ref. Tema i Reunió', 'Data de la reunió', 'Barri', 'Descripció del tema',
                   "Descripció Ordre del dia", 'Acords']]

    # Definim una màscara per identificar els espais en blanc ('') i substituïm aquests
    # i els valors nuls en la columna "Descripció Ordre del dia" per una frase tipus:

    actes = cleaning_df(actes, buits, col)

    # Convertim la columna "Data de la reunió" a format DateTime de pandas:
    actes['Data de la reunió'] = pd.to_datetime(actes['Data de la reunió'], dayfirst=True)

    # Per l'ús de la funció es pot consultar aquesta excel·lent exposició en
    # StackOverflow: https://stackoverflow.com/a/17141755 com també la doc.
    # oficial:
    actes = actes.sort_values(by=['Data de la reunió', 'Ref. Tema i Reunió'],
                              ascending=[True, True])

    return actes


def output(df, file_name: str, extensio: list, path_dest: list, reunions):
    '''
    :param df: DataFrame input.
    :file_name: Plantilla del nom del fitxer. 

    En aquest cas, aquesta funció no retornarà cap valor,
    doncs només executa una tasca concreta.
    '''    
    # Definim la data d'avui...
    avui = date.today()
    # Per la manipulació del string de la data:
    # https://codefather.tech/blog/python-datetime-days/
    avui = avui.strftime("%Y%m%d")

    # ...i també hi inclourem la referència corresponent de la darrera
    # reunió a partir de la variable global "reunions" fruït de la funció
    # principal desplegament():

    r = [d['ID_reunió'] for d in reunions.values()]
    ref = str(r[-1]).replace('/','-')

    nom_excel = str(avui) + ' ' + file_name + ' ' + ref + extensio[0]
    path_excel = path_dest[0] + "/" + nom_excel

    df.to_excel(path_excel, sheet_name = 'Actes TTM', index = False)
    print(f"S'ha creat el fitxer {nom_excel} \nen la carpeta {path_dest[0]}.")

    # I generem una versió també en format
    nom_pickle = str(avui) + ' ' + file_name + ' ' + ref + extensio[1]
    path_pickle = path_dest[1] + nom_pickle
    df.to_pickle(path_pickle)
    print(f"S'ha creat el fitxer {nom_pickle} \nen la carpeta {path_dest[1]}.")
