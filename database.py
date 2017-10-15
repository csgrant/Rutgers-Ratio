from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique = False, nullable = False)
    parties = db.relationship('Party', backref='user', lazy=True)

class Party(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), unique= False, nullable=False)
	address = db.Column(db.String(300), unique=False, nullable=False)
	latitude = db.Column(db.Float, nullable=False)
	longitude = db.Column(db.Float, nullable=False) 
	ratio = db.Column(db.String(10), nullable=False)
	payment = db.Column(db.Integer, nullable=True)
	frat = db.Column(db.String(20), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date = db.Column(db.DateTime, nullable=False)




@app.route('/list')
def listParties():
	allParties = Party.query.filter(Party.date >= (datetime.today() - timedelta(days=1)))
	return render_template('parties.html', parties=allParties)


@app.route('/list/<int:id>')
def moreInfo(id):
	return render_template('moreInfo.html', party=Party.query.get(id))

@app.route('/form', methods=['GET', 'POST'])
def form():
	if request.method == 'POST':
		#save event
		year, month, day = map(int, request.form['date'].split('-'))
		party = Party(title = request.form['title'], address = request.form['address'], latitude=40.4878751, 
			longitude=-74.439786, ratio = request.form['ratio'],payment = request.form['payment'],
			frat = request.form ['frat'], user_id=1, date = datetime(year, month, day))
		db.session.add(party)
		db.session.commit()
		return redirect(url_for('listParties')) #or (url_for('listParties')) / ('/list')
		
	else:
		return render_template('newevent.html')
