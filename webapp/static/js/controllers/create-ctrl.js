// User Settings

App.controller('createCtrl', ['$scope', '$http', function($scope, $http) {

  window.scope = $scope;

  $scope.createGroup = function() {

    var ask = confirm('Are all fields corrects?');
    if( ask == true ) {
      $('#create-group-form').submit();
    }

  }

}])
