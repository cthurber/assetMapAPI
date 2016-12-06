import sqlite3
from flask import Flask, jsonify, request, render_template
from add_form import Add_Asset_Form

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

def retrieve_assets(db_name,table_name):

    conn = sqlite3.connect(str(db_name))
    c = conn.cursor()

    retrieve_statement = "SELECT * FROM "+str(table_name)

    table_data = c.execute(retrieve_statement)

    data = {"data" : []}
    for line in table_data:
        line = str(line).lstrip('(').rstrip(')').replace('"','').replace("'",'').replace("\n",'').split(',')
        try:
            row = {
                "city": line[9].lstrip(' ').rstrip(' '),
                "contact": line[4].lstrip(' ').rstrip(' '),
                "descript": line[5].lstrip(' ').rstrip(' '),
                "id": line[0].lstrip(' ').rstrip(' '),
                "lat": float(line[6]),
                "lon": float(line[7]),
                "name": line[1].lstrip(' ').rstrip(' '),
                "state": line[10].lstrip(' ').rstrip(' '),
                "street": line[8].lstrip(' ').rstrip(' '),
                "telnum": line[2].lstrip(' ').rstrip(' '),
                "website": line[3].lstrip(' ').rstrip(' '),
                "zip": line[11].lstrip(' ').rstrip(' ')
            }
            data["data"].append(row)
        except:
            print("Could not load asset")
    return data

def add_asset(asset_array, db_name, table_name):

    conn = sqlite3.connect(str(db_name))
    c = conn.cursor()

    asset_string = str(asset_array).replace('[','(').replace(']',')')
    insert_statement = "INSERT INTO "+table_name+" VALUES"+asset_string

    c.execute(insert_statement)
    conn.commit()
    conn.close()

    return True

mapMetaData = retrieve_assets('assetMapper.db','assetdata')

@app.route('/assetMapper/api/meta/', methods=['GET'])
def get_map_data():
    return jsonify(mapMetaData)

@app.route('/assets/add/', methods = ['GET', 'POST'])
def add_asset_page():
    form = Add_Asset_Form(request.form)
    if request.method == 'POST':
        form_data = [
                form.city.data,
                form.contact.data,
                form.descript.data,
                form.idcode.data,
                form.lat.data,
                form.lon.data,
                form.name.data,
                form.state.data,
                form.street.data,
                form.telnum.data,
                form.website.data,
                form.zipcode.data
            ]

        add_asset(form_data,'assetMapper.db','assetdata')
        return render_template('index.html', response_data=form_data, form=form)
    else:
        return render_template('add-asset.html', form=form)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
