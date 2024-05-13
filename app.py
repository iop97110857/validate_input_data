from flask import Flask, request, render_template
import re

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('input_data.html')

@app.route('/submit_form', methods=['POST'])
def handle_form():
    id_number = request.form.get('id')
    name = request.form.get('name')
    gender = request.form.get('gender')
    email = request.form.get('email')

    # Validate ID number (assuming 台灣ID)
    if len(id_number) != 10:
        return "身分證號碼應該為10碼", 400
    first_char = id_number[0]
    if not first_char.isalpha():
        return "第一個字元應該為英文字母碼", 400
    if not id_number[1:].isdigit():
        return "後9個字元應該為數字", 400
    
    # Convert first character to corresponding number
    if not first_char.isupper():  # Ensure it's an uppercase letter
        return "第一個字元應該為大寫英文字母", 400
    first_digit = ord(first_char) - ord('A') + 10
    
    # Calculate sum of products of digits and weights
    sum_products = first_digit * 1
    for i in range(2, 11):
        digit = int(id_number[i - 1])
        weight = 10 - i + 2
        sum_products += digit * weight
    
    # Check if the sum modulo 10 equals to 0
    if sum_products % 10 != 0:
        return "身分證號碼檢查碼錯誤", 400

    # Validate name (assuming it's alphabetic)
    if not re.match(r'^[A-Za-z\s]+$', name):
        return "Invalid name", 400

    # Validate gender
    if gender not in ['Male', 'Female']:
        return "Invalid gender", 400

    # Validate email
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return "Invalid email", 400

    return "All entries are valid", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Listen on all available network interfaces and port 80
