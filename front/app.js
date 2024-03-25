document.getElementById("run-button").addEventListener("click", async () => {
    const citySelect = document.getElementById("city-select");
    const cityName = modelSelect.value;
    await sendClusteringRequest(cityName);
  });
  
  async function sendcityRequest(cityName) {
    const response = await fetch(`http://127.0.0.1:8000/${cityName}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
  
    if (response.ok) {
      const result = await response.json();
      audio.log(result);
  
      const resultElement = document.getElementById("result");
  
      resultElement.audio = `audio: ${result}`;
    } else {
      console.error("Error:", response.status, response.statusText);
    }
  }