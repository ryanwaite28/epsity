$(document).ready(function(){

  $('li').addClass('transition');
  $('a').addClass('transition');

  $('.rotator').click(function(){
    //console.log(this);
    $(this).toggleClass('rotate');
  });

});
