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

    return data

def add_asset(asset_array, db_name, table_name):

    conn = sqlite3.connect(str(db_name))
    c = conn.cursor()

    asset_string = str(asset_array).replace('[','(').replace(']',')')
    insert_statement = "INSERT INTO "+table_name+" VALUES"+asset_string
    print(insert_statement)

    return True

mapMetaData = retrieve_assets('assetMapper.db','assetdata')

@app.route('/assetMapper/api/meta/', methods=['GET'])
def get_map_data():
    return jsonify(mapMetaData)

@app.route('/', methods = ['GET', 'POST'])
def home():
    form = Add_Asset_Form(request.form)
    if request.method == 'POST':
        print("POST POST POST")
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
        # if form.city.data: form_data.append('city')
        # if form.contact.data: form_data.append('contact')
        # if form.descript.data: form_data.append('descript')
        # if form.idcode.data: form_data.append('idcode')
        # if form.lat.data: form_data.append('lat')
        # if form.lon.data: form_data.append('lon')
        # if form.name.data: form_data.append('name')
        # if form.state.data: form_data.append('state')
        # if form.street.data: form_data.append('street')
        # if form.telnum.data: form_data.append('telnum')
        # if form.website.data: form_data.append('website')
        # if form.zipcode.data: form_data.append('zipcode')

        print(form_data)
        add_asset(form_data,'assetMapper.db','assetdata')
        return render_template('index.html', response_data=form_data, form=form)
    else:
        print("GET GOT GOOD")
        return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
