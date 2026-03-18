
const express = require("express");
const axios = require("axios");
const mongoose = require("mongoose");
const path = require("path");
const dns = require("dns");
dns.setServers(["1.1.1.1","8.8.8.8"])

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname)));
app.set("view engine", "ejs");

// ==========================
// MongoDB Connection
// ==========================

const MONGO_URI =
    "mongodb+srv://harshsogra_db_user:abcd@cluster0.pk5jl7e.mongodb.net/?appName=Cluster0";
mongoose.connect(MONGO_URI, {
  serverSelectionTimeoutMS: 10000,   // Fail faster with clearer errors
  socketTimeoutMS: 45000,
  family: 4,                          // Force IPv4 (replaces dns.setDefaultResultOrder)
})
.then(() => {
    console.log("✅ MongoDB connected");

    app.listen(3000, () => {
        console.log("🚀 Server running on http://localhost:3000");
    });
})
.catch(err => {
    console.error("❌ MongoDB connection failed:", err.message);
});


// ==========================
// Models
// ==========================

const TrafficData = require("./trafficData.model");

// ==========================
// Routes
// ==========================

app.get("/", (req, res) => {
    res.render(path.join(__dirname, "index.ejs"));
});

// Save traffic data
app.post("/api/save-training-data", async (req, res) => {

    try {

        const docs = await TrafficData.insertMany(req.body.data);

        console.log("Saved traffic data:", docs.length);

        res.json({
            status: "success",
            inserted: docs.length
        });

    } catch (err) {

        console.error(err);

        res.status(500).json({
            status: "error",
            message: err.message
        });

    }

});


// Get traffic data for city
app.get("/api/traffic", async (req, res) => {

    const city = req.query.place;

    if (!city) {
        return res.json({ vehicleLocations: [] });
    }

    try {

        const data = await TrafficData
            .find({ city })
            .sort({ timestamp: -1 })
            .limit(50);

        res.json({ vehicleLocations: data });

    } catch (err) {

        console.error("Traffic fetch error:", err);

        res.json({ vehicleLocations: [] });

    }

});


// ==========================
// AI Prediction Endpoint
// ==========================

app.get("/traffic-prediction", async (req, res) => {

try {

const records = await TrafficData
.find()
.sort({ timestamp: -1 })
.limit(5);

if (!records.length) {
return res.json({
predictions: [],
message: "No traffic data available"
});
}

const redLightToIntersection = {
"Red Light A": "INT_1",
"Red Light B": "INT_2",
"Red Light C": "INT_3",
"Red Light D": "INT_4",
"Red Light E": "INT_5"
};

const predictions = [];

for (const rec of records) {

const payload = {

timestamp: new Date(rec.timestamp).toISOString(),

vehicle_count: rec.no_of_vehicles,

avg_speed_kmh: rec.speed,

intersection_id: redLightToIntersection[rec.red_light] || "INT_1",

weather: inferWeather(rec),

signal_time_seconds: inferSignalTime(rec)

};

const response = await axios.post(
"http://localhost:8000/predict",
payload
);

predictions.push({

red_light: rec.red_light,

prediction: response.data.prediction,

future_congestion: response.data.future_congestion,

used_input: payload

});

}

console.log("Prediction pipeline completed");

res.json({ predictions });

} catch (err) {

console.error("Prediction error:", err);

res.status(503).json({
predictions: [],
message: "Prediction service unavailable"
});

}

});


// ==========================
// Helper Functions
// ==========================

function inferWeather(record) {

if (record.humidity >= 85) return "Rainy";

if (record.humidity >= 70) return "Fog";

if (record.temperature >= 35) return "Sunny";

return "Cloudy";

}

function inferSignalTime(record) {

const estimated = Math.round(record.no_of_vehicles * 1.2);

return Math.max(20, Math.min(120, estimated));

}