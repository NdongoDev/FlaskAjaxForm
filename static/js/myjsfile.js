$( document ).ready(function() {
    $('#filiere').change(function(){ 
       var x = document.getElementById("filiere").value;
       $('#classe').children('option:not(:first)').remove();
       $('#montant_ins').val("");
       $('#mensualite').val("");
       $('#total_ins').val("");
       $.ajax({ 
          type: "GET",
          url: "/filiere&"+x,
       });
    });
 });
 
 $( document ).ready(function() {
    $('#filiere').change(function(){ 
       var x = document.getElementById("filiere").value;
       $.ajax({ 
          type: "GET",
          contentType: 'application/json; charset=utf-8',
          url: "/filiere&"+x,
          success: function(liste_classe){
             $.each(liste_classe,function(index,d){  
                $("#classe").append("<option value="+ d.id +">" + d.libelle + "</option>");
             });
          }
       });
    });
 });
 
 /****************************************ACTION NOUVEAU LISTE DES FILIERES A AFFICHER****************/
 
 
 
  /********************************AJAX CLASSE****************************/
 $( document ).ready(function() {
    $('#classe').change(function(){ 
       var x = document.getElementById("classe").value;
       $('#montant_ins').val("");
       $('#mensualite').val("");
       $('#total_ins').val("");

       $.ajax({ 
          type: "GET",
          url: "/classe&"+x,
       });
    });
 });
 
 $( document ).ready(function() {
    $('#classe').change(function(){ 
       var x = document.getElementById("classe").value;
       $.ajax({ 
          type: "GET",
          contentType: 'application/json; charset=utf-8',
          url: "/classe&"+x,
          success: function(liste_ele_classe){
             $.each(liste_ele_classe,function(index,d){
                $('#montant_ins').val(d.mont_ins);
                $('#mensualite').val(d.mensualite);
                $('#total_ins').val(parseInt(d.mont_ins) + parseInt(d.mensualite));    
             });
          }
       });
    });
 });
 /*********************************************ACTION BOUTON RADIO****************************/
 $(function() {
    var matricule = document.getElementById("mat").value;
    $('#ancien').on('click',function(){
       $('#fil').children('option:not(:first)').remove();
       $('#mat').attr('readonly', false); 
       $('#mat').val(""); 
       vider();
       lire(); 
    }); 
    $('#nouveau').on('click',function(){
 
       $('#mat').attr('readonly', true);
       $('#mat').val(matricule);
       vider();
       ecrire();
 
       $( document ).ready(function() {
          
          $('#filiere').children('option:not(:first)').remove();
          $('#classe').children('option:not(:first)').remove();

          $.ajax({ 
             type: "GET",
             url: "/listfiliere",
          });
       });
    
    $( document ).ready(function() {
          var x = document.getElementById("filiere").value;
          $.ajax({ 
             type: "GET",
             contentType: 'application/json; charset=utf-8',
             url: "/listfiliere",
             success: function(liste_filiere){
                $.each(liste_filiere,function(index,d){
 
                   $("#filiere").append("<option value="+ d.id +">" + d.libelle + "</option>");
                });
             }
          });
       });
           
    });        
 });

 /*************************************************CONTROLE CHAMP*****************************/
 
 
 
 newFunction();
 function newFunction() {
    $('.formulaire')
    .form({
       fields: {
          prenom: 'empty',
          nom: 'empty',
          date_naiss: 'empty',
          adresse: 'empty',
          email: 'empty',
          filiere : 'empty',
          classe : 'empty',
       }
    });
 }
 
 /*********************************************LES FONCTIONS***********************/
 

function convert(str) {
    var date = new Date(str),
        mnth = ("0" + (date.getMonth()+1)).slice(-2),
        day  = ("0" + date.getDate()).slice(-2);
    return [ date.getFullYear(), mnth, day].join("-");
}
 function lire(){
    $('#prenom').attr('readonly', true);
    $('#nom').attr('readonly', true);
    $('#date_naiss').attr('readonly', true);
    $('#adresse').attr('readonly', true);
    $('#email').attr('readonly', true);
 }
 function ecrire(){

    $('#prenom').attr('readonly', false);
    $('#nom').attr('readonly', false);
    $('#date_naiss').attr('readonly', false);
    $('#adresse').attr('readonly', false);
    $('#email').attr('readonly', false);

 }
 function vider(){
       $('#prenom').val("");
       $('#nom').val("");
       $('#date_naiss').val("");
       $('#adresse').val("");
       $('#email').val("");       
       $('#filiere').val("");
       $('#classe').val("");
       $('#montant_ins').val("");
       $('#mensualite').val("");
       $('#total_ins').val(""); 
 }

//recherche matricule
 $("#mat").change(function() {
    var etudiant = document.getElementById("mat").value
 
    fetch('/recherchemat/' + etudiant)
        .then(function(response) {
            response.json()
                
                .then(function(data) {
                    console.log(data)
                    document.getElementById("prenom").value = data['etudiant'][0]['prenom'];
                    document.getElementById("nom").value = data['etudiant'][0]['nom'];
                    document.getElementById("email").value = data['etudiant'][0]['email'];
                    document.getElementById("adresse").value = data['etudiant'][0]['adresse'];
                    document.getElementById("date_naiss").value = convert(data['etudiant'][0]['date_naiss']);
                })
                .catch(function(e) {
                    console.log(e)
                    alert("Le matricule n'existe pas dans la base ")
                    document.getElementById("prenom").value = "";
                    document.getElementById("nom").value = "";
                    document.getElementById("date_naiss").value = "";
                    document.getElementById("email").value = "";
                    document.getElementById("date_naiss").value ="";

                })
        })

});

