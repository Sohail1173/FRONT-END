from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse

import requests
import json

from flask import Flask, request





app = Flask(__name__)

def generate_answer(value):
    data = [
    {   "student_name": "jerry",
        "net_profit_loss_class_level": "7.00",
        "id": 3,
        "items_sold": 8,
        "money_earned": "4.00",
        "money_spent": "50.00",
        "net_loss_profit_per_student": "12.00",
        
    },
    {   "student_name": "vinay",
        "net_profit_loss_class_level": "22222.00",
        "id": 7,
        "items_sold": 222222,
        "money_earned": "222222.00",
        "money_spent": "50.00",
        "net_loss_profit_per_student": "121212.00",
        
    },
    {   "student_name": "Alice",
        "net_profit_loss_class_level": "100.00",
        "id": 8,
        "items_sold": 20,
        "money_earned": "200.00",
        "money_spent": "100.00",
        "net_loss_profit_per_student": "10.00",
        
    },
    {   "student_name": "Bob",
        "net_profit_loss_class_level": "500.00",
        "id": 9,
        "items_sold": 50,
        "money_earned": "1000.00",
        "money_spent": "500.00",
        "net_loss_profit_per_student": "20.00",
        
    },
    {   "student_name": "Sara",
        "net_profit_loss_class_level": "300.00",
        "id": 10,
        "items_sold": 30,
        "money_earned": "600.00",
        "money_spent": "300.00",
        "net_loss_profit_per_student": "20.00",
        
    },
    {   "student_name": "Mike",
        "net_profit_loss_class_level": "50.00",
        "id": 11,
        "items_sold": 5,
        "money_earned": "100.00",
        "money_spent": "50.00",
        "net_loss_profit_per_student": "10.00",
        
    }
]
    
   

    student_data = next((student for student in data if student['id'] == value), None)
    return student_data


@app.route('/whatsapp', methods=['POST'])
def sms_reply():
    query = int(request.form.get("Body"))
    print("query", query)
   
    twilio_response = MessagingResponse()
    reply = twilio_response.message()
    answer = generate_answer(query)
    for key,val in answer.items():
        print(f"{key} : {val}")
        reply.body(f"{key} : {val}\n")


    
    return str(twilio_response)  


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8005)


