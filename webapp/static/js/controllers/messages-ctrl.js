// User Settings

App.controller('messagesCtrl', ['$scope', '$http', function($scope, $http) {

  window.scope = $scope;
  var regexOne = /^[a-zA-Z0-9\-\_\!\@\#\$\%\^\&\*\(\)\=\+\{\[\}\]\:\;\'\"\,\<\.\>\/\/\?]{3,475}/;

  //

  $scope.loadMessages = function() {
    var req = {
      method: 'POST',
      url: '/action/',
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
      console.log(resp);
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

  $scope.openMessages = function(msg) {
    $scope.currentMessages = msg;
  }

  //

  $scope.sendMessage = function(sender_id, recipient_id) {
    console.log('sender_id', sender_id);
    console.log('recipient_id', recipient_id);

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

}])
