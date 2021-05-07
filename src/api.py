import json, os
from flask import Flask, request, send_file, jsonify
import redis_helper

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return ";)"

# CRUD Operations*******************

@app.route('/create', methods=['POST'])
def create():
    try:
        table = request.get_json(force=True)
        counter = 0
        for row in table:
            key = row['sub_region_1'] + '_' + row['sub_region_2'] + '_' + row['date']
            redis_helper.add_data_point(key.title(), row)
            counter = counter + 1
        return "{} rows added".format(counter)
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
        return "{} rows updated".format(counter)
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
    return "{} deleted".format(key)

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
        return "Job ID not found"
    output = {
        "id":jid,
        "status":job[b'status'].decode('utf-8'),
    }
    return output
    
@app.route('/download/<jid>', methods=['GET'])
def download(jid):
    path = f'./{jid}.png'
    with open(path, 'wb') as f:
        f.write(redis_helper.get_image(jid))
    return send_file(path, mimetype='image/png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')