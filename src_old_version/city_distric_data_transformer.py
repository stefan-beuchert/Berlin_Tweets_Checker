import re
import json

# credits to https://gist.github.com/johnberroa/cd49976220933a2c881e89b69699f2f7
def remove_umlaut(string):
    u = 'ü'.encode()
    U = 'Ü'.encode()
    a = 'ä'.encode()
    A = 'Ä'.encode()
    o = 'ö'.encode()
    O = 'Ö'.encode()
    ss = 'ß'.encode()

    string = string.encode()
    string = string.replace(u, b'ue')
    string = string.replace(U, b'Ue')
    string = string.replace(a, b'ae')
    string = string.replace(A, b'Ae')
    string = string.replace(o, b'oe')
    string = string.replace(O, b'Oe')
    string = string.replace(ss, b'ss')

    string = string.decode('utf-8')
    return string

def transform_district(txt):
    res = []

    names = txt.split(",")  # split line into different district names

    key = names[0]

    for district_name in names:
        # lower case
        district = district_name.lower()
        res.append(district)

        # replace umlaute
        if re.search("[äöüÄÖÜß]", district):
            res.append(remove_umlaut(district))

    return key, res

def get_district_versions(source):
    district_dict = {}
    # get data from berlin_districts.txt file
    with open(source, encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # removing the \n at the end of every line
            if line[0] == '#':  # skip comment lines
                continue

            # transformation
            district_key, district_versions = transform_district(line)
            district_dict[district_key] = district_versions

    return district_dict

if __name__ == '__main__':
    # consts
    source = '../data/berlin_districts.txt'
    target = '../data/berlin_districts_transformed.json'

    # get transformed results
    district_dict = get_district_versions(source)

    # safe to json file
    with open(target, 'w') as outfile:
        json.dump(district_dict, outfile)
