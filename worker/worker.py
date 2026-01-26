from flask import Flask, request, jsonify
import boto3
import os
from pydub import AudioSegment # za konverziju
import tempfile


app = Flask(__name__)

# Endpoint
@app.route('/convert', methods=["POST"])
def convert_to_wav():
    print("===== NOVI ZAHTJEV ZA KONVERZIJU =====")
    
    try:
        # podaci iz requesta, dolaze iz fronta
        data = request.get_json() 
        file_id = data.get('file_id')
        mp3_key = data.get('mp3_key')
        bucket = data.get('bucket')
        r2_account_id = data.get('r2_account_id')
        r2_access_key = data.get('r2_access_key')
        r2_secret_key = data.get('r2_secret_key')
            
        # spanjanje na bucket
        s3 = boto3.client(
            's3',
            endpoint_url=f'https://{r2_account_id}.r2.cloudflarestorage.com',
            aws_access_key_id=r2_access_key,
            aws_secret_access_key=r2_secret_key,
            region_name="auto"
        )
        
        mp3_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        s3.download_fileobj(bucket, mp3_key, mp3_file) # iz kontejnera bucket iz mp3_key u mp3_file
        mp3_file.close()  # zatvaranje fajla da ga pydub moze koristit
        mp3_path = mp3_file.name

        #konverzija
        converted = AudioSegment.from_mp3(mp3_path)
        wav_path = tempfile.mktemp(suffix='.wav')
        converted.export(wav_path, format='wav')
        print("Konverzija gotova!")
        
        # upload natrag na bucket
        wav_key = f"converted/{file_id}.wav"  # /converted folder
        print(f"\n[3/4] Uploadam WAV na R2: {wav_key}")
        
        wav_file = open(wav_path, 'rb')
        s3.upload_fileobj(
            wav_file,
            bucket,
            wav_key,
            ExtraArgs={'ContentType': 'audio/wav'}  # content type
        )
        wav_file.close()
        print("WAV uploadan!")
        
        wav_url = f"https://pub-2194dec803964e04ad9375b3af12d498.r2.dev/{wav_key}"
        
        print("\nCistim temporary fajlove...")
        os.remove(mp3_path)
        os.remove(wav_path)
        print("Temporary fajlovi obrisani!")
        
        print("\n===== KONVERZIJA USPJESNA! =====\n")
        
        # rezultati na backend
        return jsonify({
            "status": "success",
            "wav_url": wav_url,
            "wav_key": wav_key
        })
        
    except Exception as e:
        
        print(f"{str(e)}\n")
        return jsonify({"error": str(e)}), 500


# Pokreni Flask server
if __name__ == "__main__":
    print("Worker pokrenut! Slusam na portu 8000...")
    app.run(host='0.0.0.0', port=8000, debug=True)