

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SelectField, SelectMultipleField, BooleanField, IntegerField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo, Regexp
from wtforms.widgets import PasswordInput


##Form de connexion
class form_signIn(FlaskForm):
    email = StringField('Email ', validators=[DataRequired()])
    motDePasse = StringField('Mot de passe ', widget=PasswordInput(hide_value=True))
    pass

##Form de creation de compte
class form_signUp(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Regexp('[^@]+@[^@]+\.[^@]+',message="Votre email n'est possede pas le bon format")])
    fields = [("locataire", "locataire"),("proprietaire", "proprietaire")]
    typeCompte = SelectField('Type de compte', choices=fields)
    nom = StringField('Nom ', validators=[DataRequired()])
    prenom = StringField('Prenom ', validators=[DataRequired()])
    dateNaissance = DateField(validators=[DataRequired()])
    adresse = StringField('Adresse ', validators=[DataRequired()])
    ville = StringField('Ville', validators=[DataRequired()])
    codePostal = StringField('Code Postal ',validators=[DataRequired()])
    numeroTelephone = StringField('Numero de telephone', validators=[DataRequired(),Length(min=10,max=10,message="le numero de telephone n'est pas valide")])
    motDePasse = StringField('Mot de passe ', widget=PasswordInput(hide_value=True), validators=[DataRequired()])
    confirmationMotDePasse = StringField('Confirmer le mot de passe ', widget=PasswordInput(hide_value=True), validators=[DataRequired(), EqualTo('motDePasse',message="Les mots de passe ne correpondent pas")])
    pass

##Form de changement de mot de passe apres perte
class form_recoverPassword(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Regexp('[^@]+@[^@]+\.[^@]+',message="Votre email n'est possede pas le bon format")])
    pass


##Form de changement du mot de passe utilisateur
class form_utilisateurChangePassword(FlaskForm):
    ancienmdp = StringField('Ancien mot de passe ', widget=PasswordInput(hide_value=True), validators=[DataRequired()])
    nouveaumdp = StringField('Nouveau mot de passe ', widget=PasswordInput(hide_value=True), validators=[DataRequired()])
    confirmermdp = StringField('Confirmer le mot de passe ', widget=PasswordInput(hide_value=True), validators=[DataRequired()])
    pass

##Form de changement des parametre du compte utilisateur
class form_utilisateurChangeElement(FlaskForm): 
    email = StringField('Email', validators=[DataRequired(),Regexp('[^@]+@[^@]+\.[^@]+',message="Votre email n'est possede pas le bon format")])
    nom = StringField('Nom ')
    prenom = StringField('Prenom ')
    adresse = StringField('Adresse ')
    numeroTelephone = StringField('Numero de telephone', validators=[Length(min=10,max=10)])
    pass

class form_nouveauBail(FlaskForm):
    emailLocataire = StringField('Email Locataire', validators=[Regexp('[^@]+@[^@]+\.[^@]+',message="Votre email n'est possede pas le bon format")])
    nomLocataire = StringField('Nom du locataire', validators=[DataRequired()])
    prenomLocataire = StringField('Prenom du locataire', validators=[DataRequired()])
    bien = SelectField('Selection du bien', coerce=int)
    typePaiement = SelectField('Type de paiement du loyer', coerce=int, choices=[(0,'a terme echu'),(1,'avance')])
    prixLoyer = StringField('Prix du loyer hors charges', validators=[DataRequired()])
    jourPaiementLoyer = StringField('Numero du jour de paiment du loyer ', validators=[DataRequired()])
    charges = StringField('Prix charges', validators=[DataRequired()])
    typeCharges = SelectField('Type de charges', coerce=int, choices=[(0,'provision sur charges'),(1,'forfaitaire')])
    chauffageCollectif = BooleanField('Chauffage collectif')
    eauChaudeCollective = BooleanField('Eau chaude collective')
    electricite = BooleanField('Electricite')
    gaz = BooleanField('Gaz')
    internet = BooleanField('Internet')
    poubelles = BooleanField('Poubelles')
    meuble = BooleanField('meublé')
    dureePreavis = StringField('Duree du preavis en mois')
    dureeBail = StringField('Duree du bail en mois')
    DateEntreeLogement = DateField("Date d'entree du logement") ##Generation auto meuble
    premierLoyerEntreeCalcule = BooleanField('Calcul automatique du premier loyer')
    prixLoyerEntree = StringField('Cout du premier Loyer')
    depotDeGarantit = BooleanField('Depot de garantit')
    montantDepotDeGarantit = IntegerField('Montant du depot de garantit')
    nomGarant = StringField('Nom du garant')
    pass

class form_modifierBail(FlaskForm):
    typePaiement = SelectField('Type de paiement du loyer', coerce=int, choices=[(0,'a terme echu'),(1,'avance')])
    prixLoyer = StringField('Prix du loyer hors charges', validators=[DataRequired()])
    jourPaiementLoyer = StringField('Numero du jour de paiment du loyer ', validators=[DataRequired()])
    charges = StringField('Prix charges', validators=[DataRequired()])
    chauffageCollectif = BooleanField('Chauffage collectif')
    eauChaudeCollective = BooleanField('Eau chaude collective')
    electricite = BooleanField('Electricite')
    gaz = BooleanField('Gaz')
    internet = BooleanField('Internet')
    poubelles = BooleanField('Poubelles')
    meuble = BooleanField('meublé')
    depotDeGarantit = BooleanField('Depot de garantit')
    montantDepotDeGarantit = IntegerField('Montant du depot de garantit')
    nomGarant = StringField('Nom du garant')
    pass

class form_nouveauBien(FlaskForm):
    idImmeuble = SelectField("Selectionner l'immeuble", coerce=int)
    adresse = StringField('Adresse')
    ville = StringField('Ville')
    codePostal = StringField('Code Postal')
    superficie = StringField('Superficie')
    nombrePieceHabitable = StringField('Nombre de piece habitable')
    garage = BooleanField('garage')
    cellier = BooleanField('cellier')
    placeParking = BooleanField('place de parking')
    numAppartement = StringField('Numero du bien')
    etage = StringField("Numero d'etage du bien")
    ascenseur = BooleanField("Presence d'un ascenseur")
    interphone = BooleanField("Presence d'un interphone")
    typeBien = SelectField("Selectionner le type de bien",coerce=int, choices=[(0,"appartement"),(1,"maison")])
    description = TextAreaField('Description du bien', validators=[Length(max=150)])
    pass

class form_modifierBien(FlaskForm):
    superficie = StringField("Superficie")
    nombrePieceHabitable = StringField("Nombre de pieces habitables")
    garage = BooleanField('garage')
    cellier = BooleanField('Cellier')
    placeParking = BooleanField('place de parking')

class form_nouveauImmeuble(FlaskForm):
    adresse = StringField("Adresse Immeuble", validators=[DataRequired()])
    ville = StringField("ville", validators=[DataRequired()])
    codePostal = StringField("Code Postal", validators=[DataRequired(), Length(min=5,max=5,message="Le code postal n'est pas correct")])
    nombreEtage = StringField("Nombre d'etage", validators=[DataRequired()])
    pass

class form_modifierImmeuble(FlaskForm):
    adresse = StringField("Adresse")
    ville = StringField("Ville")
    codePostal = StringField("Code Postal")
    nombreEtage = StringField("Nombre d'etage")
    pass

class form_nouveauPaiement(FlaskForm):
    locataire = SelectField('Selection du locataire du bail', coerce=int)
    paiementEffectue = BooleanField()
    quittance = BooleanField("Envoyer quittance automatiquement")
    pass

class form_validerPaiement(FlaskForm):
    genererQuittance =BooleanField('Generer quittance')
    pass


