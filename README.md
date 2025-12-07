# 🌊 ESA OTC25 Intelligence Panel

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://otc25.streamlit.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ESA](https://img.shields.io/badge/Funded%20by-ESA-00BFFF.svg)](https://www.esa.int/)

**Interactive visualization platform for the ESA Ocean Colour Toward Validation Cruise 2025 (OTC25)**

Comprehensive Streamlit web application showcasing results, methodology, team, and references from the ESA-funded ocean color validation campaign conducted across the North Atlantic Ocean and Mediterranean Sea (April-June 2025).

---

## 📖 About

The **ESA OTC25 campaign** was a 24-day oceanographic validation cruise aboard the R/V Sarmiento de Gamboa designed to validate satellite ocean color products through coordinated multi-platform observations.

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
- 30+ contributors from 8 international institutions
- Principal Investigators: Victoria Hill (ODL), Sébastien Clerc (ACRI-ST)
- Interactive team profiles with expertise and contributions

### 📚 References
- 30+ peer-reviewed publications
- Categorized bibliography (algorithms, validation, hyperspectral, BGC-Argo)
- AI chatbot for literature queries
- Full DOI citations

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

## 📦 Project Structure

```
OTC_panel/
├── app.py                  # Main Streamlit application
├── image_data.py           # Base64-encoded images
├── station_data.py         # Station metadata
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── resources/             # Image assets (logos, photos, figures)
└── .streamlit/            # Streamlit configuration
    └── config.toml        # Theme settings
```

---

## 🛰️ Data Sources

**Note**: Raw datasets are not included in this repository due to data privacy. The application displays pre-processed, aggregated results.

- **Satellite**: Sentinel-3 OLCI, MODIS Aqua, PACE OCI  
- **In-situ**: HPLC chlorophyll-a, fluorometry, AC-S absorption/attenuation  
- **BGC-Argo**: Hyperspectral radiometry (WMO 5906995, 7901133)  
- **Drones**: Multispectral aerial surveys  
- **Inline**: Continuous flow-through measurements  

---

## 🌐 Deployment

### Streamlit Community Cloud

1. Push to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy!

---

## 🎨 Technology Stack

- **Frontend**: Streamlit 1.41.1
- **Data**: Pandas 2.2.3
- **Visualization**: Plotly 5.24.1
- **AI**: Anthropic Claude API
- **Design**: Custom CSS, responsive layout

---

## 🙏 Acknowledgments

### Funding
**European Space Agency (ESA)** - Ocean Colour Toward Validation Cruise 2025

### Principal Investigators
- **Victoria Hill** - Old Dominion University (ODL)
- **Sébastien Clerc** - ACRI-ST

### Contributing Institutions
Old Dominion University (ODL) • ACRI-ST • OneOcean • NASA Ocean Ecology Laboratory • Nansen Environmental and Remote Sensing Center (NERSC) • Laboratoire d'Etudes en Géophysique et Océanographie Spatiales (Lemkhul) • The Plocan Service (TPS) • Indra

### R/V Sarmiento de Gamboa
Spanish National Research Council (CSIC) for vessel operations

---

## 📞 Contact

**Project Maintainer**: Alejandro Román Gonzalo  
📧 **Email**: alejandro.roman.gonzalo@gmail.com  
🔬 **Institution**: ICMAN-CSIC, Puerto Real, Spain  
🔗 **ORCID**: [0000-0002-6989-7510](https://orcid.org/0000-0002-6989-7510)  
💼 **LinkedIn**: [Alejandro Román Gonzalo](https://www.linkedin.com/in/alejandro-román-gonzalo/)

**Campaign Lead**: Victoria Hill (ODL) • Sébastien Clerc (ACRI-ST)

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

**Made with ❤️ for ocean science**

🌊 *Advancing ocean color validation through multi-platform observations* 🛰️

[![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)](https://streamlit.io/)

</div>
