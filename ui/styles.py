"""Modern dark theme stylesheets."""

DARK_THEME = """
QMainWindow, QWidget {
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: "Segoe UI", "SF Pro Display", sans-serif;
    font-size: 13px;
}
QGroupBox {
    border: 1px solid #30363d;
    border-radius: 8px;
    margin-top: 12px;
    padding: 12px 8px 8px 8px;
    font-weight: 600;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #58a6ff;
}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 10px;
    color: #c9d1d9;
    selection-background-color: #388bfd;
}
QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus {
    border-color: #58a6ff;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox QAbstractItemView {
    background-color: #161b22;
    border: 1px solid #30363d;
    selection-background-color: #388bfd;
}
QPushButton {
    background-color: #21262d;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 8px 16px;
    color: #c9d1d9;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #30363d;
    border-color: #8b949e;
}
QPushButton:pressed {
    background-color: #161b22;
}
QPushButton#primaryBtn {
    background-color: #238636;
    border-color: #2ea043;
    color: #ffffff;
}
QPushButton#primaryBtn:hover {
    background-color: #2ea043;
}
QPushButton#accentBtn {
    background-color: #1f6feb;
    border-color: #388bfd;
    color: #ffffff;
}
QPushButton#accentBtn:hover {
    background-color: #388bfd;
}
QPushButton#dangerBtn {
    background-color: #da3633;
    border-color: #f85149;
    color: #ffffff;
}
QPushButton#dangerBtn:hover {
    background-color: #f85149;
}
QListWidget {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 4px;
}
QListWidget::item {
    padding: 8px;
    border-radius: 6px;
}
QListWidget::item:selected {
    background-color: #388bfd33;
    border: 1px solid #388bfd;
}
QScrollArea {
    border: none;
    background: transparent;
}
QSlider::groove:horizontal {
    height: 6px;
    background: #21262d;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    width: 16px;
    margin: -5px 0;
    background: #58a6ff;
    border-radius: 8px;
}
QLabel#formulaLabel {
    font-size: 15px;
    color: #79c0ff;
    padding: 8px;
    background: #161b22;
    border-radius: 8px;
    border: 1px solid #30363d;
}
QLabel#infoLabel {
    font-size: 12px;
    color: #8b949e;
}
QCheckBox {
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #30363d;
    background: #161b22;
}
QCheckBox::indicator:checked {
    background: #238636;
    border-color: #2ea043;
}
QToolTip {
    background-color: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
    padding: 6px;
    border-radius: 4px;
}
"""
