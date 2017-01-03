// User Settings

App.controller('newPostsCtrl', ['$scope', '$http', function($scope, $http) {

  window.scope = $scope;

  $(document).ready(function(){

    $('select#newpost-type').change(function(){
      if( $(this).val() == 'Text' ) {
        $('input[name="media"]').val('');
        $('input[name="media"]').hide();
      }
      else {
        $('input[name="media"]').val('');
        $('input[name="media"]').show();
      }
    });

  });

  /*

    Angular

  */

  $scope.checkMedia = function(){

    var mediaType = $('select#newpost-type').val();
    var media  = document.querySelector('input[name="media"]');

    var splitter = media.value.split('.');
    var extension = splitter[ splitter.length - 1 ].toLowerCase();
    console.log(splitter, extension);

    var pFile = ['png', 'jpg', 'jpeg', 'gif'];
    var vFile = ['mp4', 'avi', 'mov', 'webm', 'oog'];
    var aFile = ['mp3', 'wav'];

    if( mediaType == 'Text' ) {
      return true;
    }
    else if( mediaType == 'Photo' ) {
      if( pFile.indexOf(extension) == -1 ) {
        return false;
      }
    }
    else if( mediaType == 'Video' ) {
      if( vFile.indexOf(extension) == -1 ) {
        return false;
      }
    }
    else if( mediaType == 'Audio' ) {
      if( aFile.indexOf(extension) == -1 ) {
        return false;
      }
    }

  }

  $scope.createUserPost = function() {
    var check = $scope.checkMedia();
    if( check == false ) {
      alert('File Not Accepted.');
      return;
    }

    if( $('#new-user-post-form input[name="title"]').val().trim() == "" ) {
      alert('Post Title Cannot Be Blank.');
      return;
    }
    else if( $('#new-user-post-form textarea').val().trim() == "" ) {
      alert('Post Body Cannot Be Blank.');
      return;
    }

    $('#new-user-post-form input[name="origin"]').val( location.pathname );
    // $('#new-user-post-form').submit();

    var form = document.getElementById('new-user-post-form');
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
      console.log(resp);

      var elm = $(resp.data.post_html);
      $(elm).hide().prependTo('#allposts-div').fadeIn('fast');

      $('#new-user-post-form input[name="title"]').val('');
      $('#new-user-post-form textarea').val('');
      $('#new-user-post-form input[name="link"]').val('');
      $('#new-user-post-form input[name="media"]').val('');

      $('#new-post-div').removeClass('in');
      $('#newpost-arrow').toggleClass('rotate');

      $('#sample-post-div').hide();
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

  }

  $scope.createGroupPost = function() {
    var check = $scope.checkMedia();
    if( check == false ) {
      alert('File Not Accepted.');
      return;
    }

    if( $('#new-group-post-form input[name="title"]').val().trim() == "" ) {
      alert('Post Title Cannot Be Blank.');
      return;
    }
    else if( $('#new-group-post-form textarea').val().trim() == "" ) {
      alert('Post Body Cannot Be Blank.');
      return;
    }

    $('#new-group-post-form input[name="origin"]').val( location.pathname );
    // $('#new-group-post-form').submit();

    var form = document.getElementById('new-group-post-form');
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
      console.log(resp);

      var elm = $(resp.data.post_html);
      $(elm).hide().prependTo('#allposts-div').fadeIn('fast');

      $('#new-group-post-form input[name="title"]').val('');
      $('#new-group-post-form textarea').val('');
      $('#new-group-post-form input[name="link"]').val('');
      $('#new-group-post-form input[name="media"]').val('');

      $('#new-post-div').removeClass('in');
      $('#newpost-arrow').toggleClass('rotate');

      $('#sample-post-div').hide();
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });

  }

}])
