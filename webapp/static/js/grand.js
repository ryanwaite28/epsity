$(document).ready(function(){

  $('li').addClass('transition');
  $('a').addClass('transition');

  $('.rotator').click(function(){
    //console.log(this);
    $(this).toggleClass('rotate');
  });

  $('.nav li a').click(function(e) {
			e.preventDefault()
			$(this).tab('show')
	})

  $('.back-to-top').click(function(e){

    var targetID = $(this).data('elmtarget');

    if( targetID == undefined || targetID == '' ) {
      $('html, body').animate({
          scrollTop: 0 // $("#sdl").offset().top
      }, 1000);
    }
    else {
      $(targetID).animate({
          scrollTop: 0 // $("#sdl").offset().top
      }, 1000);
    }

  });

});
