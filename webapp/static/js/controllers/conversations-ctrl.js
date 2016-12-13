// User Settings

App.controller('conversationsCtrl', ['$scope', '$http', function($scope, $http) {

  window.scope = $scope;
  var regexOne = /^[a-zA-Z0-9\-\_\!\@\#\$\%\^\&\*\(\)\=\+\{\[\}\]\:\;\'\"\,\<\.\>\/\/\?]{2,475}/;

  //

  $scope.currentlyChattingWith = '';

  $scope.loadConversations = function() {
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
        action: 'loadConversations',
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      $scope.conversations = resp.data.conversations;
      $scope.you = resp.data.you;
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });
  }
  $scope.loadConversations();

  //

  $scope.sendmsgForm = true;

  $scope.getConversation = function(convo) {
    console.log(convo);
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
        action: 'getConversation',
        convo: convo,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      $scope.currentConversation = resp.data.convo;

      $scope.sendmsgForm = false;

    },
    function(resp){
      // Error Callback
      console.log(resp);
    });
  }

  //

  $scope.sendGroupMessage = function() {
    if( $scope.messageContents == '' ) {
      return;
    }
    if( !regexOne.test($scope.messageContents) ) {
      alert('Message Body Must: \
      \n\nNot Be Blank; \
      \nBe At Least 3 Characters; \
      \nNo More Than 475 Characters;');
      return;
    }

    $('#sendgroupmsg-form > input[name="origin"]').val( location.pathname );
    $('#sendgroupmsg-form > input[name="convoid"]').val( $scope.currentConversation.conversation.convo_id );
    $('#sendgroupmsg-form').submit();

  }

  $scope.sendMessageTwo = function() {
    if( $scope.you.userid == $scope.currentMessages.userA_id ) {
      var sender_id = $scope.currentMessages.userA_id;
      var recipient_id = $scope.currentMessages.userB_id;
    }
    else {
      var sender_id = $scope.currentMessages.userB_id;
      var recipient_id = $scope.currentMessages.userA_id;
    }

    console.log('sender_id', sender_id);
    console.log('recipient_id', recipient_id);
    console.log('you', $scope.you);

    if( $scope.messageContents == '' ) {
      return;
    }
    if( !regexOne.test($scope.messageContents) ) {
      alert('Message Body Must: \
      \n\nNot Be Blank; \
      \nBe At Least 3 Characters; \
      \nNo More Than 475 Characters;');
      return;
    }

    $('#sendmsg-form > input[name="origin"]').val( location.pathname );
    $('#sendmsg-form > input[name="senderid"]').val( sender_id );
    $('#sendmsg-form > input[name="recipientid"]').val( recipient_id );
    $('#sendmsg-form').submit();

  }

  $scope.showMsgAttachment = function(obj) {

    // console.log(obj);
    var modalBody = $('#modal-body');
    var splitter = obj.attachment.split('.');
    var extension = splitter[ splitter.length - 1 ].toLowerCase();

    // modalBody.html('');

    if( obj.attachment[0] == '' ) {
      obj.attachment
    }

    if( obj.attachment_type == 'photo' ) {
      modalBody.html(" \
      <img class=\"middlr max-w\" src=\"" + obj.attachment + "\"/> \
      ");
      $('#attachmentModal').modal('show');
    }

    if( obj.attachment_type == 'video' ) {
      modalBody.html(" \
      <video id=\"video-1\"  class=\"middlr max-w\" controls> \
        <source src=\" " + obj.attachment + " \" type=\"video/" + extension + "\"> \
      </audio> \
      ");
      $('#attachmentModal').modal('show');
      // document.getElementById('video-1').play();
    }

    if( obj.attachment_type == 'audio' ) {
      modalBody.html(" \
      <audio id=\"audio-1\" class=\"middlr max-w\" controls> \
        <source src=\" " + obj.attachment + " \" type=\"audio/" + extension + "\"> \
      </audio> \
      ");
      $('#attachmentModal').modal('show');
      // document.getElementById('audio-1').play();
    }

  }

}])
