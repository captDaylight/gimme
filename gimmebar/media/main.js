$(document).ready(function(){
	var handle = 'captdaylight';
	var col = 'architecture';
	
	getGimme(handle, col)
	
	
	function getGimme(gimme_handle, collection){
		$.getJSON('https://gimmebar.com/api/v0/public/assets/' + gimme_handle + '/' + collection, 
			function(data){
  				//Loop through all the returned results
  				if (data.length != 0){
  					console.log(data);
  				}
			}
		);
	}
});