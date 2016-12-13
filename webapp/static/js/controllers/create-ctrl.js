// User Settings

function initMap() {

  var map = new google.maps.Map(document.getElementById('mapdiv'), {
    center: {lat: -34.397, lng: 150.644},
    scrollwheel: true,
    zoom: 8
  });

  window.map = map;

}

App.controller('createCtrl', ['$scope', '$http', function($scope, $http) {

  window.scope = $scope;



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
    console.log(user);
    $scope.selectedConvoMembers.push(user);
  }

  $scope.removeSelected = function(user) {
    console.log(user);
    var index = $scope.selectedConvoMembers.indexOf(user);
    $scope.selectedConvoMembers.splice(index, 1);
  }

}])
