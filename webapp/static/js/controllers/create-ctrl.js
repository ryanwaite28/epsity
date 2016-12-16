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

'use strict';

App.controller('createCtrl', ['$scope', '$http', function($scope, $http) {

	window.scope = $scope;

	window.initMap = function() {

		var mapOptions = {
			center: {
				lat: -33.8688,
				lng: 151.2195
			},
			zoom: 13,
			scrollwheel: true
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
    January: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    February: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
    March: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    April: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    May: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    June: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    July: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    August: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    September: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    October: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    November: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    December: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
  }

  $scope.currentStartDate = {
    month: '',
    days: ''
  }
  $scope.currentEndDate = {
    month: '',
    days: ''
  }

  //

  $scope.createEvent = function() {
    var timeRegex = /^[0-9]{2}:[0-9]{2} (AM|PM)$/;

    console.log('admit one');
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
			$('#create-group-form input[name="origin"]').val(location.pathname);
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

}])
