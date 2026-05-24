# Math Animator

Visualizador educativo de funciones matemáticas. Permite graficar varias curvas a la vez, ajustar parámetros en tiempo real, animar el dibujo, cargar ejemplos predefinidos y consultar propiedades como dominio, rango, raíces e intersecciones.

**Repositorio:** [github.com/kyloren1540/math-animator](https://github.com/kyloren1540/math-animator)

---

## ¿Qué hace el programa?

| Función | Descripción |
|---------|-------------|
| **Graficar funciones** | Dibuja una o varias curvas en un plano cartesiano con estilo oscuro y rejilla limpia. |
| **Parámetros ajustables** | Cambia coeficientes (pendiente, amplitud, etc.) y ve el efecto al instante. |
| **Vista previa** | Antes de añadir una función al gráfico, puedes previsualizarla (escritorio con “actualización en vivo”). |
| **Varias funciones** | Añade, elimina y selecciona funciones desde un historial. |
| **Ejemplos listos** | Carga escenarios educativos (parábola, seno/coseno, exponencial/log, etc.) con un clic. |
| **Análisis automático** | Muestra dominio, rango aproximado, raíces, vértice (si aplica) e intersecciones entre curvas. |
| **Animación** | Dibuja las curvas de izquierda a derecha, con velocidad, pausa y reinicio. |
| **Efecto glow** | Resplandor suave opcional en las líneas. |
| **Exportar** | Guarda la gráfica en PNG o las funciones en JSON (escritorio). |
| **Importar** | Recupera un conjunto de funciones desde un archivo JSON (escritorio). |
| **Versión web** | Misma lógica matemática en el navegador, sin instalar nada (Streamlit). |

---

## Tipos de funciones soportadas

| Tipo | Forma general | Parámetros principales |
|------|---------------|------------------------|
| Lineal | `mx + b` | Pendiente `m`, ordenada `b` |
| Cuadrática | `ax² + bx + c` | Coeficientes `a`, `b`, `c` |
| Cúbica | `ax³ + bx² + cx + d` | Coeficientes `a`, `b`, `c`, `d` |
| Exponencial | `aˣ` | Base `a` |
| Logarítmica | `ln(x)` | — |
| Seno | `A·sin(ωx)` | Amplitud `A`, frecuencia `ω` |
| Coseno | `A·cos(ωx)` | Amplitud `A`, frecuencia `ω` |
| Tangente | `A·tan(ωx)` | Amplitud `A`, frecuencia `ω` |
| Racional | `(p₀ + p₁x) / (q₀ + q₁x)` | Coeficientes del numerador y denominador |
| Valor absoluto | `\|x\|` | — |
| Constante | `c` | Valor `c` |

---

## Cómo está construido el programa

El proyecto tiene **dos interfaces** que comparten la misma lógica matemática:

```
math_animator/
├── main.py                 # Entrada de la app de escritorio (PyQt6)
├── streamlit_app.py        # Entrada de la app web (Streamlit)
├── functions/              # Definición de cada tipo de función
│   ├── base.py             # Clase abstracta MathFunction + metadatos
│   ├── factory.py          # Registro y creación de funciones
│   ├── examples.py         # Escenarios predefinidos
│   ├── linear.py, quadratic.py, ...
├── graph/                  # Motor de gráficas
│   ├── renderer.py         # Dibuja curvas con Matplotlib (estilo, leyenda, puntos)
│   ├── animator.py         # Animación progresiva (solo escritorio)
│   └── canvas.py           # Canvas Qt embebido (solo escritorio)
├── ui/                     # Interfaz de escritorio
│   ├── main_window.py      # Ventana principal
│   ├── side_panel.py       # Panel lateral de controles
│   ├── parameter_inputs.py # Spinboxes dinámicos por tipo
│   └── styles.py           # Tema oscuro Qt
└── utils/                  # Exportación, JSON, cálculos auxiliares
    ├── math_helpers.py     # Intersecciones, formato de raíces
    ├── json_io.py          # Importar/exportar funciones
    └── export.py           # Exportar PNG
```

### Flujo de datos (resumen)

1. El usuario elige un **tipo de función** y ajusta **parámetros** en el panel (o carga un **ejemplo**).
2. `factory.create_function()` instancia la clase correspondiente (`LinearFunction`, `QuadraticFunction`, etc.).
3. `GraphRenderer` evalúa `y = f(x)` en un rango (por defecto x ∈ [−10, 10]) y dibuja con Matplotlib.
4. Cada función implementa métodos de análisis: `domain_description()`, `roots()`, `vertex()`, etc.
5. Con dos o más funciones activas, se calculan **intersecciones** numéricamente en `math_helpers`.

### Tecnologías

| Componente | Tecnología |
|------------|------------|
| Escritorio | Python 3, **PyQt6**, Matplotlib |
| Web | **Streamlit**, Matplotlib (backend Agg, sin Qt) |
| Cálculo simbólico | **SymPy** (raíces exactas en algunos tipos) |
| Arrays | **NumPy** |

La versión web **no importa PyQt** al arrancar: el paquete `graph` carga el renderizador sin depender de Qt.

---

## Instalación

### Versión web (navegador)

```bash
git clone https://github.com/kyloren1540/math-animator.git
cd math-animator
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate   # Linux / macOS
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Abre `http://localhost:8501`.

### Versión de escritorio

```bash
pip install -r requirements-desktop.txt
python main.py
```

---

## Guía de uso — App de escritorio (PyQt)

### 1. Iniciar el programa

Ejecuta `python main.py`. Verás:

- **Panel izquierdo:** controles y historial.
- **Panel derecho:** fórmula en LaTeX, datos de la función, barra de herramientas del gráfico, área de dibujo y barra de progreso de animación.

### 2. Cargar un ejemplo rápido

1. En **Ejemplos**, elige un escenario en el desplegable (p. ej. *Seno y coseno*).
2. Lee la descripción debajo del selector.
3. Pulsa **Cargar ejemplo**.
4. Las funciones del ejemplo aparecen en el gráfico y en **Historial**.

### 3. Crear tu propia función

1. En **Tipo de función**, selecciona la familia (Lineal, Cuadrática, etc.).
2. En **Parámetros**, ajusta los valores con los controles numéricos.
3. Si **Actualización en vivo** está activada, el gráfico se actualiza al mover parámetros (vista previa del borrador).
4. Pulsa **➕ Añadir función** para fijarla en el historial y en el gráfico definitivo.

### 4. Graficar y gestionar el historial

- **📈 Graficar:** redibuja todas las funciones del historial.
- **Historial:** lista las funciones activas. Haz clic en una fila para editar sus parámetros en el panel.
- **🗑:** elimina la función seleccionada en el historial.

### 5. Información de la función

En el panel derecho se muestra:

- Fórmula en notación LaTeX.
- **Dominio** y **rango** (aproximado en la ventana visible).
- **Raíces** reales detectadas.
- **Vértice** (parábolas y similares).
- **Intersecciones** entre pares de funciones (si hay al menos dos en el gráfico).

### 6. Animación

1. Añade al menos una función al historial.
2. Pulsa **▶ Animar** para dibujar las curvas de izquierda a derecha.
3. **⏸** pausa o reanuda.
4. **⏹** detiene y restaura el gráfico completo.
5. **↺ Reiniciar animación** vuelve al inicio.
6. Ajusta **Velocidad** con el deslizador.
7. Activa **Efecto glow** para un resplandor suave en las líneas.

### 7. Herramientas del gráfico (barra superior)

Usa los iconos de Matplotlib para:

- Desplazar (**pan**) y hacer **zoom**.
- Restablecer la vista (**home**).
- Guardar imagen desde la barra (además del exportador propio).

### 8. Exportar e importar

| Botón | Acción |
|-------|--------|
| **PNG** | Guarda la gráfica actual como imagen. |
| **JSON ↓** | Exporta todas las funciones del historial a un archivo. |
| **JSON ↑** | Importa funciones desde un JSON guardado antes. |

### 9. Colapsar el panel

Pulsa **◀** en la cabecera del panel izquierdo para ocultar controles y ganar espacio en el gráfico. **▶** lo vuelve a mostrar.

---

## Guía de uso — Versión web (Streamlit)

### 1. Abrir la app

Usa el enlace de Streamlit Cloud de tu despliegue, o ejecuta `streamlit run streamlit_app.py` en local.

### 2. Barra lateral

| Control | Uso |
|---------|-----|
| **Ejemplos → Escenario** | Elige un preset y pulsa **Cargar ejemplo**. |
| **Nueva función → Tipo** | Selecciona el tipo de función. |
| **Parámetros** | Ajusta coeficientes con los campos numéricos. |
| **➕ Añadir al gráfico** | Añade la función configurada. |
| **🗑 Vaciar gráfico** | Quita todas las funciones. |
| **Efecto glow** | Activa o desactiva el resplandor. |
| **Modo animación** | Muestra un deslizador de progreso (0–100 %) para simular el dibujo progresivo. |

### 3. Área principal

- **Gráfico central:** todas las funciones activas.
- **Descargar PNG:** guarda la imagen actual.
- **Funciones activas:** paneles expandibles con dominio, rango, raíces, vértice e intersecciones; botón **Quitar** por función.

Si no hay funciones cargadas, se muestra una vista de demostración (seno y coseno) como referencia.

---

## Ejemplos predefinidos

| Nombre | Contenido |
|--------|-----------|
| Parábola clásica | `y = x² − 4` |
| Seno y coseno | `sin(x)` y `cos(x)` |
| Recta y parábola | Recta + parábola (intersecciones) |
| Exponencial y logaritmo | `2ˣ` y `ln(x)` |
| Valor absoluto | `\|x\|` |
| Ondas de distinta frecuencia | `sin(2x)` y `sin(x)` |
| Función racional | Asíntota vertical |
| Cúbica con inflexión | `0.25x³ − 1.5x` |
| Tangente | `tan(x)` |
| Constante y seno | Recta horizontal + onda |

---

## Publicar en internet (Streamlit Cloud)

1. Sube el código a GitHub (`kyloren1540/math-animator`).
2. Entra en [share.streamlit.io](https://share.streamlit.io) con tu cuenta de GitHub.
3. **New app** → repositorio `kyloren1540/math-animator`.
4. **Main file path:** `streamlit_app.py`.
5. **Deploy**.

Tras el despliegue, comparte la URL pública (por ejemplo `https://math-animator-xxxx.streamlit.app`).

Script auxiliar de despliegue a GitHub:

```powershell
.\deploy.ps1
```

---

## Requisitos

- Python 3.10 o superior recomendado.
- **Web:** `matplotlib`, `numpy`, `sympy`, `streamlit` (`requirements.txt`).
- **Escritorio:** lo anterior + `PyQt6` (`requirements-desktop.txt`).

---

## Licencia

Proyecto de uso educativo libre.
