$(document).ready(function() {

    $('form').on('submit', function(e){	
            $.ajax({
                data : {
                    matricule: $('#matricule').val()
                },
                type : 'POST',
                url : '/insertapp'
            })
            .done(function(data) {
                if (data.error) {
                    $('#result').text(data.error).show();
                }
                else {
                    $('#result').html(data.matricule).show();
                }
            })

            e.preventDefault();
        });
    
var etudiants = [];	
    
function loadEtudiants(){
    $.getJSON('/etudiants', function(data, status, xhr){
        for (var i = 0; i < data.length; i++ ) {
            etudiants.push(data[i].matricule);
        }
    });
}

loadEtudiants();
    
$('#etudiant').autocomplete({
    source: etudiants, 
    });
    
});