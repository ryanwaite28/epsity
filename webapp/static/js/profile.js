/* --- Profile JS --- */

$(document).ready(function(){

  var fast = 'fast';
  var slow = 'slow';

  $('i').addClass('transition');

  $('#arrow-1').click(function(){
	  $('html, body').animate({
	    scrollTop: 0
	  }, 1000);
	});

  $('.switch-div-ctrl').click(function(){
    var id = '#prof-' + $(this).text().toLowerCase() + '-div';
    //console.log( id );
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


});

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

App.controller('epsityCtrl', ['$scope', function($scope) {

  window.scope = $scope;

  $scope.deleteAccount = function() {
    var ask = confirm('Are you sure you want to delete your account? All of your info will be deleted. This action is irreversable.');
    if( ask == true ) {
      $('#deleteaccount-form').submit();
    }
    else {
      // Do Nothing
    }
  }



}])
