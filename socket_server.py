from  socket import *
import pandas
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import csv
import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate('D:\json\graduation-bcd1c-firebase-adminsdk-26dai-b61cd4e7e9.json')
firebase_admin.initialize_app(cred,
{
'databaseURL': 'https://graduation-bcd1c.firebaseio.com/'
})
db = firestore.client()
doc_ref = db.collection(u'patients')
data = pandas.read_csv("Datasets/heart_statlog_cleveland_hungary_final.csv")
x = data.drop(['target','oldpeak','ST slope','resting bp s'],axis=1)
y = data.target
X_train_rf, X_test_rf, y_train_rf, y_test_rf=train_test_split(x,y,random_state=0,test_size=0.1)
rfclassifier=RandomForestClassifier(n_estimators=40, random_state=0, criterion='entropy',n_jobs=10)
rfclassifier.fit(X_train_rf,y_train_rf)
rf_predict=rfclassifier.predict(X_test_rf)
########################################################################################################
def predict(max_HR,ecg):
    resting_ecg=int(ecg)
    docs = doc_ref.stream()
    for doc in docs:
        patient_ref=db.collection(u'patients').document(doc.id)
        get_age=patient_ref.get({u'age'})
        age = u'{}'.format(get_age.to_dict()['age'])
        get_sex=patient_ref.get({u'gender'})
        sex = u'{}'.format(get_sex.to_dict()['gender'])
        get_chest_pt=patient_ref.get({u'chestPainType'})
        chest_pain_type= u'{}'.format(get_chest_pt.to_dict()['chestPainType'])
        get_cholesterole=patient_ref.get({u'cholesterol'})
        cholestrole = u'{}'.format(get_cholesterole.to_dict()['cholesterol'])
        get_fbs=patient_ref.get({u'fastingBloodSugarML'})
        fasting_blood_sugar = u'{}'.format(get_fbs.to_dict()['fastingBloodSugarML'])
        get_chest_angina=patient_ref.get({u'exerciseAngina'})
        exercise_angina = u'{}'.format(get_chest_angina.to_dict()['exerciseAngina'])
        file = open("Datasets/file.csv", "w", newline='')
        header = ["age", "sex", "chest pain type", "cholesterol", "fasting blood sugar", "resting ecg", "max heart rate",
              "exercise angina"]
        data = [age, sex, chest_pain_type, cholestrole, fasting_blood_sugar, resting_ecg, max_HR, exercise_angina]
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(data)
        file.close()
        patient_heart_readings = pandas.read_csv("Datasets/file.csv")
        patient_prediction = rfclassifier.predict(patient_heart_readings)
        if (patient_prediction == 1):
            pred = "heart at risk"
            sensor_data = {"ecg": str(resting_ecg), "maxHeartRate": str(max_HR), "prediction": pred}
            doc_ref.document(doc.id).update(sensor_data)
        else:
            pred = "healthy heart"
            sensor_data = {"ecg": str(resting_ecg), "maxHeartRate": str(max_HR), "prediction": pred}
            doc_ref.document(doc.id).update(sensor_data)
    return




if __name__ == '__main__':
    while True:
        sock = socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        sock.bind(("localhost", 9999))  # bind host address and port together
        # configure how many client the server can listen simultaneously
        sock.listen(1)
        conn, address = sock.accept()  # accept new connection
        max_HR = 0
        HR = conn.recv(1024).decode()
        resting_ecg = conn.recv(1024).decode()
        if int(HR) > max_HR:
            max_HR = int(HR)
            predict(max_HR, resting_ecg)
        conn.close()