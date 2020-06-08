$(document).ready(function(){
    $("#adresse").prop('disabled', false);
    $("#ville").prop('disabled', false);
    $("#codePostal").prop('disabled', false);

    $('#idImmeuble').change(function(){
        if ($('#idImmeuble option:selected').text() == "Aucun") {
            $("#adresse").prop('disabled', false);
            $("#ville").prop('disabled', false);
            $("#codePostal").prop('disabled', false);
            $('#adresse').val("");
            $('#ville').val("");
            $('#codePostal').val("");
        }
        else{
            $("#adresse").prop('disabled', true);
            $("#ville").prop('disabled', true);
            $("#codePostal").prop('disabled', true);
            jQuery.ajax({
                url : '/_get_immeuble',
                data : {
                    adresse : $('#idImmeuble option:selected').text()
                },
                type : 'POST'
            })
            .done(function(resp){
                $('#adresse').val(resp.adresse);
                $('#ville').val(resp.codePostal);
                $('#codePostal').val(resp.ville);
            });
        }
    })
});