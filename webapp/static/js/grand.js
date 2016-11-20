var App = angular.module("epsityApp", ["firebase"]);

App.factory("travelr", ["$firebaseArray",
	function($firebaseArray) {
   	var ref = new Firebase("https://the-travelr.firebaseio.com/");

   	// this uses AngularFire to create the synchronized array
    return $firebaseArray(ref);
	}
]);

App.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);

//

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

	var csrftoken = Cookies.get('csrftoken');

	$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
	});

	 window.badChars = [
    '@', '#', '$', '%', '^',
    '^', '&', '*', '(', ')',
    '-', '_', '=', '+', '`',
    '~', '[', ']', '{', '}',
    '\\', '|', '/', '?', '.',
    ',', '<', '>'
  ];

});
