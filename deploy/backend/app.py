from flask import Flask, jsonify, redirect
from flask import request
import os
from flask_cors import CORS, cross_origin
import pickle

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
        loaded_model = pickle.load(open('./static/beew.pkl', 'rb'))
        loaded_model.predict("")
        #os.remove(target)
        data['success'] = True
    except Exception as e:
        print(f"{e}")
        data['success']=False
    return jsonify(data)
    

if __name__=='__main__':
    app.run(debug=True)