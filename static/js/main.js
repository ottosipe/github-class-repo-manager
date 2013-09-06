$(document).ready(function() {

	$("input[name='group_id']").change(function(){
		$(".view_group").attr("href","/group/"+$(this).val())
	})
	$("#user_signup").submit(function(e) {
		e.preventDefault();

		var obj = {
			uniqname: $("input[name='uniqname']").val(),
			group_id: $("input[name='group_id']").val()
		}

		console.log(obj);

		$.ajax({
		    url: '/user',
		    type: 'POST',
		    data: JSON.stringify(obj),
		    headers: {
		    	"Content-Type":"application/json"
		    },
		    dataType: 'json',
		    success: function (data) {
		        console.info(data);
		    }
		});
	})

	$("#group_signup").submit(function(e) {
		e.preventDefault();

		var obj = {
			name: $("input[name='group']").val(),
			members: []
		}

		for(var i in [0,1,2]) {
			obj.members.push({
				name: getByName("name",i),
				github: getByName("github",i),
				uniqname: getByName("uniqname",i)
			})
		}

		$.ajax({
		    url: '/signup',
		    type: 'POST',
		    data: JSON.stringify(obj),
		    headers: {
		    	"Content-Type":"application/json"
		    },
		    dataType: 'json',
		    success: function (data) {
		        console.info(data);
		    }
		});
	})


});

function getByName(name, i) {
	return $($("input[name='"+name+"']")[i]).val();
}