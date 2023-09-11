'''
Aquest fitxer és l'únic que cal invocar per executar el programa
per la compilació de dades de les reunions de la Taula Tècnica de
Mobilitat. El notebook de jupyter està concebut per elaborar informes
i fer proves.

En una futura versió es preveu implementar un paral·lelisme. V. més
detalls en el fitxer README.
'''
from functools import partial
from src.utils import desplegament, parsing, cleaning, \
    manipulacio, output

# Variables globals:
# - Llista amb les dades pels paths o similars on s'ubicaran els fitxers
# de dades:
carpetes = ['data', 'data_processat', 'reports']

strings = ['Ordre del dia', 'Acta']
cols_names = ["Descripció Ordre del dia", "Acords"]
patrons_literals = ['\n', '\r', '\t', 'PROTOCOLS DE GUÀRDIA URBANA',
                    "SUPERILLA D'HORTA", "CAMPANYA DE MOTOS EN VORERA",
                    "CAMPANYES DE MOTOS EN VORERA", "PUNTS INFORMATIUS",
                    'Descripció:', "Acords:",
                    ]
patrons_regex = ["^TTM ", "^TTM:", "^- ", "^  ", "^ ", '  $', ' $', "^[0-9][0-9]/2[0-9]",
                 r'MOBILITAT[^>]+PUJOLET\)']
# patrons_regex = ["^TTM ", "^TTM: ", "^- ", "^[0-9][0-9]/2[0-9]"]
pttrns_typos_literals = {'economica': 'econòmica', 'TTM': 'Taula tècnica',
                         "taula tècnica": "Taula tècnica", "taula Tècnica": "Taula tècnica",
                         "Taula Tècnica": "Taula tècnica",
                "Guardia urbana": "Guàrdia Urbana", "Guardia Urbana": "Guàrdia Urbana",
                "GUB": "Guàrdia Urbana", "àrea verda": "Àrea Verda",
                "Àrea verda": "Àrea Verda", "àrea Verda": "Àrea Verda",
                "la escola": "l'escola", "Gran vista": "Gran Vista", 
                "brigaa": "Brigada", "brigada": "Brigada", "Psg.": "Pg.",
                "gerència": "Gerència",  "acordos": "acords", "vehícle": "vehicle",
                "respotà": "resposta", "enviaà": "enviarà",
                "St. Alejandro": "Sant Alexandre",
                "Olimpic": "Olímpic", "arenys": "Arenys", "Roquetas": "Roquetes",
                "Carmen C.": "Carmen Castaño",
                "Cristina G.": "Cristina Gil", "Raúl O.": "Raúl Ortega", 
                "Montse V.": "Montse Vico", "Jaume S.": "Jaume Sauch",
                "SSTT Dte.": "Serveis tècnics del Districte", "SSTT": "Serveis Tècnics"}
pttrns_typos_regex = {r"(\bdistricte\b)": r"Districte", r"(\bmols\b)": r"molts",
                      r"(\bambar\b)": r"àmbar", r"(\bC\b/)": r"c.",
                      r"(\bMF\b)": r"Manuel Franco", r"(\bde Gràcies\b)": r"de Gràcia",
                      r"\btaule\b": r"Taula", r"\bcarrertera\b": r"carretera"
                      }

# De moment, no està activa aquesta variable:
pttrns_null = ["tancar el tema", "tancat el tema", "Tancar tema", "tancar ambdós temes",
               "es dóna per tancat", "es dona per tancat", "donar per tancat",
               "ja estava executat", "tema que ha treballat",
               "Mateix que en el tema", "Pendent de visita", "Per valorar en la propera",
               "Protocol fet i ", "Protocol fet pendent", "Pendent d'execució",
               "pendent d'execució", "pendent de rebre", "Pendent de pressupost"
               "Pendent de modificar", "està treballant en la", "Pendent de fer el Protocol",
               "treballant en el Protocol", "protocol està fet", "ja s'ha executat",
               "ja està executat", "encarregarà el Protocol",
               "La Taula aprova el", "S'aprova per la Taula", "tramitar i executar el Protocol",
               "s'aprova el Protocol", "s'aprova la proposta de nou Protocol",
               "quan hi hagin novetats", "Pendent de conèixer", "Resta pendent", "resta pendent"
               "es gestionarà per correu electrònic",
               "Sense novetats", "No hi ha novetat",
               "Es tractarà el tema a la propera",
               "No va donar temps", "Aquesta tema no estava inclòs", "No dóna temps per",
               "No va haver prou temps", "No dóna prou temps",
               "Es valora com tema tractat",
               "La Taula es dóna per informada"]
patrons = [patrons_literals, patrons_regex, pttrns_typos_literals, pttrns_typos_regex,
           pttrns_null]

str_buits = "Aquest tema no estava inclòs en l'Ordre del dia o no comptava amb cap descripció"
file_name = "Recopilació de les actes de la TTM fins la reunió"
extensio = [".xlsx", ".pkl"]



list_dicc, reunions, barris, path_proc = desplegament(carpetes[0:2])

# El primer objecte prové de la llista de noms de carpetes del Bloc #º mentre
# que el segon objecte és el un valor que retorna de la funció desplegament():
carpetes_dest = [carpetes[2], path_proc]

ODs, Actes = parsing(list_dicc, strings[0], strings[1])

print(f"S'han compilat les dades de {len(ODs)} ordres del dia de reunions.")
print(f"S'han compilat les dades de {len(Actes)} actes de reunions.")

ODs = [cleaning(d, cols_names[0], patrons) for d in ODs]
Actes = [cleaning(d, cols_names[1], patrons) for d in Actes]

manipulacio_ = partial(output, barris=barris, reunions=reunions)
actes_ = manipulacio(ODs, Actes, str_buits, cols_names[0], reunions, barris)

# Fem ús de la funció partial a fi d'alleugerir un xic la entrada
# d'arguments a la funció output() segons es recomana en aquest
# article en LeveUpCoding (18/07/2023):
# https://levelup.gitconnected.com/the-ultimate-guide-to-writing-functions-in-python-12-best-practices-122a797883a6

output_p = partial(output, path_dest=carpetes_dest, reunions=reunions)
output_p(actes_, file_name, extensio)


