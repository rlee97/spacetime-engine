from flask import Flask, redirect, url_for, request, render_template
from inverted_index_funcs import *

# Enter http://localhost:5000/?

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client["db"]
collection = db["col"]

@app.route('/result/<result>')
def result(result):
    bookDict = openJSON('bookkeeping.json')
    search_list = result.lower().split(' ')
    result_list = query(search_list, collection, bookDict)
    for item in bookDict:
        bookDict[item] = "//" + bookDict[item]

    return render_template('result.html', result = result_list, book = bookDict)

@app.route('/')
def index():
   return render_template('SearchEngine.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'GET':
      search = request.args.get('query')
      return redirect(url_for('result',result = search))
   else:
      search = request.form['query']
      return redirect(url_for('result',result = search))

if __name__ == '__main__':
   app.run(debug = True)