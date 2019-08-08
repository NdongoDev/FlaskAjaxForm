from flask import Flask, jsonify, render_template,flash, request, url_for, Response
from flask_sqlalchemy import SQLAlchemy
import json
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'my_love_dont_try'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres19@localhost/db_apprenant'
db = SQLAlchemy(app)


class MyForm(FlaskForm):
    matricule = StringField('Etudiant', validators=[DataRequired(),
                                                    Length(max=40)], render_kw={"placeholder": "Matricule"})
class Etudiant(db.Model):
    __tablename__ = 'etudiant'

    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(60), unique=True, nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    date_naiss = db.Column(db.Date)
    adresse = db.Column(db.String(200), nullable=False)

    def __init__(self, matricule, prenom, nom, date_naiss, adresse, email):
        self.matricule = matricule
        self.prenom = prenom
        self.nom = nom
        self.date_naiss = date_naiss
        self.adresse = adresse
        self.email = email

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

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        verif_etu = Etudiant.query.all()
        control_etu = False
        control_mat = False
        for i in verif_etu:
            if request.form['matricule'] == i.matricule:
                control_mat=True
                update_id_app=i.id
            if i.email== request.form['email'].strip():
                control_etu=True
                
        if control_mat == True:
            requete_update = Inscription.query.filter_by(id=update_id_app).first()
            requete_update.date_ins=request.form['date_ins']
            requete_update.annee_accad=request.form['annee_accad'].strip()
            requete_update.id_classe=request.form['classe']
            db.session.commit()
            flash("SUCCESS : Modification avec succès!!!")
            return render_template("inscription.html")
        elif control_etu == False:
            etudiants = Etudiant(matricule = request.form['matricule'], prenom = request.form['prenom'], nom = request.form['nom'], email = request.form['email'], adresse = request.form['adresse'], date_naiss = request.form['date_naiss']) 
            db.session.add(etudiants)
            db.session.commit()

            etudiant_id=Etudiant.query.count()+1
            print(etudiant_id)
            
            inscriptions = Inscription(annee_accad = request.form['annee_accad'], date_ins = request.form['date_ins'], classe_id = request.form['classe'], etudiant_id=etudiant_id)
            db.session.add(inscriptions)
            db.session.commit()



            flash("SUCCESS : Apprenant ajouté avec succès!!!")
            return render_template("inscription.html")
        else: 
            flash("WARNING : L'apprenant existe déjà")
            return render_template("inscription.html")
    elif request.method == 'GET':
        return render_template("inscription.html",gen_mat=matricule(),annee_accad=gen_annee_aca(),filieres=filiere_find_all(),date_ins=datetime.date.today())

#generer des matricules
def matricule():
    date_actu=datetime.datetime.today().strftime("%m%Y")    
    matricule = Etudiant.query.count()
    if matricule == None:
        m = 1
        random_mat="SA-00"+str(date_actu)+str(m)
        return random_mat
    else :
        m = matricule+1
        random_mat = "SA-00"+str(date_actu)+str(m)
        return random_mat
#generer année academique
def gen_annee_aca():
    mois=int(datetime.datetime.today().strftime('%m'))
    annee1=0
    annee2=0
    annee_accad=None
    if mois>=8:
        annee1 = int(datetime.datetime.today().strftime('%Y'))
        print(annee1)
        annee2 = annee1+1
        annee_accad = str(annee1)+"/"+str(annee2)
        return annee_accad
    else:
        annee1=int(datetime.datetime.today().strftime('%Y'))
        annee2=annee1-1
        annee_accad=str(annee2)+"/"+str(annee1)
        return annee_accad
#liste filiere
def filiere_find_all():
    result=db.session.query(Filiere).all()
    filieres=[]
    for row in result:
        ma_liste = [row.id, row.libelle]  
        filieres.append(ma_liste)  
    print(filieres)
    return filieres

#liste des filieres
@app.route('/listfiliere', methods = ['GET','POST'])
def liste_filiere():
    liste_fil = Filiere.query.all()
    liste_filiere=[]
    for val in liste_fil:
        mon_dict= { "id":val.id , "libelle":val.libelle}
        liste_filiere.append(mon_dict)
    print(liste_filiere)  
    return jsonify(liste_filiere)
#liste des classes
@app.route('/filiere&<string:fil_id>', methods = ['GET','POST'])
def action_filiere(fil_id):
    print(fil_id)

    classe = Classe.query.filter_by(id=fil_id).all()
    liste_classe=[]
    for val in classe:
        mon_dict= { "id":val.id , "libelle":val.libelle }
        liste_classe.append(mon_dict)
    print(liste_classe)  
    return jsonify(liste_classe)


@app.route('/classe&<string:fil_id>', methods = ['GET','POST'])
def action_classe(fil_id):
    print(fil_id)

    ele_classe = Classe.query.filter_by(id=fil_id).all()
    liste_ele_classe=[]
    for val in ele_classe:
        mon_dict= {"mont_ins":val.montant_ins , "mensualite":val.mensualite }
        liste_ele_classe.append(mon_dict)
    print(liste_ele_classe)    
    return jsonify(liste_ele_classe)

@app.route('/recherchemat/<id_mat>')
def recherchemat(id_mat):
    lister_autre = db.session.query(Etudiant).filter_by(matricule=id_mat)
    tab = []
    print(lister_autre)
    for i in lister_autre:
        
        cl = {"prenom":i.prenom , "nom":i.nom , "email":i.email , "date_naiss":i.date_naiss, "adresse" : i.adresse }
        print(cl)
        tab.append(cl)
       
    return jsonify({'etudiant':tab})


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
