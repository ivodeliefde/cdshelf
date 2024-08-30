$(document).ready(function(){
    $('#pause').click(function() {
        $.ajax({url: "/cdshelf/pause", success: function(result){
            console.log(result)
          }});
    });
    $('#play').click(function() {
        $.ajax({url: "/cdshelf/play", success: function(result){
            console.log(result)
          }});
    });
    $('#eject').click(function() {
        $.ajax({url: "/cdshelf/eject", success: function(result){
            console.log(result)
          }});
    });
});
