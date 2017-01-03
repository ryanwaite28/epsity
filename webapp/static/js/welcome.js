/* --- Epsity | Welcome Page --- */

$(document).ready(function(){

  $(window).scroll(function(){
    var w = $(window).scrollTop();

    if( w > 375 ) {
      $("#top-bar").addClass('top-bar-style-1');
      $("#top-bar").css('background', 'black');
      $("#top-bar").css('padding', '0px');
      $("#arrow-1").removeClass('hide-1');
    }
    else {
      $("#top-bar").removeClass('top-bar-style-1');
      $("#top-bar").css('background', 'transparent');
      $("#top-bar").css('padding', '15px');
      $("#arrow-1").addClass('hide-1');
    }
  });

  $('#arrow-1').click(function(){
	  $('html, body').animate({
	    scrollTop: 0
	  }, 1000);
	});

  if( $(window).width() > 809 ) {
		$('#links-collapse').addClass('in');
	}
	else {
		$('#links-collapse').removeClass('in');
    $("#top-bar").css('padding', '15px');
    $('#links-collapse').css('background', 'black');
	}

  $(window).resize(function(){
    if( $(window).width() > 809 ) {
  		$('#links-collapse').addClass('in');
  	}
  	else {
  		$('#links-collapse').removeClass('in');
      $("#top-bar").css('padding', '15px');
      $('#links-collapse').css('background', 'black');
  	}
  });

});

// ----- //

App.controller('welcomeCtrl', ['$scope', function($scope) {

  window.scope = $scope;

  //

  $scope.googleInfo = function( str ) {

    var ref = new Firebase("https://the-travelr.firebaseio.com/");
    ref.authWithOAuthPopup("google", function(error, authData) {
      if (error) {
    		console.log("Login Failed!", error);
    	}
    	else {
    		console.log("Authenticated successfully with payload:", authData);
        $('#s-msg').text('Google Info Loaded!');
        if( str == 'login' ) {
          $scope.gLogin(authData);
        }
        else if( str == 'signup' ) {
          $('#fg-div').hide();
          $scope.gSignUp(authData);
        }
        else {
          console.log('str is undefined...');
          return;
        }
  		}
    }, {scope: "email"});

  }

  $scope.facebookInfo = function( str ) {

		var ref = new Firebase("https://the-travelr.firebaseio.com/");
		ref.authWithOAuthPopup("facebook", function(error, authData) {
  			if (error) {
    			console.log("Login Failed!", error);
  			}
  			else {
    			console.log("Authenticated successfully with payload:", authData);
          $('#s-msg').text('Facebook Info Loaded!');
          if( str == 'login' ) {
            $scope.fbLogin(authData);
          }
          else if( str == 'signup' ) {
            $('#fg-div').hide();
            $scope.fbSignUp(authData);
          }
          else {
            console.log('str is undefined...');
            return;
          }
  			}
		}, {scope: "email"});

	}

  //

  $scope.login = function(str) {
    console.log(str);

    if( str == 'facebook' ) {
      $scope.facebookInfo('login');
    }
    else if( str == 'google' ) {
      $scope.googleInfo('login');
    }
    else {
      return;
    }

  }

  $scope.signup = function(str) {
    console.log(str);

    if( str == 'facebook' ) {
      $scope.facebookInfo('signup');
    }
    else if( str == 'google' ) {
      $scope.googleInfo('signup');
    }
    else {
      return;
    }

  }

  //

  $scope.fbLogin = function( data ) {

    var obj = {
      provider: data.provider,
      email: data.facebook.email,
      displayName: data.facebook.displayName,
      img: data.facebook.profileImageURL,
      id: data.facebook.id,
      uid: data.uid
    }
    $scope.data = obj;

    $('#login-form > input[name="providerid"]').val( $scope.data.id );
    $('#login-form > input[name="email"]').val( $scope.data.email );
    $('#login-form > input[name="uid"]').val( $scope.data.uid );

    $('#login-form').submit();

  }
  $scope.fbSignUp = function( data ) {

    var obj = {
      provider: data.provider,
      email: data.facebook.email,
      displayName: data.facebook.displayName,
      img: data.facebook.profileImageURL,
      id: data.facebook.id,
      uid: data.uid
    }
    $scope.data = obj;

    alert('Account Info Loaded For: ' + obj.displayName +
    '! Please Choose A User Name And Click Create.');

  }

  $scope.gLogin = function( data ) {

    var obj = {
      provider: data.provider,
      email: data.google.email,
      displayName: data.google.displayName,
      img: data.google.profileImageURL,
      id: data.google.id,
      uid: data.uid
    }
    $scope.data = obj;

    $('#login-form > input[name="providerid"]').val( $scope.data.id );
    $('#login-form > input[name="email"]').val( $scope.data.email );
    $('#login-form > input[name="uid"]').val( $scope.data.uid );

    $('#login-form').submit();

  }
  $scope.gSignUp = function( data ) {

    var obj = {
      provider: data.provider,
      email: data.google.email,
      displayName: data.google.displayName,
      img: data.google.profileImageURL,
      id: data.google.id,
      uid: data.uid
    }
    $scope.data = obj;

    alert('Account Info Loaded For: ' + obj.displayName +
    '! Please Choose A User Name And Click Create.');

  }

  //

  $('#submit-btn').click(function(e){

    if( $scope.data == undefined ) {
      alert('Please Choose Facebook Or Google For Signup.');
      return;
    }

    var regex =/^[A-Za-z0-9\-\_]{3,25}$/;
    var uname = $('#signup-form > input[name="uname"]').val();

    if( !regex.test(uname) ) {
      alert('User Name Must Be 3-25 Characters, Letters, Numbers, Dashes, and Underscores.');
      return;
    }

    $('#signup-form > input[name="displayname"]').val( $scope.data.displayName );
    $('#signup-form > input[name="provider"]').val( $scope.data.provider );
    $('#signup-form > input[name="providerid"]').val( $scope.data.id );
    $('#signup-form > input[name="email"]').val( $scope.data.email );
    $('#signup-form > input[name="uid"]').val( $scope.data.uid );
    $('#signup-form > input[name="image"]').val( $scope.data.img );


    $('#signup-form').submit();

    /*$scope.data.username = uname;

    $.ajax({
      url: '/signup/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify($scope.data),
      success: function(data) {
        location.href = '/main';
      },
      statusCode: {
        500: function(data) {
          console.log(data);
        }
      }
    });*/

  })

}])
