$(document).ready(function() {
    /*$("#frmcca").validate({
        rules: {			
            'nombremmca': {
                required: true,
            },
            'fechaini': {
                required: true,
            },
            'fechafin': {
                required: true,
            },
        },
        messages: {
            'nombremmca': {
                required: "Introduzca el nombre del MCCA",
            },
            'fechaini': {
                required: "Introduzca la fecha inicial",
            },
            'fechafin': {
                required: "Introduzca la fecha final",
            },
        }
    });*/
});
/*************************************************************************************************************/
validaletra('id_actor');
validaletra('id_lider');
validaletra('id_observacion');
validaletra('id_nombremmc');
/*************************************************************************************************************/
tablas = Array(3);
tablas[0]='#tabla_actor';
tablas[1]='#tabla_lider';
tablas[2]='#tabla_observacion';

function actores(){
    var numtv=$('#id_numtipovarios_ac');
	var nnumtv=$("#id_numtipovarios_ac option:selected").text();
    var actor=$('#id_actor');
    var inst=$('#id_institucion_ac');
    var tabla= $(tablas[0]).find("tbody");
    var n= tabla.find("tr").length;
    var ok=true;
    if ($.trim(numtv.val())==''){
       $('#alert1').show().find('strong').text('Debe elegir el tipo de postura del actor.');
		numtv.focus();
        return false;
    }else {
		$('#alert1').hide();
	}
	
	if ($.trim(actor.val())==''){
        $('#alert1').show().find('strong').text('Debe ingresar el nombre del actor.');
		actor.focus();
        return false;
    }else {
		$('#alert1').hide();
	}
	if ($.trim(inst.val())==''){
        $('#alert1').show().find('strong').text('Debe ingresar la institucion del actor.')
		inst.focus();
        return false;
    }else {
		$('#alert1').hide();
	}
    $.each(tabla.find("tr"),function(){   
        if ($(this).find("td:eq(1) input:hidden").val()==numtv.val() & $(this).find("td:eq(2) input:hidden").val()==actor.val() & $(this).find("td:eq(3) input:hidden").val()==inst.val()){
            ok=false;
            return false;
        }
    });
    if(ok==true){
        n+=1;
        fila="<tr class='"+n+"'><td>"+n+"</td><td><input type='hidden' name='numtvac' value='"+numtv.val()+"'>"+nnumtv+"</td><td><input type='hidden' name='listactor' value='"+actor.val()+"'>"+actor.val()+"</td><td><input type='hidden' name='instac' value='"+inst.val()+"'>"+inst.val()+"</td><td> <a class='close' href='javascript: removedetalle(0,"+n+")'>&times;</a></td></tr>"
        tabla.append(fila);
		$('#alert1').hide();
    }else{
		$('#alert1').show().find('strong').text('El actor ya ha sido agregado. Ingrese otro porfavor!')
        actor.select();
        actor.focus();
        return false;
    }
    numtv.focus();
    inst.val('');
    actor.val('');
}


function lideres(){
    var numtv=$('#id_numtipovarios');
	var nnumtv=$("#id_numtipovarios option:selected").text();
    var lider=$('#id_lider');
    var inst=$('#id_institucion');
    var tabla= $(tablas[1]).find("tbody");
    var n= tabla.find("tr").length;
    var ok=true;
    if ($.trim(numtv.val())==''){
       $('#alert2').show().find('strong').text('Debe elegir el tipo de postura de lider.');
		numtv.focus();
        return false;
    }else {
		$('#alert2').hide();
	}
	
	if ($.trim(lider.val())==''){
        $('#alert2').show().find('strong').text('Debe ingresar el nombre del lider.');
		lider.focus();
        return false;
    }else {
		$('#alert2').hide();
	}
	if ($.trim(inst.val())==''){
        $('#alert2').show().find('strong').text('Debe ingresar la institucion del lider.')
		inst.focus();
        return false;
    }else {
		$('#alert2').hide();
	}
    $.each(tabla.find("tr"),function(){   
        if ($(this).find("td:eq(1) input:hidden").val()==numtv.val() & $(this).find("td:eq(2) input:hidden").val()==lider.val() & $(this).find("td:eq(3) input:hidden").val()==inst.val()){
            ok=false;
            return false;
        }
    });
    if(ok==true){
        n+=1;
        fila="<tr class='"+n+"'><td>"+n+"</td><td><input type='hidden' name='numtvli' value='"+numtv.val()+"'>"+nnumtv+"</td><td><input type='hidden' name='listlider' value='"+lider.val()+"'>"+lider.val()+"</td><td><input type='hidden' name='instli' value='"+inst.val()+"'>"+inst.val()+"</td><td> <a class='close' href='javascript: removedetalle(1,"+n+")'>&times;</a></td></tr>"
        tabla.append(fila);
		$('#alert2').hide();
    }else{
		$('#alert2').show().find('strong').text('El lider ya ha sido agregado. Ingrese otro porfavor!');
        actor.select();
        actor.focus();
        return false;
    }
    numtv.focus();
    inst.val('');
    lider.val('');
}




function observaciones(){
    var privado=$('#id_observacion');
    var tabla= $(tablas[2]).find("tbody");
    var n= tabla.find("tr").length;
    var ok=true;
    if ($.trim(privado.val())==''){
        $('#alert3').show().find('strong').text('Debe ingresar la observacion.');
		$("#id_observacion").focus();
        return false;
    }else{
		$('#alert3').hide();
	}
    $.each(tabla.find("tr"),function(){   
        if ($(this).find("td:eq(1) input:hidden").val()==privado.val()){
            ok=false;
            return false;
        }
    });
    if(ok==true){
        n+=1;
        fila="<tr class='"+n+"'><td>"+n+"</td><td><input type='hidden' name='cobs' value='"+privado.val()+"'>"+privado.val()+"</td><td> <a class='close' href='javascript: removedetalle(2,"+n+")'>&times;</a></td></tr>"
        tabla.append(fila);
		$('#alert3').hide();
    }else{
        $('#alert3').show().find('strong').text('Esta observación ya ha sido agregada. Ingrese otro porfavor!');
        privado.select();
        privado.focus();
        return false;
    }
    privado.val('');
    privado.focus();
}

function removedetalle(t,fila){
    tabla=tablas[t];
    $(tabla+" tr."+fila).remove();
    var n=1;
    var tdetalle= $(tabla);
    /*AUTO REORDENAMIENTO DE ITEMS LUEGO DE ELIMINAR*/
    $.each(tdetalle.find("tbody tr"),function(){
        this.cells[0].innerHTML=n;    
        n+=1;
    });
}



function guardar_mcc(){
					if($.trim($("#id_nombremmc").val())=="" ){
							$('#alert').show().find('strong').text('Debe ingresar el nombre.');$("#id_nombremmc").focus();
							return false;
					}else{
						$('#alert').hide();
						
					}
					if($.trim($("#id_fechaini").val())=="" ){
						$('#alert').show().find('strong').text('Debe elegir fecha inicial');$("#id_fechaini").focus();
						return false;
					}else{
						$('#alert').hide();
						
					}	
					if($.trim($("#id_fechafin").val())=="" ){
						$('#alert').show().find('strong').text('Debe elegir fecha final');$("#id_fechafin").focus();
						return false;
					}else{
						$('#alert').hide();
					}	
					if($.trim($("#id_nummcctipo").val())=="" ){
							$('#alert').show().find('strong').text('Debe elegir un tipo de caso de crisis.');$("#id_nummcctipo").focus();
							return false;
					}else{
						$('#alert').hide();
						
					}
					if($.trim($("#id_nummccestado").val())=="" ){
						$('#alert').show().find('strong').text('Debe elegir un estado');$("#id_nummccestado").focus();
						return false;
					}else{
						$('#alert').hide();
						
					}	
					if($.trim($("#id_region").val())=="" ){
						$('#alert').show().find('strong').text('Debe elegir una region');$("#id_region").focus();
						return false;
					}else{
						$('#alert').hide();
					}	
					if($.trim($("#id_provincia").val())=="" ){
							$('#alert').show().find('strong').text('Debe elegir una provincia.');$("#id_provincia").focus();
							return false;
					}else{
						$('#alert').hide();
						
					}
					if($.trim($("#id_lugar").val())=="" ){
						$('#alert').show().find('strong').text('Debe ingresar un lugar');$("#id_lugar").focus();
						return false;
					}else{
						$('#alert').hide();
						
					}	
					if($.trim($("#id_descripcionmcc").val())=="" ){
						$('#alert').show().find('strong').text('Ingrese una breve descripcion del estado actual del caso de crisis');$("#id_descripcionmcc").focus();
						return false;
					}else{
						$('#alert').hide();
					}	
					if($.trim($("#id_propuestamcc").val())=="" ){
							$('#alert4').show().find('strong').text('Debe ingresar una propuesta para el caso de crisis.');$("#id_propuestamcc").focus();
							return false;
					}else{
						$('#alert4').hide();
						
					}
					
					return true;
}