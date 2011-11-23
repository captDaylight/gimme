$(document).ready(function(){
/*
	var handle = 'captdaylight';
	var col = 'architecture';
	
	getGimme(handle, col)
	
	
	function getGimme(gimme_handle, collection){
*/
/* 		$.getJSON('http://api.twitter.com/1/statuses/user_timeline.json?callback=?&count=200&trim_user=t&screen_name=captdaylight&page=1', */
/*
		$.getJSON('https://gimmebar.com/api/v0/public/assets/captaindaylight/architecture&callback=?', 
			function(data){
				console.log("here");
  				//Loop through all the returned results
  				if (data.length != 0){
  					console.log(data);
  				}
			}
		);
	}
*/

var url = 'https://gimmebar.com/api/v0/public/assets/captaindaylight/architecture?&callback=?';
    	$.get(url, function(data) {
        	alert(data)
    	});
});

