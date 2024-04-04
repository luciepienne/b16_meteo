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
    .then(response => response.blob())
    .then(blob => {
        var audioUrl = URL.createObjectURL(blob); 
        document.getElementById("audioPlayer").src = audioUrl;
        document.getElementById("audioPlayer").style.display = "block";
    })
    .catch(error => {
        console.error("Une erreur s'est produite:", error);
    });
});