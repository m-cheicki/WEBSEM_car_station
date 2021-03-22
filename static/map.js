var mymap = L.map('map').setView([48.856614, 2.3522219], 11);

        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1,
            accessToken: 'pk.eyJ1IjoibWNoZWlja2kiLCJhIjoiY2ttZ3VlYXFyMDB5eTJ4bXF3bmp6Zng2cyJ9.ZukfPhGAAp8xIx1Xk55VPg'
        }).addTo(mymap);