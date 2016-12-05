// User Settings

App.controller('searchCtrl', ['$scope', '$http', function($scope, $http) {

  window.scope = $scope;

  //

  $scope.submitSearch = function() {
    if( $scope.searchQuery == '' ) {
      return;
    }
    else if( !alphaNumeric.test($scope.searchQuery) ) {
      alert('Alphanumeric Query Only (Letters & Numbers).');
      return;
    }

    var req = {
      method: 'POST',
      url: '/search/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: 'search query',
        query: $scope.searchQuery,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);

      $scope.srUsers = resp.data.users;
      $scope.srGroups = resp.data.groups;
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

  }

  //

  $scope.followAction = function(user) {

    var req = {
      method: 'POST',
      url: '/action/ajax/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: user.action,
        user: user,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);

      user.status = resp.data.state.status;
      user.btn = resp.data.state.btn;
      user.msg = resp.data.state.msg;
      user.action = resp.data.state.action;
      user.title = resp.data.state.title;

    },
    function(resp){
      // Error Callback
      console.log(resp);


    });
  }

  //

  $scope.groupActionTwo = function(group) {
    // console.log(group);

    // if( group.status == 'Pending Invite' ){
    //   alert('You Have A Pending Invite From This Group.  \
    //   \nGo To Your Requests Page To Accept/Decline It.');
    //   return;
    // }

    var req = {
      method: 'POST',
      url: '/action/ajax/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: group.action,
        group: group,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }

    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);

      group.status = resp.data.state.status;
      group.btn = resp.data.state.btn;
      group.msg = resp.data.state.msg;
      group.action = resp.data.state.action;
      group.title = resp.data.state.title;

    },
    function(resp){
      // Error Callback
      console.log(resp);
    });
  }

}])
