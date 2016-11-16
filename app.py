#!flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

def grab_data_as_json():
    bad_count = 0
    with open('csvDir/assetsTableComplete.csv','r') as table:
        table_data = table.readlines()
        keys = table_data[0].replace('"','').replace("'",'').replace("\n",'').split(',')
        data = {"data" : []}
        for line in table_data[1:]:
            line = line.replace('"','').replace("'",'').replace("\n",'').split(',')
            row = {
                "city": line[9],
                "contact": line[4],
                "descript": line[5],
                "id": line[0],
                "lat": float(line[6]),
                "lon": float(line[7]),
                "name": line[1],
                "state": line[10],
                "street": line[8],
                "telnum": line[2],
                "website": line[3],
                "zip": line[11]
            }
            data["data"].append(row)
    table.close()
    return data

def grab_data_as_array():
    with open('csvDir/assetsTableComplete.csv','r') as table:
        table_data = table.readlines()
        data = {"data" : []}
        for line in table_data[1:]:
            line = line.split(',')
            row = []

            for item in line:
                row.append(item.replace('\n','').replace('"',''))
            data["data"].append(row)
    table.close()
    return data

mapMetaData = grab_data_as_json()

@app.route('/assetMapper/api/meta/', methods=['GET'])
def get_map_data():
    return jsonify(mapMetaData)

if __name__ == '__main__':
    app.run(debug=True)
