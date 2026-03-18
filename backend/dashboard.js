// Frontend JS for dashboard UI
// --- Training Data Creation and Sending ---
let trainingData = [];

function createTrainingData() {
    // 5 dummy cities and 5 red lights per city
    const cities = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata'];
    const redLights = ['Red Light A', 'Red Light B', 'Red Light C', 'Red Light D', 'Red Light E'];
    const rowsPerCity = 10; // 50/5 = 10 rows per city
    trainingData = [];
    cities.forEach(city => {
        // For each city, generate one humidity and temperature
        const temperature = Math.floor(Math.random() * 40) + 10; // 10-50°C
        const humidity = Math.floor(Math.random() * 80) + 20;    // 20-100%
        for (let i = 0; i < rowsPerCity; i++) {
            const red_light = redLights[i % redLights.length];
            trainingData.push({
                timestamp: new Date(Date.now() - Math.floor(Math.random() * 100000000)),
                city,
                red_light,
                temperature,
                humidity,
                speed: Math.floor(Math.random() * 100) + 10,      // 10-110 km/h
                no_of_vehicles: Math.floor(Math.random() * 50) + 1 // 1-50 vehicles
            });
        }
    });
    renderTrainingDataTable();
}

function renderTrainingDataTable() {
    if (!trainingData.length) {
        document.getElementById('trainingDataPreview').innerHTML = '';
        return;
    }
    let html = `<div style="overflow-x:auto;"><table style="border-collapse:collapse;width:100%;font-size:0.97em;box-shadow:0 2px 8px #eee;background:#fff;">
        <thead style="background:#f7fafc;">
            <tr>
                <th style="padding:8px 6px;border-bottom:2px solid #e2e8f0;">#</th>
                <th style="padding:8px 6px;border-bottom:2px solid #e2e8f0;">City</th>
                <th style="padding:8px 6px;border-bottom:2px solid #e2e8f0;">Red Light</th>
                <th style="padding:8px 6px;border-bottom:2px solid #e2e8f0;">Timestamp</th>
                <th style="padding:8px 6px;border-bottom:2px solid #e2e8f0;">Temperature (°C)</th>
                <th style="padding:8px 6px;border-bottom:2px solid #e2e8f0;">Humidity (%)</th>
                <th style="padding:8px 6px;border-bottom:2px solid #e2e8f0;">Speed (km/h)</th>
                <th style="padding:8px 6px;border-bottom:2px solid #e2e8f0;">No. of Vehicles</th>
            </tr>
        </thead>
        <tbody>`;
    trainingData.forEach((row, idx) => {
        html += `<tr${idx%2===0? ' style="background:#f9f9fb;"':''}>
            <td style="padding:6px 4px;text-align:center;">${idx+1}</td>
            <td style="padding:6px 4px;text-align:center;">${row.city}</td>
            <td style="padding:6px 4px;text-align:center;">${row.red_light}</td>
            <td style="padding:6px 4px;text-align:center;">${new Date(row.timestamp).toLocaleString()}</td>
            <td style="padding:6px 4px;text-align:center;">${row.temperature}</td>
            <td style="padding:6px 4px;text-align:center;">${row.humidity}</td>
            <td style="padding:6px 4px;text-align:center;">${row.speed}</td>
            <td style="padding:6px 4px;text-align:center;">${row.no_of_vehicles}</td>
        </tr>`;
    });
    html += '</tbody></table></div>';
    document.getElementById('trainingDataPreview').innerHTML = html;
}

async function sendTrainingData() {
    if (!trainingData.length) {
        alert('Please create data first.');
        return;
    }
    try {
        const response = await axios.post('/api/save-training-data', { data: trainingData });
        alert('Data sent! Response: ' + JSON.stringify(response.data));
    } catch (err) {
        alert('Failed to send data.');
        console.error(err);
    }
}

// --- Dashboard Data Fetching ---
async function fetchTrafficData() {
    const place = document.getElementById('placeSelect').value;
    if (!place) {
        alert('Please select a city.');
        return;
    }
    try {
        // Fetch last 50 records for the city
        const response = await axios.get(`/api/traffic?place=${place}`);
        const { vehicleLocations } = response.data;
        renderVehicleMap(vehicleLocations || []);
        console.log(vehicleLocations)
    } catch (error) {
        alert('Failed to fetch traffic data.');
        console.error(error);
    }
}

function renderVehicleMap(vehicleLocations) {
    const map = document.getElementById('vehicleMap');
    map.innerHTML = '';
    if (!Array.isArray(vehicleLocations) || vehicleLocations.length === 0) {
        map.innerHTML = '<em>No vehicle data available.</em>';
        return;
    }
    // Group by red_light and show dots for each record at fixed positions for each red light
    const redLightPositions = {
        'Red Light A': { x: 0.2, y: 0.3 },
        'Red Light B': { x: 0.5, y: 0.5 },
        'Red Light C': { x: 0.7, y: 0.2 },
        'Red Light D': { x: 0.3, y: 0.7 },
        'Red Light E': { x: 0.8, y: 0.6 }
    };
    vehicleLocations.forEach((rec, idx) => {
        const pos = redLightPositions[rec.red_light] || { x: Math.random(), y: Math.random() };
        const dot = document.createElement('div');
        dot.className = 'car-dot';
        dot.style.left = (pos.x * 100 + Math.random() * 8 - 4) + '%';
        dot.style.top = (pos.y * 100 + Math.random() * 8 - 4) + '%';
        dot.title = `${rec.red_light} | ${rec.city} | Vehicles: ${rec.no_of_vehicles}`;
        map.appendChild(dot);
        // Optionally, label the red light
        if (idx < 5) {
            const label = document.createElement('div');
            label.style.position = 'absolute';
            label.style.left = (pos.x * 100) + '%';
            label.style.top = (pos.y * 100 + 12) + '%';
            label.style.fontSize = '0.85em';
            label.style.color = '#333';
            label.style.transform = 'translate(-50%,0)';
            label.innerText = rec.red_light;
            map.appendChild(label);
        }
    });



    
}


// Ensure car-dot style is present
if (!document.getElementById('car-dot-style')) {
    const style = document.createElement('style');
    style.id = 'car-dot-style';
    style.innerHTML = `.car-dot { position: absolute; width: 18px; height: 10px; border-radius: 3px; background: #222; border: 2px solid #fff; box-shadow: 0 1px 3px #888; }`;
    document.head.appendChild(style);
}
// Add car-dot style
const style = document.createElement('style');
style.innerHTML = `.car-dot { position: absolute; width: 18px; height: 10px; border-radius: 3px; background: #222; border: 2px solid #fff; box-shadow: 0 1px 3px #888; }`;
document.head.appendChild(style);

function renderTrafficDots(liveTraffic) {
    const map = document.getElementById('trafficMap');
    map.innerHTML = '';
    if (!Array.isArray(liveTraffic) || liveTraffic.length === 0) {
        map.innerHTML = '<em>No live traffic data available.</em>';
        return;
    }
    // Assume liveTraffic is an array of {x, y, severity}
    liveTraffic.forEach(dot => {
        const el = document.createElement('div');
        el.className = 'traffic-dot';
        el.style.left = (dot.x * 100) + '%';
        el.style.top = (dot.y * 100) + '%';
        el.style.background = dot.severity === 'high' ? '#e53e3e' : dot.severity === 'medium' ? '#ed8936' : '#38a169';
        el.title = `Severity: ${dot.severity}`;
        map.appendChild(el);
    });
}




async function getPrediction(){
const response = await axios.get("/traffic-prediction")
const data = response.data.predictions || []
const map = document.getElementById("predictionMap")
map.innerHTML = ""

if (!data.length) {
map.innerHTML = `<em>${response.data.message || "No predictions available."}</em>`
return
}

const redLightPositions={
"Red Light A":{x:20,y:30},
"Red Light B":{x:50,y:50},
"Red Light C":{x:70,y:20},
"Red Light D":{x:30,y:70},
"Red Light E":{x:80,y:60}
}

data.forEach(p=>{

const pos = redLightPositions[p.red_light]

const dot=document.createElement("div")

dot.className="traffic-dot"

dot.style.left=pos.x+"%"
dot.style.top=pos.y+"%"
const normalizedLabel = String(p.prediction_label || "").toLowerCase()
if(normalizedLabel === "high"){
dot.style.background="red"
}
else if(normalizedLabel === "medium"){
dot.style.background="orange"
}
else{
dot.style.background="green"
}

dot.title = `${p.red_light}: ${p.prediction_label || p.prediction}`

map.appendChild(dot)

})

}