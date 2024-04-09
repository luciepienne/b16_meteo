// Function to get the date of the next Saturday
function getNextSaturday() {
  var today = new Date();
  var dayOfWeek = today.getDay(); // 0 (Sunday) to 6 (Saturday)
  var daysUntilSaturday = 6 - dayOfWeek; // Days until next Saturday
  var nextSaturday = new Date(
    today.getTime() + daysUntilSaturday * 24 * 60 * 60 * 1000
  ); // Add days to get the next Saturday
  return nextSaturday;
}

// Function to get the date for Tomorrow
function getTomorrow() {
  var tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1); // Add 1 day to get tomorrow
  return tomorrow;
}

// Function to toggle visibility of date input based on radio button selection
function toggleDateInput() {
  var dateInput = document.getElementById("date");
  var chooseDateRadio = document.getElementById("chooseDate");

  if (chooseDateRadio.checked) {
    dateInput.style.display = "block";
  } else {
    dateInput.style.display = "none";
  }
}

// Add event listener to radio buttons to toggle date input visibility
var radioButtons = document.getElementsByName("dateOption");
for (var i = 0; i < radioButtons.length; i++) {
  radioButtons[i].addEventListener("change", toggleDateInput);
}

// Fetch city suggestions based on user input
var cityInput = document.getElementById("city");
var citySuggestions = document.getElementById("citySuggestions");

cityInput.addEventListener("input", function () {
  var inputValue = this.value.toUpperCase(); // Convert user input to uppercase
  if (inputValue.length >= 2) {
    // Make sure at least two characters are entered for autocomplete
    // Fetch autocomplete suggestions based on input value
    fetch(
      "http://b16api.cqhbb8bub7aghtbx.westeurope.azurecontainer.io:8002/citieswithforecasts?query=" +
        encodeURIComponent(inputValue)
    )
      .then((response) => response.json())
      .then((data) => {
        console.log("Data received from server:", data); // Log the received data for debugging
        citySuggestions.innerHTML = "";
        // Flatten the data structure to get a single array of city names
        var flattenedData = data.flatMap((city) => city);
        // Filter the data based on the input value
        var filteredData = flattenedData.filter(
          (city) => city.toUpperCase().startsWith(inputValue) // Compare city names in uppercase
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

// Handle form submission
var forecastForm = document.getElementById("forecastForm");
forecastForm.addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent the form from submitting normally

  var formData = new FormData(forecastForm);

  var city = formData.get("city").toUpperCase(); // Convert city name to uppercase
  var dateOption = formData.get("dateOption");
  var hour = formData.get("hour");

  var apiUrl =
    "http://b16api.cqhbb8bub7aghtbx.westeurope.azurecontainer.io:8002/forecast";
  var requestUrl = apiUrl + "?city=" + encodeURIComponent(city);

  // Determine the date based on the selected option
  var date;
  switch (dateOption) {
    case "today":
      date = new Date().toISOString().split("T")[0];
      break;
    case "tomorrow":
      date = getTomorrow().toISOString().split("T")[0];
      break;
    case "weekend":
      date = getNextSaturday().toISOString().split("T")[0];
      break;
    case "chooseDate":
      date = formData.get("date");
      break;
    default:
      date = new Date().toISOString().split("T")[0];
  }

  requestUrl += "&date=" + encodeURIComponent(date);

  // Include hour in the request URL only if it's provided
  if (hour) {
    requestUrl += "&hour=" + encodeURIComponent(hour);
  }

  // Show loading message
  var loadingMessage = document.getElementById("loadingMessage");
  loadingMessage.style.display = "block";

  // Fetch forecast data
  fetch(requestUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.blob();
    })
    .then((blob) => {
      var audioUrl = URL.createObjectURL(blob);
      document.getElementById("audioPlayer").src = audioUrl;
      document.getElementById("audioPlayer").style.display = "block";
    })
    .catch((error) => {
      console.error("An error occurred:", error);
    })
    .finally(() => {
      // Hide loading message
      loadingMessage.style.display = "none";
    });
});
