$(function(){
    $('a#stopsNearMeButton').click(function() {
        var lat, lng, options;
        
        options = {
            enableHighAccuracy: true
        }
        
        $(this).text('Locating...');
        
        var geo;
        if (typeof(google) != 'undefined' && typeof(google.gears) != 'undefined') {
            geo = google.gears.factory.create('beta.geolocation');
        } else if (typeof(navigator.geolocation) != 'undefined') {
            geo = navigator.geolocation;
        }
        
        geo.getCurrentPosition(successCallback, errorCallback, options);
        
        function successCallback(position) {
            lat = position.coords.latitude;
            lng = position.coords.longitude;
            
            receivedLocation(lat, lng);
        }
        
        function errorCallback(error) {
            alert('An error occurred when trying to locate your device.')
        }
        
        function receivedLocation(lat, lng) {
            window.location = '/location/'+lat+'/'+lng+'/';
        }
        
        return false;
    })
    
});