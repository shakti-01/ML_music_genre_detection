from flask import Flask, jsonify, redirect
from flask import request
import os
from flask_cors import CORS, cross_origin
import numpy as np
import tensorflow as tf
import librosa

app = Flask(__name__)
CORS(app)

#global var
genre={}
genre[0] = 'Blues';genre[1]='Classical';genre[2]='Country';genre[3]='Disco';genre[4]='Hip-hop';genre[5]='Jazz';
genre[6]= 'Metal';genre[7]='PoP';genre[8]='Reggae';genre[9]='Rock'
loaded_model = tf.keras.models.load_model(app.instance_path+'/static/my_music_model_final')
print('model loaded successfully')

def getMFCC(audio_path):
    # Load audio file
    #audio_path = '/content/drive/MyDrive/Music Genre Classification/genres_original/pop/pop.00008.wav'
    y, sr = librosa.load(audio_path, sr=22050, duration=30)

    # Extract MFCC features
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=int(sr*0.010), n_fft=int(sr*0.025))

    # Reshape MFCC features into (130,13) tensor
    if mfcc.shape[1] < 130:
        # Pad with zeros if number of frames is less than 130
        mfcc = np.pad(mfcc, ((0, 0), (0, 130-mfcc.shape[1])), mode='constant')
    elif mfcc.shape[1] > 130:
        # Truncate frames if number of frames is greater than 130
        mfcc = mfcc[:, :130]
    else:
        # Keep the same shape if number of frames is exactly 130
        pass

    # Reshape MFCC features into (1, 130, 13) tensor for input to RNN-LSTM model
    mfcc = mfcc.reshape(1, mfcc.shape[1], mfcc.shape[0])
    return mfcc

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
        
        #x = np.random.uniform(-130.5,130.6,size=(130,13))
        #print(x.shape)
        #prediction=loaded_model.predict(x.reshape(1,130,13))
        print(f"target path = {target}")
        mfcc = getMFCC(target)
        print(mfcc.shape)
        prediction = loaded_model.predict(mfcc)
        predicted_index=np.argmax(prediction, axis=1)
        print(f'prediction={prediction}')
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