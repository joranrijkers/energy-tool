const priceElement = document.getElementById('price');
const API_URL = 'http://localhost:8000';  // Tijdelijk voor testen

async function fetchPrice() {
    try {
        const response = await fetch(`${API_URL}/current-price`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        if (data.price) {
            priceElement.textContent = `Price: ${data.price} EUR at ${data.timestamp}`;
        } else {
            priceElement.textContent = "No data available";
        }
    } catch (error) {
        console.error('Error:', error);
        priceElement.textContent = "Error fetching price";
    }
}

// Fetch price every 5 seconds
setInterval(fetchPrice, 5000);
fetchPrice();
