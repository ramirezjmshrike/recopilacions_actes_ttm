'''
Aquest fitxer conté dues subfuncions de la funció principal
cleaning_dict i una subfunció de la funció principal manipulacio():

- replace_continguts(): Subfunció que fa ús de la funció replace
                        suprimir literals residuals del canvi de
                        a text pla amb el que treballa python.

- sub_continguts():     Subfunció que fa ús de la funció sub de
                        la llibreria re per suprimir encapçalaments
                        i altres cadenes de caràcters del contingut
                        original que ja no són d'utilitat en aquest
                        format.

- replace_typos():      Subfunció que fa ús de la funció replace per
                        substituir errades ortotipogràfiques per la
                        paraula o expressió morfològica correcta.

- sub_typos():          Subfunció que fa ús de la funció sub per
                        substituir errades ortotipogràfiques per la
                        paraula o expressió morfològica correcta.

- separar_paraules():   Subfunció que realitza la separació de paraules
                        potencials partint del patró minúsculaMajúscula.

- cleaning_df():        Subfunció que substitueix valors nuls (NaN)
                        i buïts ('') per una frase tipus.
'''
import pandas as pd
import re

def replace_continguts(dicc: dict, cols_names: list, literals: list):
    '''
    :param dicc: Diccionari amb els diversos camps dels emails ja parsejats.
    :param cols_names: Llista amb les etiquetes de columna de les variables
    on s'ha d'han executar les tasques de neteja del text.
    :param literals: Llista de patrons literals a eliminar.

    :return: Diccionari amb els patrons ja suprimits.
    '''

    for col in cols_names:

        for p_literal in literals:
            dicc[col] = [s.replace(p_literal, '') for s in dicc[col]]

    return dicc


def sub_continguts(dicc: dict, cols_names: list, regex: list):
    '''
    :param dicc: Diccionari amb els diversos camps dels emails ja parsejats.
    :param cols_names: Llista amb les etiquetes de columna de les variables
    on s'ha d'han executar les tasques de neteja del text.
    :param regex: Llista de patrons regex a eliminar.

    :return: Diccionari amb els patrons ja suprimits.
    '''
    for col in cols_names:

        for p_regex in regex:
            dicc[col] = [re.sub(p_regex, '', s) for s in dicc[col]]

    return dicc


def separar_paraules(dicc: dict, cols_names: list):
    '''
    :param dicc: Diccionari amb els diversos camps dels emails ja parsejats.
    :param cols_names: Llista amb les etiquetes de columna de les variables
    on s'ha d'han executar les tasques de neteja del text.

    :return: Diccionari amb les potencials paraules (minúsculaMajúscula).
    '''

    for col in cols_names:
        # Comprehension list que executa la separació de paraules segons el
        # patró (minúsculaMajúscula). Font (optem pel mètode #2):
        # https://www.geekforgeeks.org/python-add-space-between-potential-words/
        # i per l'ús de lookarounds i avaluacions per gestionar excepcions
        # consultem aquesta solució proposada en StackOverflow:
        # https://stackoverflow.com/a/25674758
        dicc[col] = [re.sub(r"(?<=[a-z])(?=[A-Z])", r" ", s) for s in dicc[col]]
        # Generem dos grups separats per un espai en blanc pels casos d'una minúscula
        # que s'ubiqui a continuació d'una paraula en majúscules i acabi en majúscula,
        # com pot ser una siga o un acrònim (patró "MAJÚSCULESminúscules"):
        dicc[col] = [re.sub(r"([A-Z]+[A-Z$])([a-z])", r"\1 \2", s) for s in dicc[col]]
        # Per afegir un espai en blanc entre un punt de puntuació i una paraula:
        # https://stackoverflow.com/a/44263500
        dicc[col] = [re.sub(r"(?<=[.,:;?!])(?=[^\s])", r" ", s) for s in dicc[col]]

    return dicc


def cleaning_df(df, buits:str, col: str):
    '''
    :param df: DataFrame d'input.
    :param buits: Frase tipus per substituir valors nuls i buits ('').
    :param col: Etiqueta de columna.

    :return: DataFrame d'output.
    '''

    mask_buit = df[col] == ''
    df[col][mask_buit] = buits
    df[col] = df[col].fillna(buits)

    return df

def replace_typos(dicc: dict, cols_names: list, literals: dict):
    '''
    :param dicc: Diccionari amb els diversos camps dels emails ja parsejats.
    :param cols_names: Llista amb les etiquetes de columna de les variables
    on s'ha d'han executar les tasques de neteja del text.
    :param literals: Diccionari amb els patrons literals a substituir (key)
                i el respectiu string que l'ha de substiuir (values).
    
    :return: Diccionari amb els patrons ja suprimits.
    '''
    
    for col in cols_names:
        
        for p_literal, string in literals.items():
            dicc[col] = [s.replace(p_literal, string) for s in dicc[col]]

    return dicc


def sub_typos(dicc: dict, cols_names: list, regex: dict):
    '''
    :param dicc: Diccionari amb els diversos camps dels emails ja parsejats.
    :param cols_names: Llista amb les etiquetes de columna de les variables
    on s'ha d'han executar les tasques de neteja del text.
    :param literals: Diccionari amb els patrons literals a substituir (key)
                i el respectiu string que l'ha de substiuir (values).
    
    :return: Diccionari amb els patrons ja suprimits.
    '''    
    for col in cols_names:
    
        for p_regex, string in regex.items():
            dicc[col] = [re.sub(p_regex, string, s) for s in dicc[col]]

    return dicc
