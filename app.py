from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


def fetch_all_data():
    url = 'https://f6dd-2409-408c-8dbe-c618-604b-621-7953-b35.ngrok-free.app/getitems'
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        return data.get('data', [])  
    except requests.exceptions.RequestException as e:
        print("Error fetching data from API:", e)
        return []

@app.route('/')
def index():
    
    all_data = fetch_all_data()

    form_data = {
        'student_name': '',
        'items_sold': '',
        'money_earned': '',
        'money_spent': '',
        'net_profit_loss_class_level': '',
        'net_loss_profit_per_student': ''
    }

    return render_template('index.html', all_data=all_data, form_data=form_data)

@app.route('/additems', methods=['POST'])
def create():
    student_name = request.form['student_name']
    items_sold = request.form['items_sold']
    money_earned = request.form['money_earned']
    money_spent = request.form['money_spent']
    net_profit_loss_class_level = request.form['net_profit_loss_class_level']
    net_loss_profit_per_student = request.form['net_loss_profit_per_student']

    create_url = 'https://f6dd-2409-408c-8dbe-c618-604b-621-7953-b35.ngrok-free.app/additems'
    payload = {
        'student_name': student_name,
        'items_sold': items_sold,
        'money_earned': money_earned,
        'money_spent': money_spent,
        'net_profit_loss_class_level': net_profit_loss_class_level,
        'net_loss_profit_per_student': net_loss_profit_per_student
    }
    try:
        response = requests.post(create_url, json=payload)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print("Error creating data via API:", e)

    return redirect(url_for('index'))

@app.route('/updateitems/<int:id>', methods=['POST', 'PUT'])
def update(id):
    student_name = request.form['student_name']
    items_sold = request.form['items_sold']
    money_earned = request.form['money_earned']
    money_spent = request.form['money_spent']
    net_profit_loss_class_level = request.form['net_profit_loss_class_level']
    net_loss_profit_per_student = request.form['net_loss_profit_per_student']

    update_url = f'https://f6dd-2409-408c-8dbe-c618-604b-621-7953-b35.ngrok-free.app/updateitems/{id}'
    payload = {
        'student_name': student_name,
        'items_sold': items_sold,
        'money_earned': money_earned,
        'money_spent': money_spent,
        'net_profit_loss_class_level': net_profit_loss_class_level,
        'net_loss_profit_per_student': net_loss_profit_per_student
    }
    try:
        response = requests.put(update_url, json=payload)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print("Error updating data via API:", e)
    return redirect(url_for('index'))

@app.route('/deleteitems/<int:id>', methods=['POST', 'DELETE'])
def delete(id):
    delete_url = f'https://f6dd-2409-408c-8dbe-c618-604b-621-7953-b35.ngrok-free.app/deleteitems/{id}'
    try:
        response = requests.delete(delete_url)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print("Error deleting data via API:", e)

    
    return redirect(url_for('index'))


