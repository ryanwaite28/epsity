// User Settings

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
      $('#create-group-form').submit();
    }

  }

}])
