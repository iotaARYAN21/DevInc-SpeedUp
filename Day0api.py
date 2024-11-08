from flask import Flask ,request,jsonify

app = Flask(__name__)

@app.route('/calculate',methods=['POST'])  # name of the endpoint and the method

def calculate():
    data = request.get_json()
    operation = data.get("operation")
    num1 =float(data.get("num1"))
    num2 = float(data.get("num2"))

    if(operation=="+"):
        result = num1+num2
    
    elif operation=='-':
        result = num1-num2
    
    elif operation == '*':
        result = num1 * num2

    elif operation == '/':
        if(num2 == 0):
            result = 'Cannot divide by Zero'
        else:
            result = num1/num2
    else:
        return jsonify({'error':"Incorrect operation"})
    return jsonify({"result":result})

if __name__ == '__main__':
    app.run(debug=True)
