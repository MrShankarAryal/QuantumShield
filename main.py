from core.behavior_analysis import BehaviorAnalysis
from core.quantum_defense import QuantumDefense
from core.threat_detection import ThreatDetection
from core.autonomous_defense import AutonomousDefense
from network_monitor.traffic_analyzer import TrafficAnalyzer
from network_monitor.honeypots import Honeypots
import sys
import time
import random
import psutil
import socket
import threading
import sqlite3
import hashlib
import logging
from datetime import datetime
from collections import defaultdict
from typing import Dict, List
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                           QTableWidgetItem, QProgressBar, QTabWidget, 
                           QTextEdit, QSystemTrayIcon, QMenu, QMessageBox,
                           QInputDialog, QFileDialog, QFrame, QGridLayout,
                           QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QIcon, QColor, QFont, QPalette, QPainter
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='quantum_shield.log'
)
logger = logging.getLogger(__name__)

class SystemMonitor(QThread):
    stats_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = True
    
    def run(self):
        while self.running:
            try:
                stats = {
                    'cpu': psutil.cpu_percent(interval=1),
                    'memory': psutil.virtual_memory().percent,
                    'disk': psutil.disk_usage('/').percent,
                    'network_sent': psutil.net_io_counters().bytes_sent,
                    'network_recv': psutil.net_io_counters().bytes_recv,
                }
                self.stats_updated.emit(stats)
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error in SystemMonitor: {str(e)}")
    
    def stop(self):
        self.running = False

class ModernProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextVisible(False)
        self.setFixedHeight(4)
        self.setStyleSheet("""
            QProgressBar {
                background-color: #F0F0F0;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 2px;
            }
        """)

class MetricCard(QFrame):
    def __init__(self, title: str, value: str = "0", parent=None):
        super().__init__(parent)
        self.setObjectName("metricCard")
        self.setStyleSheet("""
            QFrame#metricCard {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666; font-size: 14px;")
        layout.addWidget(title_label)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(self.value_label)
        
        # Progress bar
        self.progress = ModernProgressBar()
        layout.addWidget(self.progress)
        
    def update_value(self, value: str, progress: int = None):
        self.value_label.setText(str(value))
        if progress is not None:
            self.progress.setValue(progress)

class NetworkMonitor(QThread):
    packet_received = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.connections = defaultdict(int)
    
    def run(self):
        while self.running:
            try:
                connections = psutil.net_connections()
                current_connections = defaultdict(int)
                
                for conn in connections:
                    if conn.status == 'ESTABLISHED':
                        remote_ip = conn.raddr.ip if conn.raddr else 'Unknown'
                        current_connections[remote_ip] += 1
                
                # Emit connection data
                self.packet_received.emit({
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'connections': dict(current_connections)
                })
                
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error in NetworkMonitor: {str(e)}")
    
    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QuantumShield Security Suite')
        self.setGeometry(100, 100, 1280, 800)
        
        # Initialize monitoring threads
        self.system_monitor = SystemMonitor()
        self.network_monitor = NetworkMonitor()
        
        self.setup_ui()
        self.setup_monitoring()
        self.setup_database()
        self.setup_system_tray()
        
    def setup_ui(self):
        # Central widget setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = self.create_header()
        main_layout.addLayout(header)
        
        # Tabs
        tabs = self.create_tabs()
        main_layout.addWidget(tabs)
    
    def create_header(self) -> QHBoxLayout:
        header = QHBoxLayout()
        
        logo_label = QLabel("QuantumShield")
        logo_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2196F3;
            padding: 10px;
        """)
        header.addWidget(logo_label)
        
        self.status_label = QLabel("System Protected")
        self.status_label.setStyleSheet("""
            color: #4CAF50;
            font-weight: bold;
            padding: 5px 10px;
            border: 2px solid #4CAF50;
            border-radius: 15px;
        """)
        header.addStretch()
        header.addWidget(self.status_label)
        
        return header
    
    def create_tabs(self) -> QTabWidget:
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #f5f6fa;
            }
            QTabBar::tab {
                background-color: white;
                color: #666;
                padding: 12px 30px;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 4px;
            }
            QTabBar::tab:selected {
                background-color: #2196F3;
                color: white;
            }
        """)
        
        # Add tabs
        tabs.addTab(self.create_dashboard_tab(), "Dashboard")
        tabs.addTab(self.create_network_tab(), "Network Monitor")
        tabs.addTab(self.create_settings_tab(), "Settings")
        
        return tabs
    
    def create_dashboard_tab(self) -> QWidget:
        dashboard = QWidget()
        layout = QVBoxLayout(dashboard)
        layout.setSpacing(20)
        
        # Metrics
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(15)
        
        self.cpu_card = MetricCard("CPU Usage", "0%")
        self.memory_card = MetricCard("Memory Usage", "0%")
        self.network_card = MetricCard("Network Traffic", "0 MB/s")
        self.threats_card = MetricCard("Threats Blocked", "0")
        
        metrics_grid.addWidget(self.cpu_card, 0, 0)
        metrics_grid.addWidget(self.memory_card, 0, 1)
        metrics_grid.addWidget(self.network_card, 0, 2)
        metrics_grid.addWidget(self.threats_card, 0, 3)
        
        layout.addLayout(metrics_grid)
        
        # Network Activity Chart
        self.setup_network_chart(layout)
        
        # Activity Table
        self.setup_activity_table(layout)
        
        return dashboard
    
    def setup_network_chart(self, parent_layout: QVBoxLayout):
        chart_widget = QWidget()
        chart_widget.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        """)
        chart_layout = QVBoxLayout(chart_widget)
        
        self.network_chart = QChart()
        self.network_chart.setTitle("Network Activity")
        self.network_chart.setAnimationOptions(QChart.SeriesAnimations)
        
        self.network_series = QLineSeries()
        self.network_chart.addSeries(self.network_series)
        
        axis_x = QValueAxis()
        axis_x.setRange(0, 60)
        axis_x.setLabelFormat("%d")
        axis_x.setTitleText("Time (seconds)")
        
        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        axis_y.setTitleText("Network Usage (%)")
        
        self.network_chart.addAxis(axis_x, Qt.AlignBottom)
        self.network_chart.addAxis(axis_y, Qt.AlignLeft)
        self.network_series.attachAxis(axis_x)
        self.network_series.attachAxis(axis_y)
        
        chart_view = QChartView(self.network_chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_layout.addWidget(chart_view)
        
        parent_layout.addWidget(chart_widget)
    
    def setup_activity_table(self, parent_layout: QVBoxLayout):
        activity_widget = QWidget()
        activity_widget.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            padding: 15px;
        """)
        activity_layout = QVBoxLayout(activity_widget)
        
        header = QLabel("Recent Activity")
        header.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        activity_layout.addWidget(header)
        
        self.activity_table = QTableWidget()
        self.activity_table.setColumnCount(4)
        self.activity_table.setHorizontalHeaderLabels(['Time', 'Event', 'Source', 'Status'])
        self.activity_table.horizontalHeader().setStretchLastSection(True)
        self.activity_table.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                font-weight: bold;
                color: #666;
            }
        """)
        activity_layout.addWidget(self.activity_table)
        
        parent_layout.addWidget(activity_widget)
    
    def create_network_tab(self) -> QWidget:
        network_tab = QWidget()
        layout = QVBoxLayout(network_tab)
        
        # Network stats widget
        stats_widget = QWidget()
        stats_widget.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            padding: 15px;
        """)
        stats_layout = QGridLayout(stats_widget)
        
        self.network_stats = {
            'Packets In': QLabel('0'),
            'Packets Out': QLabel('0'),
            'Bandwidth Usage': QLabel('0 MB/s'),
            'Active Connections': QLabel('0'),
            'Blocked Attempts': QLabel('0')
        }
        
        for row, (label, value) in enumerate(self.network_stats.items()):
            stats_layout.addWidget(QLabel(label), row, 0)
            stats_layout.addWidget(value, row, 1)
            
        layout.addWidget(stats_widget)
        
        # Traffic table
        self.traffic_table = QTableWidget()
        self.traffic_table.setColumnCount(5)
        self.traffic_table.setHorizontalHeaderLabels([
            'Time', 'Source IP', 'Destination IP', 'Protocol', 'Size'
        ])
        self.traffic_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        layout.addWidget(self.traffic_table)
        
        return network_tab
    
    def create_settings_tab(self) -> QWidget:
        settings_tab = QWidget()
        layout = QVBoxLayout(settings_tab)
        
        categories = [
            ('Security Rules', [
                'Configure Firewall Rules',
                'Set Alert Thresholds',
                'Manage Blacklist'
            ]),
            ('System', [
                'Update Settings',
                'Backup Configuration',
                'Performance Options'
            ]),
            ('Notifications', [
                'Email Alerts',
                'Desktop Notifications',
                'Alert History'
            ])
        ]
        
        for category, settings in categories:
            group = self.create_settings_group(category, settings)
            layout.addWidget(group)
            
        layout.addStretch()
        return settings_tab
    
    def create_settings_group(self, category: str, settings: List[str]) -> QWidget:
        group = QWidget()
        group.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            margin-bottom: 15px;
        """)
        layout = QVBoxLayout(group)
        
        header = QLabel(category)
        header.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #333;
            padding: 10px;
        """)
        layout.addWidget(header)
        
        for setting in settings:
            btn = QPushButton(setting)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 12px;
                    border: none;
                    background-color: transparent
                              color: #666;
                }
                QPushButton:hover {
                    background-color: #f8f9fa;
                    color: #2196F3;
                }
            """)
            btn.clicked.connect(lambda checked, s=setting: self.handle_setting_click(s))
            layout.addWidget(btn)
            
        return group

    def handle_setting_click(self, setting: str):
        """Handle clicks on settings buttons"""
        try:
            dialog = QMessageBox(self)
            dialog.setWindowTitle(setting)
            dialog.setText(f"Configure {setting}")
            dialog.setIcon(QMessageBox.Information)
            dialog.exec_()
        except Exception as e:
            logger.error(f"Error handling setting click: {str(e)}")
            self.show_error_message("Settings Error", f"Could not open {setting} settings")

    def setup_monitoring(self):
        """Initialize and start monitoring threads"""
        try:
            # Set up system monitoring
            self.system_monitor.stats_updated.connect(self.update_system_stats)
            self.system_monitor.start()

            # Set up network monitoring
            self.network_monitor.packet_received.connect(self.update_network_stats)
            self.network_monitor.start()

            # Initialize chart data
            self.network_data_points = []
            
            # Update timer for chart
            self.chart_timer = QTimer(self)
            self.chart_timer.timeout.connect(self.update_network_chart)
            self.chart_timer.start(1000)  # Update every second
        except Exception as e:
            logger.error(f"Error setting up monitoring: {str(e)}")
            self.show_error_message("Monitoring Error", "Failed to initialize system monitoring")

    def setup_database(self):
        """Initialize SQLite database for logging"""
        try:
            self.conn = sqlite3.connect('security_logs.db')
            cursor = self.conn.cursor()
            
            # Create tables if they don't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS security_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    event_type TEXT,
                    source TEXT,
                    details TEXT,
                    severity INTEGER
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS network_traffic (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    source_ip TEXT,
                    destination_ip TEXT,
                    protocol TEXT,
                    size INTEGER,
                    blocked BOOLEAN
                )
            ''')
            
            self.conn.commit()
        except Exception as e:
            logger.error(f"Database initialization error: {str(e)}")
            self.show_error_message("Database Error", "Failed to initialize security database")

    def setup_system_tray(self):
        """Initialize system tray icon and menu"""
        try:
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setToolTip('QuantumShield Security Suite')
            
            # Create tray menu
            tray_menu = QMenu()
            
            show_action = tray_menu.addAction('Show Window')
            show_action.triggered.connect(self.show)
            
            status_action = tray_menu.addAction('System Status')
            status_action.triggered.connect(self.show_status)
            
            tray_menu.addSeparator()
            
            quit_action = tray_menu.addAction('Quit')
            quit_action.triggered.connect(self.close_application)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
        except Exception as e:
            logger.error(f"System tray setup error: {str(e)}")

    def update_system_stats(self, stats: Dict):
        """Update UI with new system statistics"""
        try:
            # Update metric cards
            self.cpu_card.update_value(f"{stats['cpu']:.1f}%", int(stats['cpu']))
            self.memory_card.update_value(f"{stats['memory']:.1f}%", int(stats['memory']))
            
            # Calculate network speed in MB/s
            bytes_per_sec = (stats['network_sent'] + stats['network_recv']) / 1024 / 1024
            self.network_card.update_value(f"{bytes_per_sec:.1f} MB/s")
            
            # Update system status based on health score
            health_score = 100 - ((stats['cpu'] + stats['memory'] + stats['disk']) / 3)
            self.update_system_status(health_score)
            
            # Log system stats
            self.log_system_stats(stats)
        except Exception as e:
            logger.error(f"Error updating system stats: {str(e)}")

    def update_network_stats(self, data: Dict):
        """Update UI with new network statistics"""
        try:
            # Update network statistics labels
            active_connections = len(data['connections'])
            self.network_stats['Active Connections'].setText(str(active_connections))
            
            # Add new network traffic entry
            current_time = data['time']
            for ip, count in data['connections'].items():
                self.add_traffic_entry(current_time, ip)
                
            # Update network data points for chart
            self.network_data_points.append(active_connections)
            if len(self.network_data_points) > 60:  # Keep last 60 seconds
                self.network_data_points.pop(0)
        except Exception as e:
            logger.error(f"Error updating network stats: {str(e)}")

    def update_network_chart(self):
        """Update network activity chart"""
        try:
            self.network_series.clear()
            for i, value in enumerate(self.network_data_points):
                self.network_series.append(i, value)
        except Exception as e:
            logger.error(f"Error updating network chart: {str(e)}")

    def add_traffic_entry(self, time_str: str, ip: str):
        """Add new entry to network traffic table"""
        try:
            row_position = self.traffic_table.rowCount()
            self.traffic_table.insertRow(row_position)
            
            self.traffic_table.setItem(row_position, 0, QTableWidgetItem(time_str))
            self.traffic_table.setItem(row_position, 1, QTableWidgetItem(ip))
            self.traffic_table.setItem(row_position, 2, QTableWidgetItem("Local"))
            self.traffic_table.setItem(row_position, 3, QTableWidgetItem("TCP"))
            self.traffic_table.setItem(row_position, 4, QTableWidgetItem("--"))
            
            # Remove old entries if too many
            while self.traffic_table.rowCount() > 100:
                self.traffic_table.removeRow(0)
        except Exception as e:
            logger.error(f"Error adding traffic entry: {str(e)}")

    def log_system_stats(self, stats: Dict):
        """Log system statistics to database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO security_events 
                (event_type, source, details, severity)
                VALUES (?, ?, ?, ?)
            ''', (
                'SYSTEM_STATS',
                'System Monitor',
                f"CPU: {stats['cpu']}%, Memory: {stats['memory']}%, Disk: {stats['disk']}%",
                1 if max(stats['cpu'], stats['memory'], stats['disk']) > 90 else 0
            ))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error logging system stats: {str(e)}")

    def update_system_status(self, health_score: float):
        """Update system status indicator based on health score"""
        if health_score > 80:
            status_text = "System Protected"
            status_color = "#4CAF50"  # Green
        elif health_score > 60:
            status_text = "System Warning"
            status_color = "#FFC107"  # Yellow
        else:
            status_text = "System At Risk"
            status_color = "#F44336"  # Red
            
        self.status_label.setText(status_text)
        self.status_label.setStyleSheet(f"""
            color: {status_color};
            font-weight: bold;
            padding: 5px 10px;
            border: 2px solid {status_color};
            border-radius: 15px;
        """)

    def show_status(self):
        """Show system status dialog"""
        status_dialog = QMessageBox(self)
        status_dialog.setWindowTitle("System Status")
        status_dialog.setText(self.status_label.text())
        status_dialog.setIcon(QMessageBox.Information)
        status_dialog.exec_()

    def show_error_message(self, title: str, message: str):
        """Show error message dialog"""
        error_dialog = QMessageBox(self)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.exec_()

    def closeEvent(self, event):
        """Handle application close event"""
        self.close_application()
        event.accept()

    def close_application(self):
        """Clean up and close application"""
        try:
            # Stop monitoring threads
            self.system_monitor.stop()
            self.network_monitor.stop()
            
            # Close database connection
            if hasattr(self, 'conn'):
                self.conn.close()
            
            # Remove tray icon
            if hasattr(self, 'tray_icon'):
                self.tray_icon.hide()
            
            QApplication.quit()
        except Exception as e:
            logger.error(f"Error closing application: {str(e)}")

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        # Set application font
        font = QFont("Segoe UI", 9)
        app.setFont(font)
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec_())
    except Exception as e:
        logger.critical(f"Application failed to start: {str(e)}")
