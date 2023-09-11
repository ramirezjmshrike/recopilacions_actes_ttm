'''
Aquest fitxer conté tant la subfunció principal parsing_ttm() que executa
també diverses tasques (cadascuna amb la seva funció):

- parse_dates():    Subfunció que localitza la data de la reunió en
                    l'assumpte de cada diccionari (correu).

- parse_referencies(): Subfunció generar la llista de referències de cada
                    tema en cada diccionari.

- parse_continguts(): Subfunció que genera la llista de continguts de cada
                    tema en cada diccionari. El nombre d'objectes ha de ser
                    exactament el mateix que els presents en la llista
                    produïda per la subfunció parse_referencies().

- split_continguts(): Subfunció que actua sobre l'output de la subfunció
                    parse_continguts() i genera dues llistes amb la descripció
                    de cada tema i el redactat de l'ordre del dia o l'acord de
                    l'acta corresponent. El nombre d'objectes ha de ser
                    exactament el mateix que els presents en la llista
                    produïda per la subfunció parse_referencies().
'''
import re

def parse_dates(subj: str):
    '''
    :param subj: Input del text corresponent a l'assumpte
    de cada email.

    :return: Retorna la data de la reunió.
    '''
    rgx = 'Mobilitat ([0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9])'
    data_reunio = re.search(rgx, subj).group(1)

    return data_reunio


def parse_referencies(body: str):
    '''
    :param body: Input del text corresponent al cos principal
    de cada email.

    :return: Retorna una llista amb les referències de cada punt
    recollit en l?ordre del dia o l'Acta de cada reunió.
    '''
    rgx = r'[0-9][0-9][0-9][0-9]/[0-9][0-9]/TTM|[0-9][0-9][0-9]/[0-9][0-9]/TTM'
    referencies = re.findall(rgx, body)

    return referencies


def parse_continguts(body: str):
    '''
    :param body: Input del text corresponent al cos principal
    de cada email.

    :return: Retorna una llista amb el text corresponent a la descripció
    del tema (una oració) el detall del tema en qüestió.
    '''
    rgx = r'[0-9][0-9][0-9][0-9]/[0-9][0-9]/|[0-9][0-9][0-9]/[0-9][0-9]/'
    particions = re.split(rgx, body)

    # Eliminem l'encapçalament corresponent a cada reunió doncs no conté
    # informació rellevant per la nostra tasca:
    n_particions = len(particions)
    particions_depurades = particions[1:n_particions]

    return particions_depurades


def split_continguts(contingut: list, patro: str):
    '''
    :param body: Input del text corresponent al cos principal
    de cada email.
    :param patro: Patró que delimita el fragment de text corresponent a
    la descripció del tema (una oració) amb el fragment corresponent amb el
    detall del tema en qüestió.

    :return: Retorna dues llistes (a, b):
    - Llista a: Amb el fragment de text corresponent a la descripció del tema
    (una oració)
    - Llista b: Amb el fragment corresponent amb el detall del tema en qüestió.
    '''
    llista = [ele.split(patro, 1) for ele in contingut]

    index = range(0, len(llista))

    a = [llista[i][0] for i in index]
    b = [llista[i][1] for i in index if len(llista[i]) == 2]

    return a, b


def parsing_ttm(msg: dict, col_name: str, patro: str):
    '''
    :param dict: Diccionari que conté l'Assumpte i el cos principal
    de text de cada email.
    :param col_name: Input de la etiqueta de columna corresponent
    a si es tracta de la "Descripció de l'Ordre del dia" o bé "Acords".
    :param patro: Patró que delimita el fragment de text corresponent a
    la descripció del tema (una oració) amb el fragment corresponent amb el
    detall del tema en qüestió.
    :return: Retorna una llista amb el text corresponent a la descripció
    del tema (una oració) el detall del tema en qüestió.
    '''
    msg['Data de la reunió'] = parse_dates(msg['subj'])
    msg['Id'] = parse_referencies(msg['body'])
    msg['Contingut'] = parse_continguts(msg['body'])

    # Atès que es detecta una errada tipogràfica prou freqüent, resulta
    # millor substituir-la de forma automatitzada en aquest moment per
    # un espai en blanc (" ").
    msg['Contingut'] = [ele.replace(" \r\n\r\n", patro + " ") for ele in msg['Contingut']]
    msg['Descripció del tema'], msg[col_name] = split_continguts(msg['Contingut'],
                                                                 patro)
    return msg