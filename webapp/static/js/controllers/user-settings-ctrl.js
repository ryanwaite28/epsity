// User Settings

App.controller('settingsCtrl', ['$scope', '$http', function($scope, $http) {

  window.scope = $scope;
  var wordsOnlyRegex = /^[a-zA-Z]{3,50}/;

  //

  $scope.interestsList = [];
  $scope.seekingList = [];
  $scope.groupsList = [];

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
          console.log(resp);
          $scope.interestsList = resp.interests;
          $scope.seekingList = resp.seeking;
          $scope.groupsList = resp.groups;

          $scope.$apply();
        })()
      }
    });

    $(document).keyup(function(e){
      if( e.keyCode == 13 ) {
        // Find Which Input Is In Focus.
        if( $('input[name="newgroupcat"]').is(':focus') ) {
          $scope.addEditGroupCategory();
          $scope.$apply();
        }

      }
    });
  });

  // --- //

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

  $scope.editAccountStatus = function() {
    var ask = confirm('Are Changes Correct?');
    if( ask == true ) {
      $('#chg-accountstatus-form').submit();
    }
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
      l += $scope.interestsList[key] + ';';
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
      l += $scope.seekingList[key] + ';';
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

  // true = hide | false = show

  $scope.groupsView = false;

  $scope.groupEditor = true;
  $scope.groupAddMemberEditor = true;
  $scope.categoryEditor = true;

  $scope.editGroup = {};
  $scope.goodGroupUserName = true;

  $scope.openGroupEditor = function(group) {
    // console.log(group);
    $scope.groupsView = true;
    $scope.groupEditor = false;
    $scope.groupAddMemberEditor = true;

    $scope.editGroup = group;

    $('#edit-groupdisplayname').val($scope.editGroup.displayname);
    $('#edit-groupuname').val($scope.editGroup.uname);
    $('#edit-groupdesc').val($scope.editGroup.desc);

    backToTop();
  }
  $scope.cancelGroupEditor = function() {
    $scope.groupsView = false;
    $scope.groupEditor = true;
    $scope.groupAddMemberEditor = true;

    $scope.editGroup = {};
  }

  $scope.addEditGroupCategory = function() {
    if( $scope.editGroup.categories.length >= 25 ) {
      alert('The Max Amount Of Categories Is 25.');
      return;
    }
    if( $scope.newEditGroupCategory == '' ) {
      return;
    }
    if( $scope.editGroup.categories.indexOf($scope.newEditGroupCategory.toLowerCase().split(' ').join('')) != -1 ) {
      alert('That Is Already A Category.');
      return;
    }
    if( !catCheck.test($scope.newEditGroupCategory) ) {
      alert('Please Use Letters & Numbers Only, 3-25 Characters Long.');
      return;
    }
    if($scope.newEditGroupCategory.substring($scope.newEditGroupCategory.length - 1) == ' ') {
      alert('Please Remove Any Trailing Space.');
      return;
    }

    $scope.editGroup.categories.push($scope.newEditGroupCategory.toLowerCase().split(' ').join(''));
    $scope.editGroup.categories.sort();
    $scope.newEditGroupCategory = '';
  }

  $scope.editGroupCategory = function(category) {
    console.log(category);
    $scope.categoryEditor = false;
    $scope.groupCategoryEditName = category;
    $scope.returnEditGroupCategory = function() {
      if( $scope.groupCategoryEditName == '' ) {
        return;
      }
      else if( $scope.editGroup.categories.indexOf($scope.groupCategoryEditName.toLowerCase().split(' ').join('')) != -1 ) {
        alert('That Is Already A Category.');
        return;
      }
      else if( !alphaNumeric.test($scope.groupCategoryEditName) ) {
        alert('Please Use Letters Only, 3-25 Characters Long.');
        return;
      }
      else if($scope.groupCategoryEditName.substring($scope.groupCategoryEditName.length - 1) == ' ') {
        alert('Please Remove Any Trailing Space.');
        return;
      }
      var index = $scope.editGroup.categories.indexOf(category);
      $scope.editGroup.categories[index] = $scope.groupCategoryEditName;
      $scope.editGroup.categories.sort();
      $scope.groupCategoryEditName = '';
      $scope.categoryEditor = true;
    }
  }
  $scope.cancelEditGroupCategory = function() {
    $scope.groupCategoryEditName = '';
    $scope.categoryEditor = true;
  }

  $scope.deleteGroupCategory = function(category) {
    console.log(category);
    var index = $scope.editGroup.categories.indexOf(category);
    $scope.editGroup.categories.splice(index, 1);
    $scope.editGroup.categories.sort();
  }

  $scope.checkGroupUserName = function() {
    var groupDisplayName = $('#edit-groupdisplayname').val().toLowerCase();
    var groupUserName = $('#edit-groupuname').val().toLowerCase();

    if(groupDisplayName.substring(groupDisplayName.length - 1) == ' ') {
      alert('Please Remove Any Trailing Space From The Group Display Name Field.');
      return;
    }
    if(groupUserName.substring(groupUserName.length - 1) == ' ') {
      alert('Please Remove Any Trailing Space From The Group UserName Field.');
      return;
    }
    if( !alphaNum_one.test(groupDisplayName) ) {
      alert('Group Display Name Must Be Lettters & Numbers, 3-25 Characters.');
      $scope.goodGroupUserName = false;
      return;
    }
    if( !alphaNum_two.test( groupUserName ) ) {
      alert('Group UserName Must Be Lettters, Numbers, dashes, and/or underscores, 3-25 Characters.');
      $scope.goodGroupUserName = false;
      return;
    }
    if ( groupUserName == $scope.editGroup.uname.toLowerCase() ) {
      $scope.goodGroupUserName = true;
      $scope.confirmGroupEdits();
    }
    if( groupUserName != $scope.editGroup.uname.toLowerCase() ) {
      $.ajax({
        url: '/checkpoint/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
          groupUserName: groupUserName,
          action: 'check group uname',
          csrfmiddlewaretoken: Cookies.get('csrftoken'),
        }),
        success: function(resp) {
          console.log(resp);
          if( resp.msg == 'taken' ) {
            $scope.goodGroupUserName = false;
            alert('Sorry, That Group UserName Is Taken.');
          }
          else {
            $scope.goodGroupUserName = true;
            $scope.confirmGroupEdits();
          }
        }
      });
    }
  }

  $scope.confirmGroupEdits = function() {
    if( $('#edit-groupdesc').val().length > 275 ) {
      alert('Group Description Must Not Exceed 275 Characters.');
      return;
    }

    var ask = confirm('Are These Edits Correct?');
    if( ask == true ) {
      if( $scope.goodGroupUserName == false ) {
        alert('Group UserName Must Be Changed (Unavailable Or Invalid).');
        return;
      }
      else {
        $scope.saveGroupEdits();
      }
    }
  }

  $scope.saveGroupEdits = function() {
    var catString = '';
    for( var key in $scope.editGroup.categories ) {
      catString += $scope.editGroup.categories[key] + ';';
    }
    catString = catString.slice(0, -1);

    $('#edit-groupid').val($scope.editGroup.gid);
    $('#edit-groupcategories').val(catString);
    $('#edit-group-form').submit();
  }

  //

  $scope.openGroupAddMemberEditor = function(group) {
    // console.log(group);
    $scope.groupsView = true;
    $scope.groupEditor = true;
    $scope.groupAddMemberEditor = false;

    $scope.editGroup = group;

    backToTop();
  }
  $scope.cancelGroupAddMemberEditor = function() {
    $scope.groupsView = false;
    $scope.groupEditor = true;
    $scope.groupAddMemberEditor = true;

    $scope.editGroup = {};
  }

  $scope.searchForMembers = function() {
    var req = {
      method: 'POST',
      url: '/search/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: JSON.stringify({
        action: 'search for members',
        gid: $scope.editGroup.gid,
        limit: 10,
        query: $scope.searchQuery,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      })
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      $scope.srMembersList = resp.data.users;
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });
  }

  //

  $scope.groupAction = function(user) {
    console.log(user);
    var req = {
      method: 'POST',
      url: '/action/',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: {
        action: user.action,
        user: user,
        group: $scope.editGroup,
        csrfmiddlewaretoken: Cookies.get('csrftoken'),
      }
    }
    $http(req).then(function(resp){
      // Success Callback
      console.log(resp);
      if(resp.data.status == 'pending') {
        user.status = 'pending invite';
        user.btn = 'default';
        user.msg = 'Pending';
        user.action = 'cancelPendingGroupInvite';
        user.title = 'Cancel Pending Group Invite';
      }
      else if(resp.data.status == 'not a member') {
        user.status = 'not a member';
        user.btn = 'success';
        user.msg = 'Send Group Invite';
        user.action = 'sendGroupInvitation';
        user.title = 'Send Group Invite';
      }
      else if(resp.data.status == 'currently a member') {
        user.status = 'currently a member';
        user.btn = 'danger';
        user.msg = 'Remove Member';
        user.action = 'removeMember';
        user.title = 'Remove From Group';
      }
    },
    function(resp){
      // Error Callback
      console.log(resp);
    });
  }

  //

  $scope.deleteGroup = function(group) {

    var ask = confirm('Are You Sure You Want To Delete This Group? \
    All Information Relating To This Group Will Be Deleted. \
    Changes Are Irreversible.');

    if( ask == true ) {
      $('#delete-group-form input[name="gid"]').val(group.gid);
      $('#delete-group-form').submit();
    }
  }

}])
