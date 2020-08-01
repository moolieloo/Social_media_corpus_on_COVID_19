function update_page(response) {
	var div = document.getElementById("maintext");
	div.innerHTML = response;
}

function submit_form (arg) {   
	if (arg == true){
		var search = 'keyword'
	}
	else {
		var search = 'category'
	}
	var form = document.getElementById("form");     
	var category = document.getElementById("form1");      
	var formData = new FormData(form);
	var searchParams = new URLSearchParams(formData);
	var queryString = searchParams.toString();
	xmlHttpRqst = new XMLHttpRequest( )
	xmlHttpRqst.onload = function(e) {update_page(xmlHttpRqst.response);} 
	xmlHttpRqst.open( "GET", "/?" + queryString + "&type=" + search);
	xmlHttpRqst.send();

}
