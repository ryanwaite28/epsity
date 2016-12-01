/* --- Profile JS --- */

$(document).ready(function(){

  var fast = 'fast';
  var slow = 'slow';

  $('#arrow-1').click(function(){
	  $('html, body').animate({
	    scrollTop: 0
	  }, 1000);
	});

  $('.switch-div-ctrl').click(function(){
    var id = '#' + $(this).attr('id').replace('ctrl', 'div')
    // console.log( id );
    $('.switch-div').hide();
    $(id).show();
  });

  $('.switch-div-x').click(function(){
    $(this).parent().parent().hide();
  });

  var width = $(window).width();
  if( width < 625 ) {
    $('#menu-c').show();
    $('#tb-collapse').removeClass('in');
  }
  else {
    $('#menu-c').hide();
    $('#tb-collapse').addClass('in');
  }

  $(window).resize(function(){

    var width = $(window).width();

    if( width < 625 ) {
      $('#menu-c').show();
      $('#tb-collapse').removeClass('in');
    }
    else {
      $('#menu-c').hide();
      $('#tb-collapse').addClass('in');
    }

  });

  // var interests = $('#interests').text().split(' ').join(', ');
  // $('#interests').text( interests );
  //
  // var seeking = $('#seeking').text().split(' ').join(', ');
  // $('#seeking').text( seeking );

});
