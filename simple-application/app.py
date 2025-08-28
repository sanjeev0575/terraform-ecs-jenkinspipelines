# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return 'Hello, World!'


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    name = request.args.get("name", "World")
    return jsonify(message=f"Hello, {name}!")

if __name__ == "__main__":
    # simple dev server (not for production)
    app.run(host="0.0.0.0", port=9000)
