import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

df = pd.read_csv('Training.csv')
dftest = pd.read_csv('Testing.csv')

disease = set(df.iloc[:, -1])
disease = list(disease)
disease.sort()

labelencoder_Y = LabelEncoder()
df.iloc[:, -1] = labelencoder_Y.fit_transform(df.iloc[:, -1].values)

with open("Coded.csv", "w") as f:
    df.to_csv(f, line_terminator="\n", encoding="ISO-8859-1")


X = df.iloc[:, 0:132].values
Y = df.iloc[:, -1].values


x_train, x_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.20, random_state=0)


from sklearn.tree import DecisionTreeClassifier
dtmodel = DecisionTreeClassifier(max_depth = 35, random_state=1)
dtmodel.fit(x_train,y_train)
y_pred = dtmodel.predict(x_test)

score = dtmodel.score(x_train,y_train)
print(" TRAINING Accuracy :",int(score*100),end='%')

score = dtmodel.score(x_test,y_test)
print(" TESTING Accuracy :",int(score*100),end='%')


def saveModel():
    import pickle
    with open("DiseasePrediction(DT)", "wb") as f:
        pickle.dump(dtmodel, f)
saveModel()

header = ['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain',
 'stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition',
 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness','lethargy',
 'patches_in_throat', 'irregular_sugar_level',
 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin',
 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes',
 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 
 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising',
 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain',
 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side',
 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium',
 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration',
 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections',
 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf',
 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
 'yellow_crust_ooze',]

# disease = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis',
#        'Drug Reaction', 'Peptic ulcer diseae', 'AIDS', 'Diabetes ',
#        'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine',
#        'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 'Jaundice',
#        'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A',
#        'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E',
#        'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia',
#        'Dimorphic hemmorhoids(piles)', 'Heart attack', 'Varicose veins',
#        'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',
#        'Osteoarthristis', 'Arthritis',
#        '(vertigo) Paroymsal  Positional Vertigo', 'Acne',
#        'Urinary tract infection', 'Psoriasis', 'Impetigo']


model_inputs = []
for x in range(0, len(header)):
    model_inputs.append(0)

inputs = [i.strip() for i in input("Enter Symptoms : ").split()]

print(inputs)

for element in range(0, len(header)):
    for symptoms in inputs:
        if symptoms == header[element]:
            model_inputs[element] = 1
print(model_inputs)

with open("DiseasePrediction(DT)","rb") as f:
    decisionTreeModel = pickle.load(f)

prediction = decisionTreeModel.predict([model_inputs])
print(prediction[0])
print(disease[prediction[0]])

import joblib
joblib.dump(dtmodel, 'disease_predictor.pkl')