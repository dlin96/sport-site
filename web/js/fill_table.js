$(document).ready(function() {
	$("#submit").click(function() {
		var player=$("#player").val();
		var player2=$("#player2").val();
		$.get("http://localhost:8000/comparison/", {player: player, player2: player2}).done(function(data) {
            if(jQuery.isEmptyObject(data)) {
                $("#message").empty();
                $("#message").prepend("Invalid entry. Please try again using the autocomplete options");
                $("#result").css("visibility", "visible");
                $("#playerTable").css("visibility", "hidden");
            } else {
                var playerData = $.parseJSON(data);
                $("#playerTable tr").remove();
                $("#playerTable th").remove();
                $("#result").css('visibility', 'visible');
                $("#message").empty();
                $("#message").prepend("Result:");
                $("#playerTable").prepend("<th>" + player2 + "</th>");
                $("#playerTable").prepend("<th>stat</th>");
                $("#playerTable").prepend("<th>" + player + "</th>");
                var neg_stats = ["pfouls", "tos", "topg"];
                for(var key in playerData[0]) {
                    if(key === "playerId")
                        continue;
                    var txt = "<tr><td id='player1" + key+"''>" + playerData[0][key] + "</td><td>" + key + "</td><td id='player2"+key+ "''>" + playerData[1][key]+"</td></tr>";
                    $("#playerTable").append(txt);
                    if(jQuery.inArray(key, neg_stats) >= 0) {
                        if(playerData[0][key] < playerData[1][key]) {
                            $("#player1"+key).css("background-color", "green");
                            $("#player2"+key).css("background-color", "red");
                        } else if(playerData[0][key] > playerData[1][key]) {
                            $("#player2"+key).css("background-color", "green");
                            $("#player1"+key).css("background-color", "red");
                        }
                    }
                    else {
                        if(playerData[0][key] > playerData[1][key]) {
                            $("#player1"+key).css("background-color", "green");
                            $("#player2"+key).css("background-color", "red");
                        } else if(playerData[0][key] < playerData[1][key]) {
                            $("#player2"+key).css("background-color", "green");
                            $("#player1"+key).css("background-color", "red");
                        }
                    }
                }
                $("#playerTable").css("visibility", "visible");
            }
		}, "json");
	});
});
