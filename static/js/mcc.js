/*************************************************************************************************************/
validaletra('id_actor');
validaletra('id_lider');
validaletra('id_observacion');
validaletra('id_nombremmc');
/*************************************************************************************************************/
tablas = Array(4);
tablas[0]='#tabla_actor';
tablas[1]='#tabla_lider';
tablas[2]='#tabla_observacion';
tablas[3]='#tabla_lugar';

function lugares(){
    var region=$('#id_region');
    var provincia=$("#id_provincia");
    var distrito=$("#id_distrito");
    var lugar=$('#id_lugar');
    var tabla= $(tablas[3]).find("tbody");
    var n= tabla.find("tr").length;
    var ok=true;
    if ($.trim(region.val())==''){
       $('#alert4').show().find('strong').text('Debe elegir la region.');
		region.focus();
        return false;
    }else {
		$('#alert4').hide();
	}
	
	if ($.trim(provincia.val())==''){
        $('#alert4').show().find('strong').text('Debe elegir la provincia.');
		provincia.focus();
        return false;
    }else {
		$('#alert4').hide();
	}

    if ($.trim(distrito.val())==''){
        $('#alert4').show().find('strong').text('Debe elegir la distrito.');
		distrito.focus();
        return false;
    }else {
		$('#alert4').hide();
	}
	/*if ($.trim(lugar.val())==''){
        $('#alert4').show().find('strong').text('Debe ingresar el lugar de acción.')
		lugar.focus();
        return false;
    }else {
		$('#alert4').hide();
	}*/
    $.each(tabla.find("tr"),function(){   
        if ($(this).find("td:eq(1) input:hidden").val()==region.val()
            & $(this).find("td:eq(2) input:hidden").val()==provincia.val()
            & $(this).find("td:eq(3) input:hidden").val()==distrito.val()
            & $(this).find("td:eq(4) input:hidden").val()==lugar.val()){
            ok=false;
            return false;
        }
    });
    if(ok==true){
        n+=1;
        fila="<tr class='"+n+"'><td>"+n+"</td><td><input type='hidden' name='col_reg' value='"+region.val()+"'>"+region.find('option:selected').text()+"</td>" +
            "<td><input type='hidden' name='col_pro' value='"+provincia.val()+"'>"+provincia.find('option:selected').text()+"</td>" +
            "<td><input type='hidden' name='col_dis' value='"+distrito.val()+"'>"+distrito.find('option:selected').text()+"</td>" +
            "<td><input type='hidden' name='col_lug' value='"+lugar.val()+"'>"+lugar.val()+"</td><td> <a href='javascript: removedetalle(3,"+n+")'><div id='delete'></div></a></td></tr>"
        tabla.append(fila);
		$('#alert4').hide();
    }else{
		$('#alert4').show().find('strong').text('El lugar ya ha sido agregado. Ingrese otro porfavor!')
        lugar.select();
        lugar.focus();
        return false;
    }
    region.focus();
    provincia.val('');
    distrito.val('');
    lugar.val('');
}

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
        fila="<tr class='"+n+"'><td>"+n+"</td><td><input type='hidden' name='numtvac' value='"+numtv.val()+"'>"+nnumtv+"</td><td style='display: none;'><input type='hidden' name='listactor' value='"+actor.val()+"'>"+actor.val()+"</td><td><input type='hidden' name='instac' value='"+inst.val()+"'>"+inst.val()+"</td><td> <a href='javascript: removedetalle(0,"+n+")'><div id='delete'></div></a></td></tr>"
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
        fila="<tr class='"+n+"'><td>"+n+"</td><td><input type='hidden' name='numtvli' value='"+numtv.val()+"'>"+nnumtv+"</td><td style='display: none;'><input type='hidden' name='listlider' value='"+lider.val()+"'>"+lider.val()+"</td><td><input type='hidden' name='instli' value='"+inst.val()+"'>"+inst.val()+"</td><td> <a href='javascript: removedetalle(1,"+n+")'><div id='delete'></div></a></td></tr>"
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
        fila="<tr class='"+n+"'><td>"+n+"</td><td><input type='hidden' name='cobs' value='"+privado.val()+"'>"+privado.val()+"</td><td> <a href='javascript: removedetalle(2,"+n+")'><div id='delete'></div></a></td></tr>"
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
					if($.trim($("#id_descripcionmcc").val())=="" ){
						$('#alert').show().find('strong').text('Ingrese una breve descripcion del estado actual del caso de crisis');$("#id_descripcionmcc").focus();
						return false;
					}else{
						$('#alert').hide();
					}	
					/*if($.trim($("#id_propuestamcc").val())=="" ){
							$('#alert4').show().find('strong').text('Debe ingresar una propuesta para el caso de crisis.');$("#id_propuestamcc").focus();
							return false;
					}else{
						$('#alert4').hide();
						
					}*/
					if($(tablas[3]).find("tbody tr").length == 0){
                                                 $('#alert4').show().find('strong').text('Debe agregar los lugares de acción');
                                                 $("#id_region").focus();
                                                 return false;
					}else{
						$('#alert4').hide();
					}
                                        if($(tablas[0]).find("tbody tr").length == 0){
                                                 $('#alert1').show().find('strong').text('Debe agregar las actores involucrados');
                                                 $("#id_actor").focus();
                                                 return false;
					}else{
						$('#alert1').hide();
					}
					return true;
}

function get_provincias(){
        var provincia = $("#id_provincia");
        var region = $("#id_region");
        var id = region.val();
        $.getJSON('/ubigeo/provincia/json/?r='+id, function(data){
            provincia.html("<option value>--ELEGIR--</option>");
            $.each(data, function(key,value){
                provincia.append("<option value='"+value.fields.numpro+"'>"+value.fields.provincia+"</option>");
            });
            get_distritos();
      });
    }

    function get_distritos(){
      var region = $("#id_region");
      var provincia = $("#id_provincia");
      var distrito = $("#id_distrito");
      $.getJSON('/ubigeo/distrito/json/?r='+region.val()+'&p='+provincia.val(), function(data){
        distrito.html("<option value>--ELEGIR--</option>");
        $.each(data, function(key,value){
          distrito.append("<option value='"+value.fields.numdis+"'>"+value.fields.distrito+"</option>");
        });
      });
    }
    $(document).ready(function(){
        get_provincias();
        get_distritos();
    });