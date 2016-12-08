import sqlite3
from flask import Flask, jsonify, request, render_template
from form_opps import Add_Asset_Form, Delete_Asset_Form

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

    id_getter = 'SELECT COUNT(*) FROM '+table_name
    c.execute(id_getter)
    id_num = int(c.fetchone()[0]) + 1

    asset_string = "('" + str(id_num) + "', "
    asset_string += str(asset_array).replace('[','').replace(']',')')
    insert_statement = "INSERT INTO "+table_name+" VALUES"+asset_string

    print(insert_statement)

    c.execute(insert_statement)
    conn.commit()
    conn.close()

    return True

def update_asset(asset_array, db_name, table_name):

    conn = sqlite3.connect(str(db_name))
    c = conn.cursor()

    id_num = str(asset_array[0])
    asset_string = ""
    for line in asset_array[1:]:
        statement = '"'+ str(form.line.label) + '" text = "' + form.line.data + '",'

    update_statement = "UPDATE "+table_name+" SET "+asset_string+' WHERE "id text" = '+id_num

    print(update_statement)

    # c.execute(update_statement)
    conn.commit()
    conn.close()

    return True

def delete_asset(asset_id, db_name, table_name):

    conn = sqlite3.connect(str(db_name))
    c = conn.cursor()

    delete_statement = 'DELETE FROM '+table_name+' WHERE "id text" = "'+str(asset_id)+'"'
    print(delete_statement)
    c.execute(delete_statement)
    conn.commit()
    conn.close()

    return True

@app.route('/assetMapper/api/meta/', methods=['GET'])
def get_map_data():
    return jsonify(retrieve_assets('assetMapper.db','assetdata'))

@app.route('/assets/add/', methods = ['GET', 'POST'])
def add_asset_page():
    form = Add_Asset_Form(request.form)
    if request.method == 'POST':
        form_data = [
                form.name.data,
                form.telnum.data,
                form.website.data,
                form.contact.data,
                form.descript.data,
                form.lat.data,
                form.lon.data,
                form.street.data,
                form.city.data,
                form.state.data,
                form.zipcode.data
            ]

        add_asset(form_data,'assetMapper.db','assetdata')
        return render_template('add-asset.html', response_data=form_data, form=form)
    else:
        return render_template('add-asset.html', form=form)

@app.route('/assets/all', methods = ['GET', 'POST'])
def asset_page():
    form = Add_Asset_Form(request.form)
    return render_template('list-assets.html', data=retrieve_assets('assetMapper.db','assetdata'), form=form)

@app.route('/assets/update/', methods = ['GET', 'POST'])
def update_asset_page():
    form = Add_Asset_Form(request.form)
    if request.method == 'POST':
        update_asset(form,'assetMapper.db','assetdata')

        """
        label_content_pair = {
            form.idcode.label : form.idcode.data,
            form.name.label : form.name.data,
            form.telnum.label : form.telnum.data,
            form.website.label : form.website.data,
            form.contact.label : form.contact.data,
            form.descript.label : form.descript.data,
            form.lat.label : form.lat.data,
            form.lon.label : form.lon.data,
            form.street.label : form.street.data,
            form.city.label : form.city.data,
            form.state.label : form.state.data,
            form.zipcode.label : form.zipcode.data
        }
        """
        
        return render_template('list-assets.html', response_data=form_data, form=form)
    else:
        return render_template('list-assets.html', form=form)

@app.route('/assets/delete/', methods = ['GET', 'POST'])
def delete_asset_page():
    form = Delete_Asset_Form(request.form)
    if request.method == 'POST':
        delete_asset(form.idcode.data,'assetMapper.db','assetdata')
        return render_template('list-assets.html', data=retrieve_assets('assetMapper.db','assetdata'), form=form)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
