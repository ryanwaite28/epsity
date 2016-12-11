// User Settings

App.controller('newPostsCtrl', ['$scope', '$http', function($scope, $http) {

  window.scope = $scope;

  $(document).ready(function(){

    $('#new-post-form select#newpost-type').change(function(){
      if( $(this).val() == 'Text' ) {
        $('#new-post-form input[name="media"]').hide();
      }
      else {
        $('#new-post-form input[name="media"]').show();
      }
    });

  });

  /*

    Angular

  */

  $scope.createUserPost = function() {
    if( $('#new-post-form input[name="title"]').val().trim() == "" ) {
      alert('Post Title Cannot Be Blank.');
      return;
    }
    else if( $('#new-post-form textarea').val().trim() == "" ) {
      alert('Post Body Cannot Be Blank.');
      return;
    }

    $('#new-post-form input[name="origin"]').val( location.pathname );
    $('#new-post-form').submit();
  }

}])
