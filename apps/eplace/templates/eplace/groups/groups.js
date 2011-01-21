var groups = {
		listUrl: 'eplace_groups_get',
		url: null,
		getList: null,
		refresh: null,
		reset: null,
		newHtml: null,
		select: null,
		deselect: null,
		deselectAll: null
};
alert = common.alert;
groups.select = function(o){
	$(o).addClass('selected');
	common.getUrl(groups.listUrl, 'gid='+$(o).attr('rel'), function(url){
		groups.url = url;		
		common.sendAjaxRequest('GET',groups.url, null, function(json){
			$('div.w-table').html(json.html);
		});
	});
};

groups.deselect = function(o){
	$(o).removeClass('selected');
};

groups.deselectAll = function(o){
	$(o).parent().find('a').removeClass('selected');
};

