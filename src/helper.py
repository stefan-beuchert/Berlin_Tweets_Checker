import json
import pandas as pd

import nltk
from nltk.corpus import stopwords

# nltk.download('stopwords')


#### json data ####
def load_data_from_json(path):
    with open(path, "r", encoding='utf8') as read_file:
        return json.load(read_file)


def save_data_to_json(path, data):
    with open(path, 'w') as outfile:
        outfile.write(data)


#### csv data ####
def load_data_from_csv(path):
    df = pd.read_csv(path, encoding='utf8')
    return df


def save_data_to_csv(data, path):
    data.to_csv(path, encoding='utf-8')


#### districts ####
def translate_district(district_name):
    if district_name == 'Charlottenburg-Wilmersdorf':
        return 'Charlottenburg-Wilm.'
    elif district_name == 'Treptow-Köpenick':
        return 'Treptow - Köpenick'
    elif district_name == 'Marzahn-Hellersdorf':
        return 'Marzahn - Hellersdorf'
    elif district_name == 'Steglitz-Zehlendorf':
        return 'Steglitz - Zehlendorf'
    elif district_name == 'Tempelhof-Schöneberg':
        return 'Tempelhof - Schöneberg'
    else:
        return district_name


#### stopwords ####
def get_stopwords():
    stop_words = stopwords.words('english')
    stop_words.extend(["rt", "berlin",
                       "mitte", "moabit", "hansaviertel", "tiergarten", "wedding", "gesundbrunnen",
                       "friedrichshein-Kreuzberg", "friedrichshain", "kreuzberg",
                       "pankow", "prenzlauer berg", "prenzlau" "prenzlauer", "berg", "weißensee", "blankenburg", "heinersdorf", "karow",
                       "stadtrandsiedlung malchow", "pankow", "blankenfelde", "buch", "französisch buchholz",
                       "niederschönhausen", "rosenthal", "wilhelmsruh",
                       "charlottenburg-wilmersdorf", "charlottenburg", "wilmersdorf", "schmargendorf",
                       "grunewald", "westend", "charlottenburg-nord", "halensee",
                       "spandau", "spandau", "haselhorst", "siemensstadt", "staaken", "gatow", "kladow",
                       "hakenfelde", "falkenhagener feld", "wilhelmstadt",
                       "steglitz-zehlendorf", "steglitz", "lichterfelde", "lankwitz", "zehlendorf", "dahlem",
                       "nikolassee", "wannsee", "schlachtensee",
                       "tempelhof-schöneberg", "schöneberg", "friedenau", "tempelhof", "mariendorf", "marienfelde",
                       "lichtenrade",
                       "neukölln", "neukölln", "britz", "buckow", "rudow", "gropiusstadt",
                       "treptow-Köpenick", "alt-treptow", "plänterwald", "baumschulenweg", "johannisthal",
                       "niederschöneweide", "altglienicke", "adlershof", "bohnsdorf", "oberschöneweide",
                       "köpenick", "friedrichshagen", "rahnsdorf", "grünau", "müggelheim", "schmöckwitz",
                       "marzahn-Hellersdorf", "marzahn", "biesdorf", "kaulsdorf", "mahlsdorf", "hellersdorf",
                       "lichtenberg", "friedrichsfelde", "karlshorst", "lichtenberg", "falkenberg", "malchow",
                       "wartenberg", "neu-hohenschönhausen", "alt-hohenschönhausen", "fennpfuhl", "rummelsburg",
                       "reinickendorf", "reinickendorf", "tegel", "konradshöhe", "heiligensee", "frohnau", "hermsdorf",
                       "waidmannslust", "lübars", "wittenau", "märkisches viertel", "borsigwalde",
                       "german", "germany", "amp", "th", "pm"])

    return set(stop_words)