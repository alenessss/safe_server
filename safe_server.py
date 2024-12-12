from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import re

app = Flask(__name__)
app.secret_key = 'secure_key'  # Для отображения flash сообщений

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.getcwd(), 'site.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель базы данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Создание всех таблиц
with app.app_context():
    db.create_all()

# Валидация данных
def is_valid_username(username):
    """Проверка, что имя пользователя содержит только допустимые символы."""
    return re.match(r"^[a-zA-Z0-9_.-]+$", username) is not None

def is_valid_email(email):
    """Проверка, что email имеет корректный формат."""
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) is not None

# Главная страница
@app.route('/', methods=['GET'])
def index():
    message = request.args.get('message', '')  # Получение сообщения безопасным способом
    users = User.query.all()  # Получение всех пользователей через ORM
    return render_template('index.html', users=users, message=message)

# Добавление пользователя
@app.route('/add', methods=['POST'])
def add_user():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    
    # Проверка валидности данных
    if not is_valid_username(username):
        flash("Некорректное имя пользователя. Допустимы только буквы, цифры и символы _ . -", "error")
        return redirect(url_for('index'))
    
    if not is_valid_email(email):
        flash("Некорректный email. Проверьте правильность ввода.", "error")
        return redirect(url_for('index'))

    try:
        # Проверка на существование email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Пользователь с таким email уже существует.", "warning")
            return redirect(url_for('index'))

        # Создание нового пользователя
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash("Пользователь успешно добавлен.", "success")
    except Exception as e:
        app.logger.error(f"Ошибка при добавлении пользователя: {e}")
        db.session.rollback()
        flash("Произошла ошибка при добавлении пользователя.", "error")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)