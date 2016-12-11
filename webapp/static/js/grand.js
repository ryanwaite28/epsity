/* Master Application */

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

// Initializers

$(document).ready(function(){

  $('li').addClass('transition');
  $('a').addClass('transition');
	$('i').addClass('transition');
	//$('input').addClass('transition');
	//$('span').addClass('transition');

  $('.rotator').click(function(){
    //console.log(this);
    $(this).toggleClass('rotate');
  });

	$('.inverter').click(function(){
    //console.log(this);
    $(this).toggleClass('invert');
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

	window.linkRegex = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
	window.alphaNumeric = /^[a-zA-Z0-9]+$/i;
	window.alphaNum_one = /^[a-zA-Z0-9\.]{3,25}/;
	window.alphaNum_two = /^[a-zA-Z0-9\_\-]{3,25}/;
	window.catCheck = /^[a-zA-Z0-9\_\-\.]{3,25}/;
	

	window.backToTop = function() {
		$('html, body').animate({
				scrollTop: 0
		}, 1000);
	}

});

//


function trimTrailingSpaces(str) {

	return str.replace(/(\s+|\s+$)/g, " ").trim();

}

function newhttpRequestObj() {
	var req = {
		method: '',
		url: '',
		headers: {
			'Content-Type': 'application/json',
			'responseType': 'json',
			"Accept" : "application/json",
			'X-CSRFToken': Cookies.get('csrftoken')
		},
		data: {
			csrfmiddlewaretoken: Cookies.get('csrftoken'),
		}
	}

	return req;
}
