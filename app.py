from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    expenses = Expense.query.all()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    amount = request.form.get('amount')
    category = request.form.get('category')
    date = request.form.get('date')
    new_expense = Expense(amount=amount, category=category, date=date)
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/report')
def report():
    expenses = Expense.query.all()
    total = sum(expense.amount for expense in expenses)
    return render_template('report.html', expenses=expenses, total=total)

if __name__ == '__main__':
    app.run(debug=True)
