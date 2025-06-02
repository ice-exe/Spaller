# <img src="https://raw.githubusercontent.com/ice-exe/Spaller/refs/heads/main/app/icon.ico" alt="Spaller Logo" width="50" height="50" align="left"> Spaller
**Software Package Installer**

<br clear="left"/>

> A modern, elegant software package installer for Windows that simplifies bulk application installation with a beautiful dark-themed interface.

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/ice-exe/Spaller)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://github.com/ice-exe/Spaller)

---

## 🌟 Features

<div align="center">
  <img src="https://raw.githubusercontent.com/ice-exe/Spaller/refs/heads/main/images/App%20UI.png" alt="Spaller Interface" width="800" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
</div>

### ✨ **Modern Interface**
- **Dark Theme**: Eye-friendly GitHub-inspired dark interface
- **Custom Title Bar**: Frameless window with custom controls
- **Animated Elements**: Smooth transitions and pulse animations
- **Responsive Design**: Adapts to different screen sizes

### 🎯 **Smart Installation**
- **Bulk Install**: Select and install multiple applications simultaneously
- **Progress Tracking**: Real-time installation progress with detailed status
- **Category Organization**: Applications organized by type (Browsers, Gaming, Development, etc.)
- **Search Functionality**: Quick search across all applications
- **Size Estimation**: View estimated download sizes before installation

### 🔧 **User-Friendly Controls**
- **Custom Download Path**: Choose where to save installers
- **Selective Installation**: Pick exactly what you need
- **One-Click Actions**: Select all, deselect all, or select by category
- **Detailed App Info**: View publisher, version, and license information

---

## 🚀 Quick Start

### Prerequisites
- **Windows 10/11** (64-bit recommended)
- **Python 3.7+** (if running from source)
- **Internet Connection** (for downloading applications)

### 📥 Installation

#### Option 1: Download Executable (Recommended)
1. Go to [Releases](https://github.com/ice-exe/Spaller/releases)
2. Download the latest `Spaller.exe`
3. Run the executable - no installation required!

#### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/ice-exe/Spaller.git
cd Spaller

# Install dependencies
pip install -r requirements.txt

# Run the application
python Spaller.py
```

---

## 🎮 How to Use

### 1. **Launch Application**
Run Spaller and wait for the loading screen to complete while application data loads.

### 2. **Browse Categories**
- Navigate through different software categories in the left sidebar
- Use the search bar to find specific applications
- View app details by clicking the info button (ℹ)

### 3. **Select Applications**
- Click on application cards to select/deselect them
- Use "Select All" for bulk selection
- View selected count and estimated size in the bottom panel

### 4. **Configure Installation**
- Choose your download path using the "Choose Path" button
- Default location: `~/Downloads/Spaller`

### 5. **Start Installation**
- Click the "Start" button to begin installation
- Monitor progress in real-time
- Applications install silently in the background

---

## 📋 Available Applications

### 🌐 **Web Browsers**
- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- And more...

### 🎮 **Gaming Platforms**
- Steam
- Epic Games Launcher
- Battle.net
- And more...

### 💻 **Development Tools**
- Visual Studio Code
- Git
- Python
- And more...

### 🎵 **Media & Entertainment**
- VLC Media Player
- Spotify
- OBS Studio
- And more...

### 📄 **Productivity**
- LibreOffice
- Notepad++
- SumatraPDF
- And more...

---

## ⚙️ Technical Details

### Built With
- **Python 3.7+** - Core application logic
- **PySide6** - Modern Qt-based GUI framework
- **Requests** - HTTP library for downloading
- **Threading** - Multi-threaded operations for smooth UI

### Architecture
```
Spaller/
├── Spaller.py          # Main application file
├── icon.ico            # Application icon
├── requirements.txt    # Python dependencies
└── resources/
    └── apps_data.json  # Application database
```

### Key Components
- **LoadingScreen**: Animated splash screen with progress bar
- **CustomTitleBar**: Frameless window controls
- **ModernCheckBox**: Custom checkbox components with app info
- **InstallationThread**: Background installation handler
- **DataLoader**: Async application data fetching

---

## 🛠️ Configuration

### Custom Application Data
Applications are loaded from a JSON configuration file hosted on GitHub. The structure includes:

```json
{
  "Category Name": {
    "App Name": {
      "description": "App description",
      "url": "download_url",
      "installer": "filename.exe",
      "size": 50,
      "icon": "📦"
    }
  }
}
```

### Adding New Applications
To add new applications, modify the `apps_data.json` file in the repository and submit a pull request.

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 **Bug Reports**
- Use the [Issues](https://github.com/ice-exe/Spaller/issues) tab
- Include detailed steps to reproduce
- Provide system information

### 💡 **Feature Requests**
- Suggest new features via Issues
- Explain the use case and benefit
- Consider implementation complexity

### 🔧 **Code Contributions**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### 📱 **Application Requests**
- Request new applications via Issues
- Provide download links and details
- Ensure applications are freely available

---

## 📞 Support & Contact

### 🆘 **Getting Help**
- **Issues**: [GitHub Issues](https://github.com/ice-exe/Spaller/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ice-exe/Spaller/discussions)
- **Email**: [Contact Form](https://abdvlrqhman.com/contact)

### 🌐 **Stay Connected**
- **Website**: [abdvlrqhman.com](https://abdvlrqhman.com)
- **GitHub**: [@ice-exe](https://github.com/ice-exe)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Third-Party Acknowledgments
- **PySide6**: Qt for Python GUI framework
- **Requests**: HTTP library for Python
- Application installers are property of their respective owners

---

## 🎯 Roadmap

### v2.1.0 (Upcoming)
- [ ] Update checking and auto-updater
- [ ] Installation history and rollback
- [ ] Custom application categories
- [ ] Portable app support

### v2.2.0 (Future)
- [ ] Plugin system for custom installers
- [ ] Installation scheduling
- [ ] Multi-language support
- [ ] Linux/macOS compatibility

---

## 📊 Statistics

![GitHub stars](https://img.shields.io/github/stars/ice-exe/Spaller?style=social)
![GitHub forks](https://img.shields.io/github/forks/ice-exe/Spaller?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/ice-exe/Spaller?style=social)

---

<div align="center">
  <h3>⭐ If you find Spaller useful, please star the repository!</h3>
  <p><strong>Made with ❤️ by Ice</strong></p>
  <p><em>Simplifying software installation, one click at a time.</em></p>
</div>

---

<div align="center">
  <sub>© 2025 Ice. All rights reserved.</sub>
</div>
