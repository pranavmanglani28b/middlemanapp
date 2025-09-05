<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Trade Middleman</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 600px; margin: auto; }
        .trade-section { border: 1px solid #ccc; padding: 20px; margin-bottom: 20px; border-radius: 8px; }
        .exchanged { background: #e0ffe0; }
        .hidden { display: none; }
        label { display: block; margin-top: 10px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 8px; margin-top: 4px; }
        button { margin-top: 15px; padding: 10px 20px; }
    </style>
</head>
<body>
<div class="container">
    <h2>Trade Middleman</h2>
    <div id="join-section" class="trade-section">
        <label for="tradeCode">Enter Trade Code to Join:</label>
        <input type="text" id="tradeCode" maxlength="12" placeholder="Trade Code">
        <button onclick="joinTrade()">Join Trade</button>
        <div id="join-error" style="color:red; margin-top:10px;"></div>
    </div>

    <div id="trade-section" class="trade-section hidden">
        <h3>Trade Code: <span id="showTradeCode"></span></h3>
        <label for="userName">Your Name:</label>
        <input type="text" id="userName" maxlength="32" placeholder="Enter your name">

        <label for="userDetails">Your Details:</label>
        <input type="text" id="userDetails" maxlength="128" placeholder="Enter your details">

        <button onclick="submitDetails()">Submit Details</button>
        <div id="wait-msg" style="margin-top:10px;"></div>
    </div>

    <div id="exchange-section" class="trade-section hidden exchanged">
        <h3>Trade Complete!</h3>
        <div>
            <strong>Your Partner:</strong> <span id="partnerName"></span><br>
            <strong>Partner's Details:</strong> <span id="partnerDetails"></span>
        </div>
    </div>
</div>

<script>
    // In-memory store for demo (would be server-side in real app)
    const trades = {};

    let currentTradeCode = '';
    let currentUserId = '';
    let partnerUserId = '';

    function joinTrade() {
        const code = document.getElementById('tradeCode').value.trim();
        const errorDiv = document.getElementById('join-error');
        if (!code) {
            errorDiv.textContent = "Please enter a trade code.";
            return;
        }
        errorDiv.textContent = "";
        currentTradeCode = code;
        currentUserId = Math.random().toString(36).substr(2, 9);

        // Create or join trade
        if (!trades[code]) {
            trades[code] = {};
        }
        if (Object.keys(trades[code]).length >= 2) {
            errorDiv.textContent = "This trade code is full. Try another.";
            return;
        }
        trades[code][currentUserId] = { name: '', details: '', ready: false };

        document.getElementById('join-section').classList.add('hidden');
        document.getElementById('trade-section').classList.remove('hidden');
        document.getElementById('showTradeCode').textContent = code;

        pollForPartner();
    }

    function submitDetails() {
        const name = document.getElementById('userName').value.trim();
        const details = document.getElementById('userDetails').value.trim();
        if (!name || !details) {
            alert("Please enter your name and details.");
            return;
        }
        trades[currentTradeCode][currentUserId] = { name, details, ready: true };
        document.getElementById('wait-msg').textContent = "Waiting for your trade partner to submit details...";

        pollForExchange();
    }

    function pollForPartner() {
        // Check if another user has joined
        const interval = setInterval(() => {
            const users = Object.keys(trades[currentTradeCode]);
            if (users.length === 2) {
                partnerUserId = users.find(uid => uid !== currentUserId);
                clearInterval(interval);
            }
        }, 1000);
    }

    function pollForExchange() {
        // Wait for both users to be ready
        const interval = setInterval(() => {
            const trade = trades[currentTradeCode];
            if (!trade) return;
            const users = Object.keys(trade);
            if (users.length < 2) return;
            const partnerId = users.find(uid => uid !== currentUserId);
            partnerUserId = partnerId;
            if (trade[currentUserId].ready && trade[partnerId].ready) {
                clearInterval(interval);
                showExchange();
            }
        }, 1000);
    }

    function showExchange() {
        const trade = trades[currentTradeCode];
        document.getElementById('trade-section').classList.add('hidden');
        document.getElementById('exchange-section').classList.remove('hidden');
        document.getElementById('partnerName').textContent = trade[partnerUserId].name;
        document.getElementById('partnerDetails').textContent = trade[partnerUserId].details;
    }
</script>
</body>
</html>
