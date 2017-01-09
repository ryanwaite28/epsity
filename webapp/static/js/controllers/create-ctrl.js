// User Settings

// function initMap() {
//
//   var map = new google.maps.Map(document.getElementById('map'), {
//     center: {lat: -34.397, lng: 150.644},
//     scrollwheel: true,
//     zoom: 8
//   });
//
//   window.map = map;
//
// }

App.controller('createCtrl', ['$scope', '$http', function($scope, $http) {

	window.scope = $scope;
	var wordsOnlyRegex = /^[a-zA-Z0-9]{3,50}/;
	var priceREG = /^[0-9]{1,}.[0-9]{2}$/;

	$scope.today = Date();
	$scope.todaySplitted = Date().split(' ');

	window.initMap = function() {

		var mapOptions = {
			center: {
				lat: -33.8688,
				lng: 151.2195
			},
			zoom: 13,
			scrollwheel: false
		};
		var map = new google.maps.Map(document.getElementById('map'),
			mapOptions);

		var input = /** @type {HTMLInputElement} */ (
			document.getElementById('pac-input'));

		// Create the autocomplete helper, and associate it with
		// an HTML text input box.
		var autocomplete = new google.maps.places.Autocomplete(input);
		autocomplete.bindTo('bounds', map);

		map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

		var infowindow = new google.maps.InfoWindow();
		var marker = new google.maps.Marker({
			map: map
		});
		google.maps.event.addListener(marker, 'click', function() {
			infowindow.open(map, marker);
		});

		// Get the full place details when the user selects a place from the
		// list of suggestions.
		google.maps.event.addListener(autocomplete, 'place_changed', function() {
			infowindow.close();
			var place = autocomplete.getPlace();
			if (!place.geometry) {
				return;
			}

			if (place.geometry.viewport) {
				map.fitBounds(place.geometry.viewport);
			} else {
				map.setCenter(place.geometry.location);
				map.setZoom(17);
			}

			// Set the position of the marker using the place ID and location.
			marker.setPlace( /** @type {!google.maps.Place} */ ({
				placeId: place.place_id,
				location: place.geometry.location
			}));
			marker.setVisible(true);

			infowindow.setContent('<div><strong>' + place.name + '</strong><br>' +
				'Place ID: ' + place.place_id + '<br>' +
				place.formatted_address + '</div>');
			infowindow.open(map, marker);

			$('input[name="eventplace"]').val( place.name );
			$('input[name="eventlocation"]').val( place.formatted_address );
		});

		//

		google.maps.event.addListener(map, 'click', function(e) {
			console.log(e, this);
		});

	}

  //

  $scope.months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
  ];

  $scope.monthDays = {
    January: [01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    February: [01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
    March: [01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    April: [01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    May: [01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    June: [01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    July: [01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    August: [01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    September: [01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    October: [01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    November: [01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    December: [01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
  }

	$scope.currentSelectedMonthS = $scope.monthDays.January;
	$scope.currentSelectedMonthE = $scope.monthDays.January;

	$('select[name="startmonth"]').change(function(){
		$scope.currentSelectedMonthS = $scope.monthDays[ $(this).val().toString() ];
		$scope.$apply();
	})
	$('select[name="endmonth"]').change(function(){
		$scope.currentSelectedMonthE = $scope.monthDays[ $(this).val().toString() ];
		$scope.$apply();
	})

  $scope.currentStartDateTime = '';
  $scope.currentEndDateTime = '';

	var currentYear = parseInt( Date().split(' ')[3] );
	$scope.years = [];
	for(var i = currentYear; i < currentYear + 21; i++ ) {
		$scope.years.push( i );
	}

	$scope.hours = [];
	for( var l = 1; l <= 12; l++ ) {
		var v = l.toString();
		if( v.length == 1 ) {
			v = "0" + v;
		}
		$scope.hours.push( v );
	}

	$scope.minutes = [];
	for( var k = 0; k <= 60; k++ ) {
		var v = k.toString();
		if( v.length == 1 ) {
			v = "0" + v;
		}
		$scope.minutes.push( v );
	}

	$scope.checkNewEventDates = function() {
		var startMonth = $('select[name="startmonth"]').val();
		var startDay = $('select[name="startday"]').val();
		var startYear = $('select[name="startyear"]').val();
		var startHour = $('select[name="starthour"]').val();
		var startMinute = $('select[name="startminute"]').val();
		var startTime = $('select[name="starttime"]').val();

		var endMonth = $('select[name="endmonth"]').val();
		var endDay = $('select[name="endday"]').val();
		var endYear = $('select[name="endyear"]').val();
		var endHour = $('select[name="endhour"]').val();
		var endMinute = $('select[name="endminute"]').val();
		var endTime = $('select[name="endtime"]').val();

		var startDateTimeString = startMonth + ' ' + startDay + ', ' + startYear + ' - ' + startHour + ':' + startMinute + ' ' + startTime;
		var endDateTimeString = endMonth + ' ' + endDay + ', ' + endYear + ' - ' + endHour + ':' + endMinute + ' ' + endTime;

		var startDateTime = new Date(startMonth + ' ' + startDay + ', ' + startYear + ' ' + startHour + ':' + startMinute + ' ' + startTime);
		var endDateTime = new Date(endMonth + ' ' + endDay + ', ' + endYear + ' ' + endHour + ':' + endMinute + ' ' + endTime);

		$scope.currentStartDateTime = startDateTime.toString().substring(0,3) + ' | ' + startDateTimeString;
		$scope.currentEndDateTime =  endDateTime.toString().substring(0,3) + ' | ' + endDateTimeString;


		if( startDateTime >= endDateTime ) {
			console.log('ERROR');
			alert('The Start Date & Time Cannot Be The Same As Or After The End Date & Time');
			return false;
		}
		else {
			console.log('OK');
			return true;
		}

	}

  //

  $scope.createEvent = function() {
    var timeRegex = /^[0-9]{2}:[0-9]{2} (AM|PM)$/;
		var yearRegex = /^[0-9]{4}$/;

		var name = trimTrailingSpaces($('#create-event-form input[name="eventname"]').val());
		var place = trimTrailingSpaces($('#create-event-form input[name="eventplace"]').val());
		var location = trimTrailingSpaces($('#create-event-form input[name="eventlocation"]').val());
		var desc = trimTrailingSpaces($('#create-event-form textarea[name="eventdescription"]').val());

		if( name.length < 7 ) {
			alert('Please Give A Descriptive Event Name.');
			return;
		}
		if( desc.length < 10 ) {
			alert('Please Give A Descriptive Event Description.');
			return;
		}
		if( place == '' || location == '' || place == undefined || location == undefined ) {
			alert('Place And Location Is Required.');
			return;
		}

		var checkDates = $scope.checkNewEventDates();
		if(checkDates == false) {
			return;
		}

		$('#create-event-form input[name="eventplace"]').prop('disabled', false);
		$('#create-event-form input[name="eventlocation"]').prop('disabled', false);
		$('#create-event-form input[name="origin"]').val( '/create/' );
		$('#create-event-form input[name="startfull"]').val( $scope.currentStartDateTime );
		$('#create-event-form input[name="endfull"]').val( $scope.currentEndDateTime );

		$('#create-event-form').submit();
  }

	$scope.createGroup = function() {
		if (!alphaNum_two.test($('input[name="displayname"]').val())) {
			alert('Group Display Name Must Be Lettters, Numbers, dashes, and/or underscores, 3-25 Characters.');
			return;
		}
		if (!alphaNum_two.test($('input[name="uname"]').val())) {
			alert('Group UserName Must Be Lettters, Numbers, dashes, and/or underscores, 3-25 Characters.');
			return;
		}
		if ($('input[name="displayname"]').val().substring($('input[name="displayname"]').val().length - 1) == ' ') {
			alert('Please Remove Any Trailing Space From The Group Display Name Field.');
			return;
		}
		if ($('input[name="uname"]').val().substring($('input[name="displayname"]').val().length - 1) == ' ') {
			alert('Please Remove Any Trailing Space From The Group UserName Field.');
			return;
		}

		var ask = confirm('Are all fields corrects?');
		if (ask == true) {
			$('#create-group-form input[name="origin"]').val( location.pathname );
			$('#create-group-form input[name="action"]').val( 'createGroup' );
			$('#create-group-form').submit();
		}

	}

	$scope.searchUsers = function() {
		if ($scope.searchQuery == '') {
			return;
		} else if (!alphaNumeric.test($scope.searchQuery)) {
			alert('Alphanumeric Query Only (Letters & Numbers).');
			return;
		}

		var req = {
			method: 'POST',
			url: '/search/',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': Cookies.get('csrftoken')
			},
			data: {
				action: 'searchUsers',
				query: $scope.searchQuery,
				csrfmiddlewaretoken: Cookies.get('csrftoken'),
			}
		}
		$http(req).then(function(resp) {
				// Success Callback
				console.log(resp);

				$scope.srUsers = resp.data.users;
				$scope.srGroups = resp.data.groups;
			},
			function(resp) {
				// Error Callback
				console.log(resp);
			});

	}

	$scope.selectedConvoMembers = [];
	$scope.addToSelected = function(user) {
		if ($scope.selectedConvoMembers.indexOf(user) != -1) {
			// alert('That user is already selected.');
			return;
		}
		$scope.selectedConvoMembers.push(user);
	}
	$scope.removeSelected = function(user) {
		var index = $scope.selectedConvoMembers.indexOf(user);
		$scope.selectedConvoMembers.splice(index, 1);
	}
	$scope.checkConvoName = function() {
		if ($scope.newConvoName == undefined) {
			alert('Conversation Name Is Needed.');
			return;
		} else if ($scope.newConvoName.length == 0) {
			alert('Conversation Name Is Needed.');
			return;
		} else if ($scope.newConvoName.trim().length == 0) {
			alert('Conversation Name Is Needed.');
			return;
		} else if ($scope.newConvoName.replace(/(\s+|\s+$)/g, " ").trim().length <= 2) {
			alert('Conversation must be at least 3 characters.');
			return;
		}

		var req = {
			method: 'POST',
			url: '/checkpoint/',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': Cookies.get('csrftoken')
			},
			data: {
				action: 'checkConvoName',
				name: $scope.newConvoName.replace(/(\s+|\s+$)/g, " ").trim(),
				csrfmiddlewaretoken: Cookies.get('csrftoken'),
			}
		}
		$http(req).then(function(resp) {
				// Success Callback
				// console.log(resp);

				if (resp.data.msg == 'available') {
					$scope.createGroupConvo();
				}

			},
			function(resp) {
				// Error Callback
				console.log(resp);
		});
	}
	$scope.createGroupConvo = function() {

		if ($scope.selectedConvoMembers.length <= 0) {
			alert('There needs to be at least 1 member to create the group conversation.');
			return;
		}

		var req = {
			method: 'POST',
			url: '/action/ajax/',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': Cookies.get('csrftoken')
			},
			data: {
				action: 'createGroupConvo',
				name: $scope.newConvoName.replace(/(\s+|\s+$)/g, " ").trim(),
				members: $scope.selectedConvoMembers,
				csrfmiddlewaretoken: Cookies.get('csrftoken'),
			}
		}
		$http(req).then(function(resp) {
				// Success Callback
				console.log(resp);
				alert(resp.data.msg);
				location.reload();
			},
			function(resp) {
				// Error Callback
				console.log(resp);
		});

	}

	$scope.productCategories = [];
	$scope.addProductCategory = function() {
		if( $scope.productCategories.length >= 10 ) {
      $scope.pText = 'The Max Is 10.';
      return;
    }

    var category = $scope.newProductCategory.toLowerCase();

    if( category == undefined || category == '' ) {
      $scope.interestMsg = 'Please Input An Interest Word';
      return;
    }
    else if( !wordsOnlyRegex.test(category) ) {
      $scope.interestMsg = 'Interest Words Must Be 3-25 Characters, Letters Only.';
      return;
    }
    else if( $scope.productCategories.indexOf(category) != -1 ) {
      $scope.interestMsg = 'You Already Have This Interest Word.';
      return;
    }

    $scope.productCategories.push( category );
    $scope.productCategories.sort();
    $scope.newProductCategory = '';

	}
	$scope.deleteProductCategory = function(obj) {

		var index = $scope.productCategories.indexOf( obj );
		$scope.productCategories.splice( index, 1 );

	}

	//

	$scope.serviceCategories = [];
	$scope.addServiceCategory = function() {
		if( $scope.serviceCategories.length >= 10 ) {
      $scope.sText = 'The Max Is 10.';
      return;
    }

    var category = $scope.newServiceCategory.toLowerCase();

    if( category == undefined || category == '' ) {
      $scope.interestMsg = 'Please Input An Interest Word';
      return;
    }
    else if( !wordsOnlyRegex.test(category) ) {
      $scope.interestMsg = 'Interest Words Must Be 3-25 Characters, Letters Only.';
      return;
    }
    else if( $scope.serviceCategories.indexOf(category) != -1 ) {
      $scope.interestMsg = 'You Already Have This Interest Word.';
      return;
    }

    $scope.serviceCategories.push( category );
    $scope.serviceCategories.sort();
    $scope.newServiceCategory = '';

	}
	$scope.deleteServiceCategory = function(obj) {

		var index = $scope.serviceCategories.indexOf( obj );
		$scope.serviceCategories.splice( index, 1 );

	}

	$scope.createProduct = function() {
		var productName = trimTrailingSpaces( $('#create-product-form input[name="name"]').val() );
		var productDesc = trimTrailingSpaces( $('#create-product-form textarea').val() );
		var productPrice = trimTrailingSpaces( $('#create-product-form input[name="price"]').val() );

		if( !wordsOnlyRegex.test(productName) ) {
			alert('Product Name Must Be 3-50 Characters; \n \
			Letters & Numbers Only.');
			return;
		}
		if( !priceREG.test(productPrice) ) {
			alert('Price Must Be In This Format: 0.00; \n \
			The Number Before The Period Can Be Any Amount Of Digits \
			But The Number After The Period Can Only Be 2 Digits.');
			return;
		}

		while(productPrice.charAt(0) === '0'){
    	productPrice = productPrice.substr(1);
		}

		var ask = confirm('Are All Fields Correct?');
		if( ask == true ) {
			var l = '';
	    for( var key in $scope.productCategories ) {
	      l += $scope.productCategories[key] + ';';
	    }
	    l = l.slice(0, -1);

			$('#create-product-form input[name="categories"]').val( l );
			$('#create-product-form input[name="origin"]').val( location.pathname );
			$('#create-product-form').submit();
		}
	}

	$scope.createService = function() {
		var serviceName = trimTrailingSpaces( $('#create-service-form input[name="name"]').val() );
		var serviceDesc = trimTrailingSpaces( $('#create-service-form textarea').val() );
		var servicePrice = trimTrailingSpaces( $('#create-service-form input[name="price"]').val() );

		if( !wordsOnlyRegex.test(serviceName) ) {
			alert('Service Name Must Be 3-50 Characters; \n \
			Letters & Numbers Only.');
			return;
		}
		if( !priceREG.test(servicePrice) ) {
			alert('Price Must Be In This Format: 0.00; \n \
			The Number Before The Period Can Be Any Amount Of Digits \
			But The Number After The Period Can Only Be 2 Digits.');
			return;
		}

		while(servicePrice.charAt(0) === '0'){
    	servicePrice = servicePrice.substr(1);
		}

		var ask = confirm('Are All Fields Correct?');
		if( ask == true ) {
			var l = '';
	    for( var key in $scope.serviceCategories ) {
	      l += $scope.serviceCategories[key] + ';';
	    }
	    l = l.slice(0, -1);

			$('#create-service-form input[name="categories"]').val( l );
			$('#create-service-form input[name="origin"]').val( location.pathname );
			$('#create-service-form').submit();
		}
	}

}]);

/*

var l = '';
for( var key in $scope.interestsList ) {
	l += $scope.interestsList[key] + ';';
}
l = l.slice(0, -1);
console.log(l);

*/
