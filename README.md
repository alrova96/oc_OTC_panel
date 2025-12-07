# 🌊 ESA OTC25 Intelligence Panel

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://otc25.streamlit.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ESA](https://img.shields.io/badge/Funded%20by-ESA-00BFFF.svg)](https://www.esa.int/)

**Interactive visualization platform for the ESA Ocean Colour Toward Validation Cruise 2025 (OTC25)**

Comprehensive Streamlit web application showcasing results, methodology, team, and references from the ESA-funded ocean color validation campaign conducted across the North Atlantic Ocean and Mediterranean Sea (April-June 2025).

---

## 📖 About

The **ESA OTC25 campaign** was an oceanographic validation exercise carried out aboard the tall ship Statsraad Lehmkuhl, with the goal of validating satellite ocean color products through coordinated multi-platform observations.

### 🎯 Scientific Objectives

- **Multi-platform validation**: HPLC chlorophyll, in-situ optical sensors, BGC-Argo floats, drones, satellites
- **Algorithm assessment**: Empirical (OC4ME) vs machine learning (Neural Networks) for chlorophyll retrieval
- **Hyperspectral validation**: BGC-Argo RAMSES radiometers and PACE OCI satellite mission
- **Geographic gradients**: 30 stations from Norwegian Sea to Mediterranean Sea

---

## 🚀 Features

### 📊 Data Analysis
- Interactive chlorophyll time series (satellite vs in-situ)
- Matchup scatter plots with statistical metrics (R², RMSE, bias)
- Geographic distribution of measurement differences
- Ocean color maps and satellite-derived products
- BGC-Argo hyperspectral float measurements

### 🔬 Methodology
- Detailed instrument cards (CTD, fluorescence, turbidity, PAR, oxygen)
- Satellite missions (Sentinel-3, MODIS, PACE)
- Drone multispectral operations
- BGC-Argo autonomous profiling floats
- AI-powered methodology chatbot

### 👥 Team
- 6 contributors from different international institutions
- Team members: Lou Andrès, Mathurin Choblet, Alba L. Guzmán-Morales, Sejal Pramlall, Alejandro Román, Luz M. Suklje
- Interactive team profiles with expertise and contributions

### 📚 References
- 30+ peer-reviewed publications
- Categorized bibliography (algorithms, validation, hyperspectral, BGC-Argo)
- AI chatbot for literature queries

---

## 🛠️ Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/OTC_panel.git
cd OTC_panel

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Requirements
- Python 3.9+
- See `requirements.txt` for packages

---

## 🛰️ Data Sources

**Note**: Raw datasets are not included in this repository due to data privacy. The application displays pre-processed, aggregated results.

- **Satellite**: Sentinel-3 OLCI, MODIS Aqua, PACE OCI  
- **In-situ**: HPLC chlorophyll-a, fluorometry, AC-S absorption/attenuation  
- **BGC-Argo**: Hyperspectral radiometry (WMO 5906995, 7901133)  
- **Drones**: Multispectral aerial surveys  
- **Inline**: Continuous flow-through measurements  

---

## 🎨 Technology Stack

- **Frontend**: Streamlit 1.41.1
- **Data**: Pandas 2.2.3
- **Visualization**: Plotly 5.24.1
- **AI**: Anthropic Claude API
- **Design**: Custom CSS, responsive layout

---

## 📄 License

This project is licensed under the MIT License.

---
