$(document).ready(function() {

	$("input[name='team_id']").change(function(){
		$(".view_team").attr("href","/team/"+$(this).val())
	})

	$(".new_team").click(function() {
		var key = Math.random().toString(36).substring(7);
		$.post("/key", { key: key }, function(data) {
			$("input[name='team_id']").val(key);
			$(".view_team").attr("href","/team/"+key)
			console.log(data);
			resetUI();
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
		    	var oldText = $("#save").html()
		    	$("#save").html("Saved!")
		    	setTimeout(function() {
		    		$("#save").html(oldText)
		    	}, 2000)
		    },
		    error: function(data) {
		    	console.log(data);
		    	alert("Something is wrong!\nBother Otto and give him this: \n\n" + data)
		    }
		});
	}

	function resetUI() {
		if($("input[name='team_id']").val()) {
			$(".new_team").hide();
			$(".view_team").show();
			$("input[name='team_id']").attr("readonly","readonly")
		} else {
			$(".view_team").hide();
		}
	}

	if(window.location.pathname == "/user") {
		saveUserInfo(null); // save right away!
		resetUI();
	} 

	$("#user_signup").submit(saveUserInfo);

	$("#team_signup").submit(function(e) {
		e.preventDefault();

		var obj = {
			name: $("input[name='team']").val()
		}

		for(var i in [0,1,2]) {
			obj.members.push({
				name: getByName("name",i),
				github: getByName("github",i),
				uniqname: getByName("uniqname",i)
			})
		}

		$.ajax({
		    url: '/team/'+$("input[name='id']").val(),
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