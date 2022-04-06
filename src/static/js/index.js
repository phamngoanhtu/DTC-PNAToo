
function cam_html(ip) {
  var index = document.createElement('div');
  console.log('Came_html', ip)
  tmp = '<img src="http://192.168.24.45:5000/stream/' + ip + '"' + 'id=' + ip + '>'
  index.innerHTML = '<a href="#!" id="' + ip + '" class="list-group-item list-group-item-action frame">' + tmp + '</a>';
  return index;
}

const cam = ['cam_01', 'cam_10', 'cam_12', 'cam_05', 'cam_09']
// , 'cam_06', 'cam_07', 'cam_08', 'cam_09', 'cam_10', 'cam_11', 'cam_12']

function update_camera() {
  document.getElementById('cam_list').innerHTML = "";
  for (let i = 0; i < cam.length; i++) {
    document.getElementById('cam_list').appendChild(cam_html(cam[i]));
  }
}


$(document).ready(function () {
  // update_members();
  update_camera();
  // var alerts = firebase.database().ref('alert/');
  // alerts.on('value', function (snapshot) {
  //   console.log(snapshot.val().toString().length);
  //   if (snapshot.val().toString().length > 5 && snapshot.val().msg != "") {
  //     console.log("-" + snapshot.val().msg + "-")
  //     document.getElementById("alert_message").innerText = snapshot.val().msg;
  //     document.getElementById('alert').play();
  //     $('#alertModal').modal("show");
  //   }
  // });
});



function set_current_panal(element) {
  console.log(element);
  document.getElementById("disp-id").innerText = element.id;
  document.getElementById("log").href = "./log/" + event.target.id;

  document.getElementById("disp-name").innerText = element.name;
  document.getElementById("disp-phone").innerText = element.phone;
  document.getElementById("disp-email").innerText = element.email;
  document.getElementById("disp-auth").innerText = element.auth;

}

$("#cam_list").on("click", function (event) {
  // document.getElementById("track_panel").style.display = "block";
  // document.getElementById("mem_panel").style.display = "none";
  // document.getElementById("cam_panel").style.display = "block";
  // console.log("ID camera", event.target.id);
  // document.getElementById("c-disp-id").innerText = event.target.id;

  // document.getElementById("frame").src = "/stream/" + event.target.id + "/frame.jpg";

  const videoElement = document.getElementById("frame");
  // videoElement.setAttribute('src', "{{url_for('stream',ip='cam01')}}");
  videoElement.setAttribute('src', "http://192.168.24.45:5000/stream/" + event.target.id);
  console.log("http://192.168.24.45:5000/stream/" + event.target.id)
});


function face_rec(time, id, name) {
  var row = document.createElement('tr');
  row.innerHTML = '<td>' + time + '</td><td>' + id + '</td><td>' + name + '</td>';
  return row;
}
// Live graph

// connect to Pusher


// Map
var camIcon = L.icon({
  iconUrl: 'https://cdn4.iconfinder.com/data/icons/smart-device-filled-outline/64/Camera_cctv_security_security_camera-512.png',
  iconSize: [50, 45], // size of the icon
  iconAnchor: [15, 30], // point of the icon which will correspond to marker's location
  popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});

var map = L.map('map').setView([10.770579, -253.30636], 11);
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 18,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1,
  accessToken: 'pk.eyJ1IjoiYmh1eWxlIiwiYSI6ImNrd2swZzhyajFuc3oybnF0eml3Nm1xM3AifQ.BUMF6n44tKn_tKUwrxixHA'
}).addTo(map);

// Add events
var set1 = L.marker([10.789129, -253.284044], { icon: camIcon }).addTo(map);
var set2 = L.marker([10.789803, -253.347387], { icon: camIcon }).addTo(map);
var set3 = L.marker([10.763328, -253.339834], { icon: camIcon }).addTo(map);
var set4 = L.marker([10.756076, -253.280439], { icon: camIcon }).addTo(map);
var set5 = L.marker([10.880511, -253.231816], { icon: camIcon }).addTo(map);
var set6 = L.marker([10.864749, -253.240743], { icon: camIcon }).addTo(map);
var set7 = L.marker([10.860955, -253.228126], { icon: camIcon }).addTo(map);
var set8 = L.marker([10.871745, -253.267179], { icon: camIcon }).addTo(map);
var set9 = L.marker([10.858848, -253.222032], { icon: camIcon }).addTo(map);
var set10 = L.marker([10.843506, -253.253875], { icon: camIcon }).addTo(map);
var set11 = L.marker([10.825803, -253.285718], { icon: camIcon }).addTo(map);
var set12 = L.marker([10.81341, -253.319836], { icon: camIcon }).addTo(map);

function send(id) {
  setTimeout(function() {
      var req = new XMLHttpRequest();
      req.open('GET', '/ajax?cam_id=' + id);
      req.send();
  }, 1000);
      return false
  // $.ajax({
  //   type: "POST",
  //   url: "./check",
  //   crossDomain: true,
  //   data: { 'cam_id': id },
  //   success: function (results) {
  //     console.log(results);
  //   },
  //   error: function (error) {
  //     console.log(error);
  //   }
  // });
}
// function loadXMLDoc()
//     {
//         var req = new XMLHttpRequest()
//         req.onreadystatechange = function()
//         {
//         }
//         req.open('POST', '/ajax')
//         req.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
//         var postVars = 'username='+'1'
//         req.send(postVars)
//         console.log(postVars)
//         return false
//     }


let pingMap = document.querySelectorAll('.leaflet-marker-icon');
pingMap.forEach((item, index) => {
  item.addEventListener('click', () => {
    // document.getElementById("mem_panel").style.display = "none";
    // document.getElementById("cam_panel").style.display = "block";
    // document.getElementById("c-disp-id").innerText = cam[index];
    const videoElement = document.getElementById("frame");
    console.log('Click', cam[index])
    videoElement.setAttribute('src', "http://192.168.24.45:5000/stream/" + cam[index]);
    document.documentElement.scrollTop = 0;
    // loadXMLDoc()
    send(index)
    // document.getElementById("graph").style.display = "block";
    // document.getElementById("price_chart").style.display = "none";
    
  })
})


