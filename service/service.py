from flask import Flask, jsonify, send_file
app = Flask(__name__)

import configparser
config = configparser.ConfigParser()
config.read('etc/conf.ini')

@app.route("/")
def root():
    return "Hello World!"

@app.route("/api/check_update/<os>/<current>")
def check_update(os, current):
    latest_version = config['update']['client_version']
    if current < latest_version:
        return jsonify({'is_latest':False,
                        'url': '{}download/client/{}/{}'.format(config['host']['url'], os, latest_version)})
    else:
        return jsonify({'is_latest':True})

@app.route("/download/client/<os>/<path>")
def client_download(os, path):
    if path is None:
        return 'invalid argument', 400
    try:
        return send_file('files/{}/ora-{}.zip'.format(os, path), as_attachment=True)
    except Exception as err:
        return 'file not found', 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')
