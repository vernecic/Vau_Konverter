import os ## za pristup/čitanje .env varijabla
from flask import Flask, jsonify, request # flask
from flask_cors import CORS # komunikacija između fronta i backa
import boto3 # aws sdk - software development kit
from dotenv import load_dotenv # loadanje varijabla iz .env
import uuid # unique ID-jevi
import requests

load_dotenv() # load .env fajla

app = Flask(__name__) # inicijalizacija flask aplikacije
CORS(app) # omogućuje komunikaciju fronta i back-a

R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')

# https://developers.cloudflare.com/r2/examples/aws/boto3/
s3 = boto3.client(
    's3',
    endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name="auto"
)

@app.route('/upload', methods=["POST"]) 
def get_upload_url():
    try:
        file_id = str(uuid.uuid4()) # random id za fajl, string
        key = f"uploads/{file_id}.mp3" # path 
        
        # metoda na s3 (boto3.client) objektu - https://developers.cloudflare.com/r2/api/s3/presigned-urls/
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': R2_BUCKET_NAME,
                'Key': key,
                'ContentType': 'audio/mpeg'
            },
            ExpiresIn=600
        )
        public_url = f"https://pub-2194dec803964e04ad9375b3af12d498.r2.dev/{key}"
        
        return jsonify({
            "upload_url": presigned_url, # ovdje se sprema mp3 file
            "file_id": file_id,
            "public_url": public_url, 
            "key": key
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/convert', methods=["POST"])
def convert_to_wav():
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        mp3_key = data.get('mp3_key')
        
        worker_url = "http://worker:8000/convert"
        
        worker_response = requests.post(
            worker_url, 
            json={
                "file_id": file_id,
                "mp3_key": mp3_key,
                "bucket": R2_BUCKET_NAME,
                "r2_account_id": R2_ACCOUNT_ID,
                "r2_access_key": R2_ACCESS_KEY_ID,
                "r2_secret_key": R2_SECRET_ACCESS_KEY
            },
            timeout=300
        )
        
        if worker_response.status_code == 200:
            result = worker_response.json()
            app.logger.info("Konverzija uspješna!")
            
            return jsonify({
                "status": "success",
                "wav_url": result.get("wav_url")
            })
        else:
            return jsonify({"error": "Greška u konverziji"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)