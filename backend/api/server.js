const express = require('express');
const app     = express();
const port    = process.env.PORT || 3000;

// JSON body parsing
app.use(express.json());

// POST /logon
app.post('/logon', (req, res) => {
    // req.body contains credentials
    // TODO: authenticate, create session/token
    res.status(200).json({message: 'logon handler (not implemented)'});
});

// GET /inventory
app.get('/inventory', (req, res) => {
    // TODO: fetch and return inventory items
    res.status(200).json({items: []});
});

// GET /pulse
app.get('/pulse', (req, res) => {
    // used as a health-check or heartbeat
    res.status(200).json({status: 'ok', timestamp: Date.now()});
});

// POST /purchase
app.post('/purchase', (req, res) => {
    // req.body contains purchase data
    // TODO: validate & process purchase
    res.status(200).json({message: 'purchase handler (not implemented)'});
});

app.listen(port, () => {
    console.log(`API server listening on port ${port}`);
});
