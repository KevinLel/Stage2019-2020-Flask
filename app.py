#coding:latin-1

from flask import Flask, render_template, request, redirect, flash, url_for, make_response, jsonify
from flask_login import LoginManager,UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from reportlab.pdfgen import canvas
from pbkdf2 import PBKDF2, crypt
from pprint import pprint 
from forms import *
from models import *
from datetime import date
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import bcrypt
import os
import string
import random
from config import Config
import pdfkit


#region init

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'kazeefazhefja'
#Captcha keys
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeHpOwUAAAAABwVDcL_zxNLTnsbt8VuBRJUNkpm'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeHpOwUAAAAANmo68CGmpqvirvA1DcRQD-EGkWc'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
#Initialisation du systeme de login flask
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(Config)

mail=Mail(app)

salt = b'$2b$12$AadPleeqS.6EaiUcDn8vte'

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.get(id=user_id)

#endregion

@app.route('/')
def home():
    return render_template('home.html')



#region logs
@app.route('/signIn', methods=['GET', 'POST', ])
def signIn():
    print("OMAO")
    form = form_signIn()
    if form.validate_on_submit():
        print('OOF')
        email = form.email.data
        motDePasse = form.motDePasse.data.encode('utf-8')
        motDePasse = bcrypt.hashpw(motDePasse, salt)
        utilisateur = Utilisateur.select().where((Utilisateur.email == email) & (Utilisateur.motDePasse == motDePasse)).first()
        print(utilisateur)
        if(utilisateur == None):
            flash("L'email ou le mot de passe ne correspond pas")
        else:
            if utilisateur.verifie == True:
                login_user(utilisateur)
                current_user.id = utilisateur.id
                logInLoader()
                if(utilisateur.role == "locataire"): #Aller sur le page de dediee en fonction du type d'utilisateur
                    return redirect(url_for('accueilLocataire'))
                else:
                    return redirect(url_for('accueilProprietaire'))
            else:
                flash("Votre compte n'a pas encore été validé, verifiez vos emails")
    return render_template('sign_in.html', form=form)

@app.route('/recoverPassword', methods=['GET', 'POST', ])
def recoverPassword():
    form = form_recoverPassword()
    if form.validate_on_submit():
        utilisateur = Utilisateur.select().where(Utilisateur.email == form.email.data).first()
        if utilisateur != None:   
            email = form.email.data
            letters = string.ascii_lowercase
            nouveaumotDePasse = ''.join(random.choice(letters) for i in range(10)) ####Generation d'un mot de passse aleatoire avec les caractere ascii
            utilisateur.motDePasse = bcrypt.hashpw(nouveaumotDePasse.encode('utf-8'), salt)
            utilisateur.save()
            msg = Message('Changement de mot de passe', recipients=['kevin.leleu.pro@gmail.com'])
            msg.html = "<p> Cette email a ete envoye automatiquement par Homeo</p><p>-----------</p><p>Merci d'utiliser le service Homeo</p><p>Bonjour %s </p><p>Vous perdu votre mot de passe, en voici un temporaire : %s que vous pouvez changer en allant directement sur https://homeo.com </p><p> Merci de votre confiance et a bientôt sur Homeo</p>" % (utilisateur.prenom, nouveaumotDePasse)
            try:
                mail.send(msg)
            except Error:
                flash("Une erreur est survenu pendant l'envoi du mail, verifiez votre connexion Internet et reessayez")
            return redirect(url_for('signIn'))  
        else:
            flash("L'email ne correpond pas")
            return redirect(url_for('recoverPassword'))  
    return render_template('recover_password.html', form=form)

@app.route('/signUp', methods=['GET', 'POST', ])
def signUp():
    print("TEST")
    form = form_signUp()
    if form.validate_on_submit():
        print("ENTERED")
        email = form.email.data
        motDePasse = form.motDePasse.data
        motDePasseConfirmation = form.confirmationMotDePasse.data
        utilisateur = Utilisateur.select().where(Utilisateur.email == email)
        print(utilisateur)
        if utilisateur == None:
            nouvelUtilisateur = Utilisateur()
            form.populate_obj(nouvelUtilisateur)
            nouvelUtilisateur.role = form.typeCompte.data
            nouvelUtilisateur.verifie = False
            nouvelUtilisateur.motDePasse = bcrypt.hashpw(form.motDePasse.data.encode('utf-8'), salt)
            nouvelUtilisateur.save()
            ##Envoi d'un mail de confirmation de compte
            token = s.dumps(email, salt='email_confirm')
            msg = Message('Confirmation de compte', recipients=[email])
            msg.html = "<p> Cette email a ete envoye automatiquement par Homeo</p><p>-----------</p><p>Merci d'utiliser le service homeo </p><p>Bonjour, </p><p>Vous venez de créer un compte sur Homeo, cliquez sur le lien suivant pour confirmer votre compte http://leleu.u13.org/confirmationEmail/%s </p><p> Merci de votre confiance et a bientôt sur Homeo</p>" % (token)
            try:
                mail.send(msg)
            except Error:
                flash("Une erreur est survenu pendant l'envoi du mail, verifiez votre connexion Internet et reessayez")
            return redirect(url_for('signIn'))
        else:
            flash("Un compte existe deja pour cette adresse mail")   
    else:
        for fieldname, errorMessage in form.errors.items():
            for err in errorMessage:
                flash(err)
    return render_template('sign_up.html', form=form)

@app.route('/confirmationEmail/<token>', methods=['GET', 'POST', ])
def confirm_email(token):
    try:
        email = s.loads(token, salt='email_confirm', max_age=600)
        utilisateur = Utilisateur.select().where(Utilisateur.email == email).first()
        utilisateur.verifie = True
        utilisateur.save()
        return render_template('verificationCompte.html', utilisateur=utilisateur)
    except SignatureExpired:
        form = form_recoverPassword()
        if form.validate_on_submit():
            email = form.email.data
            token = s.dumps(email, salt='email_confirm')
            msg = Message('Confirmation de compte', recipients=[email])
            msg.html = "<p> Cette email a ete envoye automatiquement par Homeo</p><p>-----------</p><p>Merci d'utiliser le service homeo </p><p>Bonjour, </p><p>Vous venez de créer un compte sur Homeo, cliquez sur le lien suivant pour confirmer votre compte http://leleu.u13.org/confirmationEmail/%s </p><p> Merci de votre confiance et a bientôt sur Homeo</p>" % (token)
            try:
                mail.send(msg)
            except Error:
                flash("Une erreur est survenu pendant l'envoi du mail, verifiez votre connexion Internet et reessayez")
            return redirect(url_for('signIn'))
        return render_template('renvoiToken.html', form=form)
        
#endregion

#region locataire

##Accueil de l'espace locataire
@app.route('/accueilLocataire')
@login_required
def accueilLocataire():
    return render_template('accueilLocataire.html')

#region informations
@app.route('/accueil/infoLocataire')
@login_required
def infoLocataire():
    utilisateur = Utilisateur.select().where(Utilisateur.id == current_user.id).first()
    print(utilisateur.nom)
    return render_template('infoLocataire.html',utilisateur=utilisateur)

@app.route('/accueilLocataire/info/changementMotDePasse', methods=['GET', 'POST', ])
@login_required
def changementMotDePasse():
    form = form_utilisateurChangePassword()
    return render_template()

@app.route('/accueilLocataire/info/suppresionCompte')
@login_required
def suppresionCompte():
    id = current_user.id
    logout_user()

@app.route('/espaceProprietaire/modifierLocataire', methods=['GET', 'POST', ])
@login_required
def modifierLocataire():
    utilisateur = Utilisateur.select().where(Utilisateur.id == current_user.id).first()
    form = form_utilisateurChangeElement(obj=utilisateur)
    if form.validate_on_submit():
        form.populate_obj(utilisateur)
        utilisateur.save()
        return redirect(url_for('infoLocataire'))
    return render_template("modifierLocataire.html", form=form)

@app.route('/espaceProprietaire/modifierMotPasseLocataire', methods=['GET', 'POST', ])
@login_required
def modifierMotPasseLocataire():
    utilisateur = Utilisateur.select().where(Utilisateur.id == current_user.id).first()
    form = form_utilisateurChangePassword()
    if form.validate_on_submit():
        if utilisateur.motDePasse == form.ancienmdp.data:
            utilisateur.motDePasse = bcrypt.hashpw(form.confirmermdp.data.encode('utf-8'), salt)
            utilisateur.save()
        return redirect(url_for('infoLocataire'))
    return render_template("modifierMDPLocataire.html", form=form)

@app.route('/locataire/bail')
@login_required
def bail():
    bail = Bail.select().join_from(Bail, Bien).where(Bail.idLocataire == current_user.id).first()
    return render_template("locataireBail.html", bail=bail)

#Liste les paiements pas encore valide par le proprietaire
@app.route('/locataire/paiements')
@login_required
def paiementLocataire():
    paiements = Paiement.select().join(Bail).where((Paiement.idBail.idLocataire == current_user.id) & (Paiement.paiementEffectue == True))
    nbpaiement = len(paiements)
    return render_template("locatairePaiements.html", paiements=paiements,nbpaiement=nbpaiement)

@app.route('/locataire/retards')
@login_required
def retards():
    retards = Paiement.select().where(Paiement.datePaiement < date.today())
    nbRetards = len(retards)
    return render_template("locataireRetards.html", retards=retards, nbRetards=nbRetards)

##recuperation des informations du proprietaire
@app.route('/locataire/proprietaire')
@login_required
def proprietaire():
    proprietaire = Bail.select().where(Bail.idLocataire == current_user.id).first()
    return render_template("locataireProprietaire.html", proprietaire=proprietaire)
#endregion

#endregion

#region proprietaire

##Accueil de l'espace proprietaire
@app.route('/espaceProprietaire')
@login_required
def accueilProprietaire():
    return render_template('accueilProprietaire.html')

@app.route('/espaceProprietaire/parametres')
@login_required
def parametreProprietaire():
    utilisateur = Utilisateur.select().where(Utilisateur.id == current_user.id).first()
    return render_template('infoProprietaire.html' ,utilisateur=utilisateur)

@app.route('/espaceProprietaire/modifierProprietaire', methods=['GET', 'POST', ])
@login_required
def modifierProprietaire():
    utilisateur = Utilisateur.select().where(Utilisateur.id == current_user.id).first()
    form = form_utilisateurChangeElement(obj=utilisateur)
    if form.validate_on_submit():
        form.populate_obj(utilisateur)
        utilisateur.save()
        return redirect(url_for('parametreProprietaire'))
    return render_template("modifierProprietaire.html", form=form)

@app.route('/espaceProprietaire/modifierMotDePasse', methods=['GET', 'POST', ])
@login_required
def modifierMotPasse():
    utilisateur = Utilisateur.select().where(Utilisateur.id == current_user.id).first()
    form = form_utilisateurChangePassword()
    if form.validate_on_submit():
        if utilisateur.motDePasse == form.ancienmdp.data:
            utilisateur.motDePasse = bcrypt.hashpw(form.confirmermdp.data.encode('utf-8'), salt)
            utilisateur.save()
        return redirect(url_for('parametreProprietaire'))
    return render_template("modifierMDPProprietaire.html", form=form)

#region bail

##Recupere une liste de tout les bails du proprietaire pour pouvoir les visionner et les modifier par la suite
@app.route('/espaceProprietaire/baux')
@login_required
def baux():
    bails = Bail.select(Bail.id, Bien.adresse, Bail.dateCreationBail).join(Bien, on=Bail.idBien.alias('bien')).where(Bail.idProprietaire == current_user.id).order_by(Bail.dateCreationBail.asc())
    nbBail = len(bails)
    return render_template("baux.html", bail=bails, nbBail=nbBail)

@app.route('/espaceProprietaire/baux/nouveauBail', methods=['GET', 'POST', ])
@login_required
def nouveauBail():
    form = form_nouveauBail()
    ##Affichage dans le drop down de biens ne possedant aucun bail
    listeAdresseBienLoue = Bail.select(Bien.adresse).join(Bien, on=Bail.idBien.alias("bien")).where(Bail.idProprietaire == current_user.id) #recuperation de tout les bien deja loue
    listeBien = Bien.select(Bien.id, Bien.adresse, Bien.numAppartement, Bien.etage).where(Bien.idUtilisateur == current_user.id)
    listeBienNonLouee = []
    for lsBien in listeBien:
        founded = False
        for lsBienLouee in listeAdresseBienLoue:
            if lsBien.adresse == lsBienLouee.bien.adresse and lsBien.numAppartement == lsBienLouee.bien.numAppartement:
                founded = True
        if founded == False:
            listeBienNonLouee.append(lsBien) 
    form.bien.choices=[(i.id, "Adresse : %s  -  numero propriete : %s  -  etage : %s" % (i.adresse,i.numAppartement,i.etage)) for i in listeBienNonLouee] #Application du choix dynamique de logement
    if form.validate_on_submit():
        locataire = Utilisateur.select().where(Utilisateur.email == form.emailLocataire.data).first() ##Recherche de l'id du locataire grace a son adresse email qui est unique dans la base de donnees
        if locataire == None:
            locataire = creationUtilisateurGenerique(form.emailLocataire.data, form.nomLocataire.data, form.prenomLocataire.data)
            msg = Message('Creation nouveau compte', recipients=[form.emailLocataire.data])
            msg.html = '<h4>Bienvenu sur homeo</h4><p>Bonjour, vous avez ete inscrit sur la plateforme Homeo vous pouvez vous connecter grâce a votre adresse et le mot de passe suivant : %s </p>' % (locataire.motDePasse, )
            locataireID = locataire.id
            try:
                mail.send(msg)
            except Error:
                flash("Une erreur s'est produit pendant l'envoi du mail, email incorrect") 
        else: 
            locataireID = locataire.id
        calculLoyer = request.form.get('prixLoyerEntree')
        bail = Bail()
        form.populate_obj(bail)
        bail.idLocataire = locataireID
        bail.idProprietaire = current_user.id
        bail.idBien = form.bien.data
        if form.typePaiement.data == 0:
            bail.typePaiement = "a terme echu"
        else:
            bail.typePaiement = "avance"
        if form.typeCharges.data == 0:
            bail.typeCharges = "provision sur charges"
        else:
            bail.typeCharges = "forfaitaire"
        if form.meuble.data == True:
            preavis = 1
        else:
            preavis = 3
        dureeBail = request.form.get('dureeBail')
        bail.dureePreavis = str(preavis)
        bail.dureeBail = dureeBail
        bail.prixLoyerEntree = calculLoyer
        bail.dateCreationBail = date.today()
        bail.save()
        #Creation du premier paiement qui va servir a generer les suivants
        paiement = Paiement()
        paiement.idBail = bail.id
        dateEntree = form.DateEntreeLogement.data
        dateGenere = dateEntree
        if(dateEntree.day < int(form.jourPaiementLoyer.data)):
            dateGenere.replace(day=int(form.jourPaiementLoyer.data))
        else:
            dateGenere.replace(day=int(form.jourPaiementLoyer.data), month=dateEntree.month+1)
        paiement.datePaiement = dateGenere
        paiement.paiementEffectue = False
        paiement.prixPaiement = form.prixLoyerEntree.data
        paiement.quittance = False
        paiement.traite = False
        paiement.save()
        return redirect(url_for('baux'))
    return render_template("nouveauBail.html", form=form)
        
@app.route('/espaceProprietaire/baux/visionner', methods=['GET', 'POST', ])
@login_required
def visionnerBail():
    idBail = request.args.get('idBail') ##Recupere l'id du bail qui doit etre affiche
    bail = Bail.select().where(Bail.id == idBail).first()
    return render_template('visionnerBail.html', bail=bail)

@app.route('/espaceProprietaire/baux/visionner/modifier', methods=['GET', 'POST', ])
@login_required
def modifierBail():
    idBail = request.args.get('idBail') ##Recupere l'id du bail qui doit etre affiche
    bail = Bail.select().where(Bail.id == idBail).first() ##Recuperation du bail pour affecter des valeurs par defaut
    form = form_modifierBail(obj=bail)
    if form.validate_on_submit():
        form.populate_obj(bail)
        bail.save()
        return redirect(url_for('visionnerBail', idBail = bail.id))   
    return render_template('modifierBail.html', form=form)

@app.route('/espaceProprietaire/baux/visionner/supprimer', methods=['GET', 'POST', ])
@login_required
def supprimerBail():
    idBail = request.args.get('linkFlux') ##Recupere l'id du bail qui doit etre affiche
    Bail.delete().where(Bail.id == idBail)

#endregion

#region Bien
@app.route('/espaceProprietaire/biens', methods=['GET', 'POST', ])
@login_required
def biens():
    biens = Bien.select().where(Bien.idUtilisateur == current_user.id)
    nbBien = len(biens)
    return render_template('biens.html',biens=biens, nbBien=nbBien)

@app.route('/espaceProprietaire/biens/nouveauBien', methods=['GET', 'POST', ])
@login_required
def nouveauBien():
    form = form_nouveauBien()
    form.idImmeuble.choices =[(0,"Aucun")]+[(i.id, i.adresse) for i in Immeuble.select().where(Immeuble.idProprietaire == current_user.id)]
    if form.validate_on_submit():
        print(form.idImmeuble.data)
        bien = Bien()
        form.populate_obj(bien)
        if form.idImmeuble.data == 0:
            nvxImmeuble = Immeuble()
            nvxImmeuble.idProprietaire = current_user.id
            nvxImmeuble.adresse = form.adresse.data
            nvxImmeuble.ville = form.ville.data
            nvxImmeuble.codePostal = form.codePostal.data
            nvxImmeuble.nombreEtage = form.etage.data
            nvxImmeuble.save()
            IdImmeuble = Immeuble.select().where((Immeuble.idProprietaire == current_user.id)&(Immeuble.adresse == form.ville.data)&(Immeuble.ville == form.ville.data)&(Immeuble.codePostal == form.codePostal.data)).first()
            idImmeuble = nvxImmeuble.id
            print(idImmeuble)
        else:
            immeuble = Immeuble.select().where(Immeuble.id == form.idImmeuble.data).first()
            bien.adresse = immeuble.adresse
            bien.codePostal = immeuble.codePostal
            bien.ville = immeuble.ville
            idImmeuble = immeuble.id
        bien.idImmeuble = idImmeuble
        bien.idUtilisateur = current_user.id
        bien.save()
        return redirect(url_for('biens'))
    return render_template('nouveauBien.html',form=form)

@app.route('/espaceProprietaire/biens/visionner', methods=['GET', 'POST'])
@login_required
def visionnerBien():
    idBien = request.args.get('idBien')
    bien = Bien.select().where(Bien.id == idBien).first()
    return render_template("visionnerBien.html",bien=bien)

@app.route('/espaceProprietaire/biens/modifier', methods=['GET','POST'])
@login_required
def modifierBien():
    idBien = request.args.get('idBien')
    bien = Bien.select().where(Bien.id == idBien).first()
    form = form_modifierBien(obj=bien)
    if form.validate_on_submit():
        form.populate_obj(bien)
        bien.save()
        return redirect(url_for('visionnerBien'))
    return render_template("modifierBien.html", form=form)
#endregion

#region immeuble
@app.route('/espaceProprietaire/immeubles', methods=['GET', 'POST', ])
@login_required
def immeubles():
    immeubles = Immeuble.select().where(Immeuble.idProprietaire == current_user.id)
    nbImmeuble = len(immeubles)
    return render_template("immeubles.html", immeubles=immeubles, nbImmeuble=nbImmeuble)


@app.route('/espaceProprietaire/immeubles/ajouter', methods=['GET', 'POST', ])
@login_required
def nouveauImmeuble():
    form = form_nouveauImmeuble()
    if form.validate_on_submit():
        immeuble = Immeuble()
        form.populate_obj(immeuble)
        immeuble.idProprietaire = current_user.id
        immeuble.save()
        return redirect(url_for('immeubles'))
    return render_template("nouveauImmeuble.html", form=form)

###PROBLEME DE CHANGER DE PARAMETRE LE DEFAULT N'EST PAS ENCORE PRIS
@app.route('/espaceProprietaire/immeubles/modifier', methods=['GET', 'POST', ])
@login_required
def modifierImmeuble():
    idImmeuble = request.args.get('idImmeuble')#Recuperation de l'id de l'immeuble selectionne
    immeuble = Immeuble.select().where(Immeuble.id == idImmeuble).first()
    form = form_modifierImmeuble(obj=immeuble)
    if form.validate_on_submit():
        form.populate_obj(immeuble)
        immeuble.save()
        return redirect(url_for('immeubles'))
    return render_template("modifierImmeuble.html", form=form, immeuble=immeuble)

@app.route('/espaceProprietaire/immeubles/visionner', methods=['GET', 'POST', ])
@login_required
def visionnerImmeuble():
    idImmeuble = request.args.get('idImmeuble')#Recuperation de l'id de l'immeuble selectionne
    immeuble = Immeuble.select().where(Immeuble.id == idImmeuble).first()
    utilisateur = Utilisateur.select().where(Utilisateur.id == current_user.id).first()
    print(idImmeuble)
    paiements = Paiement.select().join(Bail).join(Bien).where(Bien.idImmeuble == idImmeuble)
    print(paiements)
    nbPaiement = len(paiements)
    print(nbPaiement)
    return render_template("visionnerImmeuble.html", immeuble=immeuble, utilisateur=utilisateur, paiements=paiements, nbPaiement=nbPaiement)

#endregion

#region paiement

@app.route('/espaceProprietaire/paiements', methods=['GET', 'POST', ])
@login_required
def paiements():    
    #paiements = Paiement.select(Paiement.datePaiement, Paiement.idBail.idLocataire, Paiement.id, Paiement.paiementEffectue).join_from(Paiement, Bail).join(Utilisateur, on=Bail.idLocataire.alias('locataire')).where(Bail.idProprietaire == current_user.id)
    paiements = Paiement.select().join(Bail).where((Bail.idProprietaire == current_user.id)&(Paiement.paiementEffectue == False))
    nbPaiement = len(paiements)
    return render_template("paiements.html", paiements=paiements,nbPaiement=nbPaiement)

@app.route('/espaceProprietaire/paiements/validerUnPaiement', methods=['GET', 'POST'])
@login_required
def validationPaiement():
    idPaiement = request.args.get("idPaiement")
    print(idPaiement)
    form = form_validerPaiement()
    paiement = Paiement.select().where(Paiement.id == idPaiement).first()
    print(paiement)
    if form.validate_on_submit():
        paiement.quittance = form.genererQuittance.data
        paiement.paiementEffectue = True
        paiement.save()
        return redirect(url_for('paiements'))
    return render_template('validationPaiement.html', paiement=paiement, form=form)

@app.route('/espaceProprietaire/paiements/validationGenerationQuittance', methods=['GET', 'POST'])
@login_required
def validerGenerationQuittance():
    idPaiement = request.args.get("idPaiement")
    idImmeuble = request.args.get("idImmeuble")
    print(idPaiement)
    form = form_validerPaiement()
    paiement = Paiement.select().where(Paiement.id == idPaiement).first()
    paiement.quittance = True
    paiement.save()
    return redirect(url_for('visionnerImmeuble', idImmeuble=idImmeuble))

@app.route('/espaceProprietaire/genererQuittance', methods=['GET', 'POST'])
@login_required
def genererQuittance():
    idPaiement = request.args.get('idPaiement')
    paiement = Paiement.select().where(Paiement.id == idPaiement).first()
    if paiement.idBail.typePaiement == "a terme echu":
        dateBefore = paiement.datePaiement
        dateAfter = dateBefore
        dateAfter = dateAfter.replace(month=dateAfter.month + 1)
    else:
        dateAfter = paiement.datePaiement
        dateBefore = dateAfter
        dateBefore = dateBefore.replace(month=dateBefore.month + 1)
    #render_template('template_quittance.html',paiement=paiement, numQuittance=nbquittance+1, dateAfter=dateAfter, dateBefore=dateBefore)
    renderedQuittance = render_template('template_quittance.html',paiement=paiement, dateAfter=dateAfter, dateBefore=dateBefore)
    pdf = pdfkit.from_string(renderedQuittance, False)

    response = make_response(pdf)
    response.headers['Content-type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=quittance.pdf'
    return response


@app.route('/espaceProprietaire/retards', methods=['GET', 'POST'])
@login_required
def visionnerRetard():
    retards = Paiement.select().join(Bail).where((Bail.idProprietaire == current_user.id)&(Paiement.datePaiement < date.today())&(Paiement.paiementEffectue == False))
    nbretards = len(retards)
    return render_template("visionnerRetards.html", retards=retards, nbretards=nbretards)
#endregion

#region suppresion

@app.route('/suppresionBien', methods=['GET', 'POST', ])
@login_required
def suppresionBien():
    idBien = request.args.get('idBien')
    paiementlist = Paiement.select().join(Bail).join(Bien).where(Bien.id == idBien)
    for element in paiementlist:
        element.delete_instance()
    baillist = Bail.select().join(Bien).where(Bien.id == idBien)
    for element in baillist:
        element.delete_instance()    
    bien = Bien.select().where(Bien.id == idBien).first()
    bien.delete_instance()
    return redirect(url_for("biens"))

@app.route('/suppresionImmeuble', methods=['GET', 'POST', ])
@login_required
def suppresionImmeuble():
    idImmeuble = request.args.get('idImmeuble')
    paiementlist = Paiement.select().join(Bail).join(Bien).join(Immeuble).where(Immeuble.id == idImmeuble)
    for element in paiementlist:
        element.delete_instance()
    baillist = Bail.select().join(Bien).where(Bien.idImmeuble == idImmeuble)
    for element in baillist:
        element.delete_instance()
    bien = Bien.select().where(Bien.idImmeuble == idImmeuble).first()
    bien.delete_instance()
    immeuble = Immeuble.select().where(Immeuble.id == idImmeuble).first()
    immeuble.delete_instance(True)
    return redirect(url_for("immeubles"))

@app.route('/suppresionBail', methods=['GET', 'POST', ])
@login_required
def suppresionBail():
    idBail = request.args.get('idBail')    
    bail = Bail.select().where(Bail.id == idBail).first()
    bail.delete_instance()
    Paiement.delete().where(Paiement.idBail == idBail).execute()
    return redirect(url_for("baux"))

@app.route('/suppresionCompteLocataire', methods=['GET', 'POST', ])
@login_required
def suppresionLocataire():
    bail = Bail.select().where(Bail.idUtilisateur == current_user.id).first()
    if bail == None:
        userid = current_user.id
        logout_user()
        Utilisateur.delete().where(Utilisateur.id == userid).execute()
        return redirect(url_for('infoLocataire'))
    return redirect(url_for('infoLocataire'))    

@app.route('/suppresionCompteProprietaire', methods=['GET', 'POST', ])
@login_required
def suppresionProprietaire():
    bail = Bail.select().where(Bail.idProprietaire == current_user.id)
    biens = Bien.select().where(Bien.idUtilisateur == current_user.id)
    immeuble = Immeuble.select().where(Immeuble.idProprietaire == current_user.id)
    if bail == None and biens == None and immeuble == None:
        userid = current_user.id 
        Utilisateur.delete().where(Utilisateur.id == userid).execute()
        logout_user()
        return redirect(url_for('home'))  
    return redirect(url_for('parametreProprietaire'))  
#endregion

#endregion

#region functionGenerique

"""Fonction de creation d'un utilisateur generique.

Arguments:
email : email de l'utilisateur a creer
"""
def creationUtilisateurGenerique(email, nom, prenom):
    letters = string.ascii_lowercase
    motDePasse = ''.join(random.choice(letters) for i in range(10)) ####Generation d'un mot de passse aleatoire avec les caractere ascii
    nouvelUtilisateur = Utilisateur()
    nouvelUtilisateur.email = email
    nouvelUtilisateur.nom = nom
    nouvelUtilisateur.prenom = prenom
    nouvelUtilisateur.adresse = "XXX"
    nouvelUtilisateur.codePostal = "XXXXX"
    nouvelUtilisateur.ville = "XXXXXX"
    nouvelUtilisateur.numeroTelephone = "XXXXXXXXXX"
    nouvelUtilisateur.motDePasse = motDePasse
    nouvelUtilisateur.dateNaissance = date.today()
    nouvelUtilisateur.role = "locataire"
    nouvelUtilisateur.verifie = True
    nouvelUtilisateur.save()
    return nouvelUtilisateur

def send():
    msg = Message('Sujet de mon mail', recipients=['kevin.leleu.pro@gmail.com'])
    msg.body = 'Le jolie corps de mon mail'
    msg.html = 'Le corps facon <p>html</p>'
    mail.send(msg)
    return "message envoye"

##Finir le script de génération auto de paiement
def logInLoader():
    paiement = Paiement.select().where((Paiement.traite == False)& (Paiement.datePaiement < date.today()))
    if paiement != None:
        for element in paiement:
            element.traite = True
            nvxpaiement = Paiement()
            nvxpaiement.idBail = element.idBail
            nvxpaiement.prixPaiement = element.idBail.prixLoyer
            nvxdate = Date(element.datePaiement)
            nvxdate.replace(month=int(nvxdate.month) + 1)
            nvxpaiement.datePaiement = nvxdate
            nvxpaiement.traite = False
            nvxpaiement.paiementEffectue = False
            nvxpaiement.quittance = False
            nvxpaiement.save()

@app.route('/_get_immeuble', methods=['POST'])
def _get_immeuble():
    adresse = request.form['adresse']
    immeuble = Immeuble.select().where((Immeuble.adresse == adresse)&(Immeuble.idProprietaire == current_user.id)).first()
    if immeuble:
        return jsonify({
            'adresse' : immeuble.adresse,
            'codePostal' : immeuble.codePostal,
            'ville' : immeuble.ville            
        })
    return jsonify({'erreur' : 'Probleme'})

##Deconnexion de l'utilisateur en cours lorsque le bouton de deconnexion est presse
@app.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    return redirect(url_for('home'))

#endregion

#region cliCommand

@app.cli.command()
def initdb():
    create_tables()

@app.cli.command()
def dropdb():
    drop_tables()

#endregion