var timestamp = 0;
var url = null;
var CallInterval = 2000;
var IntervalID = 0;
var prCallback = null;

function callServer(){  
        // alert(url);
	$.get(url, 
            {time: timestamp}, 
            function(payload) {
          //        alert("correcto"); 
                  processResponse(payload);
	    },'json'
	    );
}

function processResponse(payload) {
	if(payload.status == 0) return;
	timestamp = parseFloat(payload.time.replace(',','.'));
         //alert("leyendo...");
	for(message in payload.messages) {
           //     alert(payload.messages[message].text);
		$("#chatwindow").append(payload.messages[message].text);
	}
	var objDiv = document.getElementById("chatwindow");
	objDiv.scrollTop = objDiv.scrollHeight;	
	if(prCallback != null) prCallback(payload);
}

function background_post(){
/*if($("#msg").val() == "") return false;
var men = $("#msg").val();
var token =($("input[name='csrfmiddlewaretoken']").val());
clearInterval(IntervalID);
$.post(url,{time: timestamp,action: "postmsg",message: men,csrfmiddlewaretoken:token},
	function(payload) {                        
		$("#msg").val(""); $("#msg").focus();
		processResponse(payload);
	},'json'
).complete(function() { IntervalID = setInterval(callServer, CallInterval); });                	       	
//return false;*/
}

function InitChatWindow(ChatMessagesUrl, ProcessResponseCallback){
	$("#loading").remove();
	url = ChatMessagesUrl;
	prCallback = ProcessResponseCallback;
	IntervalID = setInterval(callServer, CallInterval);  
	//callServer();
	$("form#chatform").submit(function(){
                //alert( $("#msg").val());
                var ed = tinyMCE.get('msg');                
		if(ed.getContent() == "") return false;
                var men = ed.getContent();
                var token =($("input[name='csrfmiddlewaretoken']").val());
		clearInterval(IntervalID);
		$.post(url,{time: timestamp,action: "postmsg",message: men,csrfmiddlewaretoken:token},
           		function(payload) {                        
				ed.setContent(""); tinyMCE.execCommand('mceFocus',false,'msg');
				processResponse(payload);
			},'json'
       	).complete(function() { IntervalID = setInterval(callServer, CallInterval); });                	       	
        return false;
	});


} 
function HandleRoomDescription(payload) {
	$("#chatroom_description").text(payload.description);
}

function InitChatDescription(){

	$("form#chatroom_description_form").submit(function(){
		// If user clicks to send a message on a empty message box, then don't do anything.
		if($("#id_description").val() == "") return false;
		// We don't want to post a call at the same time as the regular message update call,
		// so cancel that first.
		clearInterval(IntervalID);
		$.post(url,
				{
				time: timestamp,
				action: "change_description",
				description: $("#id_description").val()
           		},
           		function(payload) {
         						$("#id_description").val(""); // clean out contents of input field.
         						// Calls to the server always return the latest messages, so display them.
         						processResponse(payload);
       							},
       			'json'
       	);
       	// Start calling the server again at regular intervals.
       	IntervalID = setInterval(callServer, CallInterval);
		return false;
	});

}
