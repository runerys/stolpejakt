import os
import argparse
import json

parser = argparse.ArgumentParser(description='Parsing arguments for datasource validation')
parser.add_argument('--geo_file', default=None, help='Name of file with geographical structure')
parser.add_argument('--maps_file', default=None, help='Name of file with maps')
parser.add_argument('--poles_file', default=None, help='Name of file with poles')
parser.add_argument('--output_file', default=None, help='What to make')
parser.add_argument('--fylke_filter', default=None, help='Fylke-id')

args = parser.parse_args()

separator = ","

def run():
    with open(args.geo_file) as f:
        geo = json.load(f)
    with open(args.maps_file) as f:
        maps = json.load(f)
    with open(args.poles_file) as f:
        poles = json.load(f)

    maps_dict = dict()
    for map in maps['results']:
        maps_dict[map['id']] = map

    kommuner_dict = dict()
    for fylke in geo['results']:
        fylke_navn = fylke['name']
        for kommune in fylke['kommuner']:
            kommune['fylke_name'] = fylke_navn
            kommuner_dict[kommune['id']] = kommune

    export_poles(kommuner_dict, maps_dict, poles)

def append(arr, s):
    s = str(s)
    cleaned = s.replace(separator, ' ')
    arr.append(cleaned)

def export_poles(geo, areas, poles):
    output = open(args.output_file, "w")  
    output.write('Fylke,Kommune,Kart,Arrangor,Navn,Poeng,Location,Altitude'+"\n")  
    for pole in poles['results']:
        area = areas[pole['area']]
        kommune = geo[area['kommune']]
        line = []
        append(line, kommune['fylke_name'])
        append(line, kommune['name'])
        append(line, area['name'])
        append(line, area['organizer_name'])
        append(line, pole['name'])
        line.append(str(pole['points']))
        location = pole['location']
        line.append(str(location[1]) + ' ' + str(location[0]))
        line.append(str(pole['altitude']))

        s = separator.join(line)

# Filter Oslo & Viken - max 2000 in Google Maps import
        if area['fylke'] in [3, 30]:
            output.write(s+"\n")


run()