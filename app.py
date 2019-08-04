import datetime
import os
import traceback
import psycopg2
import psycopg2.extras
from flask import (Flask, flash, g, redirect, render_template, request,
                   session, url_for)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "flash message"
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres19@localhost/db_apprenant'
db = SQLAlchemy(app)
class Etudiant(db.Model):
    __tablename__ = 'etudiant'
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(100), unique=True, nullable = False)
    prenom = db.Column(db.String(200),nullable = False)
    nom = db.Column(db.String(200),nullable = False)
    email = db.Column(db.String(200),nullable = False)
    date_naiss = db.Column(db.Date)
    adresse = db.Column(db.String(200),nullable = False)
    def __init__(self,matricule,prenom,nom,email,date_naiss,adresse):
        self.matricule =  matricule
        self.prenom = prenom
        self.nom = nom
        self.email = email
        self.date_naiss = date_naiss
        self.adresse = adresse
    def __repr__(self):
        return '<etudiant %r>'  
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
    return render_template('inscription.html')
@app.route("/insertapp", methods=["POST"])
def insertapp():
    etudiants = Etudiant(request.form['matricule'], request.form['first_name'], request.form['last_name'], request.form['email'], request.form['date_naiss'], request.form['adresse'])
    db.session.add(etudiants)
    db.session.commit()

    filieres  =  Filiere(request.form['libelle'])
    db.session.add(filieres)
    db.session.commit()

    classes = Classe(request.form[libelle], request.form['montant'], request.fom['mensualite'], request.form['id_filiere'])
    db.session.add(classes)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
