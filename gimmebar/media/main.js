$(document).ready(function(){
	var handle = 'captdaylight';
	var col = 'architecture';
	
	getGimme(handle, col)
	
	function foo(data){
		console.log("hello");
		//Loop through all the returned results
		if (data.length != 0){
			console.log(data);
		}
	}
	function getGimme(gimme_handle, collection){
/* 		$.getJSON('http://api.twitter.com/1/statuses/user_timeline.json?callback=?&count=200&trim_user=t&screen_name=captdaylight&page=1', */
		$.getJSON('https://gimmebar.com/api/v0/public/assets/funkatron/development.js?jsonp_callback=foo', 
			foo
		);
	}
});

