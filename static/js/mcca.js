$(document).ready(function() {
$('#frmcca').validate({
	rules: {			
		'nombremmca': {required: true,},
		'fechaini': {required: true,},
		'fechafin': {required: true,},
     	},
	messages: {
		'nombremmca': {required: "Introduzca el nombre del MCCA",},
		'fechaini': {required: "Introduzca la fecha inicial",},
		'fechafin': {required: "Introduzca la fecha final",},
	}
});
});
/*************************************************************************************************************/
validaletra('id_privado');validaletra('id_indicador');validaletra('id_mensaje');validaletra('id_canal');
validaletra('id_acciones');validaletra('id_observacion');validaletra('id_nombremmca');
/*************************************************************************************************************/
tablas = Array(7);
tablas[0]='#tabla_estado';
tablas[1]='#tabla_privado';
tablas[2]='#tabla_indicador';
tablas[3]='#tabla_mensaje';
tablas[4]='#tabla_canal';
tablas[5]='#tabla_accion';
tablas[6]='#tabla_observacion';
function sectores_estado(){
var organismo=$('#id_organismo');var norganismo=$("#id_organismo option:selected").text();
var dependencia=$('#id_dependencia');var ndependencia=$("#id_dependencia option:selected").text();
var tabla= $(tablas[0]).find("tbody");var n= tabla.find("tr").length;var ok=true;
if ($.trim(organismo.val())==''){
alert("Seleccione el organismo");organismo.focus();return false;
}else if ($.trim(dependencia.val())==''){
alert("Seleccione el dependencia");dependencia.focus();return false;
}
$.each(tabla.find("tr"),function(){
var idorg =$(this).find("td:eq(1) input:hidden").val();
var iddep =$(this).find("td:eq(2) input:hidden").val();    
	if (organismo.val()==idorg & dependencia.val()==iddep){
	ok=false;return false;
	}
});
if(ok==true){
n+=1;
fila="<tr class='fila"+n+"'><td>"+n+"</td><td><input type='hidden' name='corg' value='"+organismo.val()+"'>"+norganismo+"</td><td><input type='hidden' name='cdep' value='"+dependencia.val()+"'>"+ndependencia+"</td><td> <a class='close' href='javascript: removedetalle(0,"+n+")'>&times;</a></td></tr>"
tabla.append(fila);}else{alert('El sector ya ha sido agregado. Escoja otro porfavor!');return false;}
}
function sectores_privado(){
var privado=$('#id_privado');
var tabla= $(tablas[1]).find("tbody");var n= tabla.find("tr").length;var ok=true;
if ($.trim(privado.val())==''){
alert("Escriba el nombre del Sector");privado.focus();return false;
}
$.each(tabla.find("tr"),function(){   
	if ($(this).find("td:eq(1) input:hidden").val()==privado.val()){
	ok=false;return false;
	}
});
if(ok==true){
n+=1;
fila="<tr class='fila"+n+"'><td>"+n+"</td><td><input type='hidden' name='cpri' value='"+privado.val()+"'>"+privado.val()+"</td><td> <a class='close' href='javascript: removedetalle(1,"+n+")'>&times;</a></td></tr>"
tabla.append(fila);}else{alert('El sector ya ha sido agregado. Ingrese otro porfavor!');privado.select();privado.focus();return false;}
privado.val('');privado.focus();
}

function indicadores(){
var privado=$('#id_indicador');
var tabla= $(tablas[2]).find("tbody");var n= tabla.find("tr").length;var ok=true;
if ($.trim(privado.val())==''){
alert("Escriba el nombre del Indicador");privado.focus();return false;
}
$.each(tabla.find("tr"),function(){   
	if ($(this).find("td:eq(1) input:hidden").val()==privado.val()){
	ok=false;return false;
	}
});
if(ok==true){
n+=1;
fila="<tr class='fila"+n+"'><td>"+n+"</td><td><input type='hidden' name='cind' value='"+privado.val()+"'>"+privado.val()+"</td><td> <a class='close' href='javascript: removedetalle(2,"+n+")'>&times;</a></td></tr>"
tabla.append(fila);}else{alert('El indicador ya ha sido agregado. Ingrese otro porfavor!');privado.select();privado.focus();return false;}
privado.val('');privado.focus();
}

function mensajes(){
var privado=$('#id_mensaje');
var tabla= $(tablas[3]).find("tbody");var n= tabla.find("tr").length;var ok=true;
if ($.trim(privado.val())==''){
alert("Escriba el nombre del Mensaje");privado.focus();return false;
}
$.each(tabla.find("tr"),function(){   
	if ($(this).find("td:eq(1) input:hidden").val()==privado.val()){
	ok=false;return false;
	}
});
if(ok==true){
n+=1;
fila="<tr class='fila"+n+"'><td>"+n+"</td><td><input type='hidden' name='cmen' value='"+privado.val()+"'>"+privado.val()+"</td><td> <a class='close' href='javascript: removedetalle(3,"+n+")'>&times;</a></td></tr>"
tabla.append(fila);}else{alert('El mensaje ya ha sido agregado. Ingrese otro porfavor!');privado.select();privado.focus();return false;}
privado.val('');privado.focus();
}

function canales(){
var tipo=$('#id_tipommca');var canal=$('#id_canal');var ttipo=$("#id_tipommca option:selected").text();
var tabla= $(tablas[4]).find("tbody");var n= tabla.find("tr").length;var ok=true;
if ($.trim(tipo.val())==''){
alert("Seleccione el tipo de Canal");tipo.focus();return false;
}else if ($.trim(canal.val())==''){
alert("Escriba el nombre del Canal");canal.focus();return false;
}
$.each(tabla.find("tr"),function(){   
	if ($(this).find("td:eq(1) input:hidden").val()==tipo.val() & $(this).find("td:eq(2) input:hidden").val()==canal.val()){
	ok=false;return false;
	}
});
if(ok==true){
n+=1;
fila="<tr class='fila"+n+"'><td>"+n+"</td><td><input type='hidden' name='ctipo' value='"+tipo.val()+"'>"+ttipo+"</td><td><input type='hidden' name='ccan' value='"+canal.val()+"'>"+canal.val()+"</td><td> <a class='close' href='javascript: removedetalle(4,"+n+")'>&times;</a></td></tr>"
tabla.append(fila);}else{alert('El Canal ya ha sido agregado. Ingrese otro porfavor!');canal.select();canal.focus();return false;}
tipo.val('');tipo.focus();canal.val('');
}

function accion(){
var fini=$('#id_fechaini_acc');var ffin=$('#id_fechafin_acc');var accion=$('#id_acciones');
var tabla= $(tablas[5]).find("tbody");var n= tabla.find("tr").length;var ok=true;
if ($.trim(fini.val())==''){
alert("Seleccione la Fecha Inicial");fini.focus();return false;
}else if ($.trim(ffin.val())==''){
alert("Seleccione la Fecha Inicial");ffin.focus();return false;
}else if ($.trim(accion.val())==''){
alert("Escriba las acciones tomadas.");accion.focus();return false;
}
$.each(tabla.find("tr"),function(){   
	if ($(this).find("td:eq(1) input:hidden").val()==accion.val() & $(this).find("td:eq(2) input:hidden").val()==fini.val() & $(this).find("td:eq(3) input:hidden").val()==ffin.val()){
	ok=false;return false;
	}
});
if(ok==true){
n+=1;
fila="<tr class='fila"+n+"'><td>"+n+"</td><td><input type='hidden' name='cacc' value='"+accion.val()+"'>"+accion.val()+"</td><td><input type='hidden' name='caccfini' value='"+fini.val()+"'>"+fini.val()+"</td><td><input type='hidden' name='caccffin' value='"+ffin.val()+"'>"+ffin.val()+"</td><td> <a class='close' href='javascript: removedetalle(5,"+n+")'>&times;</a></td></tr>"
tabla.append(fila);}else{alert('La accion ya ha sido agregada. Ingrese otro porfavor!');accion.select();accion.focus();return false;}
fini.val('');fini.focus();ffin.val('');accion.val('');
}

function observaciones(){
var privado=$('#id_observacion');
var tabla= $(tablas[6]).find("tbody");var n= tabla.find("tr").length;var ok=true;
if ($.trim(privado.val())==''){
alert("Escriba la Observación OGCS");privado.focus();return false;
}
$.each(tabla.find("tr"),function(){   
	if ($(this).find("td:eq(1) input:hidden").val()==privado.val()){
	ok=false;return false;
	}
});
if(ok==true){
n+=1;
fila="<tr class='fila"+n+"'><td>"+n+"</td><td><input type='hidden' name='cobs' value='"+privado.val()+"'>"+privado.val()+"</td><td> <a class='close' href='javascript: removedetalle(6,"+n+")'>&times;</a></td></tr>"
tabla.append(fila);}else{alert('Esta observación ya ha sido agregada. Ingrese otro porfavor!');privado.select();privado.focus();return false;}
privado.val('');privado.focus();
}

function removedetalle(t,fila){
tabla=tablas[t];
$(tabla+" tr.fila"+fila).remove();
var n=1;
var tdetalle= $(tabla);
/*AUTO REORDENAMIENTO DE ITEMS LUEGO DE ELIMINAR*/
$.each(tdetalle.find("tbody tr"),function(){
    this.cells[0].innerHTML=n;    
    n+=1;
});
}
