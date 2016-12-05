// User Settings

App.controller('postsCtrl', ['$scope', '$http', function($scope, $http) {

  $('.btn-action').click(function(){

    if( 1 == 1 ) {
      $(this).removeClass('like-btn-o').addClass('like-btn-f');
    }
    else {
      $(this).removeClass('like-btn-f').addClass('like-btn-o');
    }


  });

}])
