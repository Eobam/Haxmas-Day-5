const form = document.getElementById("giftForm")
const giftsContainer = document.getElementById("gifts");
const statsContainer = document.getElementById("stats");

async function loadGifts() {
    const response = await fetch('/gifts');
    const gifts = await response.json();
    
    giftsContainer.innerHTML = '';
    gifts.forEach(gift => {
        const item = document.createElement("p");
        item.textContent = `What was submitted: Country = ${gift.name}, Time For Delivery = ${gift.time}, and Item = ${gift.gift}`;
        giftsContainer.appendChild(item);
    });
}

async function loadStats() {
    const response = await fetch('/stats');
    const stats = await response.json();
    
    if (stats.length == 0) {
        statsContainer.innerHTML = '<p> Bruh, no one submitted anything, submit smth! </p>';
        return;
    }
    let tableHTML = `
        <h2>Average Delivery Time by Country</h2>
        <table>
            <thead>
                <tr>
                    <th>Country</th>
                    <th>Average Delivery Time</th>
                    <th>Total Gifts</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    stats.forEach(stat => {
        tableHTML += `
        <tr>
            <td>${stat.country}</td>
            <td>${stat.avg_time} hrs</td>
            <td>${stat.total_gifts}</td>
        </tr>
        `;
    });
    
    tableHTML += `
            </tbody>
        </table>
    `;
    
    statsContainer.innerHTML = tableHTML;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const name = form.elements.name.value;
    const gift = form.elements.gift.value;
    const time = form.elements.time.value;

    await fetch('/gifts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, gift, time })
    });

    form.reset();
    await loadGifts();
    await loadStats();
});

loadGifts();
loadStats();