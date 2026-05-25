"""Qt table widget for function value tables."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem


class ValueTableWidget(QTableWidget):
    """Read-only dark-themed value table."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setMaximumHeight(220)
        self.verticalHeader().setVisible(False)
        self.setStyleSheet(
            """
            QTableWidget {
                background-color: #151b23;
                color: #c9d1d9;
                gridline-color: #2a3140;
                border: 1px solid #2a3140;
                border-radius: 6px;
                font-size: 12px;
            }
            QTableWidget::item { padding: 4px; }
            QTableWidget::item:alternate { background-color: #1a2130; }
            QHeaderView::section {
                background-color: #21262d;
                color: #8b949e;
                padding: 6px;
                border: none;
                border-bottom: 1px solid #2a3140;
                font-weight: 600;
            }
            """
        )

    def populate(self, headers: list[str], rows: list[list[str]]) -> None:
        self.clear()
        if not headers:
            self.setRowCount(0)
            self.setColumnCount(0)
            return

        self.setColumnCount(len(headers))
        self.setRowCount(len(rows))
        self.setHorizontalHeaderLabels(headers)

        for r, row in enumerate(rows):
            for c, cell in enumerate(row):
                item = QTableWidgetItem(cell)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.setItem(r, c, item)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStretchLastSection(True)
