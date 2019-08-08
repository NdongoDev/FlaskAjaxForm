import datetime
import os
import traceback
from flask import Flask, jsonify, render_template,request, url_for, Response
from flask_sqlalchemy import SQLAlchemy 
import json
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.secret_key = "flash message"
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres19@localhost/db_apprenant'
db = SQLAlchemy(app)

class MyForm(FlaskForm):
	matricule = StringField('Etudiant', validators=[DataRequired(),
	Length(max=40)],render_kw={"placeholder": "Matricule"})

class Etudiant(db.Model):
    __tablename__ = 'etudiant'
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(100), unique=True, nullable = False)
    prenom = db.Column(db.String(200),nullable = False)
    nom = db.Column(db.String(200),nullable = False)
    email = db.Column(db.String(200),nullable = False)
    date_naiss = db.Column(db.Date)
    adresse = db.Column(db.String(200),nullable = False)
    def __repr__(self):
	        return '{} - {}'.format(self.matricule, self.prenom)
    def as_dict(self):
		    return {'matricule': self.matricule}
####################### table filiere###############################
class Filiere(db.Model):
    __tablename__ = 'filiere'
    id= db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(200))
    def __init__(self,libelle):
        self.libelle =libelle
    def __repr__(self):
        return '<filiere %r>'% self.libelle 
####################### table classe################################       
class Classe(db.Model):
    __tablename__ = 'classe'
    id= db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(200))
    montant_ins = db.Column(db.String(200))
    mensualite = db.Column(db.String(200))
    filiere_id=db.Column(db.Integer, db.ForeignKey('filiere.id'))
    def __init__(self,libelle,montant_ins, mensualite,filiere_id):
        self.libelle = libelle
        self.montant_ins = montant_ins
        self.mensualite =  mensualite
        self.filiere_id =  filiere_id
    def __repr__(self):
        return '<classe %r>'% self.libelle  
#######################table inscription###########################       
class Inscription(db.Model):
    __tablename__ = 'inscription'
    id= db.Column(db.Integer, primary_key=True)
    annee_accad = db.Column(db.String(200))
    date_ins = db.Column(db.Date)
    classe_id=db.Column(db.Integer, db.ForeignKey('classe.id'))
    etudiant_id=db.Column(db.Integer, db.ForeignKey('etudiant.id')) 
    def __init__(self, annee_accad, date_ins, classe_id, etudiant_id):
        self.annee_accad = annee_accad
        self.date_ins = date_ins
        self.classe_id =  classe_id
        self.etudiant_id = etudiant_id
    def __repr__(self):
        return '<inscription %r>'% self.annee_accad 

@app.route('/')
def index():
    form = MyForm()
    return render_template('inscription.html', form=form)

@app.route('/etudiants')
def etudiantdic():
    res = Etudiant.query.all()
    list_etudiants =  [r.as_dict() for r in res]
    return jsonify(list_etudiants)

@app.route('/process', methods = ['POST'])
def process():
    matricule = request.form['matricule']
    if matricule:
        return jsonify({'matricule':matricule})
    return jsonify({'error': 'missing data...'})


if __name__ == "__main__":
    app.run(debug=True)
