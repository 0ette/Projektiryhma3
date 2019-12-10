
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
    html = open("index.html")
    response = html.read().replace('\n', '')
    html.close()
    return response
    
@app.route("/<otakuva>/")
def otakuva(otakuva):
    if otakuva == 'otakuva':
        print("ok")
    
    return otakuva
    
if __name__ == "__main__":
   app.run(host= '0.0.0.0')
