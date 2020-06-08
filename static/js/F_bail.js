$(document).ready(function(){
    var today = new Date()
    $("#montantDepotDeGarantit").prop('disabled', true);
    $("#nomGarant").prop('disabled', true);
    dureePreavis = 3
    dureeBail = 36
    $("#dureePreavis").prop('disabled', false);
    $("#dureeBail").prop('disabled', false);
    $('#dureePreavis').val(dureePreavis)
    $('#dureeBail').val(dureeBail)
    /*
        Affectation de la duree du bail et du preavis en fonction du logement meuble ou non
    */
    $('#meuble').change(function(){
        if ($(this).is(":checked")){
            dureePreavis = 1
            dureeBail = 12
            $("#dureePreavis").prop('disabled', true);
            $("#dureeBail").prop('disabled', false);
        }
        else{
            dureePreavis = 3
            dureeBail = 36
            $("#dureePreavis").prop('disabled', false);
            $("#dureeBail").prop('disabled', false);
        }
        $('#dureePreavis').val(dureePreavis)
        $('#dureeBail').val(dureeBail)
    })
    /*
    Calcul automatique du premier loyer
    */
    $('#premierLoyerEntreeCalcule').change(function(){
        if ($(this).is(":checked")){
            var dateEntreeDuLogement = new Date($('#DateEntreeLogement').val())
            var jourPaiementDuLoyer = $('#jourPaiementLoyer').val()
            var prixLoyerHorsCharge = $('#prixLoyer').val()
            var prixLoyerAuJour = (parseInt(prixLoyerHorsCharge) * 12) / 365  
            if (dateEntreeDuLogement.getDate() > parseInt(jourPaiementDuLoyer)){
                var dateProvisoire = dateEntreeDuLogement
                dateProvisoire = new Date()
                dateProvisoire.setDate(jourPaiementDuLoyer)
                dateProvisoire.setYear(dateEntreeDuLogement.getFullYear())
                dateProvisoire.setMonth(dateEntreeDuLogement.getMonth() + 1)
                var differenceJour = (dateProvisoire.getTime() - dateEntreeDuLogement.getTime()) / (1000 * 3600 * 24)
                console.log(differenceJour)
                var prixLoyer = differenceJour * prixLoyerAuJour
                $("#prixLoyerEntree").val(parseInt(prixLoyer))
            }
            else{
                var differenceJour = jourPaiementDuLoyer - dateEntreeDuLogement.getDate()
                var prixLoyer = differenceJour * prixLoyerAuJour
                $("#prixLoyerEntree").val(parseInt(prixLoyer))
            }
            $("#prixLoyerEntree").prop('disabled', false);
        }
        else{
            $("#prixLoyerEntree").prop('disabled', false);
        }
    })
    
    $('#depotDeGarantit').change(function(){
        if ($(this).is(":checked")){
            $("#montantDepotDeGarantit").prop('disabled', false);
            $("#nomGarant").prop('disabled', false);
        }
        else{
            
            $("#montantDepotDeGarantit").prop('disabled', true);
            $("#nomGarant").prop('disabled', true);
        }
    })
})