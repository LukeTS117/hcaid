import flask
import pickle
import pandas as pd

with open(f'model/bike_model_xgboost.pkl', 'rb') as f:
    model = pickle.load(f)

app = flask.Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method =='GET':
        return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':
        age = int(flask.request.form['age'])
        avg_glucose_level = float(flask.request.form['glucose_level'])
        bmi = float(flask.request.form['bmi'])
        gender = int(flask.request.form['gender'])
        hypertension = int(flask.request.form['hypertension'])
        heart_disease = int(flask.request.form['heart_disease'])
        ever_married = int(flask.request.form['ever_married'])
        Residence_type = int(flask.request.form['Residence_type'])
        

        if flask.request.form['work_type'] == "work_type_Govt_job":
            work_type_Govt_job = 1
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children = 0
        elif flask.request.form['work_type'] == "work_type_Never_worked":
            work_type_Govt_job = 0
            work_type_Never_worked = 1
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children = 0
        elif flask.request.form['work_type'] == "work_type_Private":
            work_type_Govt_job = 0
            work_type_Never_worked = 0
            work_type_Private = 1
            work_type_Self_employed = 0
            work_type_children = 0
        elif flask.request.form['work_type'] == "work_type_Self_employed":
            work_type_Govt_job = 0
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 1
            work_type_children = 0
        elif flask.request.form['work_type'] == "work_type_children":
            work_type_Govt_job = 0
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children = 1
        
        if flask.request.form['smoking_status'] == "smoking_status_Unknown":
            smoking_status_Unknown = 1
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0
        elif flask.request.form['smoking_status'] == "smoking_status_formerly_smoked":
            smoking_status_Unknown = 0
            smoking_status_formerly_smoked = 1
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0
        elif flask.request.form['smoking_status'] == "smoking_status_never_smoked":
            smoking_status_Unknown = 0
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 1
            smoking_status_smokes = 0
        elif flask.request.form['smoking_status'] == "smoking_status_smokes":
            smoking_status_Unknown = 0
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 1

        dataframe_columns = model.get_booster().feature_names
        input_variables = pd.DataFrame([[gender, age, hypertension, heart_disease, ever_married, Residence_type, avg_glucose_level, bmi, work_type_Govt_job, work_type_Never_worked, work_type_Private, work_type_Self_employed, work_type_children, smoking_status_Unknown, smoking_status_never_smoked, smoking_status_formerly_smoked, smoking_status_smokes]],
        columns=dataframe_columns)
        prediction = model.predict_proba(input_variables)[0][1]
        percentage = "{:.2%}".format(prediction * 10)
        print(percentage)

        return flask.render_template('main.html', result=percentage)

if __name__ == '__main__':
    app.run()