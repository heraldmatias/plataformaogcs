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

