// User Settings

App.controller('settingsCtrl', ['$scope', function($scope) {

  window.scope = $scope;
  var wordsOnlyRegex = /^[a-zA-Z]{3,50}/;

  //

  $scope.interestsList = [];
  $scope.seekingList = [];

  //

  $(document).ready(function(){
    var csrftoken = Cookies.get('csrftoken');

    var obj = {
      action: 'load settings lists',
      csrfmiddlewaretoken: csrftoken,
    }

    $.ajax({
      url: '/user/settingsaction/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(obj),
      success: function(resp) {
        (function(){
          // console.log(resp);
          $scope.interestsList = resp.interests;
          $scope.seekingList = resp.seeking;

          $scope.$apply();
        })()
      }
    });
  });

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

    var csrftoken = Cookies.get('csrftoken');

    var obj = {
      bio: bio,
      action: 'update bio',
      csrfmiddlewaretoken: csrftoken,
    }

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
    /*else if( interest.indexOf(' ') != -1 ) {
      $scope.interestMsg = 'No Spaces In Interest Word.';
      return;
    }*/

    $scope.interestsList.push( interest );
    $scope.interestsList.sort();
    $scope.newInterest = '';
    $scope.interestMsg = 'New Interest Added!';

    setTimeout(function(){
      $scope.interestMsg = '';
      $scope.$apply();
    } , 3000)

    $scope.updateInterestsList();

  }

  //

  $scope.addNewSeeking = function() {

    if( $scope.seekingList.length > 20 ) {
      $scope.seekingMsg = 'The Max Is 20 Items.';
      return;
    }

    var seeking = $scope.newSeeking.toLowerCase();

    if( seeking == undefined || seeking == '' ) {
      $scope.seekingMsg = 'Please Input A Seeking Word';
      return;
    }
    else if( !wordsOnlyRegex.test(seeking) ) {
      $scope.seekingMsg = 'Seeking Words Must Be 3-25 Characters, Letters Only.';
      return;
    }
    else if( $scope.seekingList.indexOf(seeking) != -1 ) {
      $scope.seekingMsg = 'You Already Have This Seeking Word.';
      return;
    }
    /*else if( seeking.indexOf(' ') != -1 ) {
      $scope.seekingMsg = 'No Spaces In Seeking Word.';
      return;
    }*/

    $scope.seekingList.push( seeking );
    $scope.seekingList.sort();
    $scope.newSeeking = '';
    $scope.seekingMsg = 'New Seeking Added!';

    setTimeout(function(){
      $scope.seekingMsg = '';
      $scope.$apply();
    } , 3000)

    $scope.updateSeekingList();

  }

  //

  $scope.deleteListItem = function(item, msg) {
    if(msg == '' || msg == undefined) { return }

    if(msg == 'interest') {
      var index = $scope.interestsList.indexOf(item);
      $scope.interestsList.splice(index, 1);
      $scope.interestMsg = 'Interest Word Deleted!';
      $scope.editInterestForm = true;
      $scope.editInterest = '';

      setTimeout(function(){
        $scope.interestMsg = '';
        $scope.$apply();
      } , 3000)
      $scope.updateInterestsList();
    }
    else if(msg == 'seeking') {
      var index = $scope.interestsList.indexOf(item);
      $scope.seekingList.splice(index, 1);
      $scope.seekingMsg = 'Seeking Word Deleted!';
      $scope.editSeekingForm = true;
      $scope.editSeeking = '';

      setTimeout(function(){
        $scope.seekingMsg = '';
        $scope.$apply();
      } , 3000)
      $scope.updateSeekingList();
    }
  }

  //

  $scope.editInterestForm = true;
  $scope.editSeekingForm = true;

  $scope.cancelAddItem = function(msg) {
    if(msg == '' || msg == undefined) { return }

    if(msg == 'interest') {
      $scope.editInterestForm = true;
      $scope.editInterest = '';
    }
    else if(msg == 'seeking') {
      $scope.editSeekingForm = true;
      $scope.editSeeking = '';
    }
  }

  $scope.editInterestItem = function(item) {

      $scope.editInterestForm = false;
      $scope.editInterest = item;

      $scope.confirmEditInterest = function() {
        var update = $scope.editInterest.toLowerCase();

        if( update == undefined || update == '' ) {
          $scope.interestMsg = 'Please Input An Interest Word';
          return;
        }
        else if( !wordsOnlyRegex.test(update) ) {
          $scope.interestMsg = 'Interest Words Must Be 3-25 Characters, Letters Only.';
          return;
        }
        else if( $scope.interestsList.indexOf(update) != -1 ) {
          $scope.interestMsg = 'You Already Have This Interest Word.';
          return;
        }
        /*else if( update.indexOf(' ') != -1 ) {
          $scope.interestMsg = 'No Spaces In Seeking Word.';
          return;
        }*/

        var index = $scope.interestsList.indexOf(item);
        $scope.interestsList[index] = update;

        $scope.editInterest = '';
        $scope.interestMsg = 'Interest Edited!';
        $scope.editInterestForm = true;

        setTimeout(function(){
          $scope.interestMsg = '';
        } , 3000)

        $scope.updateInterestsList();

      }
  }


  $scope.editSeekingItem = function(item) {

      $scope.editSeekingForm = false;
      $scope.editSeeking = item;

      $scope.confirmEditSeeking = function() {
        var update = $scope.editSeeking.toLowerCase();

        if( update == undefined || update == '' ) {
          $scope.seekingMsg = 'Please Input A Seeking Word';
          return;
        }
        else if( !wordsOnlyRegex.test(update) ) {
          $scope.seekingMsg = 'Seeking Words Must Be 3-25 Characters, Letters Only.';
          return;
        }
        else if( $scope.interestsList.indexOf(update) != -1 ) {
          $scope.seekingMsg = 'You Already Have This Seeking Word.';
          return;
        }
        /*else if( update.indexOf(' ') != -1 ) {
          $scope.seekingMsg = 'No Spaces In Seeking Word.';
          return;
        }*/

        var index = $scope.seekingList.indexOf(item);
        $scope.seekingList[index] = update;

        $scope.editSeeking = '';
        $scope.seekingMsg = 'Interest Edited!';
        $scope.editSeekingForm = true;

        setTimeout(function(){
          $scope.seekingMsg = '';
        } , 3000)

        $scope.updateSeekingList();

      }
  }

  //

  $scope.updateInterestsList = function() {

    var l = '';
    for( var key in $scope.interestsList ) {
      l += $scope.interestsList[key] + ' ';
    }
    l = l.slice(0, -1);
    console.log(l);

    var csrftoken = Cookies.get('csrftoken');

    var obj = {
      str: l,
      action: 'update interests',
      csrfmiddlewaretoken: csrftoken,
    }

    $.ajax({
      url: '/user/settingsaction/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(obj),
      success: function(resp) {
        // console.log(resp);
        // $scope.$apply();
      }
    });

  }

  $scope.updateSeekingList = function() {

    var l = '';
    for( var key in $scope.seekingList ) {
      l += $scope.seekingList[key] + ' ';
    }
    l = l.slice(0, -1);
    console.log(l);

    var csrftoken = Cookies.get('csrftoken');

    var obj = {
      str: l,
      action: 'update seeking',
      csrfmiddlewaretoken: csrftoken,
    }

    $.ajax({
      url: '/user/settingsaction/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(obj),
      success: function(resp) {
        // console.log(resp);
        // $scope.$apply();
      }
    });

  }

  $scope.editDisplayName = function() {
    var regex = /[a-zA-z0-9]{2,30}/;
    if( !regex.test( $('#chg-dpn-form input[name="displayname"]').val() ) ) {
      alert('That isn\'t a good displayname. It must be letters and numbers, 2-30 characters.');
      return;
    }
    var ask = confirm('Are Changes Correct?');
    if( ask == true ) {
      $('#chg-dpn-form').submit();
    }
    else {
      // Do Nothing
    }
  }

  $scope.editAviLink = function() {

  }

  $scope.editWpLink = function() {

  }

}])
