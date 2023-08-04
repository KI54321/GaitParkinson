import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import Dense
from sklearn.ensemble import RandomForestClassifier
import os

# 0 for control & 1 for parkinsons
control_files = os.listdir("control")
parkinsons_files = os.listdir("parkinsons")

controlData = pd.DataFrame()
parkinsonData = pd.DataFrame()

# Reads csv and assigns the class 0
for one_file in control_files:
  if (one_file[0] != '.'):
    tempControlData = pd.read_csv("control/" + one_file, delimiter="\t")
    tempControlData.columns = ["Time", "VGRFL1", "VGRFL2", "VGRFL3", "VGRFL4", "VGRFL5", "VGRFL6", "VGRFL7", "VGRFL8",
                               "VGRFR1", "VGRFR2", "VGRFR3", "VGRFR4", "VGRFR5", "VGRFR6", "VGRFR7", "VGRFR8",
                               "TotalVGRFL", "TotalVGRFR"]
    tempControlData = tempControlData.assign(Class=0)
    controlData = pd.concat([controlData, tempControlData])

# Reads csv and assigns the class 1
for one_file in parkinsons_files:
  if (one_file[0] != '.'):
    tempParkinsonData = pd.read_csv("parkinsons/" + one_file, delimiter="\t")
    tempParkinsonData.columns = ["Time", "VGRFL1", "VGRFL2", "VGRFL3", "VGRFL4", "VGRFL5", "VGRFL6", "VGRFL7", "VGRFL8",
                                 "VGRFR1", "VGRFR2", "VGRFR3", "VGRFR4", "VGRFR5", "VGRFR6", "VGRFR7", "VGRFR8",
                                 "TotalVGRFL", "TotalVGRFR"]
    tempParkinsonData = tempParkinsonData.assign(Class=1)
    parkinsonData = pd.concat([parkinsonData, tempParkinsonData])

totalData = pd.concat([controlData, parkinsonData])


totalDroppedLeft = (totalData[["VGRFL7", "VGRFL6", "VGRFL5", "VGRFL2"]].sum(axis=1))
totalDroppedRight = (totalData[["VGRFR7", "VGRFR6", "VGRFR5", "VGRFR2"]].sum(axis=1))


# print(totalDroppedLeft)
# print()
# print(totalDroppedRight)
# print("______________")
# print(totalData["TotalVGRFL"])
# print()
# print(totalData["TotalVGRFR"])


totalData["TotalVGRFL"] -= totalDroppedLeft
totalData["TotalVGRFR"] -= totalDroppedRight
# print("______________")
# print(totalData["TotalVGRFL"])
# print()
# print(totalData["TotalVGRFR"])

totalData = totalData.drop(columns=["Time", "VGRFL8", "VGRFL7", "VGRFL6", "VGRFL5", "VGRFL4", "VGRFL3", "VGRFL2", "VGRFL1", "VGRFR8", "VGRFR7", "VGRFR6", "VGRFR5", "VGRFR4", "VGRFR3", "VGRFR2", "VGRFR1"])
totalData = totalData.sample(frac=1)



x_data = totalData.iloc[:, 0:2]
y_data = totalData.iloc[:, 2]

# parkinsonScaler = StandardScaler()
# x_data_scaled = (parkinsonScaler.fit_transform(x_data))
# print(x_data_scaled)
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, random_state=1)
print(y_test)
def createForestModel():

  gaitModel = RandomForestClassifier()
  gaitModel.fit(x_train, y_train)
  joblib.dump(gaitModel, "Gait_Model_V2.joblib")
  print(gaitModel.score(x_test, y_test))
def createSequentialMode():
  gaitModel = Sequential()

  gaitModel.add(Dense(16, activation="relu", kernel_initializer="random_normal", input_dim=18))
  gaitModel.add(Dense(16, activation="relu", kernel_initializer="random_normal"))
  gaitModel.add(Dense(16, activation="relu", kernel_initializer="random_normal"))
  gaitModel.add(Dense(16, activation="relu", kernel_initializer="random_normal"))
  gaitModel.add(Dense(16, activation="relu", kernel_initializer="random_normal"))
  gaitModel.add(Dense(16, activation="relu", kernel_initializer="random_normal"))
  gaitModel.add(Dense(16, activation="relu", kernel_initializer="random_normal"))
  gaitModel.add(Dense(1, activation="sigmoid", kernel_initializer="random_normal"))

  gaitModel.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
  gaitModel.fit(x_train, y_train, batch_size=16, epochs=30)

  gaitModel.save("gait_model.h5")
  gaitModel.save_weights("gait_model_weights")


def testSequentialModel():
  gaitModel = tf.keras.models.load_model("gait_model.h5")
  gaitModel.load_weights("gait_model_weights")
  print(type(y_test))
  print()
  testData = (gaitModel.predict(x_train))
  corr = 0
  total = 0
  for i, value in (y_train.items()):
    print(str(value) + " vs " + str(round(testData[i][0])) + " - " + str(value == round(testData[i][0])))
    if (value == round(testData[i][0])):
      corr += 1
    total += 1

def testForestModel():
  gaitModel = joblib.load("Gait_Model_V2.joblib")
  print(gaitModel.score(x_test, y_test))

createForestModel();
