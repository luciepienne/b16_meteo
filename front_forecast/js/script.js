document.getElementById('forecastForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Empêche le formulaire de se soumettre normalement

    var form = event.target;
    var formData = new FormData(form);

    var city = formData.get('city');
    var date = formData.get('date');
    var hour = formData.get('hour');

    var apiUrl = 'http://127.0.0.1:8000/forecast';
    var requestUrl = apiUrl + '?city=' + encodeURIComponent(city) + '&date=' + encodeURIComponent(date) + '&hour=' + encodeURIComponent(hour);

    fetch(requestUrl)
        .then(response => response.json())
        .then(data => {
            var audioFile = "http://127.0.0.1:8001/" + data.audio_file; // Ajoutez l'URL de base de votre serveur
            document.getElementById("audioPlayer").src = audioFile;
            document.getElementById("audioPlayer").style.display = "block";
        })
        .catch(error => {
            console.error('Une erreur s\'est produite:', error);
        });
});

http://localhost:8001/forecast_storage/audio/audio_razengues_2024-03-26_22.mp3