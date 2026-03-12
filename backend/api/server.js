const express = require('express');
const app     = express();
const port    = process.env.PORT || 3000;

// JSON body parsing
app.use(express.json());

// ── Base-price table (inventory data) ──────────────────────────
const inventory = [
    { id: 1, name: 'Duck Spell A', price: 9.99,  image: 'duck-a.png' },
    { id: 2, name: 'Duck Spell B', price: 12.50, image: 'duck-b.png' },
    { id: 3, name: 'Fire Spell',   price: 5.00,  image: 'fire.png'   }
];

// POST /logon – no authentication, just echoes the user back
app.post('/logon', (req, res) => {
    const { user, pass } = req.body;
    if (!user || !pass) {
        return res.status(400).json({ status: 'error', message: 'user and pass are required' });
    }
    res.status(200).json({ status: 'ok', user });
});

// GET /inventory – return all items from the base-price table
app.get('/inventory', (req, res) => {
    res.status(200).json({ items: inventory });
});

// GET /inventory/search – filter by name, price, or image via query params
app.get('/inventory/search', (req, res) => {
    const { name, price, image } = req.query;
    let results = inventory;

    if (name)  results = results.filter(i => i.name === name);
    if (price) results = results.filter(i => i.price === parseFloat(price));
    if (image) results = results.filter(i => i.image === image);

    res.status(200).json({ items: results });
});

// GET /inventory/:id – lookup a single item by its unique ID
app.get('/inventory/:id', (req, res) => {
    const id = parseInt(req.params.id, 10);
    const item = inventory.find(i => i.id === id);
    if (!item) {
        return res.status(404).json({ status: 'error', message: 'item not found' });
    }
    res.status(200).json(item);
});

// GET /pulse – health check / heartbeat
app.get('/pulse', (req, res) => {
    res.status(200).json({ status: 'ok', timestamp: Date.now() });
});

// POST /purchase – process a purchase
app.post('/purchase', (req, res) => {
    const { itemId, qty } = req.body;

    if (!itemId || !qty || qty < 1) {
        return res.status(400).json({ status: 'error', message: 'itemId and qty (>= 1) are required' });
    }

    const item = inventory.find(i => i.id === itemId);
    if (!item) {
        return res.status(404).json({ status: 'error', message: 'item not found' });
    }

    const total = item.price * qty;
    res.status(200).json({
        status: 'ok',
        orderId: Date.now(),
        item: item.name,
        qty,
        total
    });
});

app.listen(port, () => {
    console.log(`API server listening on port ${port}`);
});
