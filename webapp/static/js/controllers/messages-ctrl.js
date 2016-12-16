// User Settings

App.controller('messagesCtrl', ['$scope', '$http', function($scope, $http) {

  window.scope = $scope;
  var regexOne = /^[a-zA-Z0-9\-\_\!\@\#\$\%\^\&\*\(\)\=\+\{\[\}\]\:\;\'\"\,\<\.\>\/\/\?]{2,475}/;

  //

  $(document).ready(function(){
    $(document).on('click', '.attachment-btn', function(){
      // console.log(this);

      var obj = {
        attachment: $(this).data('attachment-link'),
        attachment_type: $(this).data('attachment-type').toLowerCase()
      }

      $scope.showMsgAttachment(obj);
    });
  });

  $scope.currentlyChattingWith = '';

  $scope.loadMessages = function() {
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
        action: 'load messages',
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      // console.log(resp);
      $scope.messages = resp.data.messages;
      $scope.you = resp.data.you;
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });
  }
  $scope.loadMessages();

  //

  $scope.sendmsgForm = true;
  $scope.openMessages = function(msg) {
    $scope.sendmsgForm = false;
    $scope.currentMessages = msg;
    if( $scope.you.userid == msg.userA_id ) {
      $scope.currentlyChattingWith = msg.userB_rel.uname;
    }
    else {
      $scope.currentlyChattingWith = msg.userA_rel.uname;
    }

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
        action: 'loadMessageReplies',
        mid: msg.mid,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      // console.log(resp);
      $scope.currentMessages.replies = resp.data.replies;
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });
  }

  //

  $scope.sendMessage = function(sender_id, recipient_id) {
    // console.log('sender_id', sender_id);
    // console.log('recipient_id', recipient_id);

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
    // $('#sendmsg-form').submit();

    var form = document.getElementById('sendmsg-form');
    var formData = new FormData( form );

    $http({
      method: 'POST',
      url: '/action/form/',
      headers: {
        'Content-Type': undefined,
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      processData: false,
      data: formData
    }).then(function(resp){
      // Success Callback
      // console.log(resp);
      alert('Message Sent!');
      $scope.messageContents = '';
      $('#sendmsg-form > input[name="media"]').val('');
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

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

    // console.log('sender_id', sender_id);
    // console.log('recipient_id', recipient_id);
    // console.log('you', $scope.you);

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
    // $('#sendmsg-form').submit();

    var form = document.getElementById('sendmsg-form');
    var formData = new FormData( form );

    $http({
      method: 'POST',
      url: '/action/form/',
      headers: {
        'Content-Type': undefined,
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      processData: false,
      data: formData
    }).then(function(resp){
      // Success Callback
      // console.log(resp);
      $scope.currentMessages.replies.push(resp.data.reply);
      $scope.messageContents = '';
      $('#sendmsg-form > input[name="media"]').val('');
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

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
