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

    //

    $('.add-comment-btn').click(function(){
      var id = "#cmbox-" + $(this).data('post-id');
      var input = $(id);

      if( $(input).css('display') == 'none' ) {
        $(input).css('display', 'block');
      }
      else {
        $(input).css('display', 'none');
      }
    });

    $('.add-reply-btn').click(function(){
      var id = "#cmrly-" + $(this).data('comment-id');
      var input = $(id);

      if( $(input).css('display') == 'none' ) {
        $(input).css('display', 'block');
      }
      else {
        $(input).css('display', 'none');
      }
    });

  });

  //

  $('.add-comment-box').keyup(function(e){
    if( e.keyCode != 13 ) {
      return;
    }

    var input = $(this);
    var comment = trimTrailingSpaces( input.val() );

    var dataObj = {
      post_id: input.data('post-id'),
      post_type: input.data('post-type'),
      postOwner_id: input.data('owner-id'),
      postOwner_type: input.data('owner-type')
    }

    if( comment.replace(/\s/g, '').length > 0 ) {
      if( comment.length > 500 ) {
        alert('The Max Length For A Comment Is 500 Characters.');
        return;
      }
      else {
        dataObj.comment = comment;
        $scope.addPostCommentUser(input , dataObj);
      }
    }
  });

  $('.add-reply-box').keyup(function(e){
    if( e.keyCode != 13 ) {
      return;
    }

    var input = $(this);
    var reply = trimTrailingSpaces( input.val() );


    var dataObj = {
      comment_id: input.data('comment-id'),
      commentOwner_id: input.data('owner-id'),
      commenttOwner_type: input.data('owner-type')
    }

    if( reply.replace(/\s/g, '').length > 0 ) {
      if( reply.length > 500 ) {
        alert('The Max Length For A Reply Is 500 Characters.');
        return;
      }
      else {
        dataObj.reply = reply;
        $scope.addCommentReplyUser(input , dataObj);
      }
    }
  });

  //

  $scope.createUserPost = function() {
    $('#new-post-form input[name="origin"]').val( location.pathname );
    $('#new-post-form').submit();
  }

  $scope.addPostCommentUser = function(inputELM, dataObj) {
    if( inputELM == undefined || dataObj == undefined ) {
      console.log('Missing Inputs...');
      return;
    }

    console.log(dataObj);
    // return;

    var req = {
      method: 'POST',
      url: '/action/ajax/',
      headers: {
        'Content-Type': 'application/json',
        'responseType': 'json',
        "Accept" : "application/json",
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: 'addPostCommentUser',
        info: dataObj,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }

    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      $(inputELM).val('');
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });
  }

  $scope.addCommentReplyUser = function(inputELM, dataObj) {
    if( inputELM == undefined || dataObj == undefined ) {
      console.log('Missing Inputs...');
      return;
    }

    console.log(dataObj);
    // return;

    var req = {
      method: 'POST',
      url: '/action/ajax/',
      headers: {
        'Content-Type': 'application/json',
        'responseType': 'json',
        "Accept" : "application/json",
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: 'addCommentReplyUser',
        info: dataObj,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }

    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      $(inputELM).val('');
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });
  }

}])
