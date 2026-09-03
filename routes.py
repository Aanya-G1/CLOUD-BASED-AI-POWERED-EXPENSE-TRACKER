from flask import request, jsonify, session, redirect, render_template, flash
from datetime import date
from main import app, db, model, vectorizer
from models import Expense
from analytics import analyze_finances
from io import BytesIO
from openpyxl import Workbook
import io, os
from supabase import create_client
from datetime import datetime



@app.route('/')
def main_page():
    return render_template("index.html")

@app.route('/predict-category', methods=['POST'])
def predict_category():
    data = request.get_json()
    description = data.get('description', '')

    if not description:
        return jsonify({'error': 'Description is required'}), 400

    vectorized = vectorizer.transform([description])
    category = model.predict(vectorized)[0]

    return jsonify({'category': category})


@app.route('/add-expense', methods=['POST'])

def add_expense():
    data = request.get_json()

    description = data.get('description')
    amount = data.get('amount')
    notes = data.get('notes', '')
    category = data.get('category') 
    date_str = data.get('date')     

    if not description or amount is None:
        return jsonify({'error': 'Description and amount are required'}), 400


    if not category:
        vectorized_desc = vectorizer.transform([description])
        category = model.predict(vectorized_desc)[0]

    try:
        expense_date = date.today() if not date_str else date.fromisoformat(date_str)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    new_expense = Expense(
        description=description,
        amount=amount,
        category=category,
        notes=notes,
        date=expense_date
    )

    db.session.add(new_expense)
    db.session.commit()

    return jsonify({
        'message': 'Expense added successfully',
        'expense': {
            'id': new_expense.id,
            'description': new_expense.description,
            'amount': new_expense.amount,
            'category': new_expense.category,
            'date': new_expense.date.isoformat(),
            'notes': new_expense.notes
        }
    })

@app.route('/view-expenses', methods=['GET'])
def view_expenses():
    expenses = Expense.query.all()
    result = [
        {
            "id": e.id,
            "description": e.description,
            "amount": e.amount,
            "category": e.category,
            "notes": e.notes,
            "date": e.date.strftime("%Y-%m-%d")
        } for e in expenses
    ]
    return jsonify(result)


@app.route('/update-expense/<int:id>', methods=['PUT'])
def update_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({"error": "Expense not found!"})

    data = request.get_json()
    expense.description = data.get('description', expense.description)
    expense.amount = data.get('amount', expense.amount)
    expense.category = data.get('category', expense.category)
    expense.notes = data.get('notes', expense.notes)
    expense.date = date.fromisoformat(data.get('date')) if data.get('date') else expense.date
    db.session.commit()

    return jsonify({"message": "Expense updated successfully!"})


@app.route('/delete-expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get(id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({"message": "Expense deleted!"})
    else:
        return jsonify({"error": "Expense not found!"})


@app.route('/income')
def income_page():
    return render_template('income.html')



from models import User

@app.route('/login-page')
def login_page():
    return render_template('login.html')

@app.route('/signup-page')
def signup_page():
    return render_template('signup.html')


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    existing = User.query.filter_by(email=email).first()
    if existing:
        flash("Email already exists. Please login.", "error")
        return redirect('/signup-page')

    user = User(name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    session['email'] = email
    return redirect('/welcome')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email, password=password).first()

    if not user:
        flash("Invalid email or password", "error")
        return redirect('/login-page')

    session['email'] = email
    return redirect('/welcome')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login-page')

@app.route('/expense-page')
def expense_page():
    if 'email' not in session:
        return redirect('/login-page')
    return render_template("entryFront.html")

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect('/login-page')
    return render_template("dashboard.html")

@app.route('/welcome')
def welcome():
    if 'email' not in session:
        return redirect('/login-page')

    user = User.query.filter_by(email=session['email']).first()
    return render_template("welcome.html", name=user.name)

# ------------------ ANALYTICS API ------------------

from flask import send_file
from models import Income, Expense
from analytics import analyze_finances
from io import BytesIO
from openpyxl import Workbook
from datetime import datetime

@app.route("/analytics")
def analytics_api():
    try:
        # Fetch from your SQLAlchemy database
        income = Income.query.all()
        expenses = Expense.query.all()

        # Convert Income rows → JSON structure expected by analytics.py
        income_data = [
            {
                "name": i.name,
                "source": i.source,
                "amount": i.amount,
                "notes": i.notes,
                "date": i.date.isoformat()
            }
            for i in income
        ]

        # Convert Expense rows → JSON structure
        expense_data = [
            {
                "description": e.description,
                "amount": e.amount,
                "category": e.category,
                "notes": e.notes,
                "date": e.date.isoformat()
            }
            for e in expenses
        ]

        # Pass to your analytics engine
        result = analyze_finances(income_data, expense_data)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------ EXPORT EXCEL ------------------

@app.route("/export/excel")
def export_excel():
    try:
        income = Income.query.all()
        expenses = Expense.query.all()

        wb = Workbook()
        ws = wb.active
        ws.title = "Finance Report"

        ws.append(["Type", "Name/Description", "Source", "Amount", "Category", "Notes", "Date"])

        # Income rows
        for i in income:
            ws.append([
                "Income",
                i.name,
                i.source,
                i.amount,
                "Income",
                i.notes,
                i.date.isoformat()
            ])

        # Expense rows
        for e in expenses:
            ws.append([
                "Expense",
                e.description,
                "",
                e.amount,
                e.category,
                e.notes,
                e.date.isoformat()
            ])

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name=f"Finance_Report_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------ ANALYTICS PAGE ------------------

@app.route("/analytics-page")
def analytics_page():
    if "email" not in session:
        return redirect("/login-page")
    return render_template("analytics.html")
