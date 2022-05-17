import imp
from flask import Flask,render_template,request,redirect, url_for
import newScrapper
import bunk_calculator

app = Flask(__name__)


obj = newScrapper.scrapper('https://webstream.sastra.edu/sastraparentweb/')
flag = True

@app.route("/",methods=['POST','GET'])
def home():
    print(1)
    global flag
    if flag == False:
       global obj
       obj = newScrapper.scrapper('https://webstream.sastra.edu/sastraparentweb/')
    flag = False
    return render_template('index.html')

@app.route("/cal",methods=['POST'])
def callScrapper():
    fo = dict(request.form)
    result,total = obj.getTimeTable(fo['regNo'],fo['dob'],fo['captcha'])
    if result == False:
        return redirect(url_for('home'))
    for res in result:
        print(*res,sep='\t')
    return render_template('calculator.html',result=result,total=total)

if __name__ == "__main__":
    app.run(debug=True)