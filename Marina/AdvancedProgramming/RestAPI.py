from flask import Flask, jsonify, render_template, request
from withRelu import input_prediction

app = Flask(__name__)

@app.route("/")
def input_form(): 
    return render_template('form.html')

@app.route("/form", methods = ['POST', 'GET'])
def form(): 
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


if __name__ == "__main__": 
    app.run(debug=True)


