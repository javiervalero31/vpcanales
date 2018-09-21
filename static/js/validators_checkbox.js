

$('#checkAll').click(function () {

        if ($("#actividades").val() != "baja") {
          $('input:checkbox:not("#o2,#o3,#o4")').not(this).prop('checked', this.checked);
        }
        else{
          $('input:checkbox:not("#o1")').not(this).prop('checked', this.checked);
        }
    });




function act_desc_actividad() {


      if ($("#actividades").val() != "baja") {
        $("#bruta,#neta,#reactivada").hide();
        $("#cantidad,#nan_baja").show();
      }
      else{
        $("#cantidad,#nan_baja").hide();
        $("#bruta,#neta,#reactivada").show();
      }

      $('input[type=checkbox]').each(function() {
          this.checked = false;
        });


      $("#submit1").prop('disabled', false);


      }





// $('#renta_t,#recarga_t').click(function () {
//   if ($('#renta_t,#recarga_t').is(':checked')){

//    if ($("#actividades").val() != "baja") {
//       if ($('#o1').is(':checked')===false ){
//         $("#o1").prop('checked',true)
//     }
//    }else{
//     if ($('#o4').is(':checked')===false ) {
//       $("#o4").prop('checked',true)
//     }



//    }
//   }
// });


$('#renta_m, #recarga_m').click(function () {
  if ($('#renta_m,#recarga_m').is(':checked')){
    $("#codigoplan").prop('checked',true)

  }else{$("#codigoplan").prop('checked',false)}


  


});
