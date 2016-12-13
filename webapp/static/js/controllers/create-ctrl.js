// User Settings

// function initMap() {
//
//   var map = new google.maps.Map(document.getElementById('map'), {
//     center: {lat: -34.397, lng: 150.644},
//     scrollwheel: true,
//     zoom: 8
//   });
//
//   window.map = map;
//
// }

'use strict';

App.controller('createCtrl', ['$scope', '$http', function($scope, $http) {

  window.scope = $scope;

  window.initMap = function() {

    var map = new google.maps.Map(document.getElementById('mapdiv'), {
      center: {lat: -34.397, lng: 150.644},
      scrollwheel: true,
      zoom: 8
    });

    google.maps.event.trigger(map, 'resize');

    window.map = map;

  }

  $scope.createGroup = function() {
    if( !alphaNum_two.test(  $('input[name="displayname"]').val() ) ) {
      alert('Group Display Name Must Be Lettters, Numbers, dashes, and/or underscores, 3-25 Characters.');
      return;
    }
    if( !alphaNum_two.test(  $('input[name="uname"]').val() ) ) {
      alert('Group UserName Must Be Lettters, Numbers, dashes, and/or underscores, 3-25 Characters.');
      return;
    }
    if( $('input[name="displayname"]').val().substring( $('input[name="displayname"]').val().length - 1) == ' ' ) {
      alert('Please Remove Any Trailing Space From The Group Display Name Field.');
      return;
    }
    if( $('input[name="uname"]').val().substring( $('input[name="displayname"]').val().length - 1) == ' ' ) {
      alert('Please Remove Any Trailing Space From The Group UserName Field.');
      return;
    }

    var ask = confirm('Are all fields corrects?');
    if( ask == true ) {
      $('#create-group-form input[name="origin"]').val( location.pathname );
      $('#create-group-form').submit();
    }

  }

  $scope.searchUsers = function() {
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
        action: 'searchUsers',
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

  $scope.selectedConvoMembers = [];

  $scope.addToSelected = function(user) {
    if( $scope.selectedConvoMembers.indexOf(user) != -1 ) {
      // alert('That user is already selected.');
      return;
    }
    $scope.selectedConvoMembers.push(user);
  }

  $scope.removeSelected = function(user) {
    var index = $scope.selectedConvoMembers.indexOf(user);
    $scope.selectedConvoMembers.splice(index, 1);
  }

  $scope.checkConvoName = function() {
    if( $scope.newConvoName == undefined ) {
      alert('Conversation Name Is Needed.');
      return;
    }
    else if( $scope.newConvoName.length == 0 ) {
      alert('Conversation Name Is Needed.');
      return;
    }
    else if( $scope.newConvoName.trim().length == 0 ) {
      alert('Conversation Name Is Needed.');
      return;
    }
    else if( $scope.newConvoName.replace(/(\s+|\s+$)/g, " ").trim().length <= 2 ) {
      alert('Conversation must be at least 3 characters.');
      return;
    }

    var req = {
      method: 'POST',
      url: '/checkpoint/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: 'checkConvoName',
        name: $scope.newConvoName.replace(/(\s+|\s+$)/g, " ").trim(),
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      // console.log(resp);

      if( resp.data.msg == 'available' ) {
        $scope.createGroupConvo();
      }

    },
    function(resp){
      // Error Callback
      console.log(resp);
    });
  }

  $scope.createGroupConvo = function() {

    if( $scope.selectedConvoMembers.length <= 0 ) {
      alert('There needs to be at least 1 member to create the group conversation.');
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
        action: 'createGroupConvo',
        name: $scope.newConvoName.replace(/(\s+|\s+$)/g, " ").trim(),
        members: $scope.selectedConvoMembers,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

  }

}])
