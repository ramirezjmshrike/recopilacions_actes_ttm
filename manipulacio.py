'''
Aquest fitxer conté les dues subfuncions de
manipulació de dades de la funció principal
manipulacio():

- to_df():              Subfunció generadora del DataFrame.

- gen_ref_reunions():   Subfunció generadora de la
                        nova columna "Ref. Tema i Reunió".
'''

import pandas as pd

def to_df(diccionaris: list):
    '''
    :param diccionaris: Llista de diccionaris amb els diversos camps dels
    emails ja parsejats.

    :return: DataFrame.
    '''

    dfs = [pd.DataFrame(d) for d in diccionaris]
    df = pd.concat(dfs)

    return df


def gen_ref_reunions(df, reunions_lst: list):
    '''
    :param df: DataFrame d'input.
    :param reunions_lst: Llista de diccionaris amb la ID de cada
    reunió i la seva data corresponent:

    :return: DataFrame.
    '''

    # Generem la nova columna "Ref. Tema i Reunió":
    df['Ref. Tema i Reunió'] = df['Id'] + ' ' + df['Data de la reunió']
    # Realitzem la substitució:
    for d in reunions_lst:
        df['Ref. Tema i Reunió'] = df['Ref. Tema i Reunió'].str.replace(d['Data'], d['ID_reunió'], regex=False)

    return (df)
