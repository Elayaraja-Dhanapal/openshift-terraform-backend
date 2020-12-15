import os
from flask import Flask,request,jsonify,json
from flask_cors import CORS,cross_origin
import json
from pathlib import Path
import configparser, os
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

path_current_directory = os.path.dirname(__file__)

app = Flask(__name__)
UPLOAD_FOLDER = '/var/terraform'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/api/upload', methods=['POST'])
def file_upload():
    logging.info('start')
    try:    
        uploaded_file = request.files['file']
        logging.info('Uploadedfile: %s', uploaded_file)
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))

        with open(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename), 'r') as f:
            config_string = '[dummy_section]\n' + f.read()        
        config = configparser.ConfigParser()
        config.read_string(config_string)
        cluster_id = dict(config.items('dummy_section'))['cluster_id_prefix']
        f.close()
        cluster_id_path = os.path.join(app.config['UPLOAD_FOLDER'], cluster_id.replace('"', ''))
        logging.info('Cluster path: %s', cluster_id_path)
        os.makedirs(cluster_id_path, exist_ok=True)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename), 'r') as fr:
            with open(os.path.join(cluster_id_path, uploaded_file.filename), "w") as w:
                for line in fr:
                    w.write(line)
        fr.close()
        w.close()
    except OSError as error:
        logging.error(error)
    except Exception as e:
        logging.error(e)
    logging.info('done')
    return 'File upload success', 200


@app.route("/hello")
def hello():
    logging.info('Hello beauty!')
    return "hello beautiful world redhat hackathon!!"


if __name__ == "__main__":
    app.run()