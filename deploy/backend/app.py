from flask import Flask, jsonify, redirect
from flask import request
import os
from flask_cors import CORS, cross_origin
import numpy as np
import tensorflow as tf

app = Flask(__name__)
CORS(app)

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
        genre={}
        genre[0] = 'Blues';genre[1]='Classical';genre[2]='Jazz';genre[3]='Country';genre[4]='Pop';genre[5]='Disco';
        genre[6]= 'Reggae';genre[7]='Hiphop';genre[8]='Disco';genre[9]='Rock'
        
        # Load the model from the file
        loaded_model = tf.keras.models.load_model(app.instance_path+'/static/my_music_model')
        print('model loaded successfully')
        x = np.random.uniform(-130.5,130.6,size=(130,13))
        #print(x.shape)
        prediction=loaded_model.predict(x.reshape(1,130,13))
        predicted_index=np.argmax(prediction, axis=1)
        #print(f'predicted index={predicted_index}')
        pgenre = genre[predicted_index[0]]
        print(pgenre)
        #os.remove(target)
        data['success'] = True
        data['genre'] = pgenre
    except Exception as e:
        print(f"{e}")
        data['success']=False
    return jsonify(data)
    

if __name__=='__main__':
    app.run(debug=True)