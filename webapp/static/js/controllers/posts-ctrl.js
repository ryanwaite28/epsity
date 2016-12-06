// User Settings

App.controller('postsCtrl', ['$scope', '$http', function($scope, $http) {

  $(document).ready(function(){

    $('#new-post-form select#newpost-type').change(function(){
      if( $(this).val() == 'Text' ) {
        $('#new-post-form input[name="media"]').hide();
      }
      else {
        $('#new-post-form input[name="media"]').show();
      }
    });

    $('.add-comment-btn').click(function(){
      var btn = $(this);
      var input = $(this).siblings('textarea.add-comment-box');

      var dataObj = {
        post_id: input.data('post-id'),
        post_type: input.data('post-type'),
        postOwner_id: input.data('owner-id'),
        postOwner_type: input.data('owner-type')
      }

      console.log(dataObj);
    });

  });

  //

  $scope.createUserPost = function() {
    $('#new-post-form input[name="origin"]').val( location.pathname );
    $('#new-post-form').submit();
  }

  $scope.addPostComment = function(inputELM, dataObj) {
    if( inputELM == undefined || dataObj == undefined ) {
      console.log('Missing Inputs...');
      return;
    }

    console.log(inputELM);
    console.log(dataObj);
  }

}])
