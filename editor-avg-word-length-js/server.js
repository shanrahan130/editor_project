const express = require('express');
const app = express();
const PORT = 80;

app.get('/', (req, res) => {
    // Add CORS headers to allow access from different origins
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    const text = req.query.text || "";
    const words = text.split(/\s+/).filter(word => word.length > 0);
    const wordCount = words.length;
    const charCount = words.reduce((sum, word) => sum + word.length, 0);
    const avgLength = wordCount > 0 ? (charCount / wordCount).toFixed(2) : 0;

    res.json({
        error: false,
        string: `Average word length is ${avgLength}`,
        answer: parseFloat(avgLength)
    });
});

app.listen(PORT, () => {
    console.log(`Average Word Length Service running on port ${PORT}`);
});
