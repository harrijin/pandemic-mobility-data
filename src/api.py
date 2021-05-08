import json, os, csv
from flask import Flask, request, send_file, jsonify
import redis_helper

app = Flask(__name__)

def add_data(table):
    counter = 0
    for row in table:
        key = row['sub_region_1'] + '_' + row['sub_region_2'] + '_' + row['date']
        redis_helper.add_data_point(key.title(), row)
        counter = counter + 1
    return jsonify({"response": "{} rows added".format(counter)})

@app.route('/', methods=['GET'])
def home():
    return ";)"

@app.route('/db_size')
def check_db_size():
    return {"response" : "{} datapoints in database".format(redis_helper.db_size())}

@app.route('/load_data', methods=['GET'])
def load_data():
    columns_to_keep = ['sub_region_1', 'sub_region_2', 'date', 'retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline', 'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline']

    table = list()
    for file in os.listdir('data'):
        with open('data/' + file, encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # sub_region_1 is state, sub_region_2 is county
                filtered_row = dict()
                for column in columns_to_keep:
                    filtered_row[column] = row[column]
                table.append(filtered_row)
    return add_data(table)

# CRUD Operations*******************

@app.route('/create', methods=['POST'])
def create():
    try:
        table = request.get_json(force=True)
        return add_data(table)
    except Exception as e:
        return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)}), 403

@app.route('/read/<date>/<state>', methods=['GET'])
def read(date, state):
    key = ""
    state = state.title()
    if state == "Usa":
        key = f'__{date}'
    else:
        arguments = request.args
        if "county" in arguments:
            county = arguments["county"].title()
            key = f'{state}_{county}_{date}'
        else:
            key = f'{state}__{date}'
    return jsonify(redis_helper.get_data_point(key))

@app.route('/update', methods=['POST'])
def update():
    try:
        table = request.get_json(force=True)
        counter = 0
        for row in table:
            key = row['sub_region_1'] + '_' + row['sub_region_2'] + '_' + row['date']
            redis_helper.update_data_point(key.title(), row)
            counter = counter + 1
        return jsonify({"response":"{} rows updated".format(counter)})
    except Exception as e:
        return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)}), 403

@app.route('/delete/<date>/<state>', methods=['GET'])
def delete(date, state):
    key = ""
    state = state.title()
    if state == "Usa":
        key = f'__{date}'
    else:
        arguments = request.args
        if "county" in arguments:
            county = arguments["county"].title()
            key = f'{state}_{county}_{date}'
        else:
            key = f'{state}__{date}'
    redis_helper.delete_data_point(key)
    return jsonify({"response":"{} deleted".format(key)})

# Job operations **********************

@app.route('/new_job', methods=['POST'])
def new_job():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return jsonify(redis_helper.add_job(job['sub_region_1'], job['sub_region_2'], job['start_date'], job['end_date'], job['interested_categories']))

@app.route('/job/<jid>', methods=['GET'])
def jobs_api(jid):
    job = redis_helper.get_job(jid)
    if len(job) == 0:
        return jsonify({"response":"Job ID not found"})
    output = {
        "id":jid,
        "status":job[b'status'].decode('utf-8'),
    }
    return jsonify(output)
    
@app.route('/download/<jid>', methods=['GET'])
def download(jid):
    path = f'./{jid}.png'
    with open(path, 'wb') as f:
        f.write(redis_helper.get_image(jid))
    return send_file(path, mimetype='image/png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')