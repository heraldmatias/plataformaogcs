function cerrarformulario(formulario){
var frm=$('#'+formulario);
frm.html(" ");
}
function confirmar(mensaje){
	if (confirm(mensaje))
		return true;
	return false;
}

function provincias(){
        var id= $("#id_region").val();
	var provincia = $("#id_provincia");
        var idpro = provincia.val();var select=true;    
	provincia.find('option').remove();
provincia.append("<option selected='selected' value=''>---------</option>");
	$.getJSON('/ubigeo/provincia/json/?r='+id, function(data){
	$.each(data, function(key,value){
                if(value.fields.numpro==idpro){
		provincia.append("<option value='"+value.fields.numpro+"' selected='selected'>"+value.fields.provincia+"</option>");select=false;
 		}else{
		provincia.append("<option value='"+value.fields.numpro+"'>"+value.fields.provincia+"</option>");
		}
	});//if(select){provincia.append("<option selected='selected' value=''>---------</option>");}else{provincia.append("<option value=''>---------</option>");}
	});
}

function dependencias(){
        var id= $("#id_organismo").val();
	var dependencia = $("#id_dependencia");
        var iddep = $("#id_dep").val();var select=true;
	dependencia.find('option').remove();
dependencia.append("<option selected='selected' value=''>---------</option>");
	$.getJSON('/dependencia/dependencias/json/?r='+id, function(data){
	$.each(data, function(key,value){
                if(id==1){
                   if(value.fields.nummin==iddep){
		      dependencia.append("<option value='"+value.fields.nummin+"' selected='selected'>"+value.fields.ministerio+"</option>");select=false;
                   }else{
                      dependencia.append("<option value='"+value.fields.nummin+"'>"+value.fields.ministerio+"</option>");
                   }
                }
                if(id==2){
                   if(value.fields.numodp==iddep){
                      dependencia.append("<option value='"+value.fields.numodp+"' selected='selected'>"+value.fields.odp+"</option>");select=false;
                   }else{
                      dependencia.append("<option value='"+value.fields.numodp+"'>"+value.fields.odp+"</option>");
                   } 
                }
                if(id==3){
                   if(value.fields.numgob==iddep){
                      dependencia.append("<option value='"+value.fields.numgob+"' selected='selected'>"+value.fields.gobernacion+"</option>");select=false;
                   }else{
                      dependencia.append("<option value='"+value.fields.numgob+"'>"+value.fields.gobernacion+"</option>");
                   } 
                }		
	});
//if(select){dependencia.append("<option selected='selected' value=''>---------</option>");}else{dependencia.append("<option value=''>---------</option>");}
	});
}

function validaletra(campo){
var l='';
 $('#'+campo).keyup(function () {
  this.value = this.value.replace(/[^A-Za-záéíóúÁÉÍÓÚÜü ]/g,'');
  l = this.value.toUpperCase();
  $('#'+campo).val(l);
});
}
function validanumero(campo){
 $('#'+campo).keyup(function () {
  this.value = this.value.replace(/[^0-9]/g,'');
});}
