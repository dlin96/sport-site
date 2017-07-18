$(document).ready(function() {
	$("#submit").click(function() {
		var player=$("#player").val();
		var player2=$("#player2").val();
		$.post("http://localhost:3000/comparison/" + player + "/" + player2, {player: player, player2: player2}).done(function(data) {
            var playerData = $.parseJSON(data);
            console.log(playerData);
            $("#playerTable tr").remove();
            $("#playerTable th").remove();
            $("#result").css('visibility', 'visible');
            $("#playerTable").prepend("<th>" + player2 + "</th>");
            $("#playerTable").prepend("<th>stat</th>");
            $("#playerTable").prepend("<th>" + player + "</th>");
            for(var key in playerData[0]) {
                if(key === "playerId")
                    continue;
                var txt = "<tr><td id='player1" + key+"''>" + playerData[0][key] + "</td><td>" + key + "</td><td id='player2"+key+ "''>" + playerData[1][key]+"</td></tr>";
                $("#playerTable").append(txt);
                if(playerData[0][key] > playerData[1][key]) {
                    $("#player1"+key).css("background-color", "green");
                    $("#player2"+key).css("background-color", "red");
                } else if(playerData[0][key] < playerData[1][key]) {
                    $("#player2"+key).css("background-color", "green");
                    $("#player1"+key).css("background-color", "red");
                }
            }
			// $("#result").append(JSON.stringify(data));
		}, "json");
	});
});
