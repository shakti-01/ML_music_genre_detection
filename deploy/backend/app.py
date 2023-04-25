from flask import Flask, jsonify
from flask import request
import os
from flask_cors import CORS, cross_origin
import numpy as np
import tensorflow as tf
import librosa
import math

app = Flask(__name__)
CORS(app)

#global var
genre={}
genre[0] = 'Blues';genre[1]='Classical';genre[2]='Country';genre[3]='Disco';genre[4]='Hip-hop';genre[5]='Jazz';
genre[6]= 'Metal';genre[7]='Pop';genre[8]='Reggae';genre[9]='Rock'
loaded_model = tf.keras.models.load_model(app.instance_path+'/static/my_music_model_final')
print('model loaded successfully')

def getMFCC(audio_path):
    y, sr_y=librosa.load(audio_path)

    SAMPLE_RATE=22050
    DURATION=30
    SAMPLES_PER_TRACK=SAMPLE_RATE*DURATION
    n_fft=2048 #int(SAMPLE_RATE*0.025)
    hop_length=512 #int(SAMPLE_RATE*0.010)
    num_segments=10
    num_samples_per_segment=int(SAMPLES_PER_TRACK/num_segments)
    expected_num_mfcc_vectors_per_segment =math.ceil(num_samples_per_segment/hop_length)

    data={'mfcc':[]}
    for s in range(num_segments):
        start_sample = num_samples_per_segment * s
        finish_sample= start_sample + num_samples_per_segment
        mfcc = librosa.feature.mfcc(y=y[start_sample:finish_sample], 
                                    sr=SAMPLE_RATE, 
                                    n_fft=n_fft,
                                    hop_length=hop_length,
                                    n_mfcc=13
                                    )
        mfcc=mfcc.T
        if len(mfcc) == expected_num_mfcc_vectors_per_segment:
            data['mfcc'].append(mfcc.tolist())


    return np.array(data['mfcc'][0]).reshape(1,130,13)

@app.route('/')
def home():
    return "<p>Hello, World!</p>"


@app.route("/upload",methods=["POST"])
@cross_origin()
def upload():
    data={}
    try:
        target = os.path.join(app.instance_path, 'temp/')
        file = request.files['audio-file'] 
        filename = file.filename
        file.save(""+target+filename) #saving file in temp folder
        print("upload Completed")
        target=os.path.join(app.instance_path,'temp/'+filename)
        #model stuff
        
        
        # Load the model from the file
        
        
        print(f"target path = {target}")
        mfcc = getMFCC(target)
        print(mfcc.shape)
        prediction = loaded_model.predict(mfcc)
        
        predicted_index=np.argmax(prediction, axis=1)
        print(f'prediction={prediction}')

        data['confidence']=prediction[0][predicted_index[0]]*100.0
        print('predicted with: {:.4f}'.format(data['confidence']))
        pgenre = genre[predicted_index[0]]
        print(pgenre)
        os.remove(target)
        data['success'] = True
        data['genre'] = pgenre
    except Exception as e:
        print(f"{e}")
        data['success']=False
    return jsonify(data)
    

if __name__=='__main__':
    app.run(debug=True)
