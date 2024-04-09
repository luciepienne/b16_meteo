document.addEventListener("DOMContentLoaded", function () {
  var cityInput = document.getElementById("city");
  var citySuggestions = document.getElementById("citySuggestions");
  var selectedSuggestionIndex = -1; // Initialize index of selected suggestion

  // Function to highlight the selected suggestion
  function highlightSuggestion(index) {
    var suggestions = citySuggestions.querySelectorAll(".autocomplete-item");
    // Remove highlight from all suggestions
    suggestions.forEach((suggestion) => {
      suggestion.classList.remove("selected");
    });
    // Add highlight to the selected suggestion
    if (index >= 0 && index < suggestions.length) {
      suggestions[index].classList.add("selected");
    }
  }

  cityInput.addEventListener("input", function () {
    var inputValue = this.value.toLowerCase();
    if (inputValue.length >= 2) {
      // Make sure at least two characters are entered for autocomplete
      // Fetch autocomplete suggestions based on input value
      fetch(
        "http://localhost:8002/citieswithforecasts?query=" +
          encodeURIComponent(inputValue)
      )
        .then((response) => response.json())
        .then((data) => {
          console.log("Data received from server:", data); // Log the received data for debugging
          citySuggestions.innerHTML = "";
          // Flatten the data structure to get a single array of city names
          var flattenedData = data.flatMap((city) => city);
          // Filter the data based on the input value
          var filteredData = flattenedData.filter((city) =>
            city.toLowerCase().startsWith(inputValue)
          );
          console.log("Filtered data:", filteredData); // Log the filtered data for debugging
          filteredData.forEach((city) => {
            var suggestion = document.createElement("div");
            suggestion.classList.add("autocomplete-item");
            suggestion.textContent = city;
            suggestion.addEventListener("click", function () {
              cityInput.value = city;
              citySuggestions.innerHTML = "";
            });
            citySuggestions.appendChild(suggestion);
          });
        })
        .catch((error) => {
          console.error("Error fetching autocomplete suggestions:", error);
        });
    } else {
      citySuggestions.innerHTML = "";
    }
  });

  // Update the date container content when the date input changes
  document.addEventListener("keydown", function (event) {
    if (event.key === "ArrowDown") {
      // Move to the next suggestion
      selectedSuggestionIndex++;
      highlightSuggestion(selectedSuggestionIndex);
    } else if (event.key === "ArrowUp") {
      // Move to the previous suggestion
      selectedSuggestionIndex--;
      highlightSuggestion(selectedSuggestionIndex);
    } else if (event.key === "Enter") {
      // Select the currently highlighted suggestion
      var selectedSuggestion = citySuggestions.querySelector(".selected");
      if (selectedSuggestion) {
        cityInput.value = selectedSuggestion.textContent;
        citySuggestions.innerHTML = "";
      }
    }
  });

  document
    .getElementById("forecastForm")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the form from submitting normally

      var form = event.target;
      var formData = new FormData(form);

      var city = formData.get("city");
      var date = formData.get("date");
      var hour = formData.get("hour");

      var apiUrl = "http://localhost:8002/forecast";
      var requestUrl =
        apiUrl +
        "?city=" +
        encodeURIComponent(city) +
        "&date=" +
        encodeURIComponent(date);

      // Include hour in the request URL only if it's provided
      if (hour) {
        requestUrl += "&hour=" + encodeURIComponent(hour);
      }

      fetch(requestUrl)
        .then((response) => response.blob())
        .then((blob) => {
          var audioUrl = URL.createObjectURL(blob);
          document.getElementById("audioPlayer").src = audioUrl;
          document.getElementById("audioPlayer").style.display = "block";
        })
        .catch((error) => {
          console.error("Une erreur s'est produite:", error);
        });
    });
});
