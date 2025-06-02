import sys
import os
import json
import requests
import subprocess
import threading
import time
from urllib.parse import urlparse

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QPushButton, QCheckBox, QScrollArea,
                              QFrame, QProgressBar, QFileDialog, QMessageBox, QSplashScreen,
                              QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy, QToolTip,
                              QLineEdit)
from PySide6.QtCore import Qt, QThread, Signal, QPropertyAnimation, QEasingCurve, QTimer, QRect, QPoint, QSize
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor, QLinearGradient, QPen, QBrush, QMouseEvent, QCursor, QIcon
import webbrowser

class LoadingScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap(450, 280)
        pixmap.fill(QColor(13, 17, 23))
        
        super().__init__(pixmap)
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        
        self.progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(13, 17, 23))
        painter.drawRoundedRect(self.rect(), 12, 12)
        
        painter.setPen(QColor(88, 166, 255))
        painter.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title_rect = QRect(0, 70, self.width(), 40)
        painter.drawText(title_rect, Qt.AlignCenter, "Spaller")
        
        painter.setPen(QColor(125, 133, 144))
        painter.setFont(QFont("Segoe UI", 12))
        subtitle_rect = QRect(0, 120, self.width(), 25)
        painter.drawText(subtitle_rect, Qt.AlignCenter, "Software Package Installer")
        
        bar_width = 300
        bar_height = 4
        bar_x = (self.width() - bar_width) // 2
        bar_y = 180
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(33, 38, 45))
        painter.drawRoundedRect(bar_x, bar_y, bar_width, bar_height, 2, 2)
        
        progress_width = int((bar_width * self.progress) / 100)
        if progress_width > 0:
            gradient = QLinearGradient(bar_x, 0, bar_x + progress_width, 0)
            gradient.setColorAt(0, QColor(88, 166, 255))
            gradient.setColorAt(1, QColor(58, 139, 253))
            painter.setBrush(QBrush(gradient))
            painter.drawRoundedRect(bar_x, bar_y, progress_width, bar_height, 2, 2)
        
        painter.setPen(QColor(125, 133, 144))
        painter.setFont(QFont("Segoe UI", 10))
        status_rect = QRect(0, 220, self.width(), 25)
        painter.drawText(status_rect, Qt.AlignCenter, "Loading application data...")
    
    def update_progress(self):
        self.progress = (self.progress + 2) % 101
        self.update()

class CustomTitleBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(45)
        self.setup_ui()
        self.drag_position = QPoint()
    
    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #161b22;
                border: none;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 15, 12)
        layout.setSpacing(12)
        
        title_label = QLabel("Spaller")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setStyleSheet("color: #58a6ff; border: none;")
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Software Package Installer")
        subtitle_label.setFont(QFont("Segoe UI", 9))
        subtitle_label.setStyleSheet("color: #8b949e; border: none;")
        layout.addWidget(subtitle_label)
        
        layout.addStretch()
        
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(6)
        
        self.minimize_btn = QPushButton("−")
        self.minimize_btn.setFixedSize(30, 22)
        self.minimize_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #21262d;
                color: #f0f6fc;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #30363d;
            }
            QPushButton:pressed {
                background-color: #1c2128;
            }
        """)
        self.minimize_btn.clicked.connect(self.minimize_window)
        controls_layout.addWidget(self.minimize_btn)
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(30, 22)
        self.close_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #da3633;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f85149;
            }
            QPushButton:pressed {
                background-color: #b91c1c;
            }
        """)
        self.close_btn.clicked.connect(self.close_window)
        controls_layout.addWidget(self.close_btn)
        
        layout.addLayout(controls_layout)
    
    def minimize_window(self):
        if self.parent_window:
            self.parent_window.showMinimized()
    
    def close_window(self):
        if self.parent_window:
            self.parent_window.close()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.parent_window.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

class PulseButton(QPushButton):
    def __init__(self, text, style="primary", icon="", parent=None):
        super().__init__(parent)
        self.button_style = style
        self.icon_text = icon
        self.setup_style()
        self.setText(f"{icon} {text}" if icon else text)
        
        self.animation = QPropertyAnimation(self, b"size")
        self.animation.setDuration(1000)
        self.animation.setLoopCount(-1)  # Infinite loop
        self.pulse_active = False
    
    def setup_style(self):
        styles = {
            "primary": {
                "bg": "#238636",
                "hover": "#2ea043",
                "text": "#ffffff",
                "disabled": "#21262d"
            },
            "secondary": {
                "bg": "#21262d", 
                "hover": "#30363d",
                "text": "#f0f6fc",
                "disabled": "#21262d"
            },
            "accent": {
                "bg": "#1f6feb",
                "hover": "#388bfd", 
                "text": "#ffffff",
                "disabled": "#21262d"
            },
            "danger": {
                "bg": "#da3633",
                "hover": "#f85149",
                "text": "#ffffff",
                "disabled": "#21262d"
            }
        }
        
        style = styles.get(self.button_style, styles["primary"])
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {style['bg']};
                color: {style['text']};
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-family: 'Segoe UI';
                font-size: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {style['hover']};
            }}
            QPushButton:pressed {{
                background-color: {style['bg']};
            }}
            QPushButton:disabled {{
                background-color: {style['disabled']};
                color: #484f58;
            }}
        """)
    
    def start_pulse(self):
        """Start pulsing animation"""
        if not self.pulse_active:
            original_size = self.size()
            self.animation.setStartValue(original_size)
            self.animation.setKeyValueAt(0.5, QSize(original_size.width() + 5, original_size.height() + 2))
            self.animation.setEndValue(original_size)
            self.animation.start()
            self.pulse_active = True
    
    def stop_pulse(self):
        """Stop pulsing animation"""
        if self.pulse_active:
            self.animation.stop()
            self.pulse_active = False
    
    def setEnabled(self, enabled):
        """Override to control pulse animation"""
        super().setEnabled(enabled)
        if enabled:
            self.start_pulse()
        else:
            self.stop_pulse()

class ModernCheckBox(QFrame):
    stateChanged = Signal(bool)
    
    def __init__(self, title, description="", app_id="", app_size=50, app_icon="📦", parent=None):
        super().__init__(parent)
        self.title = title
        self.description = description
        self.app_id = app_id
        self.app_size = app_size  # Size in MB
        self.app_icon = app_icon  # Icon from JSON
        self.is_checked = False
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        self.setMinimumHeight(70)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setCursor(Qt.PointingHandCursor)  # Make entire card clickable
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 12, 18, 12)
        layout.setSpacing(12)
        
        icon_label = QLabel(self.app_icon)
        icon_label.setFont(QFont("Segoe UI", 16))
        icon_label.setFixedSize(32, 32)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("""
            QLabel {
                background-color: #21262d;
                border-radius: 6px;
                color: #58a6ff;
                border: none;
            }
        """)
        
        layout.addWidget(icon_label)
        
        self.checkbox = QCheckBox()
        self.checkbox.setFixedSize(20, 20)
        self.checkbox.stateChanged.connect(self._on_checkbox_changed)
        layout.addWidget(self.checkbox)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)
        
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)
        
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title_label.setStyleSheet("color: #f0f6fc; border: none;")
        title_label.setWordWrap(True)
        title_layout.addWidget(title_label)
        
        info_btn = QPushButton("ℹ")
        info_btn.setFixedSize(18, 18)
        info_btn.setFont(QFont("Segoe UI", 10))
        info_btn.setStyleSheet("""
            QPushButton {
                background-color: #30363d;
                color: #58a6ff;
                border: none;
                border-radius: 9px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #58a6ff;
                color: #ffffff;
            }
        """)
        
        tooltip_text = f"{self.app_icon} {self.title}\n👤 Publisher: {self.get_publisher()}\n📊 Version: Latest\n💾 Size: ~{self.app_size}MB\n\nClick for more details"
        info_btn.setToolTip(tooltip_text)
        info_btn.clicked.connect(lambda: self.show_app_info())
        title_layout.addWidget(info_btn)
        title_layout.addStretch()
        
        text_layout.addLayout(title_layout)
        
        if self.description:
            desc_label = QLabel(self.description)
            desc_label.setFont(QFont("Segoe UI", 9))
            desc_label.setStyleSheet("color: #8b949e; border: none;")
            desc_label.setWordWrap(True)
            desc_label.setMaximumHeight(40)
            text_layout.addWidget(desc_label)
        
        layout.addLayout(text_layout)
        
        size_label = QLabel(f"{self.app_size} MB")
        size_label.setFont(QFont("Segoe UI", 9))
        size_label.setStyleSheet("color: #8b949e; border: none;")
        size_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(size_label)
    
    def _on_checkbox_changed(self, state):
        """Internal handler for checkbox state changes"""
        self.is_checked = state == Qt.Checked.value
        self.update_checkbox_appearance(state)
        self.stateChanged.emit(self.is_checked)
    
    def get_publisher(self):
        """Get publisher info for the app"""
        publishers = {
            "chrome": "Google LLC", "firefox": "Mozilla", "edge": "Microsoft",
            "steam": "Valve Corporation", "epic": "Epic Games", "battle": "Blizzard",
            "discord": "Discord Inc.", "vscode": "Microsoft", "git": "Git Team",
            "vlc": "VideoLAN", "spotify": "Spotify AB", "obs": "OBS Project",
            "libre": "The Document Foundation", "notepad": "Don Ho", 
            "sumatra": "Krzysztof Kowalczyk", "power": "Microsoft"
        }
        
        title_lower = self.title.lower()
        for key, publisher in publishers.items():
            if key in title_lower:
                return publisher
        return "Unknown Publisher"
    
    def get_license(self):
        """Get license info for the app"""
        licenses = {
            "chrome": "Proprietary", "firefox": "MPL 2.0", "edge": "Proprietary",
            "steam": "Proprietary", "epic": "Proprietary", "battle": "Proprietary",
            "discord": "Proprietary", "vscode": "MIT", "git": "GPL v2",
            "vlc": "GPL v2", "spotify": "Proprietary", "obs": "GPL v2",
            "libre": "MPL 2.0", "notepad": "GPL v3", "sumatra": "GPL v3",
            "power": "Proprietary"
        }
        
        title_lower = self.title.lower()
        for key, license in licenses.items():
            if key in title_lower:
                return license
        return "Unknown"
    
    def show_app_info(self):
        """Show detailed app information"""
        QMessageBox.information(self, f"{self.title} - Information", 
                               f"Application: {self.title}\n"
                               f"Publisher: {self.get_publisher()}\n"
                               f"Description: {self.description}\n"
                               f"Version: Latest Available\n"
                               f"Size: ~{self.app_size} MB\n"
                               f"License: {self.get_license()}")
    
    def setup_style(self):
        self.checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 0px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 2px solid #30363d;
                background-color: #161b22;
            }
            QCheckBox::indicator:hover {
                border-color: #58a6ff;
                background-color: #1c2128;
            }
            QCheckBox::indicator:checked {
                background-color: #238636;
                border-color: #238636;
            }
        """)
        
        self.setStyleSheet("""
            QFrame {
                background-color: #161b22;
                border: 1px solid #21262d;
                border-radius: 5px;
                margin: 1px;
            }
        """)
    
    def update_checkbox_appearance(self, state):
        if state == Qt.Checked.value:
            self.checkbox.setText("✓")
            self.checkbox.setStyleSheet("""
                QCheckBox {
                    spacing: 0px;
                    color: white;
                    font-weight: bold;
                    font-size: 10px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 3px;
                    border: 2px solid #238636;
                    background-color: #238636;
                }
            """)
        else:
            self.checkbox.setText("")
            self.checkbox.setStyleSheet("""
                QCheckBox {
                    spacing: 0px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 3px;
                    border: 2px solid #30363d;
                    background-color: #161b22;
                }
                QCheckBox::indicator:hover {
                    border-color: #58a6ff;
                    background-color: #1c2128;
                }
            """)
    
    def mousePressEvent(self, event):
        """Make entire card clickable"""
        if event.button() == Qt.LeftButton:
            new_state = not self.checkbox.isChecked()
            self.checkbox.setChecked(new_state)
        super().mousePressEvent(event)
    
    def isChecked(self):
        return self.checkbox.isChecked()
    
    def setChecked(self, checked):
        self.checkbox.blockSignals(True)
        self.checkbox.setChecked(checked)
        self.checkbox.blockSignals(False)
        
        self.is_checked = checked
        self.update_checkbox_appearance(Qt.Checked.value if checked else Qt.Unchecked.value)
        self.stateChanged.emit(checked)
    
    def get_size(self):
        """Return app size in MB"""
        return self.app_size

class CategoryButton(QPushButton):
    def __init__(self, text, count=0, parent=None):
        super().__init__(parent)
        self.category_text = text
        self.count = count
        self.is_active = False
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedHeight(42)
        self.setText(f"{self.category_text}")
        self.setFont(QFont("Segoe UI", 10))
        self.update_style()
        self.setCursor(Qt.PointingHandCursor)
    
    def update_style(self):
        if self.is_active:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #21262d;
                    color: #f0f6fc;
                    border: none;
                    border-left: 3px solid #58a6ff;
                    border-radius: 0px;
                    padding: 10px 16px;
                    text-align: left;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #30363d;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #161b22;
                    color: #7d8590;
                    border: none;
                    border-left: 3px solid transparent;
                    border-radius: 0px;
                    padding: 10px 16px;
                    text-align: left;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #21262d;
                    color: #f0f6fc;
                }
            """)
    
    def set_active(self, active):
        self.is_active = active
        self.update_style()
    
    def set_count(self, count):
        self.count = count
        display_text = f"{self.category_text} ({count})"
        if len(display_text) > 20:
            display_text = f"{self.category_text[:12]}... ({count})"
        self.setText(display_text)

class EmptyStateWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 40, 20, 40)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)
        
        icon_label = QLabel("📦")
        icon_label.setFont(QFont("Segoe UI", 32))
        icon_label.setStyleSheet("color: #30363d;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        title_label = QLabel("No Applications Selected")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setStyleSheet("color: #8b949e;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        message_label = QLabel("Select applications from the list above to install them.")
        message_label.setFont(QFont("Segoe UI", 11))
        message_label.setStyleSheet("color: #6e7681;")
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

class DataLoader(QThread):
    data_loaded = Signal(dict)
    status_updated = Signal(str)
    error_occurred = Signal(str)
    
    def run(self):
        try:
            self.status_updated.emit("Connecting to server...")
            response = requests.get(
                "https://raw.githubusercontent.com/ice-exe/Spaller/main/resources/apps_data.json",
                timeout=15
            )
            response.raise_for_status()
            
            self.status_updated.emit("Processing data...")
            data = response.json()
            
            self.status_updated.emit("Ready!")
            self.data_loaded.emit(data)
            
        except Exception as e:
            self.error_occurred.emit(str(e))

class SpallerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.apps_data = {}
        self.selected_apps = {}
        self.app_checkboxes = {}
        self.current_category = None
        self.category_buttons = {}
        self.downloading = False
        
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads", "Spaller")
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setFixedSize(1000, 650)
        
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - 1000) // 2
        y = (screen.height() - 650) // 2
        self.move(x, y)
        
        main_container = QFrame()
        main_container.setStyleSheet("""
            QFrame {
                background-color: #0d1117;
                border-radius: 6px;
                border: 1px solid #21262d;
            }
        """)
        self.setCentralWidget(main_container)
        
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        self.create_header(main_layout)
        
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        self.create_sidebar(content_layout)
        
        self.create_main_content(content_layout)
        
        main_layout.addLayout(content_layout)
        
        self.create_bottom_section(main_layout)
        
        self.create_footer(main_layout)
    
    def create_header(self, layout):
        header = QFrame()
        header.setFixedHeight(75)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #161b22, stop:1 #1c2128);
                border: none;
                border-bottom: 1px solid #21262d;
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(25, 15, 25, 15)
        header_layout.setSpacing(20)
        
        path_layout = QVBoxLayout()
        path_layout.setSpacing(3)
        
        path_label = QLabel("📁 Download Path:")
        path_label.setFont(QFont("Segoe UI", 8))
        path_label.setStyleSheet("color: #8b949e; border: none;")
        path_layout.addWidget(path_label)
        
        self.path_display = QLabel(self.truncate_path(self.download_path))
        self.path_display.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.path_display.setStyleSheet("color: #f0f6fc; border: none;")
        self.path_display.setToolTip(self.download_path)  # Full path on hover
        self.path_display.setMaximumWidth(300)
        path_layout.addWidget(self.path_display)
        
        header_layout.addLayout(path_layout)
        
        search_layout = QVBoxLayout()
        search_layout.setSpacing(3)
        
        search_label = QLabel("🔍 Search Apps:")
        search_label.setFont(QFont("Segoe UI", 8))
        search_label.setStyleSheet("color: #8b949e; border: none;")
        search_layout.addWidget(search_label)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search applications...")
        self.search_bar.setFixedWidth(200)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background-color: #21262d;
                border: 1px solid #30363d;
                border-radius: 4px;
                padding: 6px 10px;
                color: #f0f6fc;
                font-size: 9px;
            }
            QLineEdit:focus {
                border-color: #58a6ff;
            }
        """)
        self.search_bar.textChanged.connect(self.filter_apps)
        search_layout.addWidget(self.search_bar)
        
        header_layout.addLayout(search_layout)
        header_layout.addStretch()
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)  # More spacing between button groups
        
        selection_group = QHBoxLayout()
        selection_group.setSpacing(8)
        
        self.select_all_btn = PulseButton("Select All", "accent")
        self.select_all_btn.setFixedSize(85, 30)
        self.select_all_btn.clicked.connect(self.toggle_select_all)
        selection_group.addWidget(self.select_all_btn)
        
        buttons_layout.addLayout(selection_group)
        
        path_group = QHBoxLayout()
        path_group.setSpacing(8)
        
        self.path_btn = PulseButton("Choose Path", "secondary", "📁")
        self.path_btn.setFixedSize(110, 30)
        self.path_btn.clicked.connect(self.choose_path)
        path_group.addWidget(self.path_btn)
        
        buttons_layout.addLayout(path_group)
        
        header_layout.addLayout(buttons_layout)
        
        layout.addWidget(header)
    
    def truncate_path(self, path, max_length=35):
        """Truncate path for display"""
        if len(path) <= max_length:
            return path
        return "..." + path[-(max_length-3):]
    
    def filter_apps(self, text):
        """Filter applications globally across all categories"""
        if not hasattr(self, 'apps_data') or not self.apps_data:
            return
        
        search_text = text.lower()
        
        if not search_text:
            if self.current_category:
                self.switch_category(self.current_category)
            return
        
        self.app_checkboxes.clear()
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        found_apps = []
        for category, apps in self.apps_data.items():
            for app_name, app_info in apps.items():
                if (search_text in app_name.lower() or 
                    search_text in app_info.get('description', '').lower()):
                    found_apps.append((category, app_name, app_info))
        
        self.category_title.setText(f"Search Results for '{text}'")
        self.category_count.setText(f"({len(found_apps)} applications found)")
        
        for category, app_name, app_info in found_apps:
            app_id = f"{category}:{app_name}"
            
            app_size = app_info.get('size', 50)
            app_icon = app_info.get('icon', '📦')
            
            checkbox = ModernCheckBox(app_name, app_info['description'], app_id, app_size, app_icon)
            self.scroll_layout.addWidget(checkbox)
            
            self.app_checkboxes[app_id] = checkbox
            
            if app_id in self.selected_apps:
                checkbox.setChecked(self.selected_apps[app_id]['selected'])
            
            checkbox.stateChanged.connect(
                lambda checked, aid=app_id: self.update_selection(aid, checked)
            )
        
        if not found_apps:
            empty_widget = QWidget()
            empty_layout = QVBoxLayout(empty_widget)
            empty_layout.setAlignment(Qt.AlignCenter)
            
            empty_label = QLabel("No applications found matching your search.")
            empty_label.setFont(QFont("Segoe UI", 12))
            empty_label.setStyleSheet("color: #8b949e;")
            empty_label.setAlignment(Qt.AlignCenter)
            
            empty_layout.addWidget(empty_label)
            self.scroll_layout.addWidget(empty_widget)
        
        self.scroll_layout.addStretch()
        
        self.update_selected_count()
    
    def create_sidebar(self, layout):
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #161b22;
                border: none;
                border-right: 1px solid #21262d;
            }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 15, 0, 0)
        sidebar_layout.setSpacing(0)
        
        categories_label = QLabel("Categories")
        categories_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        categories_label.setStyleSheet("color: #f0f6fc; padding: 0 16px 12px 16px; border: none;")
        sidebar_layout.addWidget(categories_label)
        
        self.categories_container = QVBoxLayout()
        self.categories_container.setSpacing(1)
        sidebar_layout.addLayout(self.categories_container)
        
        sidebar_layout.addStretch()
        layout.addWidget(sidebar)
    
    def create_main_content(self, layout):
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame { 
                background-color: #0d1117; 
                border: none; 
            }
        """)
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 15, 15, 15)
        content_layout.setSpacing(12)
        
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(3)
        
        self.category_title = QLabel("")
        self.category_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.category_title.setStyleSheet("color: #f0f6fc; border: none;")
        self.category_title.setWordWrap(True)
        title_layout.addWidget(self.category_title)
        
        self.category_count = QLabel("")
        self.category_count.setFont(QFont("Segoe UI", 10))
        self.category_count.setStyleSheet("color: #8b949e; border: none;")
        title_layout.addWidget(self.category_count)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        self.select_category_btn = PulseButton("Select All", "secondary")
        self.select_category_btn.setFixedSize(85, 28)
        self.select_category_btn.clicked.connect(self.select_current_category)
        header_layout.addWidget(self.select_category_btn)
        
        content_layout.addLayout(header_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
                background: transparent;
            }
            QScrollBar:vertical {
                background-color: #21262d;
                width: 16px;
                border-radius: 8px;
                border: none;
                margin: 3px;
            }
            QScrollBar::handle:vertical {
                background-color: #58a6ff;
                border-radius: 8px;
                min-height: 25px;
                border: none;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #388bfd;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
                background: transparent;
            }
        """)
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 8, 0)
        self.scroll_layout.setSpacing(6)
        
        # Empty state widget (will be shown when no apps are selected)
        self.empty_state = EmptyStateWidget()
        
        scroll_area.setWidget(self.scroll_widget)
        content_layout.addWidget(scroll_area)
        
        layout.addWidget(content_frame)
    
    def create_bottom_section(self, layout):
        bottom_frame = QFrame()
        bottom_frame.setFixedHeight(85)  # Increased height for better spacing
        bottom_frame.setStyleSheet("""
            QFrame {
                background-color: #0d1117;
                border: none;
                border-top: 1px solid #21262d;
            }
        """)
        
        bottom_layout = QVBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(30, 20, 30, 20)  # Better margins
        bottom_layout.setSpacing(12)  # More spacing between elements
        
        top_row_layout = QHBoxLayout()
        top_row_layout.setSpacing(15)
        
        self.selected_count_label = QLabel("No applications selected")
        self.selected_count_label.setFont(QFont("Segoe UI", 10))  # Slightly larger font
        self.selected_count_label.setStyleSheet("color: #8b949e; border: none;")
        top_row_layout.addWidget(self.selected_count_label)
        
        top_row_layout.addStretch(1)  # Push button to the right
        
        self.install_btn = PulseButton("Start", "primary", "▶")
        self.install_btn.setFixedSize(120, 45)  # Significantly increased height from 36 to 45
        self.install_btn.clicked.connect(self.start_installation)
        self.install_btn.setEnabled(False)  # Start disabled
        top_row_layout.addWidget(self.install_btn)
        
        bottom_layout.addLayout(top_row_layout)
        
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(20)  # More spacing

        self.status_label = QLabel("Ready to install")
        self.status_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.status_label.setStyleSheet("color: #f0f6fc; border: none;")
        self.status_label.setFixedWidth(140)  # Further reduced width
        progress_layout.addWidget(self.status_label)

        # Progress bar in the middle - improved styling with proper alignment
        progress_container = QWidget()
        progress_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # Allow progress bar to expand
        progress_container_layout = QVBoxLayout(progress_container)
        progress_container_layout.setContentsMargins(0, 0, 0, 0)
        progress_container_layout.setSpacing(0)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(12)  # Taller progress bar
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 6px;
                background-color: #21262d;
                text-align: center;
                color: #f0f6fc;
                font-size: 9px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #58a6ff, stop:1 #388bfd);
            }
        """)
        progress_container_layout.addWidget(self.progress_bar, 0, Qt.AlignVCenter)
        progress_layout.addWidget(progress_container, 1)  # Give progress bar stretch factor of 1
        
        # Add a spacer widget to create space where the button used to be
        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(140)  # Width similar to the button container
        progress_layout.addWidget(spacer_widget)

        bottom_layout.addLayout(progress_layout)
        
        layout.addWidget(bottom_frame)
    
    def create_footer(self, layout):
        footer = QFrame()
        footer.setFixedHeight(28)
        footer.setStyleSheet("""
            QFrame {
                background-color: #161b22;
                border: none;
            }
        """)
        
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(25, 8, 25, 8)
        
        copyright_label = QLabel("© 2025 Ice - github.com/ice-exe")
        copyright_label.setFont(QFont("Segoe UI", 8))
        copyright_label.setStyleSheet("color: #8b949e; border: none;")
        footer_layout.addWidget(copyright_label)
        
        footer_layout.addStretch()
        
        version_label = QLabel("v2.0.0")
        version_label.setFont(QFont("Segoe UI", 8))
        version_label.setStyleSheet("color: #8b949e; border: none;")
        footer_layout.addWidget(version_label)
        
        layout.addWidget(footer)
    
    def load_data(self):
        self.loader = DataLoader()
        self.loader.data_loaded.connect(self.on_data_loaded)
        self.loader.error_occurred.connect(self.on_data_error)
        self.loader.start()
    
    def on_data_loaded(self, data):
        self.apps_data = data
        self.initialize_selection_state()
        self.setup_categories()
        if self.apps_data:
            first_category = list(self.apps_data.keys())[0]
            self.switch_category(first_category)
    
    def on_data_error(self, error):
        
        result = QMessageBox.critical(
            self,
            "Connection Error",
            f"Failed to load application data:\n{error}\n\nClick OK to visit the developer's contact page for assistance.",
            QMessageBox.Ok | QMessageBox.Cancel
        )
        
        if result == QMessageBox.Ok:
            webbrowser.open('https://abdvlrqhman.com/contact')
            
        self.close()  # Close the application since we can't proceed without data
    
    def initialize_selection_state(self):
        """Initialize the global selection state for all apps"""
        self.selected_apps = {}
        for category, apps in self.apps_data.items():
            for app_name, app_info in apps.items():
                app_id = f"{category}:{app_name}"
                app_size = app_info.get('size', 50)
                self.selected_apps[app_id] = {
                    'selected': False,
                    'info': app_info,
                    'category': category,
                    'name': app_name,
                    'size': app_size
                }
    
    def setup_categories(self):
        for category in self.apps_data.keys():
            btn = CategoryButton(category, len(self.apps_data[category]))
            btn.clicked.connect(lambda checked, cat=category: self.switch_category(cat))
            self.categories_container.addWidget(btn)
            self.category_buttons[category] = btn
    
    def switch_category(self, category):
        for cat, btn in self.category_buttons.items():
            btn.set_active(cat == category)
        
        self.current_category = category
        
        apps_count = len(self.apps_data.get(category, {}))
        self.category_title.setText(category)
        self.category_count.setText(f"({apps_count} applications available)")
        
        self.app_checkboxes.clear()
        
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if category in self.apps_data:
            for app_name, app_info in self.apps_data[category].items():
                app_id = f"{category}:{app_name}"
                
                app_size = app_info.get('size', 50)
                app_icon = app_info.get('icon', '📦')
                
                checkbox = ModernCheckBox(app_name, app_info['description'], app_id, app_size, app_icon)
                self.scroll_layout.addWidget(checkbox)
                
                self.app_checkboxes[app_id] = checkbox
                
                if app_id in self.selected_apps:
                    checkbox.setChecked(self.selected_apps[app_id]['selected'])
                
                checkbox.stateChanged.connect(
                    lambda checked, aid=app_id: self.update_selection(aid, checked)
                )
        
        self.scroll_layout.addStretch()
        
        self.update_selected_count()
    
    def update_selection(self, app_id, checked):
        """Update the global selection state"""
        if app_id in self.selected_apps:
            self.selected_apps[app_id]['selected'] = checked
            self.update_selected_count()
    
    def update_selected_count(self):
        """Update the selected applications count with enhanced feedback"""
        selected_count = sum(1 for app in self.selected_apps.values() if app['selected'])
        
        if selected_count == 0:
            self.selected_count_label.setText("Select applications to install from the list above")
            self.selected_count_label.setStyleSheet("color: #8b949e; border: none; font-style: italic;")
            self.install_btn.setText("Start")
            self.install_btn.setEnabled(False)
        else:
            estimated_size = sum(app['size'] for app in self.selected_apps.values() if app['selected'])
            size_text = f"{estimated_size} MB" if estimated_size < 1000 else f"{estimated_size/1000:.1f} GB"
            
            if selected_count == 1:
                self.selected_count_label.setText(f"1 app selected • ~{size_text} total")
            else:
                self.selected_count_label.setText(f"{selected_count} apps selected • ~{size_text} total")
            
            self.selected_count_label.setStyleSheet("color: #58a6ff; border: none; font-weight: bold;")
            self.install_btn.setText("Start")  # Always just "Start"
            self.install_btn.setEnabled(True)
    
    def select_current_category(self):
        if not self.current_category:
            return
        
        category_app_ids = [app_id for app_id, app in self.selected_apps.items() 
                          if app['category'] == self.current_category]
        
        all_selected = all(self.selected_apps[app_id]['selected'] 
                          for app_id in category_app_ids)
        
        for app_id in category_app_ids:
            self.selected_apps[app_id]['selected'] = not all_selected
            
            if app_id in self.app_checkboxes:
                self.app_checkboxes[app_id].setChecked(not all_selected)
        
        self.select_category_btn.setText("Deselect All" if not all_selected else "Select All")
        self.update_selected_count()
    
    def toggle_select_all(self):
        all_selected = all(app['selected'] for app in self.selected_apps.values())
        
        for app_id, app_data in self.selected_apps.items():
            app_data['selected'] = not all_selected
            
            if app_id in self.app_checkboxes:
                self.app_checkboxes[app_id].setChecked(not all_selected)
        
        self.select_all_btn.setText("Deselect All" if not all_selected else "Select All")
        self.update_selected_count()
    
    def choose_path(self):
        path = QFileDialog.getExistingDirectory(self, "Choose Download Directory")
        if path:
            self.download_path = path
            self.path_display.setText(self.truncate_path(path))
            self.path_display.setToolTip(path)
    
    def start_installation(self):
        if self.downloading:
            return
        
        selected_apps = [(app_id, app_data) for app_id, app_data in self.selected_apps.items() 
                        if app_data['selected']]
        
        if not selected_apps:
            QMessageBox.warning(self, "No Selection", "Please select at least one application to install.")
            return
        
        self.downloading = True
        self.install_btn.setEnabled(False)
        self.install_btn.stop_pulse()  # Stop pulsing during installation
        self.install_btn.setText("Installing...")
        
        self.installer = InstallationThread(selected_apps, self.download_path)
        self.installer.progress_updated.connect(self.update_progress)
        self.installer.finished.connect(self.installation_finished)
        self.installer.start()
    
    def update_progress(self, value, status, current_app="", total_apps=0):
        self.progress_bar.setValue(int(value))
        
        if value > 0:
            self.progress_bar.setFormat(f"{int(value)}%")
        else:
            self.progress_bar.setFormat("")
        
        if current_app and total_apps > 0:
            self.status_label.setText(f"{status}: {current_app}")
        else:
            self.status_label.setText(status)
        
        if "error" in status.lower() or "failed" in status.lower():
            self.status_label.setStyleSheet("color: #f85149; border: none;")
        elif "completed" in status.lower():
            self.status_label.setStyleSheet("color: #3fb950; border: none;")
        else:
            self.status_label.setStyleSheet("color: #f0f6fc; border: none;")
    
    def installation_finished(self):
        self.downloading = False
        self.install_btn.setEnabled(True)
        self.install_btn.setText("Start")
        self.progress_bar.setFormat("")  # Clear percentage display
        self.update_selected_count()

class InstallationThread(QThread):
    progress_updated = Signal(float, str, str, int)
    
    def __init__(self, selected_apps, download_path):
        super().__init__()
        self.selected_apps = selected_apps
        self.download_path = download_path
    
    def run(self):
        try:
            os.makedirs(self.download_path, exist_ok=True)
            total_apps = len(self.selected_apps)
            
            for i, (app_id, app_data) in enumerate(self.selected_apps):
                app_name = app_data['name']
                app_info = app_data['info']
                app_size = app_data.get('size', 50)  # Get app size
                
                base_progress = (i / total_apps) * 100
                
                self.progress_updated.emit(
                    base_progress,
                    f"Downloading ({i+1} of {total_apps})",
                    app_name,
                    total_apps
                )
                
                try:
                    installer_path = self.download_file(app_info['url'], app_info['installer'], 
                                                     base_progress, base_progress + 40, app_name, i+1, total_apps)
                    
                    self.progress_updated.emit(
                        base_progress + 40,
                        f"Installing ({i+1} of {total_apps})",
                        app_name,
                        total_apps
                    )
                    
                    self.install_application(installer_path, app_name)
                    
                    self.progress_updated.emit(
                        ((i + 1) / total_apps) * 100,
                        f"Completed ({i+1} of {total_apps})",
                        app_name,
                        total_apps
                    )
                    
                except Exception as e:
                    self.progress_updated.emit(
                        ((i + 1) / total_apps) * 100,
                        f"Failed ({i+1} of {total_apps})",
                        f"{app_name} - {str(e)}",
                        total_apps
                    )
                    continue
            
            self.progress_updated.emit(100, "All installations completed!", "", 0)
            
        except Exception as e:
            self.progress_updated.emit(0, f"Error: {str(e)}", "", 0)
    
    def download_file(self, url, filename, start_progress, end_progress, app_name, current, total):
        file_path = os.path.join(self.download_path, filename)
        
        response = requests.get(url, stream=True, timeout=30,
                              headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        download_progress = (downloaded / total_size) * (end_progress - start_progress)
                        self.progress_updated.emit(
                            start_progress + download_progress,
                            f"Downloading ({current} of {total})",
                            f"{app_name} - {downloaded // 1024} KB",
                            total
                        )
        
        return file_path
    
    def install_application(self, installer_path, app_name):
        if installer_path.endswith('.msi'):
            subprocess.run(['msiexec', '/i', installer_path, '/quiet', '/norestart'],
                         check=True, timeout=300)
        else:
            subprocess.run([installer_path, '/S'], check=True, timeout=300)
        
        time.sleep(1)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    splash = LoadingScreen()
    splash.show()
    
    window = SpallerMainWindow()
    
    QTimer.singleShot(3000, splash.close)
    QTimer.singleShot(3000, window.show)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
