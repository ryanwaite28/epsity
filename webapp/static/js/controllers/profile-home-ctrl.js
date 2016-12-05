// User Settings

App.controller('profileHomeCtrl', ['$scope', function($scope) {

  window.scope = $scope;

  //

  $scope.createUserPost = function() {
    $('#new-post-form input[name="origin"]').val( location.pathname );
    $('#new-post-form').submit();
  }

}])
