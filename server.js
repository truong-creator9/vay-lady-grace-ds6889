const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;
const WAITLIST_FILE = path.join(__dirname, 'waitlist.json');

app.use(cors());
app.use(express.json());
// Serve static files from the current directory (for index.html, etc.)
app.use(express.static(__dirname));

// API endpoint for waitlist form submission
app.post('/api/waitlist', (req, res) => {
    let currentData = [];
    
    // Read existing data if file exists
    if (fs.existsSync(WAITLIST_FILE)) {
        try {
            const fileContent = fs.readFileSync(WAITLIST_FILE, 'utf8');
            if (fileContent.trim() !== '') {
                currentData = JSON.parse(fileContent);
            }
        } catch (error) {
            console.error('Error reading waitlist.json:', error);
            // Backup corrupted file
            fs.copyFileSync(WAITLIST_FILE, `${WAITLIST_FILE}.bak_${Date.now()}`);
            currentData = []; 
        }
    }
    
    // Append new data
    const newEntry = req.body;
    currentData.push(newEntry);
    
    // Save to file
    try {
        fs.writeFileSync(WAITLIST_FILE, JSON.stringify(currentData, null, 2), 'utf8');
        res.status(200).json({ message: 'Thông tin đã được lưu thành công!' });
    } catch (error) {
        console.error('Error writing to waitlist.json:', error);
        res.status(500).json({ error: 'Đã xảy ra lỗi khi lưu thông tin. Vui lòng thử lại sau.' });
    }
});

app.listen(PORT, () => {
    console.log(`\n======================================================`);
    console.log(`🚀 Server đang chạy tại: http://localhost:${PORT}`);
    console.log(`👉 Mở trình duyệt và truy cập: http://localhost:${PORT}`);
    console.log(`======================================================\n`);
});
