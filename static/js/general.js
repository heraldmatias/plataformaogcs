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
        var idpro = provincia.val();        
	provincia.find('option').remove();
	provincia.append("<option value=''>---------</option>");
	$.getJSON('/ubigeo/provincia/json/?r='+id, function(data){
	$.each(data, function(key,value){
                if(value.fields.numpro==idpro){
		provincia.append("<option value='"+value.fields.numpro+"' selected='selected'>"+value.fields.provincia+"</option>");
 		}else{
		provincia.append("<option value='"+value.fields.numpro+"'>"+value.fields.provincia+"</option>");
		}
	});
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
