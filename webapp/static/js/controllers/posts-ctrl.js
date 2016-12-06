// User Settings

App.controller('postsCtrl', ['$scope', '$http', function($scope, $http) {

  $(document).ready(function(){

    $('textarea[data-elm-kind="add-comment-box"]').keyup(function(e){
      if(e.keyCode == 13) {
        var input = $(this);

        var dataObj = {
          post_id: input.data('post-id'),
          post_type: input.data('post-type'),
          postOwner_id: input.data('owner-id'),
          postOwner_type: input.data('owner-type')
        }

      $scope.addPostComment( input, dataObj );
      }
    });

  });

  //

  $scope.addPostComment = function(inputELM, dataObj) {
    if( inputELM == undefined || dataObj == undefined ) {
      console.log('Missing Inputs...');
      return;
    }

    console.log(inputELM);
    console.log(dataObj);
  }

}])
