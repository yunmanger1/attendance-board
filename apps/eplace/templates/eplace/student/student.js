var student = {
		listUrl: 'eplace_students_get',
		url: '',
		page: 1,
		getList: null,
		refresh: null,
		reset: null,
		newHtml: null,
		filter: null,
};
student.newHtml = function(html){
	$('div.w-table').html(html);
};
student.getList = function(){
	common.getUrl(student.listUrl, null, function(url){
		student.url = url;
		common.sendAjaxRequest("POST", url, null, function(json){
			student.newHtml(json.html);
		});
	});
};
student.filter = function(search){
	student.reset(search);
};
student.reset = function(search){
	var k = eval($('input#page-input').val());
	//var csrf = $('input[name=csrfmiddlewaretoken]').val();
	var data = 'page='+k;
	if (search == null){
		search = $('input#filter-input').val();
	}
	if (search != ''){
		data = data+'&q='+search;
	}
	common.sendAjaxRequest("POST", student.url, data, function(json){
		student.newHtml(json.html);
	});
};
student.next = function(){
	var k = eval($('input#page-input').val())+1;
	$('input#page-input').val(k);
	student.reset();
};
student.prev = function(){
	var k = eval($('input#page-input').val())-1;
	if (k < 1){
		k = 1;
	}
	$('input#page-input').val(k);
	student.reset();
};
student.refresh = function(){
	
};