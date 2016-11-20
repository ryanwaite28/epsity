// User Settings

App.controller('settingsCtrl', ['$scope', function($scope) {

  window.scope = $scope;
  var badChars = [
    '@', '#', '$', '%', '^',
    '^', '&', '*', '(', ')',
    '-', '_', '=', '+', '`',
    '~', '[', ']', '{', '}',
    '\\', '|', '/', '?', '.',
    ',', '<', '>'
  ];

  var wordsOnlyRegex = /^[a-zA-A]{3,25}/;

  //

  $scope.interestsList = [];
  $scope.seekingList = [];

  //

  $scope.deleteAccount = function() {
    var ask = confirm('Are you sure you want to delete your account? All of your info will be deleted. This action is irreversable.');
    if( ask == true ) {
      $('#deleteaccount-form').submit();
    }
    else {
      // Do Nothing
    }
  }

  //

  $scope.updateBioImg = true;
  $scope.updateBioBtn = false;
  $scope.updateAccountBio = function() {

    var form = $('#bio-form');
    var bio = $('#update-bio-content').val();
    console.log(bio);

    if( bio == '' || bio == undefined ) {
      var ask = confirm('Bio Was Left Empty/Blank. A Default Bio Will Be Added. Continue?');
      if( ask == false ) {
        return null;
      }
    }
    else if( bio.length > 150 ) {
      msg.text('Bio Is Too long...');
      setTimeout(function(){ msg.text(''); } , 3000 );
      return null;
    }

    var obj = {
      bio: bio,
      action: 'update bio',
      csrfmiddlewaretoken: csrftoken,
    }
    var csrftoken = Cookies.get('csrftoken');

    $scope.updateBioImg = false;
    $scope.updateBioBtn = true;

    $.ajax({
      url: '/user/settingsaction/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(obj),
      success: function(resp) {
        console.log(resp);
        $scope.updateBioImg = true;
        $scope.updateBioBtn = false;
        $scope.updateBioMsg = 'Update Successful!';
        $scope.$apply();
      }
    });
  }

  //

  $scope.addNewInterest = function() {

    if( $scope.interestsList.length >= 20 ) {
      $scope.interestMsg = 'The Max Is 20 Items.';
      return;
    }

    var interest = $scope.newInterest.toLowerCase();

    if( interest == undefined || interest == '' ) {
      $scope.interestMsg = 'Please Input An Interest Word';
      return;
    }
    else if( !wordsOnlyRegex.test(interest) ) {
      $scope.interestMsg = 'Interest Words Must Be 3-25 Characters, Letters Only.';
      return;
    }
    else if( $scope.interestsList.indexOf(interest) != -1 ) {
      $scope.interestMsg = 'You Already Have This Interest Word.';
      return;
    }

    $scope.interestsList.push( interest );
    $scope.interestsList.sort();
    $scope.newInterest = '';
    $scope.interestMsg = 'New Interest Added!';

    setTimeout(function(){
      $scope.interestMsg = '';
      $scope.$apply();
    } , 3000)

    var l = '';
    for( var key in $scope.interestsList ) {
      l += $scope.interestsList[key] + ' ';
    }

    console.log(l);

  }

  //

  $scope.addNewSeeking = function() {

    if( $scope.seekingList.length > 20 ) {
      $scope.seekingMsg = 'The Max Is 20 Items.';
      return;
    }

    var seeking = $scope.newSeeking.toLowerCase();

    if( seeking == undefined || seeking == '' ) {
      $scope.seekingMsg = 'Please Input An Interest Word';
      return;
    }
    else if( !wordsOnlyRegex.test(seeking) ) {
      $scope.seekingMsg = 'Interest Words Must Be 3-25 Characters, Letters Only.';
      return;
    }
    else if( $scope.seekingList.indexOf(seeking) != -1 ) {
      $scope.seekingMsg = 'You Already Have This Seeking Word.';
      return;
    }

    $scope.seekingList.push( seeking );
    $scope.seekingList.sort();
    $scope.newSeeking = '';
    $scope.seekingtMsg = 'New Seeking Added!';

    setTimeout(function(){
      $scope.seekingMsg = '';
      $scope.$apply();
    } , 3000)

    var l = '';
    for( var key in $scope.seekingList ) {
      l += $scope.seekingList[key] + ' ';
    }

    console.log(l);

  }

}])
