$(document).ready(function() {
	
				$(".corners_5").corner("5px");
				$(".corners_15").corner("15px");
				$(".corners_20").corner("20px");
				$(".corners_arriba").corner("top");
				$(".corners_arriba_15").corner("top 15px");
				$(".corners_derecha").corner("right");
				$(".corners_derecha_15").corner("right");
				$(".corners_izquierda").corner("left");
				$(".corners_abajo").corner("bottom 10px");
				$(".corners_abajo_15").corner("bottom 15px");				
				$(".corners_abajo_tr").corner("tr bottom 5px");
				$(".corners_abajo_tl").corner("tl bottom 10px");
				
				
				var fechaActual = new Date();
				dia = fechaActual.getDate();
				mes = fechaActual.getMonth() +1;
				anno = fechaActual.getFullYear();
			   
			 
				if (dia <10) dia = "0" + dia;
				if (mes <10) mes = "0" + mes;  
			 
				fechaHoy = dia + "/" + mes + "/" + anno;
				//$(".fecha").html(""+fechaHoy)
				

				
});

function agregar_estado(){
					if($("#id_organismo").val()=="" || $("#id_organismo").val()==null){
						$('#alert1').show().find('strong').text('Debe elegir organismo.');
						return;
					}else{
						$('#alert1').hide();
						
					}	
					if($("#id_dependencia").val()=="" || $("#id_dependencia").val()==null){
							$('#alert1').show().find('strong').text('Debe elegir dependencia.')
							return;
					}else{
						$('#alert1').hide();
						
					}
					location.href="/comunicacion/mcca/add/?tipo=add&id_org="+$("#id_organismo").val()+"&id_dep="+$("#id_dependencia").val()
}

function Eliminar_estado(data){
				
					location.href="/comunicacion/mcca/add/?tipo=delete&id_org="+data
}


function agregar_privado(){
					if($("#id_privado").val()==""){
						$('#alert2').show().find('strong').text('Debe ingresar el sector privado.');
						return;
					}else{
						$('#alert2').hide();
						
					}	
					location.href="/comunicacion/mcca/add/?tipo=add&privado="+$("#id_privado").val()
}

function Eliminar_privado(data){
				
					location.href="/comunicacion/mcca/add/?tipo=delete&privado="+data
}


function agregar_indicador(){
					if($("#id_indicador").val()==""){
						$('#alert3').show().find('strong').text('Debe ingresar el indicador.');
						return;
					}else{
						$('#alert3').hide();
						
					}	
					location.href="/comunicacion/mcca/add/?tipo=add&indicador="+$("#id_indicador").val()
}

function Eliminar_indicador(data){
				
					location.href="/comunicacion/mcca/add/?tipo=delete&indicador="+data
}


function agregar_mensaje(){
					if($("#id_mensaje").val()==""){
						$('#alert4').show().find('strong').text('Debe ingresar el mensaje.');
						return;
					}else{
						$('#alert4').hide();
						
					}	
					location.href="/comunicacion/mcca/add/?tipo=add&mensaje="+$("#id_mensaje").val()
}

function Eliminar_mensaje(data){
				
					location.href="/comunicacion/mcca/add/?tipo=delete&mensaje="+data
}


function agregar_canal(){
					if($("#id_tipommca").val()=="" || $("#id_tipommca").val()==null){
						$('#alert5').show().find('strong').text('Debe elegir el tipo de canal de comunicacion');
						return;
					}else{
						$('#alert5').hide();
						
					}	
					if($("#id_canal").val()=="" ){
							$('#alert5').show().find('strong').text('Debe ingresar el canal de comunicacion.')
							return;
					}else{
						$('#alert5').hide();
						
					}
					location.href="/comunicacion/mcca/add/?tipo=add&tipocc="+$("#id_tipommca").val()+"&canal="+$("#id_canal").val()
}

function Eliminar_canal(data){
				
					location.href="/comunicacion/mcca/add/?tipo=delete&canal="+data
}


function agregar_accion(){
					if($("#id_fechaini_acc").val()=="" ){
						$('#alert6').show().find('strong').text('Debe elegir fecha inicial');
						return;
					}else{
						$('#alert6').hide();
						
					}	
					if($("#id_fechafin_acc").val()=="" ){
						$('#alert6').show().find('strong').text('Debe elegir fecha final');
						return;
					}else{
						$('#alert6').hide();
						
					}	
					
					if($("#id_acciones").val()=="" ){
							$('#alert6').show().find('strong').text('Debe ingresar la accion.')
							return;
					}else{
						$('#alert6').hide();
						
					}
					location.href="/comunicacion/mcca/add/?tipo=add&ini="+$("#id_fechaini_acc").val()+"&fin="+$("#id_fechafin_acc").val()+"&accion="+$("#id_acciones").val()
}

function Eliminar_accion(data){
				
					location.href="/comunicacion/mcca/add/?tipo=delete&accion="+data
}



function agregar_observacion(){
					if($("#id_observacion").val()==""){
						$('#alert7').show().find('strong').text('Debe ingresar la observacion.');
						return;
					}else{
						$('#alert7').hide();
						
					}	
					location.href="/comunicacion/mcca/add/?tipo=add&obs="+$("#id_observacion").val()
}

function Eliminar_observacion(data){
				
					location.href="/comunicacion/mcca/add/?tipo=delete&obs="+data
}






function agregar_actor(){
					if($("#id_numtipovarios_ac").val()=="" ){
						$('#alert1').show().find('strong').text('Debe elegir el tipo de postura.');
						return;
					}else{
						$('#alert1').hide();
						
					}	
					if($("#id_actor").val()=="" ){
						$('#alert1').show().find('strong').text('Debe ingresar el nombre del lider.');
						return;
					}else{
						$('#alert1').hide();
						
					}	
					
					if($("#id_institucion_ac").val()=="" ){
							$('#alert1').show().find('strong').text('Debe ingresar la institucion del actor.')
							return;
					}else{
						$('#alert1').hide();
						
					}
					location.href="/comunicacion/mcc/add/?tipo=add&varios="+$("#id_numtipovarios_ac").val()+"&actor="+$("#id_actor").val()+"&inst="+$("#id_institucion_ac").val()
}

function Eliminar_actor(data){
				
					location.href="/comunicacion/mcc/add/?tipo=delete&actor="+data
}


function agregar_lider(){
					if($("#id_numtipovarios").val()=="" ){
						$('#alert2').show().find('strong').text('Debe elegir el tipo de postura.');
						return;
					}else{
						$('#alert2').hide();
						
					}	
					if($("#id_lider").val()=="" ){
						$('#alert2').show().find('strong').text('Debe ingresar el nombre del lider.');
						return;
					}else{
						$('#alert2').hide();
						
					}	
					
					if($("#id_institucion").val()=="" ){
							$('#alert2').show().find('strong').text('Debe ingresar la institucion del lider.')
							return;
					}else{
						$('#alert2').hide();
						
					}
					location.href="/comunicacion/mcc/add/?tipo=add&varios="+$("#id_numtipovarios").val()+"&lider="+$("#id_lider").val()+"&inst="+$("#id_institucion").val()
}

function Eliminar_lider(data){
				
					location.href="/comunicacion/mcc/add/?tipo=delete&lider="+data
}



function agregar_observacion_mcc(){
					if($("#id_observacion").val()==""){
						$('#alert3').show().find('strong').text('Debe ingresar la observacion.');
						return;
					}else{
						$('#alert3').hide();
						
					}	
					location.href="/comunicacion/mcc/add/?tipo=add&obs="+$("#id_observacion").val()
}

function Eliminar_observacion_mcc(data){
				
					location.href="/comunicacion/mcc/add/?tipo=delete&obs="+data
}