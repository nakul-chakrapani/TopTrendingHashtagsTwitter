var server_name = "http://127.0.0.1:3000/";
var server = io.connect(server_name);

var count = 1;
var numhashtags = 0;
$('#getTopTrendingButton').click(function() {
  console.log("clicked");
  var ckey = $("#ckey").val();
  var csecret = $("#csecret").val();
  var atoken = $("#atoken").val();
  var asecret = $("#asecret").val();
  var numwindows = $("#numwindows").val();
  var numtweets = $("#numtweets").val();
  numhashtags = $("#numhashtags").val();
  server.emit('getdata', {ckey: ckey, csecret: csecret, atoken: atoken, asecret: asecret, numwindows: numwindows, numtweets: numtweets, numhashtags: numhashtags})
  document.getElementById("statsdisplayarea").style.visibility="visible";
});

server.on("new_hashtags", function(data) {
  var output = '';
  for (var property in data) {
    output += data[property];
  }
  if (count <= numhashtags) {
    document.getElementById("stats").innerHTML += output + "<br>";
    count += 1;
  } else {
    document.getElementById("stats").innerHTML = output + "<br>";
    count = 2;
  }
});
