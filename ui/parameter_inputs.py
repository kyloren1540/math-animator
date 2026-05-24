"""Dynamic parameter input widgets."""

from __future__ import annotations

from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QWidget,
)

from functions.base import MathFunction
from functions.factory import FUNCTION_REGISTRY


class ParameterPanel(QWidget):
    """Builds spinboxes from function PARAM_SPECS."""

    def __init__(
        self,
        on_change: Callable[[str, float], None] | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self._on_change = on_change
        self._layout = QFormLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(8)
        self._spinboxes: dict[str, QDoubleSpinBox] = {}
        self._current_type: str | None = None

    def build_for_type(self, type_id: str) -> dict[str, float]:
        self._clear()
        self._current_type = type_id
        cls = FUNCTION_REGISTRY[type_id]
        values: dict[str, float] = {}
        if not cls.PARAM_SPECS:
            lbl = QLabel("Sin parámetros adicionales")
            lbl.setObjectName("infoLabel")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._layout.addRow(lbl)
            return values

        for key, label, default in cls.PARAM_SPECS:
            spin = QDoubleSpinBox()
            spin.setRange(-1000, 1000)
            spin.setDecimals(4)
            spin.setSingleStep(0.1)
            spin.setValue(default)
            spin.setToolTip(f"Parámetro {label}")
            spin.valueChanged.connect(
                lambda v, k=key: self._emit_change(k, v)
            )
            self._spinboxes[key] = spin
            self._layout.addRow(label + ":", spin)
            values[key] = default
        return values

    def load_from_function(self, fn: MathFunction) -> None:
        self.build_for_type(fn.TYPE_ID)
        for key, spin in self._spinboxes.items():
            if key in fn.params:
                spin.blockSignals(True)
                spin.setValue(fn.params[key])
                spin.blockSignals(False)

    def get_params(self) -> dict[str, float]:
        return {k: s.value() for k, s in self._spinboxes.items()}

    def _emit_change(self, key: str, value: float) -> None:
        if self._on_change:
            self._on_change(key, value)

    def _clear(self) -> None:
        while self._layout.count():
            item = self._layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        self._spinboxes.clear()
