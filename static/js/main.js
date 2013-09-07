$(document).ready(function() {

	$("input[name='team_id']").change(function(){
		$(".view_team").attr("href","/team/"+$(this).val())
	})
	$(".new_team").click(function() {
		var key = Math.random().toString(36).substring(7);
		$.post("/key", { key: key }, function(data) {
			console.log(data);
		})
	})

	function saveUserInfo(e) {
		if(e) e.preventDefault();

		var obj = {
			uniqname: $("input[name='uniqname']").val(),
			team_id: $("input[name='team_id']").val()
		}

		$.ajax({
		    url: '/user',
		    type: 'POST',
		    data: JSON.stringify(obj),
		    headers: {
		    	"Content-Type":"application/json"
		    },
		    dataType: 'json',
		    success: function (data) {
		    	console.log(data);
		    	$(".status").html("Info Saved!")
		    	setTimeout(function() {
		    		$(".status").html("")
		    	}, 1000)
		    },
		    error: function(data) {
		    	console.log(data);
		    	alert("Something is wrong!\nBother Otto and give him this: \n\n" + data)
		    }
		});
	}

	if(window.location.pathname == "/user") {
		saveUserInfo(null); // save right away!
	}
	$("#user_signup").submit(saveUserInfo);

	$("#team_signup").submit(function(e) {
		e.preventDefault();

		var obj = {
			name: $("input[name='team']").val(),
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