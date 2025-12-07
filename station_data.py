"""
Station data extracted from Supplementary Table 1 of the ESA-OTC25 Final Report
Contains information about each sampling station including coordinates and measurements collected
"""

STATION_DATA = {
    "1": {
        "name": "Station 1",
        "date": "23/4/2025",
        "lat": 69.90,
        "lon": 12.86,
        "location": "Norwegian Sea",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a", "Absorption Chl-a", "SPM*", "POC*", "SBE CTD", "Drone data"]
    },
    "2": {
        "name": "Station 2",
        "date": "24/4/2025",
        "lat": 69.81,
        "lon": 8.54,
        "location": "Norwegian Sea",
        "measurements": ["Fluorimetric Chl-a", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD", "Drone data"]
    },
    "4": {
        "name": "Station 4",
        "date": "25/4/2025",
        "lat": 69.61,
        "lon": 1.91,
        "location": "Norwegian Sea",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD", "Drone data"]
    },
    "5": {
        "name": "Station 5",
        "date": "26/4/2025",
        "lat": 69.27,
        "lon": 1.64,
        "location": "Norwegian Sea",
        "measurements": ["Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD"]
    },
    "6": {
        "name": "Station 6",
        "date": "26/4/2025",
        "lat": 69.01,
        "lon": 1.53,
        "location": "Norwegian Sea",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a", "Absorption Chl-a", "SPM*", "POC*", "SBE CTD", "Drone data"]
    },
    "7": {
        "name": "Station 7",
        "date": "28/4/2025",
        "lat": 67.99,
        "lon": -7.10,
        "location": "Norwegian Sea",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "SBE CTD", "Drone data"]
    },
    "8": {
        "name": "Station 8",
        "date": "29/4/2025",
        "lat": 67.39,
        "lon": -11.86,
        "location": "Iceland Basin",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*"]
    },
    "9A": {
        "name": "Station 9A",
        "date": "1/5/2025",
        "lat": 66.88,
        "lon": -18.03,
        "location": "Iceland Basin",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*"]
    },
    "9B": {
        "name": "Station 9B",
        "date": "1/5/2025",
        "lat": 66.80,
        "lon": -18.28,
        "location": "Iceland Basin",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*"]
    },
    "10": {
        "name": "Station 10",
        "date": "2/5/2025",
        "lat": 66.71,
        "lon": -20.85,
        "location": "Iceland Basin",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a", "SPM*"]
    },
    "11A.2": {
        "name": "Station 11A.2",
        "date": "3/5/2025",
        "lat": 66.28,
        "lon": -21.31,
        "location": "Reykjavik, Iceland",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "Drone data", "Satellite data"]
    },
    "11B": {
        "name": "Station 11B",
        "date": "3/5/2025",
        "lat": 66.27,
        "lon": -22.69,
        "location": "Reykjavik, Iceland",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "Drone data", "Satellite data"]
    },
    "12": {
        "name": "Station 12",
        "date": "10/5/2025",
        "lat": 61.99,
        "lon": -18.20,
        "location": "North Atlantic Ocean",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a (x3)", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD", "Drone data"]
    },
    "13": {
        "name": "Station 13",
        "date": "11/5/2025",
        "lat": 60.23,
        "lon": -17.27,
        "location": "North Atlantic Ocean",
        "measurements": ["HPLC Chl-a (5m)*", "Fluorimetric Chl-a (x3)", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD", "Drone data"]
    },
    "14": {
        "name": "Station 14",
        "date": "12/5/2025",
        "lat": 59.28,
        "lon": -16.49,
        "location": "North Atlantic Ocean",
        "measurements": ["HPLC Chl-a (x3)*", "Fluorimetric Chl-a (x3)", "Absorption Chl-a", "SPM*", "POC*", "SBE CTD", "Drone data"]
    },
    "Int": {
        "name": "Station Int",
        "date": "13/5/2025",
        "lat": 57.44,
        "lon": -15.47,
        "location": "North Atlantic Ocean",
        "measurements": ["Fluorimetric Chl-a (x3)", "Absorption Chl-a", "SPM*", "POC*", "Drone data", "Satellite data"]
    },
    "15": {
        "name": "Station 15",
        "date": "14/5/2025",
        "lat": 54.88,
        "lon": -16.95,
        "location": "North Atlantic Ocean",
        "measurements": ["HPLC Chl-a (2m)*", "Fluorimetric Chl-a (x3)", "Absorption Chl-a", "SPM*", "POC*", "SBE CTD", "Drone data", "Satellite data"]
    },
    "16": {
        "name": "Station 16",
        "date": "15/5/2025",
        "lat": 53.35,
        "lon": -16.38,
        "location": "North Atlantic Ocean",
        "measurements": ["HPLC Chl-a (2m)*", "Fluorimetric Chl-a (x3)", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD", "Drone data"]
    },
    "17": {
        "name": "Station 17",
        "date": "16/5/2025",
        "lat": 51.52,
        "lon": -17.17,
        "location": "North Atlantic Ocean",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a (x3)", "Absorption Chl-a", "SPM*", "POC*", "SBE CTD", "Drone data"]
    },
    "18": {
        "name": "Station 18",
        "date": "18/5/2025",
        "lat": 48.83,
        "lon": -16.37,
        "location": "North Atlantic Ocean",
        "measurements": ["HPLC Chl-a (3m)*", "Fluorimetric Chl-a (x3)", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD", "Drone data"]
    },
    "19": {
        "name": "Station 19",
        "date": "20/5/2025",
        "lat": 45.06,
        "lon": -12.35,
        "location": "North Atlantic Ocean",
        "measurements": ["Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD", "Drone data"]
    },
    "20": {
        "name": "Station 20",
        "date": "22/5/2025",
        "lat": 41.53,
        "lon": -9.11,
        "location": "North Atlantic Ocean",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a (x3)", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD", "Drone data", "Satellite data"]
    },
    "21": {
        "name": "Station 21",
        "date": "23/5/2025",
        "lat": 38.54,
        "lon": -10.53,
        "location": "Atlantic Ocean",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a (x3)", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD", "Drone data"]
    },
    "22": {
        "name": "Station 22",
        "date": "24/5/2025",
        "lat": 36.13,
        "lon": -10.53,
        "location": "Atlantic Ocean",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a (x3)", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD", "Drone data", "Satellite data"]
    },
    "23": {
        "name": "Station 23",
        "date": "25/5/2025",
        "lat": 36.97,
        "lon": -7.17,
        "location": "Mediterranean Sea",
        "measurements": ["SPM*", "SBE CTD", "Drone data", "Satellite data"]
    },
    "24": {
        "name": "Station 24",
        "date": "26/5/2025",
        "lat": 35.81,
        "lon": -6.85,
        "location": "Mediterranean Sea",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a (x3)", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD", "Drone data"]
    },
    "25": {
        "name": "Station 25",
        "date": "27/5/2025",
        "lat": 35.92,
        "lon": -4.84,
        "location": "Mediterranean Sea",
        "measurements": ["HPLC Chl-a*", "Fluorimetric Chl-a (x3)", "SPM*", "SBE CTD", "Drone data", "Satellite data"]
    },
    "26": {
        "name": "Station 26",
        "date": "28/5/2025",
        "lat": 35.65,
        "lon": -0.04,
        "location": "Mediterranean Sea",
        "measurements": ["Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD"]
    },
    "27": {
        "name": "Station 27",
        "date": "29/5/2025",
        "lat": 37.60,
        "lon": 0.15,
        "location": "Mediterranean Sea",
        "measurements": ["HPLC Chl-a*", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD"]
    },
    "28": {
        "name": "Station 28",
        "date": "30/5/2025",
        "lat": 38.88,
        "lon": 2.92,
        "location": "Mediterranean Sea",
        "measurements": ["Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD"]
    },
    "30": {
        "name": "Station 30",
        "date": "02/6/2025",
        "lat": 41.21,
        "lon": 5.75,
        "location": "Nice, France",
        "measurements": ["HPLC Chl-a*", "Absorption Chl-a", "Absorption CDOM*", "SPM*", "POC*", "SBE CTD"]
    }
}

# Abbreviations guide
ABBREVIATIONS = {
    "HPLC": "High-Performance Liquid Chromatography",
    "Chl-a": "Chlorophyll-a",
    "TSPM": "Total Suspended Particulate Matter",
    "Fluor": "Fluorimetric",
    "Abs": "Absorption",
    "CDOM": "Colored Dissolved Organic Matter",
    "SPM": "Suspended Particulate Matter",
    "POC": "Particulate Organic Carbon",
    "SBE CTD": "Sea-Bird Electronics Conductivity-Temperature-Depth sensor",
    "Sat": "Satellite"
}
