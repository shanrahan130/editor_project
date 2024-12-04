const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const fs = require('fs');

const app = express();
const PORT = 80;

// Load configuration from config.json dynamically
let config = JSON.parse(fs.readFileSync('./config.json', 'utf-8'));

// Function to reload config dynamically
function loadConfig() {
    config = JSON.parse(fs.readFileSync('./config.json', 'utf-8'));
}

// Watch for changes in config.json and reload if it changes
fs.watchFile('./config.json', loadConfig);

// Middleware to log all incoming requests
app.use((req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
});

// Middleware to add CORS headers
app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");

    // Handle OPTIONS requests immediately
    if (req.method === 'OPTIONS') {
        return res.sendStatus(200);
    }

    next();
});

// Set up proxy routes based on config with extended timeouts
Object.keys(config.routes).forEach(route => {
    app.use(
        `/api/${route}`,
        createProxyMiddleware({
            target: config.routes[route],
            changeOrigin: true,
            pathRewrite: { [`^/api/${route}`]: '' },
            timeout: 30000, // Wait 30 seconds before timeout (default is 20 seconds)
            proxyTimeout: 30000, // Wait for backend services to respond
            onError: (err, req, res) => {
                console.error(`Error in proxy for route /api/${route}: ${err.message}`);
                res.status(500).json({ error: true, message: "Service unavailable" });
            }
        })
    );
});

app.listen(PORT, () => {
    console.log(`Proxy server is running on port ${PORT}`);
});
