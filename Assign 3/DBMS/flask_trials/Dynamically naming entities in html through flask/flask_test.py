from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def order_rest():
   return render_template('order.html',rest='Foodies')

if __name__ == '__main__':
   app.run(debug = True)