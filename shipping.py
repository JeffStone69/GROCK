import http.server
import socketserver
import json
import random
import webbrowser
import sys
from typing import List, Dict

# Enhanced mock data with real-time AIS data sources simulation
VESSELS: List[Dict] = [
    {
        "id": "MSCU1234567",
        "vessel_name": "MSC Isabella",
        "imo": "IMO 9461234",
        "mmsi": "636019876",
        "vessel_type": "Container Ship",
        "cargo": "Consumer Electronics",
        "location": "Strait of Malacca",
        "destination": "Port of Rotterdam, Netherlands",
        "value": 2450000,
        "impact": 65,
        "lat": 3.82,
        "lng": 100.12,
        "dest_lat": 51.95,
        "dest_lng": 4.05,
        "course": 285,
        "speed_knots": 18.4,
        "weather": {"temp_c": 29, "condition": "Clear Skies", "icon": "☀️", "impact": 3},
        "last_ais_update": "just now",
        "destination_congestion": 68,
        "ais_source": "MarineTraffic + VesselFinder"
    },
    {
        "id": "CMAU4567890",
        "vessel_name": "CMA CGM Marco Polo",
        "imo": "IMO 9456789",
        "mmsi": "228123456",
        "vessel_type": "Container Ship",
        "cargo": "Automotive Components",
        "location": "Indian Ocean",
        "destination": "Port of Los Angeles, USA",
        "value": 890000,
        "impact": 30,
        "lat": -7.45,
        "lng": 78.3,
        "dest_lat": 33.75,
        "dest_lng": -118.2,
        "course": 92,
        "speed_knots": 16.7,
        "weather": {"temp_c": 26, "condition": "High Winds", "icon": "🌬️", "impact": 22},
        "last_ais_update": "just now",
        "destination_congestion": 42,
        "ais_source": "ExactEarth + Orbcomm"
    },
    {
        "id": "EISU9876543",
        "vessel_name": "Evergreen Ever Given",
        "imo": "IMO 9876543",
        "mmsi": "352987654",
        "vessel_type": "Container Ship",
        "cargo": "Pharmaceuticals",
        "location": "Suez Canal",
        "destination": "Port of Hamburg, Germany",
        "value": 1200000,
        "impact": 80,
        "lat": 30.15,
        "lng": 32.55,
        "dest_lat": 53.55,
        "dest_lng": 9.95,
        "course": 0,
        "speed_knots": 12.1,
        "weather": {"temp_c": 22, "condition": "Fog", "icon": "🌫️", "impact": 15},
        "last_ais_update": "just now",
        "destination_congestion": 55,
        "ais_source": "MarineTraffic"
    },
    {
        "id": "TEMU1122334",
        "vessel_name": "Maersk Memphis",
        "imo": "IMO 9345678",
        "mmsi": "219876543",
        "vessel_type": "Container Ship",
        "cargo": "Textiles & Apparel",
        "location": "Pacific Ocean",
        "destination": "Port of Oakland, USA",
        "value": 675000,
        "impact": 45,
        "lat": 24.8,
        "lng": -142.3,
        "dest_lat": 37.8,
        "dest_lng": -122.3,
        "course": 68,
        "speed_knots": 19.8,
        "weather": {"temp_c": 24, "condition": "Calm Seas", "icon": "🌊", "impact": 2},
        "last_ais_update": "just now",
        "destination_congestion": 29,
        "ais_source": "VesselFinder + Spire"
    },
    {
        "id": "OOLU5566778",
        "vessel_name": "OOCL Hong Kong",
        "imo": "IMO 9123456",
        "mmsi": "477112233",
        "vessel_type": "Container Ship",
        "cargo": "Machinery Parts",
        "location": "Gulf of Aden",
        "destination": "Port of New York, USA",
        "value": 1580000,
        "impact": 55,
        "lat": 12.95,
        "lng": 49.8,
        "dest_lat": 40.65,
        "dest_lng": -74.0,
        "course": 275,
        "speed_knots": 14.5,
        "weather": {"temp_c": 31, "condition": "Stormy", "icon": "⛈️", "impact": 28},
        "last_ais_update": "just now",
        "destination_congestion": 71,
        "ais_source": "MarineTraffic"
    },
    # Oil Tanker 1
    {
        "id": "TANK1122334",
        "vessel_name": "TI Europe",
        "imo": "IMO 9181234",
        "mmsi": "636012345",
        "vessel_type": "Oil Tanker",
        "cargo": "Crude Oil",
        "location": "Persian Gulf",
        "destination": "Port of Rotterdam, Netherlands",
        "value": 45200000,
        "impact": 75,
        "lat": 27.5,
        "lng": 51.2,
        "dest_lat": 51.95,
        "dest_lng": 4.05,
        "course": 310,
        "speed_knots": 13.2,
        "weather": {"temp_c": 33, "condition": "Moderate Seas", "icon": "🌊", "impact": 12},
        "last_ais_update": "just now",
        "destination_congestion": 68,
        "ais_source": "Orbcomm + ExactEarth"
    },
    # Oil Tanker 2
    {
        "id": "TANK5566778",
        "vessel_name": "Seawise Giant",
        "imo": "IMO 9123456",
        "mmsi": "477998877",
        "vessel_type": "Oil Tanker",
        "cargo": "Crude Oil",
        "location": "Gulf of Mexico",
        "destination": "Port of Los Angeles, USA",
        "value": 32800000,
        "impact": 40,
        "lat": 28.0,
        "lng": -88.5,
        "dest_lat": 33.75,
        "dest_lng": -118.2,
        "course": 255,
        "speed_knots": 11.8,
        "weather": {"temp_c": 27, "condition": "Clear Skies", "icon": "☀️", "impact": 4},
        "last_ais_update": "just now",
        "destination_congestion": 42,
        "ais_source": "MarineTraffic"
    }
]

PORTS: List[Dict] = [
    {"name": "Port of Rotterdam, Netherlands", "congestion": 68, "lat": 51.95, "lng": 4.05},
    {"name": "Port of Los Angeles, USA", "congestion": 42, "lat": 33.75, "lng": -118.2},
    {"name": "Port of Hamburg, Germany", "congestion": 55, "lat": 53.55, "lng": 9.95},
    {"name": "Port of Oakland, USA", "congestion": 29, "lat": 37.8, "lng": -122.3},
    {"name": "Port of New York, USA", "congestion": 71, "lat": 40.65, "lng": -74.0},
    {"name": "Port of Singapore", "congestion": 35, "lat": 1.25, "lng": 103.8}
]

MANUFACTURERS: List[Dict] = [
    {"name": "Tesla Inc.", "delay_days": 9, "affected_vessel": "MSCU1234567", "risk_score": 82},
    {"name": "Apple Inc.", "delay_days": 14, "affected_vessel": "OOLU5566778", "risk_score": 91},
    {"name": "Boeing", "delay_days": 5, "affected_vessel": "TANK1122334", "risk_score": 67},
    {"name": "Samsung Electronics", "delay_days": 11, "affected_vessel": "CMAU4567890", "risk_score": 78},
    {"name": "General Motors", "delay_days": 3, "affected_vessel": "TEMU1122334", "risk_score": 54}
]

class ContainerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_html_page()
        elif self.path == "/data":
            self.send_container_data()
        else:
            self.send_error(404, "Not Found")

    def send_html_page(self):
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShipTrack Live • Real-time AIS + Risk Analytics</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;display=swap');
        body { font-family: 'Inter', system_ui, sans-serif; }
        .title-font {
            font-family: 'Inter', system_ui, sans-serif;
            font-weight: 700;
            letter-spacing: -2px;
        }
        .card { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 25px 50px -12px rgb(16 185 129);
        }
        #map { filter: brightness(0.95) contrast(1.05); }
        .leaflet-popup-content-wrapper {
            border-radius: 16px;
            box-shadow: 0 25px 50px -12px rgb(16 185 129);
        }
        .ship-marker {
            animation: shippulse 1.8s infinite ease-in-out;
        }
        @keyframes shippulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.12); }
        }
    </style>
</head>
<body class="bg-zinc-950 text-zinc-100">
    <div class="max-w-screen-2xl mx-auto">
        <nav class="bg-zinc-900 border-b border-zinc-800 px-8 py-5 flex items-center justify-between sticky top-0 z-50">
            <div class="flex items-center gap-x-4">
                <div class="w-10 h-10 bg-emerald-500 rounded-2xl flex items-center justify-center text-3xl shadow-inner">🚢</div>
                <div>
                    <h1 class="title-font text-4xl tracking-[-1px]">ShipTrack <span class="text-emerald-400 text-xl align-super font-normal">AIS LIVE</span></h1>
                </div>
                <span class="px-3 py-1 text-xs font-semibold bg-emerald-500 text-white rounded-3xl flex items-center gap-x-1">
                    <span class="relative flex h-2 w-2">
                        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                        <span class="relative inline-flex rounded-full h-2 w-2 bg-white"></span>
                    </span>
                    REAL-TIME
                </span>
            </div>

            <div class="flex items-center gap-x-6">
                <div class="flex items-center bg-zinc-800 rounded-3xl px-5 py-2 text-sm">
                    <span class="text-zinc-400 mr-3">Poll every</span>
                    <input id="poll-interval" type="number" value="4" min="1" max="60"
                           class="w-14 bg-transparent text-center font-mono text-emerald-400 focus:outline-none focus:ring-1 focus:ring-emerald-400 rounded-xl">
                    <span class="text-zinc-400 ml-2">seconds</span>
                </div>

                <button onclick="togglePolling()" id="poll-btn"
                        class="flex items-center gap-x-2 bg-white hover:bg-emerald-400 hover:text-white text-zinc-900 font-semibold px-6 h-10 rounded-3xl transition-colors">
                    <span id="btn-icon" class="text-lg">▶️</span>
                    <span id="btn-text">START POLLING</span>
                </button>

                <div class="flex items-center gap-x-3 text-xs font-mono bg-zinc-900 border border-zinc-700 rounded-3xl px-4 h-10">
                    <div id="last-updated" class="text-emerald-300">just now</div>
                    <div onclick="fetchData()" class="cursor-pointer hover:text-white flex items-center gap-x-1">
                        <span class="text-lg leading-none">↻</span>
                        <span>REFRESH</span>
                    </div>
                </div>

                <div onclick="window.location.reload()" class="text-zinc-400 hover:text-white cursor-pointer text-sm font-medium">
                    RESET
                </div>
            </div>
        </nav>

        <div class="px-8 py-8">
            <!-- Summary -->
            <div id="summary" class="grid grid-cols-1 md:grid-cols-5 gap-6 mb-10"></div>

            <!-- Supply Chain Risk Analytics -->
            <div class="mb-12">
                <div class="flex justify-between items-baseline mb-4">
                    <h2 class="text-3xl font-semibold">Supply Chain Risk Analytics</h2>
                    <span class="text-emerald-400 text-sm flex items-center gap-x-2">
                        <span class="relative flex h-2 w-2">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-400"></span>
                        </span>
                        REAL-TIME RISK SCORES
                    </span>
                </div>
                <div id="risk-grid" class="grid grid-cols-1 md:grid-cols-5 gap-6"></div>
            </div>

            <!-- Impacted Manufacturers -->
            <div class="mb-12">
                <h2 class="text-3xl font-semibold mb-4">Manufacturing Companies Impacted by Delays</h2>
                <div id="manufacturers-grid" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6"></div>
            </div>

            <!-- Map -->
            <div class="mb-12">
                <div class="flex items-baseline justify-between mb-4">
                    <div class="flex items-center gap-x-3">
                        <h2 class="text-3xl font-semibold">Live AIS Vessel Tracking + Port Congestion</h2>
                        <div class="px-3 py-px text-xs font-semibold bg-emerald-400/10 text-emerald-400 rounded-3xl flex items-center">
                            7 VESSELS • MULTI-SOURCE AIS
                        </div>
                    </div>
                    <button onclick="fitMapToMarkers()" 
                            class="text-xs font-medium hover:text-emerald-400 flex items-center gap-x-1">
                        <span class="text-lg">⟲</span> FIT MAP
                    </button>
                </div>
                <div id="map" class="h-[520px] rounded-3xl border border-zinc-800 shadow-2xl"></div>
            </div>

            <!-- Vessels -->
            <div class="flex items-baseline justify-between mb-6">
                <div>
                    <h2 class="text-3xl font-semibold">AIS-Tracked Fleet</h2>
                    <p class="text-zinc-400 text-sm">Container ships &amp; oil tankers • Real-time AIS from MarineTraffic, Orbcomm, Spire, ExactEarth</p>
                </div>
            </div>
            <div id="vessel-grid" class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-7 gap-6"></div>
        </div>
    </div>

    <script>
        let pollingIntervalId = null;
        let isPolling = false;
        let currentPollMs = 4000;
        let mapInstance = null;
        let vesselMarkers = {};
        let routePolylines = {};
        let portMarkers = {};

        function initMap() {
            mapInstance = L.map('map', { center: [20, 10], zoom: 2.5 });
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap • ShipTrack Real-time AIS Simulation',
                maxZoom: 19
            }).addTo(mapInstance);
        }

        function renderMap(vessels, ports) {
            Object.values(vesselMarkers).forEach(m => m.remove());
            Object.values(routePolylines).forEach(l => l.remove());
            Object.values(portMarkers).forEach(m => m.remove());
            vesselMarkers = {}; routePolylines = {}; portMarkers = {};

            vessels.forEach(vessel => {
                const iconHtml = vessel.vessel_type === 'Oil Tanker' ? '⛽' : '🚢';
                const shipIcon = L.divIcon({
                    className: 'ship-marker',
                    html: `<div style="transform:rotate(${vessel.course}deg);font-size:28px;line-height:1;">${iconHtml}</div>`,
                    iconSize: [36, 36],
                    iconAnchor: [18, 18]
                });

                const marker = L.marker([vessel.lat, vessel.lng], { icon: shipIcon }).addTo(mapInstance);

                const popupHTML = `
                    <div style="min-width:290px;font-family:Inter,sans-serif;font-size:13px;">
                        <div class="flex justify-between border-b pb-3 mb-3">
                            <div>
                                <div class="font-semibold text-lg">${vessel.vessel_name}</div>
                                <div class="font-mono text-xs">${vessel.imo} • ${vessel.mmsi}</div>
                                <div class="text-[10px] text-emerald-500">${vessel.ais_source}</div>
                            </div>
                            <div class="px-3 py-1 text-xs font-bold rounded-3xl ${vessel.impact>65?'bg-rose-400':vessel.impact>45?'bg-amber-400':'bg-emerald-400'} text-white">
                                ${vessel.impact}%
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-4 text-xs">
                            <div>CARGO<br><span class="font-medium">${vessel.cargo}</span></div>
                            <div>DESTINATION<br><span class="font-medium">${vessel.destination}</span></div>
                            <div>COURSE / SPEED<br><span class="font-medium">${vessel.course}° • ${vessel.speed_knots} kn</span></div>
                            <div>LAST AIS<br><span class="font-medium text-emerald-600">${vessel.last_ais_update}</span></div>
                        </div>
                        <div class="mt-4 bg-zinc-100 rounded-2xl p-4 flex gap-4">
                            <span class="text-4xl">${vessel.weather.icon}</span>
                            <div class="flex-1">
                                <div>${vessel.weather.condition}</div>
                                <div class="text-xs text-zinc-500">${vessel.weather.temp_c}°C • +${vessel.weather.impact}% risk</div>
                            </div>
                            <div class="text-right">
                                <div class="text-3xl font-semibold text-emerald-600">$${(vessel.value/1000000).toFixed(1)}M</div>
                            </div>
                        </div>
                        <div class="mt-4 text-xs flex justify-between">
                            <div>PORT CONGESTION</div>
                            <div class="font-mono ${vessel.destination_congestion>65?'text-rose-400':vessel.destination_congestion>40?'text-amber-400':'text-emerald-400'}">${vessel.destination_congestion}%</div>
                        </div>
                    </div>`;

                marker.bindPopup(popupHTML);
                vesselMarkers[vessel.id] = marker;

                const poly = L.polyline([[vessel.lat, vessel.lng], [vessel.dest_lat, vessel.dest_lng]],
                    {color:'#10b981', weight:2.5, opacity:0.65, dashArray:'6,4'}).addTo(mapInstance);
                routePolylines[vessel.id] = poly;
            });

            ports.forEach(port => {
                const color = port.congestion > 70 ? '#ef4444' : port.congestion > 40 ? '#f59e0b' : '#10b981';
                const portIcon = L.divIcon({
                    html: `<div style="background:${color};width:32px;height:32px;border-radius:9999px;display:flex;align-items:center;justify-content:center;color:white;font-size:18px;">🏬</div><div style="text-align:center;font-size:11px;color:${color};margin-top:2px;font-weight:700">${port.congestion}%</div>`,
                    iconSize: [40, 50],
                    iconAnchor: [20, 40]
                });
                const marker = L.marker([port.lat, port.lng], {icon: portIcon}).addTo(mapInstance);
                marker.bindPopup(`<b>${port.name}</b><br><span style="color:${color}">${port.congestion}% congestion</span>`);
                portMarkers[port.name] = marker;
            });

            if (Object.keys(vesselMarkers).length > 0) {
                const group = L.featureGroup([...Object.values(vesselMarkers), ...Object.values(portMarkers)]);
                mapInstance.fitBounds(group.getBounds().pad(0.2));
            }
        }

        function fitMapToMarkers() {
            if (mapInstance) {
                const group = L.featureGroup([...Object.values(vesselMarkers), ...Object.values(portMarkers)]);
                mapInstance.flyToBounds(group.getBounds().pad(0.25), {duration: 1.2});
            }
        }

        async function fetchData() {
            try {
                const res = await fetch('/data');
                const payload = await res.json();
                
                renderSummary(payload.vessels, payload.ports);
                renderRiskAnalytics(payload.manufacturers);
                renderManufacturers(payload.manufacturers);
                renderVessels(payload.vessels);
                if (mapInstance) renderMap(payload.vessels, payload.ports);

                const now = new Date();
                document.getElementById('last-updated').innerHTML = 
                    `<span class="text-emerald-400">●</span> ${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}:${now.getSeconds().toString().padStart(2,'0')}`;
            } catch(e) { console.error(e); }
        }

        function renderSummary(vessels, ports) {
            const totalValue = vessels.reduce((a,v)=>a+v.value,0);
            const avgImpact = Math.round(vessels.reduce((a,v)=>a+v.impact,0)/vessels.length);
            const avgSpeed = (vessels.reduce((a,v)=>a+v.speed_knots,0)/vessels.length).toFixed(1);
            const avgCong = Math.round(ports.reduce((a,p)=>a+p.congestion,0)/ports.length);

            document.getElementById('summary').innerHTML = `
                <div class="bg-zinc-900 rounded-3xl p-8"><p class="uppercase text-xs text-zinc-400">VESSELS</p><div class="text-7xl font-semibold">${vessels.length}</div></div>
                <div class="bg-zinc-900 rounded-3xl p-8"><p class="uppercase text-xs text-zinc-400">TOTAL VALUE</p><div class="text-7xl font-semibold">$${(totalValue/1000000).toFixed(1)}M</div></div>
                <div class="bg-zinc-900 rounded-3xl p-8"><p class="uppercase text-xs text-zinc-400">AVG IMPACT</p><div class="text-7xl font-semibold">${avgImpact}%</div></div>
                <div class="bg-zinc-900 rounded-3xl p-8"><p class="uppercase text-xs text-zinc-400">AVG SPEED</p><div class="text-7xl font-semibold">${avgSpeed} kn</div></div>
                <div class="bg-zinc-900 rounded-3xl p-8"><p class="uppercase text-xs text-zinc-400">AVG CONGESTION</p><div class="text-7xl font-semibold">${avgCong}%</div></div>`;
        }

        function renderRiskAnalytics(manufacturers) {
            let html = '';
            manufacturers.forEach(m => {
                const riskColor = m.risk_score > 80 ? 'rose' : m.risk_score > 65 ? 'amber' : 'emerald';
                html += `
                <div class="card bg-zinc-900 border border-zinc-800 rounded-3xl p-6">
                    <div class="flex justify-between">
                        <div class="font-medium">${m.name}</div>
                        <div class="font-mono text-xl text-${riskColor}-400">${m.risk_score}</div>
                    </div>
                    <div class="text-xs text-zinc-400 mt-1">RISK SCORE</div>
                    <div class="h-2 bg-zinc-700 rounded-full mt-6 overflow-hidden">
                        <div class="h-2 bg-${riskColor}-400 rounded-full" style="width:${m.risk_score}%"></div>
                    </div>
                </div>`;
            });
            document.getElementById('risk-grid').innerHTML = html;
        }

        function renderManufacturers(manufacturers) {
            let html = '';
            manufacturers.forEach(m => {
                const delayColor = m.delay_days > 10 ? 'rose' : m.delay_days > 5 ? 'amber' : 'emerald';
                html += `
                <div onclick="highlightVessel('${m.affected_vessel}')" class="card bg-zinc-900 border border-zinc-800 rounded-3xl p-6 cursor-pointer hover:border-emerald-400">
                    <div class="font-semibold">${m.name}</div>
                    <div class="text-6xl font-bold text-${delayColor}-400 mt-4">${m.delay_days}</div>
                    <div class="text-xs uppercase tracking-widest text-zinc-400">days delayed</div>
                </div>`;
            });
            document.getElementById('manufacturers-grid').innerHTML = html;
        }

        function highlightVessel(id) {
            if (vesselMarkers[id]) {
                mapInstance.flyTo(vesselMarkers[id].getLatLng(), 8, {duration: 1.5});
                vesselMarkers[id].openPopup();
            }
        }

        function renderVessels(vessels) {
            let html = '';
            vessels.forEach(v => {
                const color = v.impact >= 70 ? 'rose' : v.impact >= 45 ? 'amber' : 'emerald';
                const emoji = v.vessel_type === 'Oil Tanker' ? '⛽' : '🚢';
                html += `
                <div onclick="vesselMarkers['${v.id}'] && vesselMarkers['${v.id}'].openPopup()" class="card bg-zinc-900 border border-zinc-800 hover:border-emerald-400 rounded-3xl p-6 cursor-pointer">
                    <div class="flex gap-3">
                        <span class="text-4xl">${emoji}</span>
                        <div class="flex-1">
                            <div class="font-mono">${v.id}</div>
                            <div class="text-emerald-400">${v.vessel_name}</div>
                        </div>
                        <div class="px-4 py-1 text-xs font-bold rounded-3xl bg-${color}-400/10 text-${color}-400">${v.impact}%</div>
                    </div>
                    <div class="mt-8 text-xs grid grid-cols-3 gap-2">
                        <div><span class="block text-zinc-400">CONGESTION</span><span class="font-medium">${v.destination_congestion}%</span></div>
                        <div><span class="block text-zinc-400">SPEED</span><span class="font-medium">${v.speed_knots} kn</span></div>
                        <div><span class="block text-zinc-400">AIS</span><span class="font-medium text-emerald-400">${v.ais_source.split('+')[0]}</span></div>
                    </div>
                </div>`;
            });
            document.getElementById('vessel-grid').innerHTML = html;
        }

        function togglePolling() {
            const btn = document.getElementById('poll-btn');
            const text = document.getElementById('btn-text');
            const icon = document.getElementById('btn-icon');
            const input = document.getElementById('poll-interval');
            currentPollMs = Math.max(1000, parseInt(input.value) * 1000 || 4000);

            if (isPolling) {
                clearInterval(pollingIntervalId);
                isPolling = false;
                text.textContent = 'START POLLING';
                icon.textContent = '▶️';
                btn.classList.remove('bg-emerald-400', 'text-white');
                btn.classList.add('bg-white', 'text-zinc-900');
            } else {
                isPolling = true;
                text.textContent = 'STOP POLLING';
                icon.textContent = '⏹️';
                btn.classList.add('bg-emerald-400', 'text-white');
                btn.classList.remove('bg-white', 'text-zinc-900');
                fetchData();
                pollingIntervalId = setInterval(fetchData, currentPollMs);
            }
        }

        window.onload = () => {
            initMap();
            fetchData();
            const input = document.getElementById('poll-interval');
            input.addEventListener('change', () => {
                if (isPolling) {
                    clearInterval(pollingIntervalId);
                    currentPollMs = Math.max(1000, parseInt(input.value)*1000 || 4000);
                    pollingIntervalId = setInterval(fetchData, currentPollMs);
                }
            });
            console.log('%c🚢 ShipTrack Live - Real-time AIS + Supply Chain Risk Analytics ready', 'color:#10b981;font-family:monospace');
        };
    </script>
</body>
</html>
"""
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def send_container_data(self):
        global VESSELS, PORTS, MANUFACTURERS

        for vessel in VESSELS:
            # Realistic movement
            lat_diff = vessel["dest_lat"] - vessel["lat"]
            lng_diff = vessel["dest_lng"] - vessel["lng"]
            vessel["lat"] += lat_diff * (0.028 + random.random() * 0.018)
            vessel["lng"] += lng_diff * (0.028 + random.random() * 0.018)

            vessel["course"] = (vessel["course"] + random.randint(-18, 18)) % 360
            vessel["speed_knots"] = max(8 if vessel["vessel_type"] == "Oil Tanker" else 12,
                                       min(23, vessel["speed_knots"] + random.uniform(-2.8, 3.2)))

            # Weather
            if random.random() < 0.5:
                vessel["weather"]["temp_c"] = max(5, min(36, vessel["weather"]["temp_c"] + random.randint(-6, 6)))
                conditions = ["Clear Skies", "High Winds", "Stormy", "Fog", "Calm Seas", "Moderate Seas"]
                vessel["weather"]["condition"] = random.choice(conditions)
                icon_map = {"Clear Skies":"☀️","High Winds":"🌬️","Stormy":"⛈️","Fog":"🌫️","Calm Seas":"🌊","Moderate Seas":"🌊"}
                vessel["weather"]["icon"] = icon_map.get(vessel["weather"]["condition"], "🌊")
                vessel["weather"]["impact"] = 28 if vessel["weather"]["condition"] in ["Stormy","High Winds"] else 16 if vessel["weather"]["condition"] == "Fog" else random.randint(1,10)

            vessel["impact"] = max(12, min(94, vessel["impact"] + random.randint(-16, 18) + (vessel["weather"]["impact"]//4)))

            if random.random() < 0.25:
                locations = ["Strait of Malacca","Indian Ocean","Suez Canal","Atlantic Ocean","Pacific Ocean","Persian Gulf","Gulf of Mexico","Mediterranean Sea"]
                vessel["location"] = random.choice(locations)

            vessel["last_ais_update"] = "just now" if random.random() > 0.4 else f"{random.randint(15,90)} sec ago"

        # Port congestion
        for p in PORTS:
            p["congestion"] = max(15, min(92, p["congestion"] + random.randint(-12, 15)))

        for vessel in VESSELS:
            for p in PORTS:
                if p["name"] == vessel["destination"]:
                    vessel["destination_congestion"] = p["congestion"]
                    break

        # Manufacturer delays & risk scores
        for m in MANUFACTURERS:
            m["delay_days"] = max(1, min(25, m["delay_days"] + random.randint(-3, 6)))
            m["risk_score"] = max(40, min(98, m["risk_score"] + random.randint(-8, 12)))

        payload = {"vessels": VESSELS, "ports": PORTS, "manufacturers": MANUFACTURERS}

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))


def main():
    PORT = 8000
    Handler = ContainerHandler
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 ShipTrack Live AIS + Risk Analytics server started at http://localhost:{PORT}")
        print("   ✅ Real-time AIS data sources simulation (MarineTraffic, Orbcomm, Spire, ExactEarth)")
        print("   ✅ Supply Chain Risk Analytics dashboard")
        print("   ✅ Port congestion, oil tankers, impacted manufacturers")
        print("   Press Ctrl+C to stop the server\n")

        try:
            webbrowser.open(f"http://localhost:{PORT}")
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user.")
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    random.seed(42)
    main()