import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os


HOST=os.getenv('HOST')
ROOT=os.getenv('ROOT')
PASSWORD=os.getenv('PASSWORD')
DB=os.getenv('DB')

app = Flask(__name__)

CORS(app)
# CORS(app, resources={r"/getitems": {"origins": "https://127.0.0.1:5000"}})
CORS(app, resources={r"/": {"origins": ""}})
def connection(host,user,password,database):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn



def create_table():
    conn = connection(HOST,ROOT,PASSWORD,DB)
    cur = conn.cursor()

    student_table = """CREATE TABLE IF NOT EXISTS jaya (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_name VARCHAR(45),
        money_spent DECIMAL(19,2),
        items_sold INT,
        money_earned DECIMAL(19,2),
        net_loss_profit_per_student DECIMAL(19,2),
        net_profit_loss_class_level DECIMAL(19,2)
    )"""

    cur.execute(student_table)
    conn.commit()  
    cur.close()    
    print("Table created successfully")

@app.route('/')
def hello():
    return 'Your Flask Server Running'

@app.route('/additems', methods=['POST'])
def Insert_values():
    conn = connection(HOST,ROOT,PASSWORD,DB)
    cur = conn.cursor()
    try:
        data=request.get_json()

        print(data)
        student_name=data["student_name"]
        money_spent=data["money_spent"]
        items_sold=data["items_sold"]
        money_earned=data["money_earned"]
        net_loss_profit_per_student=data["net_loss_profit_per_student"]
        net_profit_loss_class_level=data["net_profit_loss_class_level"]
    
        # cur.executemany('INSERT INTO  jaya ("id",student_name, money_spent, items_sold, money_earned, net_loss_profit_per_student, net_profit_loss_class_level) VALUES (%s, %s, %s, %s, %s, %s,%s)', (id,student_name, money_spent, items_sold, money_earned, net_loss_profit_per_student, net_profit_loss_class_level))
        cur.execute(
            'INSERT INTO jaya (student_name, money_spent, items_sold, money_earned, net_loss_profit_per_student, net_profit_loss_class_level) VALUES (%s, %s, %s, %s, %s, %s)',
            ( student_name, money_spent, items_sold, money_earned, net_loss_profit_per_student, net_profit_loss_class_level)
        )
        conn.commit()  
        cur.close()   

        response = {
            'error' : False,
            'message': 'Item Added Successfully',
            'data': data         
        }
        return jsonify(response), 201
    except Exception as e:
        response = {
            'error' : False,
            'message': f'Error Ocurred: {e}',
            'data': None         
        }
        return jsonify(response), 500
    
@app.route('/getitems', methods = ['GET'])
def Read_data():
    conn = connection(HOST,ROOT,PASSWORD,DB)
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM jaya")
        rows = cur.fetchall()

        item=[{"id":item[0],"student_name":item[1], "money_spent":item[2], "items_sold":item[3], "money_earned":item[4], "net_loss_profit_per_student":item[5]," net_profit_loss_class_level":item[6]} for item in rows]
        
        conn.commit()  
        cur.close()    
        response = {
            'error' : False,
            'message': 'Items Fetched Successfully',
            'data': item

        }
        return jsonify(response), 200
    except Exception as e:
        response = {
            'error' : False,
            'message': f'Error Ocurred: {e}',
            'data': None         
        }
        return jsonify(response), 500
@app.route('/updateitems/<int:item_id>', methods=['PUT'])
def Update_data(item_id):
        
        conn = connection(HOST,ROOT,PASSWORD,DB)
        cur = conn.cursor()
        try:
            data=request.get_json()
            student_name=data["student_name"]
            money_spent=data["money_spent"]
            items_sold=data["items_sold"]
            money_earned=data["money_earned"]
            net_loss_profit_per_student=data["net_loss_profit_per_student"]
            net_profit_loss_class_level=data["net_profit_loss_class_level"]

            cur.execute('UPDATE jaya  SET student_name=%s,money_spent=%s, items_sold=%s,money_earned=%s,net_loss_profit_per_student=%s,net_profit_loss_class_level=%s WHERE id = %s', (student_name,money_spent, items_sold,money_earned,net_loss_profit_per_student,net_profit_loss_class_level,item_id))


            # cur.execute('UPDATE jaya SET student_name = %s,money_spent=%s WHERE id = %s', (student_name,money_spent,item_id))
            conn.commit()
            cur.close()
            response = {
            'error' : False,
            'message': 'Items Updated Successfully',
            'data': { 'item_id': item_id }
        }
            return jsonify(response), 201
            
           
        except Exception as e:
            response = {
            'error' : False,
            'message': f'Error Ocurred: {e}',
            'data': None         
        }
        return jsonify(response), 500

@app.route('/deleteitems/<int:item_id>', methods=['DELETE'])
def delete_items(item_id):
    conn = connection(HOST,ROOT,PASSWORD,DB)
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM jaya WHERE id = %s',(item_id,))
        # cur.execute('DELETE FROM items WHERE id = %s', (item_id,))

        conn.commit()
        cur.close()
        response = {
            'error' : False,
            'message': 'Item Deleted Successfully',
            'data': { 'item_id': item_id }
        }
        return jsonify(response), 201
    except Exception as e:
        response = {
            'error' : False,
            'message': f'Error Ocurred: {e}',
            'data': None         
        }
        return jsonify(response), 500


if __name__ == '__main__':
    create_table()
    app.run(host="0.0.0.0",port=8001)