from flask import Flask, render_template, url_for, request, flash, redirect, request
from disease_prediction import app, db, bcrypt, mail
import pandas as pd
import joblib
import pickle
from disease_prediction.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                     RequestResetForm, ResetPasswordForm)
from disease_prediction.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


filename = "disease_prediction/DiseasePrediction(DT)"
with open(filename,"rb") as f:
    decisionTreeModel = pickle.load(f)

# filename = "DiseasePrediction(RFC)"
# with open(filename,"rb") as f:
#     randomForestModel = pickle.load(f)

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
 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf',
 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
 'yellow_crust_ooze']

disease = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis',
       'Drug Reaction', 'Peptic ulcer diseae', 'AIDS', 'Diabetes',
       'Gastroenteritis', 'Bronchial Asthma', 'Hypertension', 'Migraine',
       'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 'Jaundice',
       'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A',
       'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E',
       'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia',
       'Dimorphic hemmorhoids(piles)', 'Heart attack', 'Varicose veins',
       'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',
       'Osteoarthristis', 'Arthritis',
       '(vertigo) Paroymsal  Positional Vertigo', 'Acne',
       'Urinary tract infection', 'Psoriasis', 'Impetigo']

precautions = {
    'Fungal infection': ['bath twice', 'use detol or neem in bathing water', 'keep infected area dry', 'use clean cloths'],
     'Allergy': ['apply calamine', 'cover area with bandage', 'Anti-inflammatory medication', 'use ice to compress itching'],
      'GERD': ['avoid fatty spicy food', 'avoid lying down after eating','maintain healthy weight', 'exercise'],
       'Chronic cholestasis': ['cold baths','anti itch medicine','consult doctor','eat healthy'],
       'Drug Reaction': ['stop irritation','consult nearest hospital','stop taking drug','follow up'],
        'Peptic ulcer diseae': ['avoid fatty spicy food 	consume probiotic food 	eliminate milk 	limit alcohol'],
         'AIDS': ['avoid open cuts','wear ppe if possible','consult doctor','follow up'], 
         'Diabetes': ['have balanced diet','exercise','consult doctor','follow up'],
         'Gastroenteritis': ['stop eating solid food for while','try taking small sips of water','rest','ease back into eating'],
        'Bronchial Asthma': ['switch to loose cloothing','take deep breaths','get away from trigger','seek help'],
         'Hypertension': ['meditation','salt baths','reduce stress','get proper sleep'],
          'Migraine': ['meditation','reduce stress','use poloroid glasses in sun','consult doctor'],
       'Cervical spondylosis': ['use heating pad or cold pack', 'exercise', 'take otc pain reliver', 'consult doctor'],
        'Paralysis (brain hemorrhage)': ['massage', 'eat healthy', 'exercise', 'consult doctor'],
         'Jaundice': ['drink plenty of water','consume milk thistle','eat fruits and high fiberous food','medication'],
       'Malaria': ['Consult nearest hospital','avoid oily food','avoid non veg food','keep mosquitos out'],
        'Chicken pox': ['use neem in bathing','consume neem leaves','take vaccine','avoid public places'],
         'Dengue': ['drink papaya leaf juice','avoid fatty spicy food','keep mosquitos away','keep hydrated'], 
         'Typhoid': ['eat high calorie vegitables','antiboitic therapy','consult doctor','medication'],
          'hepatitis A': ['Consult nearest hospital','wash hands through','avoid fatty spicy food','medication'],
       'Hepatitis B': ['consult nearest hospital','vaccination','eat healthy','medication'],
        'Hepatitis C': ['Consult nearest hospital','vaccination','eat healthy','medication'],
         'Hepatitis D': ['consult doctor','medication','eat healthy','follow up'],
          'Hepatitis E': ['stop alcohol consumption','rest','consult doctor','medication'],
       'Alcoholic hepatitis': ['stop alcohol consumption','consult doctor','medication','follow up'],
        'Tuberculosis': ['cover mouth','consult doctor','medication','rest'],
         'Common Cold': ['drink vitamin c rich drinks','take vapour','avoid cold food','keep fever in check'],
          'Pneumonia': ['consult doctor','medication','rest','follow up'],
       'Dimorphic hemmorhoids(piles)': ['avoid fatty spicy food','consume witch hazel','warm bath with epsom salt','consume alovera juice'],
        'Heart attack': ['call ambulance','chew or swallow asprin','keep calm','Eat a healthy diet'],
         'Varicose veins': ['lie down flat and raise the leg high','use oinments','use vein compression','dont stand still for long'],
       'Hypothyroidism': ['reduce stress','exercise','eat healthy','get proper sleep'],
       'Hyperthyroidism': ['eat healthy','massage','use lemon balm','take radioactive iodine treatment'], 
       'Hypoglycemia': ['lie down on side','check in pulse','drink sugary drinks','consult doctor'],
       'Osteoarthristis': ['acetaminophen','consult nearest hospital','follow up','salt baths'],
        'Arthritis': ['exercise','use hot and cold therapy','try acupuncture','massage'],
       '(vertigo) Paroymsal  Positional Vertigo': ['lie down','avoid sudden change in body','avoid abrupt head movment','relax'],
        'Acne': ['bath twice','avoid fatty spicy food','drink plenty of water','avoid too many products'],
       'Urinary tract infection': ['drink plenty of water','increase vitamin c intake','drink cranberry juice','take probiotics'],
        'Psoriasis': ['wash hands with warm soapy water','stop bleeding using pressure','consult doctor','salt baths'],
         'Impetigo': ['soak affected area in warm water','use antibiotics','remove scabs with wet compressed cloth','consult doctor']
}
# DiseasePred = joblib.load(open('disease_predictor.pkl','rb'))


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/submit', methods=["POST", "GET"])
def submit():
    if current_user.is_authenticated and request.method=='POST':
        email = current_user.email
        val = request.form.get('emoji')
        return redirect('mailto:yashgoyalg400@gmail.com,achal.v123@gmail.com,yashrai2201@gmail.com?subject='+'Feedback of Predict Genics from '+str(email)+'&body='+'Hello,\nMy overall experience over your website was '+str(val)+'.')
    else:
        return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

predictionDT = []

@app.route("/diseaseprediction", methods=["POST", "GET"])
def Disease():

    symptoms = []
    for x in range(0, len(header)):
            symptoms.append(0)

    inputs = []
    if request.method == "POST":
        rf = request.form
        # print(rf)
        for key, value in rf.items():
            # print(key)
            inputs.append(value)

        for element in range(0, len(header)):
            for symptom in inputs:
                if symptom == header[element]:
                    symptoms[element] = 1
                    
    
        if len(inputs) < 3 or len(inputs) > 8:
            flash("Please Select symptoms only between 3 and 8 Inclusive")
        else:
            global predictionDT
            predictionDT = decisionTreeModel.predict([symptoms])
            if predictionDT:
                return render_template("Infected.html", disease=predictionDT[0])
            else:
                return render_template("NonInfected.html")
    return render_template("dp.html")

@app.route("/precations", methods=["POST", "GET"])
def Precautions():
    if predictionDT:
        return render_template('precautions.html', precaution=precautions[predictionDT[0]])
    else:
        return render_template("dp.html")

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='yashgoyalg400@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route('/confirm_mail', methods=['GET', 'POST'])
def confirm_mail(user):
    token = user.get_reset_token()
    msg = Message('Email Confirmation on Predict Genics',
                  sender='yashgoyalg400@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Confirm your email address,

Thank you for signing up for Predict Genics!

To confirm your account, visit the following link:
{url_for('confirm_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

a = ''

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # db.session.add(user)
        # db.session.commit()
        global a 
        a = user
        confirm_mail(user)
        flash('We have sent an email to '+user.email+'. Click on the link provided to finish signing up.', 'info')
        return redirect(url_for('login')) #home is the function of the route
    return render_template('register.html', title='Register', form=form)

@app.route("/email_confirmed/<token>", methods=['GET', 'POST'])
def confirm_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    db.session.add(a)
    db.session.commit()
    flash('Your account has been created! You are now able to log in', 'success')
    return render_template('mail_confirmed.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    print(user)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)