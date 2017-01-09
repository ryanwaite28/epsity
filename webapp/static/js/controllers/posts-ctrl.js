// User Settings

App.controller('postsCtrl', ['$scope', '$http', function($scope, $http) {

  window.scope = $scope;

  $(document).ready(function(){

    $http({
      method: 'POST',
      url: '/checkpoint/',
      headers: {
        'Content-Type': 'application/json',
        'responseType': 'json',
        "Accept" : "application/json",
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: 'checkLoginState',
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }).then(function(resp){
      // Success Callback
      console.log(resp);
      $scope.you = resp.data.you;
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

    $(document).on('click', '.add-comment-btn', function(){
      var id = "#cmbox-" + $(this).data('post-id');
      var input = $(id);

      if( $(input).css('display') == 'none' ) {
        $(input).css('display', 'block');
      }
      else {
        $(input).css('display', 'none');
      }
    });

    $(document).on('click', '.add-reply-btn', function(){
      var id = "#cmrly-" + $(this).data('comment-id');
      var input = $(id);

      if( $(input).css('display') == 'none' ) {
        $(input).css('display', 'block');
      }
      else {
        $(input).css('display', 'none');
      }
    });

    $(document).on('click', '.like-btn', function(){
      if( $scope.checkLoginState() == false ) { return location.href = '/login'; }

      var likeStatus = $(this).data('like-status-json');
      var contentType = $(this).data('content-type');
      var contentID = $(this).data('content-id');
      var likeMeter_id = '#' + contentType.toLowerCase() + '-' + 'likemeter' + '-' + contentID;
      var likeMeter_elm = $(likeMeter_id);

      // console.log( likeStatus, contentType, $(likeMeter_elm) );

      var obj = {
        likeStatus: likeStatus,
        contentType: contentType,
        contentID: contentID,
        likeMeter_elm: likeMeter_elm,
        likes: parseInt( $(likeMeter_elm).text() ),
        og_elm: $(this)
      }

      $scope.likeAction(obj);

    });

    $(document).on('click', '.share-btn', function(){
      if( $scope.checkLoginState() == false ) { return location.href = '/login'; }

      var ask = confirm('Share This Content?');
      if( ask == false ) { return; }

      var contentType = $(this).data('content-type');
      var contentID = $(this).data('content-id');
      var fromType = $(this).data('from-type');
      var fromID = $(this).data('from-id');

      var obj = {
        contentType: contentType,
        contentID: contentID,
        fromType: fromType,
        fromID: fromID,
        og_elm: $(this)
      }

      $scope.shareAction(obj);

    });

    $(document).on('keyup', '.add-comment-box', function(e){
      if( e.keyCode != 13 ) {
        return;
      }
      if( $scope.checkLoginState() == false ) { return location.href = '/login'; }

      var input = $(this);
      var comment = trimTrailingSpaces( input.val() );

      var contentType = $(this).data('content-type');
      var contentID = $(this).data('content-id');
      var commentMeter_id = '#' + contentType.toLowerCase() + '-' + 'commentmeter' + '-' + contentID;
      var commentMeter_elm = $(commentMeter_id);

      var dataObj = {
        post_id: input.data('post-id'),
        post_type: input.data('post-type'),
        postOwner_id: input.data('owner-id'),
        postOwner_type: input.data('owner-type'),
        contentType: contentType,
        contentID: contentID,
        commentMeter_elm: commentMeter_elm,
        comments: parseInt( $(commentMeter_elm).text() ),
        og_elm: $(this)
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

    $(document).on('keyup', '.add-reply-box', function(e){
      if( e.keyCode != 13 ) {
        return;
      }
      if( $scope.checkLoginState() == false ) { return location.href = '/login'; }

      var input = $(this);
      var reply = trimTrailingSpaces( input.val() );

      var contentType = $(this).data('content-type');
      var contentID = $(this).data('content-id');
      var replyMeter_id = '#' + contentType.toLowerCase() + '-' + 'replymeter' + '-' + contentID;
      var replyMeter_elm = $(replyMeter_id);

      var dataObj = {
        comment_id: input.data('comment-id'),
        commentOwner_id: input.data('owner-id'),
        commenttOwner_type: input.data('owner-type'),
        contentType: contentType,
        contentID: contentID,
        replyMeter_elm: replyMeter_elm,
        replies: parseInt( $(replyMeter_elm).text() ),
        og_elm: $(this)
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

  });

  /*

    Angular

  */

  $scope.checkLoginState = function() {
    // console.log('admit one');
    if( $scope.you == undefined || $scope.you == null ) {
      return false;
    }
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
      var id = '#cmlst-' + dataObj.post_id;
      var elm = $(resp.data.comment_html);
      $(id).append(elm);
      $(inputELM).val('');
      $(dataObj.commentMeter_elm).text(resp.data.commentMeter);
      // $scope.applyNewLikeListeners(elm);
      // $scope.applyNewCommentListeners(elm);

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
      var id = '#rplst-' + dataObj.comment_id;
      var elm = $(resp.data.reply_html);
      $(id).append(elm);
      $(inputELM).val('');
      $(dataObj.replyMeter_elm).text(resp.data.replyMeter);
      // $scope.applyNewLikeListeners(elm);

    },
    function(resp){
      // Error Callback
      console.log(resp);
    });
  }

  $scope.likeAction = function(dataObj) {
    // console.log(dataObj);

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
        action: dataObj.likeStatus.action,
        info: dataObj,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }

    $http(req).then(function(resp){
      // Success Callback
      // console.log(resp);
      $(dataObj.og_elm).data('like-status-json', resp.data.likeStatus);
      $(dataObj.og_elm).removeClass(dataObj.likeStatus.class).addClass(resp.data.likeStatus.class);
      $(dataObj.og_elm).children('span.like-text').text(resp.data.likeStatus.text);
      $(dataObj.likeMeter_elm).text(resp.data.likeMeter);
    },
    function(resp){
      // Error Callback
      // console.log(resp);
    });
  }

  $scope.shareAction = function(dataObj) {

    $http({
      method: 'POST',
      url: '/action/ajax/',
      headers: {
        'Content-Type': 'application/json',
        'responseType': 'json',
        "Accept" : "application/json",
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: 'shareContent',
        info: dataObj,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }).then(function(resp){
      // Success Callback
      console.log('OK ---', resp);
      // $(dataObj.og_elm).data('like-status-json', resp.data.likeStatus);
      // $(dataObj.og_elm).removeClass(dataObj.likeStatus.class).addClass(resp.data.likeStatus.class);
      // $(dataObj.og_elm).children('span.like-text').text(resp.data.likeStatus.text);
      // $(dataObj.likeMeter_elm).text(resp.data.likeMeter);

      $('#postMsgModal-body').html('<p class="text-center">Content Shared To Your Wall!</p>');
      $('#postMsgModal').modal("show");

    },
    function(resp){
      // Error Callback
      // console.log(resp);
    });
  }

}])
