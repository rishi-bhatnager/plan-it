from flask import Flask
app = Flask(__name__)

@app.route("/")
def output():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
