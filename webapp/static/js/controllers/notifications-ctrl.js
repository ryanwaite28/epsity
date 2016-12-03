// User Settings

App.controller('notificationsCtrl', ['$scope', '$http', function($scope, $http) {

  window.scope = $scope;

  //

  $scope.loadNotesAll = function() {

    var req = {
      method: 'POST',
      url: '/action/ajax/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: 'load notes all',
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      $scope.pendingFollows = resp.data.pendingFollows;
      $scope.pendingGroupInvites = resp.data.pendingGroupInvites;
      $scope.pendingGroupRequests = resp.data.pendingGroupRequests;
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

  }
  $scope.loadNotesAll();

  // --- //

  $scope.acceptFollow = function(pf) {
    console.log(pf);


    var req = {
      method: 'POST',
      url: '/action/ajax/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: 'accept follow',
        pf: pf,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      var index = $scope.pendingFollows.indexOf(pf);
      $scope.pendingFollows.splice(index, 1);
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

  }

  $scope.declineFollow = function(pf) {
    console.log(pf);


    var req = {
      method: 'POST',
      url: '/action/ajax/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: 'decline follow',
        pf: pf,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      var index = $scope.pendingFollows.indexOf(pf);
      $scope.pendingFollows.splice(index, 1);
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

  }

  // --- //

  $scope.acceptGroupInvite = function(pi) {
    console.log(pi);
    //return;

    var req = {
      method: 'POST',
      url: '/action/ajax/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: 'accept group invite',
        pi: pi,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      var index = $scope.pendingGroupInvites.indexOf(pi);
      $scope.pendingGroupInvites.splice(index, 1);
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

  }

  $scope.declineGroupInvite = function(pi) {
    console.log(pi);
    //return;

    var req = {
      method: 'POST',
      url: '/action/ajax/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: 'decline group invite',
        pi: pi,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      var index = $scope.pendingGroupInvites.indexOf(pi);
      $scope.pendingGroupInvites.splice(index, 1);
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

  }

  //

  $scope.acceptGroupRequest = function(pr) {
    console.log(pr);
    //return;

    var req = {
      method: 'POST',
      url: '/action/ajax/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: pr.options.accept,
        pr: pr,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      var index = $scope.pendingGroupRequests.indexOf(pr);
      $scope.pendingGroupRequests.splice(index, 1);
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

  }

  $scope.declineGroupRequest = function(pr) {
    console.log(pr);
    //return;

    var req = {
      method: 'POST',
      url: '/action/ajax/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: pr.options.decline,
        pr: pr,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      var index = $scope.pendingGroupRequests.indexOf(pr);
      $scope.pendingGroupRequests.splice(index, 1);
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

  }

}])
