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
	$.getJSON('/ubigeo/provincia/json/?r='+id, function(data){
	$.each(data, function(key,value){
                if(value.fields.numpro==idpro){
		provincia.append("<option value='"+value.fields.numpro+"' selected='selected'>"+value.fields.provincia+"</option>");select=false;
 		}else{
		provincia.append("<option value='"+value.fields.numpro+"'>"+value.fields.provincia+"</option>");
		}
	});	if(select){provincia.append("<option selected='selected' value=''>TODOS</option>");}else{provincia.append("<option value=''>TODOS</option>");}
	});
}

function dependencias(){
        var id= $("#id_organismo").val();
	var dependencia = $("#id_dependencia");
	dependencia.find('option').remove();
	dependencia.append("<option value=''>---------</option>");
	$.getJSON('/dependencia/dependencias/json/?r='+id, function(data){
	$.each(data, function(key,value){
                if(id==1){		
		dependencia.append("<option value='"+value.fields.nummin+"'>"+value.fields.ministerio+"</option>");}
                if(id==2){		
		dependencia.append("<option value='"+value.fields.numodp+"'>"+value.fields.odp+"</option>");}
                if(id==3){		
		dependencia.append("<option value='"+value.fields.numgob+"'>"+value.fields.gobernacion+"</option>");}		
	});
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
