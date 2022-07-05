'''
Creates web app to be used to make prediction with user input. 

Can be imported as module.

Requires `flask` python library 
and function `input_prediction` from package `neural_network` and file `input_prediction.py` on project folder. 
'''

from flask import Flask, render_template, request
from neural_network.input_prediction import input_prediction

def create_app(): 
    '''Creates web app using flask framework '''

    app = Flask(__name__)

    @app.route("/")
    def input_form(): 
        '''
        Initial function called once website is activated. 

        Renders form.html template with a form for user input on localost, in gate 5000. 
        '''

        return render_template('form.html')

    @app.route("/form", methods = ['POST', 'GET'])
    def form(): 
        '''
        Takes user input via POST HTTP method to use for prediction. 

        Calls input_prediction function that makes and returns the prediction.

        Renders form.html template again passing prediction parameter to it. 
        '''

        demands = []
        renewables = []
        if request.method == 'POST': 
            demands.append(request.form['demand1'])
            demands.append(request.form['demand2'])
            demands.append(request.form['demand3'])
            demands.append(request.form['demand4'])
            demands.append(request.form['demand5'])
            renewables.append(request.form['renewable1'])
            renewables.append(request.form['renewable2'])
            renewables.append(request.form['renewable3'])
            renewables.append(request.form['renewable4'])
            renewables.append(request.form['renewable5'])

            prediction = input_prediction(demands, renewables)

        return render_template('form.html', prediction = prediction[0])
    
    return app

    


