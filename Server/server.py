import firebase_admin
import joblib
from flask import Flask, request, render_template, session
# import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import pandas as pd
from firebase_admin import firestore, credentials
from uuid import uuid4
from sklearn import *
server = Flask(__name__)
gaitCredentials = credentials.Certificate("gait-76343-firebase-adminsdk-90tdf-dc32870b96.json")
firebase_admin.initialize_app(gaitCredentials)
dbClient = firestore.client()
gaitModel = None
# def loadSequentialModel():
#     gaitModel = tf.keras.models.load_model("gait_model.h5")
#     gaitModel.load_weights("model_weights/gait_model_weights")
parkinsonScaler = StandardScaler()
server.leftModelData = []
server.rightModelData = []
gaitModel = joblib.load("Gait_Model_V2.joblib")

@server.route("/")
def home():
    return render_template("landing.html")
@server.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@server.route("/leftmodel")
def leftModel():
    server.leftModelData = []
    for i in range(4):
        server.leftModelData.append(float(request.args.get("data" + str(i+1))))
        #Checks if its time to call the model function
    print(server.leftModelData)
    print(server.rightModelData)
    if (len(server.rightModelData) > 0):
        model()
        return "Model"
    else:
        return "Recorded"
@server.route("/rightmodel")
def rightModel():
    server.rightModelData = []
    for i in range(4):
       server.rightModelData.append(float(request.args.get("data" + str(i+1))))
    #Checks if its time to call the model function
    print(server.leftModelData)
    print(server.rightModelData)
    if (len(server.leftModelData) > 0):
        model()
        return "Model"
    else:
        return "Recorded"


def model():
    columns = ["VGRFL1", "VGRFL3", "VGRFL4", "VGRFL8",
               "VGRFR1", "VGRFR3", "VGRFR4", "VGRFR8",
               "TotalVGRFL", "TotalVGRFR"]
    dataframeDict = {}

    totalVGRFLData = 0
    for left in server.leftModelData:
        totalVGRFLData += left

    totalVGRFRData = 0
    for right in server.rightModelData:
        totalVGRFRData += right


    data = server.leftModelData + server.rightModelData + [totalVGRFLData, totalVGRFRData]
    # data = [199.1, 87.34, 91.08, 24.09, 21.12, 87.67, 87.23, 64.57, 163.9, 79.86, 112.42, 50.82, 13.75, 102.74, 144.98, 79.53, 662.2, 748]
    for i in range(10):
        dataframeDict[columns[i]] = data[i]

    dataframeData = pd.DataFrame(dataframeDict, index=[0])

    predictedClass = (gaitModel.predict(dataframeData)[0])

    tempDataframDict = dataframeDict
    tempDataframDict["time"] = firestore.SERVER_TIMESTAMP
    tempDataframDict["class"] = int(predictedClass)

    dbClient.collection("data").document(str(uuid4())).set(tempDataframDict)

    server.rightModelData = []
    server.leftModelData = []

    return str(predictedClass)

if __name__ == "__main__":  
    # Krish's Phone - 172.20.10.2
    # EEC172 - 192.168.1.129
    # server.run(debug=True)
    server.run(host="172.20.10.7")
    # server.run(host="0.0.0.0", port=5000)
 
