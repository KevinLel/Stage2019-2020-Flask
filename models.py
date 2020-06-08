#coding:latin-1

from peewee import *
from flask_login import UserMixin

database = SqliteDatabase("./database.sqlite3")

class BaseModel(Model):
    class Meta: database = database



class Utilisateur(BaseModel, UserMixin):
    nom = CharField(null=False)
    prenom = CharField(null=False)
    adresse = CharField(null=False)
    codePostal = CharField(null=False)
    ville = CharField(null=False)  
    numeroTelephone = CharField()
    motDePasse = CharField(null=False)
    email = CharField(null=False)
    dateNaissance = DateField(null=False)
    role = CharField(null=False)
    verifie = BooleanField()

class Immeuble(BaseModel):
    idProprietaire = ForeignKeyField(Utilisateur, null=False)
    adresse = CharField(null=False)
    ville = CharField(null=False)
    codePostal = CharField(null=False)
    nombreEtage = CharField(null=False)
    

class Bien(BaseModel):
    idUtilisateur = ForeignKeyField(Utilisateur, null=False)
    idImmeuble = ForeignKeyField(Immeuble, null=True) ##Un bien n'est pas forcement liee a un immeuble
    adresse = CharField(null=False)
    ville = CharField(null=False)
    codePostal = CharField(null=False)
    superficie = IntegerField(null=False)
    nombrePieceHabitable = IntegerField(null=False)
    garage = BooleanField()
    cellier = BooleanField()
    placeParking = BooleanField()
    numAppartement = IntegerField(null=False)
    etage = CharField(null=False)
    ascenseur = BooleanField()
    interphone = BooleanField()
    typeBien = CharField()
    description = TextField()

class Bail(BaseModel):
    idLocataire = ForeignKeyField(Utilisateur, null=False)
    idProprietaire = ForeignKeyField(Utilisateur, null=False)
    idBien = ForeignKeyField(Bien, null=False)
    prixLoyer = IntegerField(null=False)
    jourPaiementLoyer = CharField(null=False)
    charges = IntegerField(null=False)
    typeCharges = CharField(null=False)
    typePaiement = CharField(null=False)
    dureePreavis = IntegerField(null=False)
    prixLoyerEntree = FloatField(null=False)
    DateEntreeLogement = DateField(null=False)
    nomGarant = CharField(null=True)
    dateCreationBail = DateField(null=False)
    dureeBail = CharField(null=False)
    chauffageCollectif = BooleanField()
    meuble = BooleanField()
    eauChaudeCollective = BooleanField()
    depotDeGarantit = BooleanField()
    montantDepotDeGarantit = IntegerField(null=True)
    electricite = BooleanField()
    gaz = BooleanField()
    internet = BooleanField()
    poubelles = BooleanField()

class Paiement(BaseModel):
    idBail = ForeignKeyField(Bail, null=False)
    datePaiement = DateField(null=False)
    paiementEffectue = BooleanField()
    prixPaiement = CharField(null=False)
    traite = BooleanField()
    quittance = BooleanField()


def create_tables():
    with database:
        database.create_tables([Utilisateur, Bien, Bail, Paiement, Immeuble])

def drop_tables():
    with database:
        database.drop_tables([Utilisateur, Bien, Bail, Paiement, Immeuble])