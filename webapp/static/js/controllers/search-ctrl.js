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

    // console.log(user);

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
      // console.log(resp);
      if( resp.data.status == 'following' ) {
        user.status = 'Currently Following';
        user.btn = 'warning';
        user.msg = 'Unfollow';
        user.action = 'unfollowUser';
        user.title = 'Unfollow User';
      }
      else if( resp.data.status == 'not following' ) {
        user.status = 'Not Following';
        user.btn = 'success';
        user.msg = 'Follow';
        user.action = 'followUser';
        user.title = 'Follow User';
      }
      else if( resp.data.status == 'pending' ) {
        user.status = 'Pending Follow';
        user.btn = 'default';
        user.msg = 'Pending';
        user.action = 'cancelPendingFollow';
        user.title = 'Cancel Pending Follow Request';
      }
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });
  }

  //

  $scope.groupAction = function(group) {
    // console.log(group);

    if( group.status == 'Pending Invite' ){
      alert('You Have A Pending Invite From This Group.  \
      \nGo To Your Requests Page To Accept/Decline It.');
      return;
    }

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
      if(resp.data.status == 'pending') {
        user.status = 'Pending Invite';
        user.btn = 'default';
        user.msg = 'Pending';
        user.action = 'cancelPendingGroupInvite';
        user.title = 'Cancel Pending Group Invite';
      }
      else if(resp.data.status == 'not a member') {
        user.status = 'not a member';
        user.btn = 'success';
        user.msg = 'Send Group Invite';
        user.action = 'sendGroupInvitation';
        user.title = 'Send Group Invite';
      }
      else if(resp.data.status == 'currently a member') {
        user.status = 'currently a member';
        user.btn = 'danger';
        user.msg = 'Remove Member';
        user.action = 'removeMember';
        user.title = 'Remove From Group';
      }
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });
  }

}])
