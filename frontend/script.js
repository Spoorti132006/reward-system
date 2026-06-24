const BASE_URL = "http://127.0.0.1:8000";


// Add Transaction
async function addTransaction() {

    const request_id = "tx" + Date.now();
    const user_id = document.getElementById("user_id").value;
    const amount = Number(document.getElementById("amount").value);

    const response = await fetch(`${BASE_URL}/transaction`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            request_id,
            user_id,
            amount
        })
    });

    const data = await response.json();

    document.getElementById("transactionResult").innerHTML =
        JSON.stringify(data);
}


// Get Summary
async function getSummary() {

    const userId = document.getElementById("summary_user").value;

    const response = await fetch(`${BASE_URL}/summary/${userId}`);

    const data = await response.json();

    document.getElementById("summaryResult").innerHTML = `
        <p>Total Amount: ${data.total_amount}</p>
        <p>Total Points: ${data.total_points}</p>
        <p>Transaction Count: ${data.transaction_count}</p>
    `;
}


// Get Ranking
async function getRanking() {

    const response = await fetch(`${BASE_URL}/ranking`);

    const data = await response.json();

    let html = `
        <table>
            <tr>
                <th>Rank</th>
                <th>User ID</th>
                <th>Score</th>
            </tr>
    `;

    data.forEach(user => {

        html += `
            <tr>
                <td>${user.rank}</td>
                <td>${user.user_id}</td>
                <td>${user.score}</td>
            </tr>
        `;
    });

    html += "</table>";

    document.getElementById("rankingResult").innerHTML = html;
}