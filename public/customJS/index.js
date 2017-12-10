var c_response;
var onReturnCallback = function(response) { 
    c_response = response;
    //console.log(c_response)
}; 

$(document).ready(function () {

    $("#start").click(function(){
      $.ajax({
        url:"/init",
        type:"POST",
        data: JSON.stringify({
          category: $('.btn.btn-primary').parent().index(),
          goals: {
            calories: $('input[name=Calories]:checked', 'form').val(),
            protein: $('input[name=Protein]:checked', 'form').val(),
            fat: $('input[name=Fat]:checked', 'form').val()
          },
          "g-recaptcha-response": c_response
        }),
        contentType:"application/json; charset=utf-8",
        dataType: "json",
        success: function(data){
	  console.log(data)
          if (data.success){
            window.location.href = "game.html";
          }
        }
      });
    });
    
    $('.main-cus .btn').on('click', function(e) {
      $('.main-cus .btn').removeClass('btn-primary');
      $('.main-cus .btn').addClass('btn-default');
      $(this).removeClass('btn-default');
      $(this).addClass('btn-primary');
    })

    
});
