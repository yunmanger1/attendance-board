$.tools.dateinput.localize("{{LANGUAGE_CODE}}", {
   months: '{{_("January")}},{{_("February")}},{{_("March")}},{{_("April")}},{{_("May")}},{{_("June")}},{{_("July")}},{{_("August")}},{{_("September")}},{{_("October")}},{{_("November")}},{{_("December")}}',
   shortMonths:  '{{_("Jan")}},{{_("Feb")}},{{_("Mar")}},{{_("Apr")}},{{_("May")}},{{_("Jun")}},{{_("Jul")}},{{_("Aug")}},Sep")}},Oct")}},{{_("Nov")}},{{_("Dec")}}',
   days:         '{{_("Sunday")}},{{_("Monday")}},{{_("Tuesday")}},{{_("Wednesday")}},{{_("Thursday")}},{{_("Friday")}},{{_("Saturday")}}',
   shortDays:    '{{_("Sun")}},{{_("Mon")}},{{_("Tue")}},{{_("Wed")}},{{_("Thu")}},{{_("Fri")}},{{_("Sat")}}'
});
var teacher = {
	lang: 'en',
	debug: true, 
	group: '',
	subject: '',
	urlname: 'eplace_teacher_subject_group',
	url: null, 
	groups: {},
	subjects: {},
	loadSuccess: false, 
	loadPage: null,
	alert: null,
	showLoading: null,
	container:'div.w-table',
	form:'form#tick-form',
	lessonFormContainer: 'div#lesson-day-form',
	genLessonFormContainer: 'div#generate-lesson-day-form',
	refresh: null,
	nextValue: null,
	reset: null,
	save: null,
	clonedInput: null,
	getClonedInput: null,
	id: 0,
	ldApi: null,
	gldApi: null,
	addLD: null,
	genLD:null,
	sendAjaxRequest: null,
	newHtml: null,
	getUrl: null,
	openALDOverlay: null,
	openGLDOverlay: null,
};
teacher.openALDOverlay = function(){
	if (teacher.ldApi != null){
		teacher.ldApi.removeData('overlay');
		$(this).removeData('overlay');
	}
	teacher.ldApi = $(this);
	teacher.ldApi.overlay({
		target: teacher.lessonFormContainer,
		mask: '#ccc',
	});	
	teacher.ldApi.overlay().load();
};
teacher.openGLDOverlay = function(){
	if (teacher.gldApi != null){
		teacher.gldApi.removeData('overlay');
		$(this).removeData('overlay');
	}
	teacher.gldApi = $(this);
	teacher.gldApi.overlay({
		target: teacher.genLessonFormContainer,
		mask: '#ccc',
	});	
	teacher.gldApi.overlay().load();
};
teacher.getUrl = function(url, data, callback){	
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
			teacher.url = html;
			if (callback != null){
				callback(teacher.url);
			}
		}
	},
	error: function(){
		teacher.alert("Couldn't get URL");
	}
	});
}
teacher.newHtml = function(h){
	$(teacher.container).html(h);
	teacher.refresh();
}
teacher.sendAjaxRequest = function(type, url, data, success_callback){
	teacher.showLoading(true);
	if (data == null){
		data = 'getpage='+teacher.url;
	}else{
		data = data+'&getpage='+teacher.url;
	}
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
				if (teacher.debug){
					teacher.alert(json.m);
				}
				teacher.showLoading(false);
			}
		},
		error: function(){
			teacher.showLoading(false);
			if (teacher.debug){
				teacher.alert("Couldnt get "+url);
			}
		}
	});
};
//	teacher.confirm = window.confirm;
teacher.refresh = function(){
	$(teacher.container).find('td.tick').click(function(){
		var v = $(this).html();
		v = teacher.nextValue(v);
		$(this).addClass('changed');
		$(this).html(v);
	});
	if (teacher.ldApi != null){
		teacher.ldApi.removeData('overlay');
		teacher.ldApi = null;
	}
	if (teacher.gldApi != null){
		teacher.gldApi.removeData('overlay');
		teacher.gldApi = null;
	}
	$('a#ap-handle').each(function(){
		$(this).click(function(){
			var id = '#'+$(this).attr('rel');
			$('.w-table').find(id).html('+').addClass('changed');
//			$('.w-table').find(id).each(function(){
//				
//			});
		});
	});
	$('a#del-lesson-day').click(function(){
		if (confirm('Do you want to delete this lesson-day?')){
			teacher.sendAjaxRequest("POST", $(this).attr('href'), null, function(json){
				teacher.alert('Deleted successfully!');
				teacher.newHtml(json.html);
			});
		}
		return false;
	});		
};
teacher.addLD = function(){
	var data=$(teacher.lessonFormContainer).find("form").serialize();
	var url = $(teacher.lessonFormContainer).find("form").attr('action');
	teacher.sendAjaxRequest("POST", url, data, function(json){
		teacher.alert('Successfull save!');
		teacher.ldApi.overlay().close();
		teacher.newHtml(json.html);
		//teacher.loadPage();
	});	
};
teacher.genLD = function(){
	var data = $(teacher.genLessonFormContainer).find("form").serialize();
	var url = $(teacher.genLessonFormContainer).find("form").attr('action');
	teacher.sendAjaxRequest("POST", url, data, function(json){
		teacher.alert('Successfull save!');
		teacher.gldApi.overlay().close();
		teacher.newHtml(json.html);
		//teacher.loadPage();
	});	
};
teacher.getClonedInput = function(){
	if (teacher.clonedInput == null){
		teacher.clonedInput = $(teacher.form).find('input[name=tick]').clone();
		$(teacher.form).find('input[name=tick]').remove('');
	}
	return teacher.clonedInput;
}
teacher.save = function(){
	if (teacher.group != '' && teacher.subject != ''){
		teacher.getClonedInput();
		$(teacher.form).find('input[name=tick]').remove('');
		$('td.tick').filter('.changed').each(function(){
			var v = $(this).attr('rel')+':'+$(this).html();
			//teacher.alert(val);
			var clone = $(teacher.getClonedInput()).clone();
			teacher.id+=1;
			$(clone).val(v);
			//$(clone).attr('value',v);
			$(clone).attr('id','tick'+teacher.id);
			$(teacher.form).append($(clone));
		});
		var url = $(teacher.form).attr('action');
		var data = $(teacher.form).serialize();
		teacher.sendAjaxRequest("POST", url, data, function(json){
			teacher.alert('Saved!');
			teacher.newHtml(json.html);
//			teacher.loadPage();
		});
	}else{
		teacher.alert('Subject and group are not selected!');
	}
};
teacher.reset = function(){
	if (teacher.group != '' && teacher.subject != ''){
		teacher.loadPage();
	}else{
		teacher.alert('Subject and group are not selected!');
	}
};
teacher.alert = function(m){
	$.jGrowl(m);
};
teacher.nextValue = function(v){
	if (v == '?') return '-';
	if (v == '-') return '+';
	if (v == '+') return 'I';
	if (v == 'I') return '?';
}
teacher.showLoading = function(s){
	if (s == true){
		$('div.w-loading').show();
	}else{
		$('div.w-loading').hide();
	}
};
teacher.groups.select = function(o){
	$(o).addClass('selected');
	teacher.group = $(o).attr('rel');
	teacher.loadSuccess = false;
	if (teacher.group != '' && teacher.subject != ''){
		teacher.loadPage();
	}
}
teacher.groups.deselect = function(o){
	$(o).removeClass('selected');
	teacher.group = '';
}
teacher.groups.deselectAll = function(){
	$('div.w-group').find('a').each(function(){
		teacher.groups.deselect(this);
	});
}
teacher.subjects.select = function(o){
	$(o).addClass('selected');
	teacher.subject = $(o).attr('rel');
	teacher.loadSuccess = false;
	if (teacher.group != '' && teacher.subject != ''){
		teacher.loadPage();
	}
}
teacher.subjects.deselect = function(o){
	$(o).removeClass('selected');
	teacher.subject = '';
}
teacher.subjects.deselectAll = function(){
	$('div.w-subject').find('a').each(function(){
		teacher.subjects.deselect(this);
	});
}
teacher.loadPage = function(){
//	if (teacher.url == null){
		teacher.getUrl(teacher.urlname,'sid='+teacher.subject+'&gid='+teacher.group, function(url){
			teacher.sendAjaxRequest("GET",url, null, function(json){
				teacher.newHtml(json.html);
				teacher.loadSuccess = true;
				teacher.alert('Successful load!');
			});
		});
//	}else{
//		teacher.sendAjaxRequest("GET",teacher.url, null, function(json){
//			teacher.newHtml(json.html);
//			teacher.loadSuccess = true;
//			teacher.alert('Successful load!');
//		});
//	}
}
