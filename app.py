from models import db, User, Obra, Gasto, Department
from flask import Flask, render_template_string, redirect, url_for, request, flash
from flask_login import (
    LoginManager, UserMixin,
    login_user, login_required,
    logout_user, current_user
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'troque_para_uma_chave_segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- TEMPLATES EMBUTIDOS ---
login_tpl = """
<!doctype html>
<title>Login</title>
<h2>Login</h2>
<form method="post">
  <label>E-mail:</label><input name="email" type="email" required><br>
  <label>Senha:</label><input name="password" type="password" required><br>
  <button type="submit">Entrar</button>
</form>
<p>ou <a href='{{ url_for('register') }}'>Cadastre-se</a></p>
{% with msgs = get_flashed_messages() %}
  {% for m in msgs %}<p style='color:red;'>{{ m }}</p>{% endfor %}
{% endwith %}
"""

register_tpl = """
<!doctype html>
<title>Cadastro</title>
<h2>Cadastro de usuário</h2>
<form method="post">
  <label>Nome:</label><input name="name" required><br>
  <label>E-mail:</label><input name="email" type="email" required><br>
  <label>Senha:</label><input name="password" type="password" required><br>
  <label>Departamento:</label>
  <select name="department_id" required>
    {% for d in departments %}
      <option value="{{ d.id }}">{{ d.name }}</option>
    {% endfor %}
  </select><br>
  <label>Obra:</label>
  <select name="obra_id" required>
    {% for o in obras %}
      <option value="{{ o.id }}">{{ o.name }}</option>
    {% endfor %}
  </select><br>
  <button type="submit">Cadastrar</button>
</form>
<p><a href="{{ url_for('login') }}">Já tenho conta</a></p>
{% with msgs = get_flashed_messages() %}
  {% for m in msgs %}<p style='color:red;'>{{ m }}</p>{% endfor %}
{% endwith %}
"""

dashboard_tpl = """
<!doctype html>
<title>Dashboard</title>
<h2>Seja bem-vindo, {{ current_user.name }}!</h2>
<h3>Departamento: {{ current_user.department.name }}</h3>
<ul>
  {% if current_user.department.name == 'RH' %}
    <li><a href="#">Cadastro de Funcionários</a></li>
    <li><a href="#">Folha de Pagamento (Holerite)</a></li>
  {% elif current_user.department.name == 'Fiscal' %}
    <li><a href="#">Lançar Locações</a></li>
  {% elif current_user.department.name == 'Segurança' %}
    <li><a href="#">Cadastro de EPIs</a></li>
    <li><a href="#">Registro de Retirada de EPIs</a></li>
  {% endif %}
  <li><a href="#">Obras Cadastradas</a></li>
</ul>
<p><a href="{{ url_for('logout') }}">Logout</a></p>
"""

# --- ROTAS ---
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(email=request.form['email']).first()
        if u and u.check_password(request.form['password']):
            login_user(u)
            return redirect(url_for('dashboard'))
        flash('E-mail ou senha incorretos.')
    return render_template_string(login_tpl)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pw    = request.form['password']
        dept = Department.query.get(int(request.form['department_id']))
        obra = Obra.query.get(int(request.form['obra_id']))
        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.')
        else:
            u = User(name=name, email=email,
                     department=dept, obra=obra)
            u.set_password(pw)
            db.session.add(u)
            db.session.commit()
            flash('Cadastro realizado! Faça o login.')
            return redirect(url_for('login'))
    depts = Department.query.all()
    obras = Obra.query.all()
    return render_template_string(register_tpl,
                                  departments=depts,
                                  obras=obras)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template_string(dashboard_tpl)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.before_first_request
def init_db():
    db.create_all()
    for nome in ['RH','Fiscal','Segurança']:
        if not Department.query.filter_by(name=nome).first():
            db.session.add(Department(name=nome))
    if Obra.query.count() == 0:
        for i in range(5):
            rnd = ''.join(random.choices(string.ascii_uppercase, k=4))
            db.session.add(Obra(name=f"Obra {rnd}"))
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
