let map;
let marcador = null;
let coordenadasSeleccionadas = null;
let circulo = null;

let latSeleccionada = null;
let lngSeleccionada = null;

function initMap() {
  const defaultCenter = { lat: -34.6037, lng: -58.3816 };

  map = new google.maps.Map(document.getElementById("map"), {
    center: defaultCenter,
    zoom: 14,
  });

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const ubicacionActual = {
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
        };

        map.setCenter(ubicacionActual);

        circulo = new google.maps.Circle({
          strokeColor: "#FF0000",
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: "#FF0000",
          fillOpacity: 0.35,
          map: map,
          center: ubicacionActual,
          radius: 20,
          clickable: false,
        });
      },
      () => {
        console.log("Geolocalización no permitida.");
      }
    );
  }

  map.addListener("click", function (event) {
    const latLng = event.latLng;

    if (!marcador) {
      marcador = new google.maps.Marker({
        position: latLng,
        map: map,
      });
    } else {
      marcador.setPosition(latLng);
    }

    coordenadasSeleccionadas = {
      lat: latLng.lat(),
      lng: latLng.lng(),
    };

    document.getElementById("okButton").style.display = "block";
  });
}

function confirmarSeleccion() {
  if (coordenadasSeleccionadas) {
    latSeleccionada = coordenadasSeleccionadas.lat;
    lngSeleccionada = coordenadasSeleccionadas.lng;

    const contenido = `lat=${latSeleccionada}\nlng=${lngSeleccionada}`;

    const blob = new Blob([contenido], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "coordenadas.txt";
    a.click();

    alert(`Coordenadas guardadas:\n${contenido}`);
    window.close();
  } else {
    alert("Primero seleccioná una ubicación en el mapa.");
  }
}

document.getElementById("okButton").addEventListener("click", confirmarSeleccion);

