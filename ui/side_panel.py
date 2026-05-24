"""Collapsible side panel with controls and history."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from functions.examples import example_choices, get_example
from functions.factory import function_choices
from ui.parameter_inputs import ParameterPanel


class SidePanel(QWidget):
    """Left control panel — can collapse."""

    function_type_changed = pyqtSignal(str)
    param_changed = pyqtSignal(str, float)
    plot_clicked = pyqtSignal()
    animate_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    restart_clicked = pyqtSignal()
    add_clicked = pyqtSignal()
    remove_clicked = pyqtSignal()
    export_png_clicked = pyqtSignal()
    export_json_clicked = pyqtSignal()
    import_json_clicked = pyqtSignal()
    history_selected = pyqtSignal(int)
    glow_toggled = pyqtSignal(bool)
    speed_changed = pyqtSignal(float)
    live_update_toggled = pyqtSignal(bool)
    example_load_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._collapsed = False
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 8, 8, 8)
        outer.setSpacing(10)

        header = QHBoxLayout()
        self.title = QLabel("📐 Funciones")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; color: #58a6ff;")
        self.toggle_btn = QPushButton("◀")
        self.toggle_btn.setFixedWidth(36)
        self.toggle_btn.setToolTip("Colapsar panel lateral")
        self.toggle_btn.clicked.connect(self._toggle_collapse)
        header.addWidget(self.title)
        header.addStretch()
        header.addWidget(self.toggle_btn)
        outer.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(12)

        # Function type
        type_group = QGroupBox("Tipo de función")
        type_layout = QVBoxLayout(type_group)
        self.type_combo = QComboBox()
        self.type_combo.setToolTip("Selecciona la familia de función a graficar")
        for type_id, name in function_choices():
            self.type_combo.addItem(name, type_id)
        self.type_combo.currentIndexChanged.connect(self._on_type_changed)
        type_layout.addWidget(self.type_combo)
        layout.addWidget(type_group)

        # Examples
        examples_group = QGroupBox("Ejemplos")
        examples_layout = QVBoxLayout(examples_group)
        self.examples_combo = QComboBox()
        self.examples_combo.setToolTip("Escenarios listos para cargar en el gráfico")
        for ex_id, title in example_choices():
            self.examples_combo.addItem(title, ex_id)
        self.examples_combo.currentIndexChanged.connect(self._on_example_selected)
        self.example_desc = QLabel()
        self.example_desc.setObjectName("infoLabel")
        self.example_desc.setWordWrap(True)
        self.load_example_btn = QPushButton("Cargar ejemplo")
        self.load_example_btn.setObjectName("accentBtn")
        self.load_example_btn.setToolTip(
            "Reemplaza las funciones del gráfico por las del ejemplo seleccionado"
        )
        self.load_example_btn.clicked.connect(self._on_load_example)
        examples_layout.addWidget(self.examples_combo)
        examples_layout.addWidget(self.example_desc)
        examples_layout.addWidget(self.load_example_btn)
        layout.addWidget(examples_group)
        self._on_example_selected()

        # Parameters
        param_group = QGroupBox("Parámetros")
        param_layout = QVBoxLayout(param_group)
        self.param_panel = ParameterPanel(on_change=self._on_param)
        param_layout.addWidget(self.param_panel)
        layout.addWidget(param_group)

        # Actions
        btn_group = QGroupBox("Acciones")
        btn_layout = QVBoxLayout(btn_group)
        self.add_btn = QPushButton("➕ Añadir función")
        self.add_btn.setObjectName("primaryBtn")
        self.add_btn.setToolTip("Añade la función actual al gráfico")
        self.add_btn.clicked.connect(self.add_clicked.emit)

        row1 = QHBoxLayout()
        self.plot_btn = QPushButton("📈 Graficar")
        self.plot_btn.setObjectName("accentBtn")
        self.plot_btn.setToolTip("Dibuja todas las funciones en el gráfico")
        self.plot_btn.clicked.connect(self.plot_clicked.emit)
        self.remove_btn = QPushButton("🗑")
        self.remove_btn.setToolTip("Elimina la función seleccionada del historial")
        self.remove_btn.clicked.connect(self.remove_clicked.emit)
        row1.addWidget(self.plot_btn, stretch=1)
        row1.addWidget(self.remove_btn)

        row2 = QHBoxLayout()
        self.animate_btn = QPushButton("▶ Animar")
        self.animate_btn.setToolTip("Animación progresiva izquierda → derecha")
        self.animate_btn.clicked.connect(self.animate_clicked.emit)
        self.pause_btn = QPushButton("⏸")
        self.pause_btn.setToolTip("Pausar / reanudar animación")
        self.pause_btn.clicked.connect(self.pause_clicked.emit)
        self.stop_btn = QPushButton("⏹")
        self.stop_btn.setObjectName("dangerBtn")
        self.stop_btn.setToolTip("Detener animación")
        self.stop_btn.clicked.connect(self.stop_clicked.emit)
        row2.addWidget(self.animate_btn, stretch=1)
        row2.addWidget(self.pause_btn)
        row2.addWidget(self.stop_btn)

        self.restart_btn = QPushButton("↺ Reiniciar animación")
        self.restart_btn.setToolTip("Reinicia la animación desde el inicio")
        self.restart_btn.clicked.connect(self.restart_clicked.emit)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addLayout(row1)
        btn_layout.addLayout(row2)
        btn_layout.addWidget(self.restart_btn)
        layout.addWidget(btn_group)

        # Animation settings
        anim_group = QGroupBox("Animación")
        anim_layout = QVBoxLayout(anim_group)
        speed_row = QHBoxLayout()
        speed_row.addWidget(QLabel("Velocidad:"))
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 50)
        self.speed_slider.setValue(10)
        self.speed_slider.setToolTip("Controla la velocidad de dibujo")
        self.speed_slider.valueChanged.connect(
            lambda v: self.speed_changed.emit(v / 10.0)
        )
        speed_row.addWidget(self.speed_slider)
        anim_layout.addLayout(speed_row)
        self.live_check = QCheckBox("Actualización en vivo")
        self.live_check.setChecked(True)
        self.live_check.setToolTip(
            "Actualiza la gráfica al cambiar parámetros sin pulsar Graficar"
        )
        self.live_check.toggled.connect(self.live_update_toggled.emit)
        self.glow_check = QCheckBox("Efecto glow")
        self.glow_check.setToolTip("Resplandor suave en las curvas")
        self.glow_check.toggled.connect(self.glow_toggled.emit)
        anim_layout.addWidget(self.live_check)
        anim_layout.addWidget(self.glow_check)
        layout.addWidget(anim_group)

        # Export
        export_group = QGroupBox("Exportar")
        export_layout = QHBoxLayout(export_group)
        png_btn = QPushButton("PNG")
        png_btn.setToolTip("Guardar gráfica como imagen PNG")
        png_btn.clicked.connect(self.export_png_clicked.emit)
        json_out = QPushButton("JSON ↓")
        json_out.setToolTip("Exportar funciones a archivo JSON")
        json_out.clicked.connect(self.export_json_clicked.emit)
        json_in = QPushButton("JSON ↑")
        json_in.setToolTip("Importar funciones desde JSON")
        json_in.clicked.connect(self.import_json_clicked.emit)
        export_layout.addWidget(png_btn)
        export_layout.addWidget(json_out)
        export_layout.addWidget(json_in)
        layout.addWidget(export_group)

        # History
        hist_group = QGroupBox("Historial")
        hist_layout = QVBoxLayout(hist_group)
        self.history_list = QListWidget()
        self.history_list.setToolTip("Funciones activas en el gráfico")
        self.history_list.currentRowChanged.connect(
            lambda i: self.history_selected.emit(i) if i >= 0 else None
        )
        hist_layout.addWidget(self.history_list)
        layout.addWidget(hist_group)

        layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll, stretch=1)

        self._content = scroll
        self._full_width = 320
        self.setFixedWidth(self._full_width)
        self.param_panel.build_for_type(self.type_combo.currentData())

    def current_type_id(self) -> str:
        return self.type_combo.currentData()

    def get_params(self) -> dict[str, float]:
        return self.param_panel.get_params()

    def _on_type_changed(self) -> None:
        type_id = self.type_combo.currentData()
        self.param_panel.build_for_type(type_id)
        self.function_type_changed.emit(type_id)

    def _on_param(self, key: str, value: float) -> None:
        self.param_changed.emit(key, value)

    def _on_example_selected(self, _index: int = -1) -> None:
        ex_id = self.examples_combo.currentData()
        preset = get_example(ex_id) if ex_id else None
        if preset:
            self.example_desc.setText(preset.description)
        else:
            self.example_desc.setText("")

    def _on_load_example(self) -> None:
        ex_id = self.examples_combo.currentData()
        if ex_id:
            self.example_load_clicked.emit(ex_id)

    def _toggle_collapse(self) -> None:
        self._collapsed = not self._collapsed
        if self._collapsed:
            self._content.hide()
            self.title.hide()
            self.setFixedWidth(48)
            self.toggle_btn.setText("▶")
            self.toggle_btn.setToolTip("Expandir panel lateral")
        else:
            self._content.show()
            self.title.show()
            self.setFixedWidth(self._full_width)
            self.toggle_btn.setText("◀")
            self.toggle_btn.setToolTip("Colapsar panel lateral")

    def update_history(self, items: list[str], select: int = -1) -> None:
        self.history_list.blockSignals(True)
        row = select if select >= 0 else self.history_list.currentRow()
        self.history_list.clear()
        self.history_list.addItems(items)
        if items:
            self.history_list.setCurrentRow(min(max(row, 0), len(items) - 1))
        self.history_list.blockSignals(False)

    def set_formula_preview(self, text: str) -> None:
        pass  # handled in main window info panel
