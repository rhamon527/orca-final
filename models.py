from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Departamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuarios = db.relationship('User', backref='departamento', lazy=True)

class Obra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    gastos = db.relationship('Gasto', backref='obra', lazy=True)
    usuarios = db.relationship('User', backref='obra_relacionada', lazy=True)

class User(db.Model, UserMixin):
    active = db.Column(db.Boolean, default=True)

    @property
    def is_active(self):
        return self.active

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'visualizador' ou 'editor'

    obra_id = db.Column(db.Integer, db.ForeignKey('obra.id'), nullable=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=True)

class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_nota = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_nota = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    aprovador = db.Column(db.String(100), nullable=False)
    obra_id = db.Column(db.Integer, db.ForeignKey('obra.id'), nullable=False)
 from flask_sqlalchemy import SQLAlchemy
 from flask_login import UserMixin

 db = SQLAlchemy()

+class Department(db.Model):
+    __tablename__ = 'department'
+    id   = db.Column(db.Integer, primary_key=True)
+    name = db.Column(db.String(50), unique=True, nullable=False)
+    users = db.relationship('User', backref='department', lazy=True)
+
 class Obra(db.Model):
     __tablename__ = 'obra'
     id     = db.Column(db.Integer, primary_key=True)
     nome   = db.Column(db.String(200), nullable=False)
     gastos = db.relationship('Gasto', backref='obra', lazy=True)
+    users  = db.relationship('User', backref='obra', lazy=True)

 class User(db.Model, UserMixin):
     __tablename__ = 'user'
     id             = db.Column(db.Integer, primary_key=True)
     nome           = db.Column(db.String(100), nullable=False)
     email          = db.Column(db.String(120), unique=True, nullable=False)
     senha          = db.Column(db.String(128), nullable=False)
     tipo           = db.Column(db.String(20), nullable=False, default='visualizador')
     active         = db.Column(db.Boolean, default=True)
-    # remova ou comente este campo, se existir:
-    # obra_id = db.Column(db.Integer, db.ForeignKey('obra.id'))
+    # adicione estas duas colunas para linkar ao departamento e à obra:
+    department_id  = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
+    obra_id        = db.Column(db.Integer, db.ForeignKey('obra.id'), nullable=False)

     @property
     def is_active(self):
         return self.active

 class Gasto(db.Model):
     __tablename__ = 'gasto'
     id        = db.Column(db.Integer, primary_key=True)
     tipo_nota = db.Column(db.String(200), nullable=False)
     valor     = db.Column(db.Float, nullable=False)
     data_nota = db.Column(db.Date, nullable=False)
     descricao = db.Column(db.Text, nullable=True)
     aprovador = db.Column(db.String(100), nullable=False)
     obra_id   = db.Column(db.Integer, db.ForeignKey('obra.id'), nullable=False)
