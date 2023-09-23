Aquest paquet està conformat per set arxius:

- `src/utils`: En la carpeta src. Conté les funcionalitats
principals que agrupen subfuncions amb tasques concretes.
- src/desplegament.py`: En la carpeta stc. Conté les funcionalitats
que executen tasques.
- `src/parsing.py`: En la carpeta src. Conté les funcionalitats que
executen tasques per parsejar la informació en brut continguda en els
fitxers MSG i la organitza en noves variables.
- `src/cleaning.py`: En la carpeta src. Conté les funcionalitats que
executen tasques de neteja de dades.
- `src/manipulacio.py`: En la carpeta src. Conté les funcionalitats que
executen tasques relacionades amb la manipulació de dades principalment
amb la llibreria pandas.
- `src/output.py`: En la carpeta src. Executa tasques relacionades amb la
generació de fitxers del conjunt de dades en el DataFrame en formats útils
per als usuaris o bé per realitzar processament posteriors.
- `main`: És el fitxer principal i l'únic que cal executar.

### Instal·lació:

Podeu instal·lar el programa fent la crida des de la carpeta arrel

```
python3 ruta/subcarpetes/Parser_Actes_TTM_install.py
```

També es duu a terme el desplegament del sistema de carpetes:
	- data
	- reports

En el cas que es volgués només descomprimir el fitxer Parsing_Emails_v_2_X_XX.zip
serà necessari crear manualment les carpetes:
	- data/
	- data/data_processat
	- reports/

### Com executar aquest programa

Podeu crear un entorn virtual mitjançant la instrucció:

```
virtualenv env
```

I podeu procedir a instal·lar els mòduls corresponents així:
```
pip install -r requirements.txt
```

La cadena de funcions completa s'executarà amb aquesta invocació des de
la carpeta en s'hagi instal·lat el paquet:
```
python3 main.py
```

En el cas de disposar de dos o més CPU disponibles en el vostre equip, el
programa executarà automàticament un paral·lelisme amb les CPU disponibles.
En el cas que el vostre equip només disposi d'una CPU el programa s'executarà 
igualment però el temps d'execució augmentarà sensiblement, entre el 15% i el 25%.


Com es pot constatar, s'obté una reducció considerable del temps d'execució, 
d'aproximadament del 25% al disposar de dos CPU. Aquesta diferència pot reduir-se
fins ser nul·la en funció dels processos que s'estiguin executant en aquell moment
en el vostre equip i els accessos que s'hi estiguin fent al vostre disc dur. La nostra 
prova l'hem realitzar en un IDE virtual amb SO Ubuntu 20.04 en PythonAnyWhere (Amazon 
Web services) amb quatre CPU i disposant de recursos segons la demanda i disponibilitat
d'aquests per PAW per realitzar el joc de proves.

També cal tenir present que durant la execució d'aquest programa es genera un arxiu .pkl
amb una imatge del dataframe final que s'exporta en format XLSX. Aquest fitxer PKL es pot
trobar en:
	- data/data_processat

En el cas que es volgués desviar la sortida per pantalla cap a un arxiu de text pla
en la carpeta reports, juntament amb tota la representació gràfica, llavors cal fer
la invocació amb aquestes comandes en l'ordre indicat:
```
python3 main.py > reports/report.txt
```
El codi del programa ja preveu la possibilitat que, prèviament a la seva execució,
ja existís aquesta carpeta. També cal tenir present que pot fer augmentar una mica
el temps d'execució del programa.

### Testing
Tot i que el programa sí sha testejat durant el procès de disseny, encara representació
pendent d'escriure el codi que realitzi aquestes tasques juntament amb el mòdul unittest.

