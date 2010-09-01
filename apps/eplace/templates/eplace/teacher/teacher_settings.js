$.tools.dateinput.localize("{{LANGUAGE_CODE}}", {
   months: '{{_("January")}},{{_("February")}},{{_("March")}},{{_("April")}},{{_("May")}},{{_("June")}},{{_("July")}},{{_("August")}},{{_("September")}},{{_("October")}},{{_("November")}},{{_("December")}}',
   shortMonths:  '{{_("Jan")}},{{_("Feb")}},{{_("Mar")}},{{_("Apr")}},{{_("May")}},{{_("Jun")}},{{_("Jul")}},{{_("Aug")}},Sep")}},Oct")}},{{_("Nov")}},{{_("Dec")}}',
   days:         '{{_("Sunday")}},{{_("Monday")}},{{_("Tuesday")}},{{_("Wednesday")}},{{_("Thursday")}},{{_("Friday")}},{{_("Saturday")}}',
   shortDays:    '{{_("Sun")}},{{_("Mon")}},{{_("Tue")}},{{_("Wed")}},{{_("Thu")}},{{_("Fri")}},{{_("Sat")}}'
});
var teacher = {
	urlname: 'eplace_settings_get',
	loadSuccess: false, 
	loadPage: null,
	alert: null,
	showLoading: null,
	container:'div.w-table',
	form:'form#settings-form',
	refresh: null,
	reset: null,
	save: null,
	sendAjaxRequest: null,
};
teacher.sendAjaxRequest = function(type, url, data, success_callback){
	teacher.showLoading(true);
	$.ajax({
		type: type,
		dataType: "json",
		data: data,
		url: url,
		success: function(json){
			if (json.m == "OK"){
				teacher.showLoading(false);
				if (success_callback != null){
					success_callback(json);
				}
			}else{
				teacher.showLoading(false);
			}
		},
		error: function(){
			teacher.showLoading(false);
		}
	});
}
//	teacher.confirm = window.confirm;
teacher.refresh = function(){
};
teacher.save = function(){
	var data = $(teacher.form).serialize();
	var url = $(teacher.form).attr('action');
	teacher.sendAjaxRequest("POST", url, data, function(json){
		teacher.alert('Saved!');
		$(teacher.container).html(json.html);
	});
};
teacher.reset = function(){
	teacher.loadPage();
};
teacher.alert = function(m){
	$.jGrowl(m);
};
teacher.showLoading = function(s){
	if (s == true){
		$('div.w-loading').show();
	}else{
		$('div.w-loading').hide();
	}
};
teacher.loadPage = function(){
		teacher.showLoading(true);
		$.ajax({
		dataType: 'HTML',
		url: '/geturl/',
		type: 'GET', 
		data: 'urlname='+teacher.urlname,
		success: function(html){
			if (html != "ERROR"){
				var the_url = html;
				teacher.sendAjaxRequest("POST",the_url, null, function(json){
					teacher.alert('Page reloaded!');
					$(teacher.container).html(json.html);
				});
			}else{
				teacher.alert("Couldn't get URL");
				teacher.showLoading(false);
			}
		},
		error: function(){
			teacher.alert("Couldn't get URL");
			teacher.showLoading(false);
		}
	});
}
