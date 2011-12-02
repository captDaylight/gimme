$(document).ready(function(){
	var handle = 'captdaylight';
	var col = 'architecture';
	
	getGimme(handle, col)
	
	function getGimme(gimme_handle, collection){
/* 		$.getJSON('http://api.twitter.com/1/statuses/user_timeline.json?callback=?&count=200&trim_user=t&screen_name=captdaylight&page=1', */
		$.getJSON('https://gimmebar.com/api/v0/public/assets/captdaylight/architecture.js?limit=50&jsonp_callback=?', 
			function(data){
				console.log("hello");
				var ts = Math.round((new Date()).getTime() / 1000);
				var day = 86400;
				var week = 604800;
				//one day is 86400 seconds
				var count = 0;
				base_url = "http://chart.apis.google.com/chart?cht=lc&chd=t:"
				//Loop through all the returned results
				if (data.length != 0){
					$.each(data.records, function(i,item){
						var difference = ts - item.date;
						while (day < difference){
						  count++;
						  difference = difference - day;
						}
						
						
/* 						"http://chart.apis.google.com/chart?cht=lc&chd=t:1,2,1,3,5,3,1,1,4,3,1,1,3,5,3,1,1,0,0,01,2,1,3,5,3,1,1,4,3,1,1,3,5,3,1,1,0,0,0|0,0&chds=0,6&chls=0,1,0&chs=1000x125&chm=b,99ff00,0,1,0" */
						console.log("days: " + count);
						count = 0;
				    });
				}
			}
		);
	}
});

