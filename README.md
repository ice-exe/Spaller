# 🚀 Spaller - Software Package Installer

<div align="center">

![Spaller UI](https://raw.githubusercontent.com/ice-exe/Spaller/refs/heads/main/App%20UI.png)

*A modern, elegant desktop application for installing multiple software packages with ease*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-Qt-green?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/ice-exe/Spaller?style=for-the-badge&logo=github)](https://github.com/ice-exe/Spaller/stargazers)

</div>

## ✨ Features

- **🎨 Modern Dark UI** - Beautiful GitHub-inspired dark theme with smooth animations
- **📱 Frameless Design** - Custom title bar with minimize/close controls
- **🔍 Smart Search** - Real-time search across all applications and categories
- **📂 Category Organization** - Browse apps by categories like Browsers, Development Tools, Media, etc.
- **🎯 Bulk Selection** - Select all apps in a category or across all categories
- **📊 Progress Tracking** - Real-time download and installation progress with detailed status
- **📁 Custom Download Path** - Choose where to download installers
- **💾 Size Estimation** - See estimated download sizes before installation
- **🔄 Multi-threaded** - Non-blocking UI with background downloads
- **🛡️ Error Handling** - Robust error handling with user-friendly messages

## 🖥️ Screenshots

### Main Interface
The application features a clean, modern interface with:
- **Sidebar Navigation** - Easy category browsing
- **Application Cards** - Detailed app information with icons
- **Progress Tracking** - Real-time installation status
- **Smart Controls** - Intuitive selection and installation controls

## 🏗️ Architecture

### Core Components

- **`SpallerMainWindow`** - Main application window with modern UI
- **`ModernCheckBox`** - Custom styled application selection cards
- **`PulseButton`** - Animated buttons with visual feedback
- **`CustomTitleBar`** - Frameless window with custom controls
- **`LoadingScreen`** - Animated splash screen
- **`InstallationThread`** - Multi-threaded installation process
- **`DataLoader`** - Async data loading from remote sources

### Key Features Implementation

```python
# Modern UI Components
- Custom styled widgets with GitHub-inspired theme
- Smooth animations and hover effects
- Responsive layout design

# Multi-threaded Architecture
- Background data loading
- Non-blocking installation process
- Real-time progress updates

# Smart Application Management
- Dynamic category filtering
- Global search functionality
- Batch selection operations
```

## 🚀 Installation

### Prerequisites

- **Python 3.8+**
- **Windows OS** (for application installations)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/ice-exe/Spaller.git
   cd Spaller
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python spaller.py
   ```

### Dependencies

```txt
PySide6>=6.0.0
requests>=2.25.0
```

## 📝 Usage

### Getting Started

1. **Launch Spaller** - Run the application and wait for data to load
2. **Browse Categories** - Use the sidebar to explore different app categories
3. **Search Applications** - Use the search bar to find specific apps
4. **Select Applications** - Click on app cards to select them for installation
5. **Choose Download Path** - Set where installers should be downloaded
6. **Start Installation** - Click the "Start" button to begin batch installation

### Advanced Features

#### Bulk Operations
- **Select All** - Select all visible applications
- **Category Selection** - Select all apps in current category
- **Smart Deselection** - Toggle between select/deselect modes

#### Search & Filter
- **Global Search** - Search across all categories
- **Real-time Results** - Instant filtering as you type
- **Description Search** - Searches both names and descriptions

#### Installation Management
- **Progress Tracking** - See download and installation progress
- **Error Handling** - Automatic retry and error reporting
- **Concurrent Downloads** - Efficient multi-app processing

## 🔧 Configuration

### Application Data

Applications are loaded from a remote JSON source:
```
https://raw.githubusercontent.com/ice-exe/Spaller/main/resources/apps_data.json
```

### Data Structure

```json
{
  "category_name": {
    "app_name": {
      "description": "App description",
      "url": "download_url",
      "installer": "installer_filename",
      "size": 50,
      "icon": "📦"
    }
  }
}
```

### Custom Styling

The application uses a GitHub-inspired dark theme with:
- **Primary Colors**: `#58a6ff` (blue), `#238636` (green)
- **Background**: `#0d1117` (dark), `#161b22` (secondary)
- **Text**: `#f0f6fc` (primary), `#8b949e` (secondary)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

1. **🐛 Bug Reports** - Report issues on GitHub
2. **💡 Feature Requests** - Suggest new features
3. **🔧 Code Contributions** - Submit pull requests
4. **📚 Documentation** - Improve docs and examples
5. **🎨 UI/UX Improvements** - Enhance the user experience

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Maintain consistent formatting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Ice** - *Lead Developer*
- GitHub: [@ice-exe](https://github.com/ice-exe)
- Website: [abdvlrqhman.com](https://abdvlrqhman.com)

## 🙏 Acknowledgments

- **Qt/PySide6** - For the excellent cross-platform GUI framework
- **GitHub** - For UI/UX inspiration
- **Contributors** - Thanks to all who have contributed to this project

## 📊 Project Stats

- **Language**: Python
- **Framework**: PySide6 (Qt)
- **Architecture**: Multi-threaded desktop application
- **Platform**: Windows (primary), Cross-platform compatible
- **Version**: 2.0.0

---

<div align="center">

**Made with ❤️ by Ice**

[⭐ Star this project](https://github.com/ice-exe/Spaller) • [🐛 Report Bug](https://github.com/ice-exe/Spaller/issues) • [💡 Request Feature](https://github.com/ice-exe/Spaller/issues)

</div>
