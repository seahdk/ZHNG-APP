    const apiKey='pk.eyJ1IjoiMjAxMzA0YyIsImEiOiJja3hteWY4cGQzc3RxMnBxOTNxdzVsN2ttIn0.Cy2h95jXqjb_XY0Q7zjr_g';

    const map = L.map('map').setView([1.3721, 103.8198], 13);

  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: apiKey
}).addTo(map);

var marker = L.marker([1.434095, 103.788092]).addTo(map);
var marker1 = L.marker([1.357339, 103.876123]).addTo(map);
var marker2 = L.marker([1.341228, 103.795378]).addTo(map);

marker.bindPopup('<h1>Ah Beng Servicing Centre</h1> <h2>Type: Bicycle</h2> <p>Location: Woodlands Block 369 </p>')
marker1.bindPopup('<h1>YCK car servicing centre</h1> <h2>Type: Car</h2> <p>Location: 30 Yio Chu Kang Rd</p>');
marker2.bindPopup('<h1>KNNCCB servicing centre</h1> <h2>Type: Motorcycle</h2> <p>Location: Bukit Timah</p>');

function reset() {
marker.setLatLng([1.434095, 103.788092]).update();
marker1.setLatLng([1.357339, 103.876123]).update();
marker2.setLatLng([1.341228, 103.795378]).update();
}

function filterCar() {
marker.setLatLng([-30.88992, 146.632589]).update();
marker1.setLatLng([1.357339, 103.876123]).update();
marker2.setLatLng([50.341228, 103.795378]).update();
}

function filterMC() {
marker.setLatLng([-30.88992, 146.632589]).update();
marker1.setLatLng([30.357339, 103.876123]).update();
marker2.setLatLng([1.341228, 103.795378]).update();
}

function filterBC() {
marker.setLatLng([1.434095, 103.788092]).update();
marker1.setLatLng([30.357339, 103.876123]).update();
marker2.setLatLng([50.341228, 103.795378]).update();
}
