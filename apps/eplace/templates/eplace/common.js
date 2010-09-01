var common = {
		debug: true,
		getUrl: null,						
		alert: null,
		showLoading: null,
};
common.getUrl = function(url, data, callback){	
	var the_data= 'urlname='+url;
	if (data != null){
		the_data = the_data + '&' + data;
	}
	$.ajax({
	dataType: 'HTML',
	url: '/geturl/',
	type: 'GET', 
	data: the_data,
	success: function(html){
		if (html != "ERROR"){
			if (callback != null){
				callback(html);
			}
		}
	},
	error: function(){
		common.alert("Couldn't get URL");
	}
	});
};
common.alert = function(m){
	$.jGrowl(m);
};
common.showLoading = function(s){
	if (s == true){
		$('div.w-loading').show();
	}else{
		$('div.w-loading').hide();
	}
};
common.sendAjaxRequest = function(type, url, data, success_callback){
	common.showLoading(true);
	$.ajax({
		type: type,
		dataType: "json",
		data: data,
		url: url,
		success: function(json){
			if (json.m == "OK"){
				common.showLoading(false);
				if (success_callback != null){
					success_callback(json);
				}
			}else{
				if (common.debug){
					common.alert(json.m);
				}
				common.showLoading(false);
			}
		},
		error: function(){
			common.showLoading(false);
			if (common.debug){
				common.alert("Couldnt get "+url);
			}
		}
	});
};
