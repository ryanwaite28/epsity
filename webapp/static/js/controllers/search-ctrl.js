// User Settings

App.controller('searchCtrl', ['$scope', '$http', function($scope, $http) {

  window.scope = $scope;

  $scope.submitSearch = function() {

    if( $scope.searchQuery == '' ) {
      return;
    }
    else if( !alphaNumeric.test($scope.searchQuery) ) {
      alert('Alphanumeric Query Only (Letters & Numbers).');
      return;
    }

    var csrftoken = Cookies.get('csrftoken');

    var req = {
      method: 'POST',
      url: '/search/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      data: JSON.stringify({
        action: 'search query',
        query: $scope.searchQuery,
        csrfmiddlewaretoken: csrftoken,
      })
    }

    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      $scope.srUsers = resp.data.users;
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

  }

}])
