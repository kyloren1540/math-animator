"""Math Animator — versión web (Streamlit)."""

from __future__ import annotations

import io

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.figure import Figure

from functions.base import MathFunction
from functions.examples import (
    create_functions_from_example,
    example_choices,
    get_example,
)
from functions.factory import FUNCTION_REGISTRY, create_function, function_choices
from graph.renderer import GraphRenderer
from utils.math_helpers import format_roots, intersections_text

st.set_page_config(
    page_title="Math Animator",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0f1419; }
    [data-testid="stSidebar"] { background-color: #151b23; }
    h1, h2, h3, p, label, .stMarkdown { color: #e6edf3 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


def _init_state() -> None:
    if "functions" not in st.session_state:
        st.session_state.functions: list[MathFunction] = []


def _render_figure(
    functions: list[MathFunction],
    *,
    glow: bool = False,
    progress: float | None = None,
) -> Figure:
    fig = Figure(figsize=(10, 5.5), dpi=110)
    ax = fig.add_subplot(111)
    renderer = GraphRenderer(fig, ax, glow=glow)
    if progress is None:
        renderer.draw_full(functions)
    else:
        renderer.draw_partial(functions, progress)
    return fig


def _show_info(fn: MathFunction, all_funcs: list[MathFunction]) -> None:
    st.markdown(f"**{fn.formula_text()}**")
    c1, c2 = st.columns(2)
    c1.caption(f"Dominio: {fn.domain_description()}")
    c2.caption(f"Rango: {fn.range_description()}")
    st.caption(f"Raíces: {format_roots(fn.roots())}")
    v = fn.vertex()
    if v:
        st.caption(f"Vértice: ({v[0]:.4g}, {v[1]:.4g})")
    if len(all_funcs) >= 2:
        st.caption(
            intersections_text(all_funcs, -10.0, 10.0).replace("\n", "  \n")
        )


def _sidebar() -> tuple[bool, float | None]:
    st.sidebar.title("📐 Math Animator")
    st.sidebar.caption("Visualizador de funciones — enlace público")

    # Examples
    st.sidebar.subheader("Ejemplos")
    ex_titles = {ex_id: title for ex_id, title in example_choices()}
    ex_id = st.sidebar.selectbox(
        "Escenario",
        options=list(ex_titles.keys()),
        format_func=lambda k: ex_titles[k],
        label_visibility="collapsed",
    )
    preset = get_example(ex_id)
    if preset:
        st.sidebar.caption(preset.description)
    if st.sidebar.button("Cargar ejemplo", use_container_width=True):
        st.session_state.functions = create_functions_from_example(ex_id)
        st.rerun()

    st.sidebar.divider()

    # New function
    st.sidebar.subheader("Nueva función")
    type_map = {tid: name for tid, name in function_choices()}
    type_id = st.sidebar.selectbox(
        "Tipo",
        options=list(type_map.keys()),
        format_func=lambda k: type_map[k],
    )
    cls = FUNCTION_REGISTRY[type_id]
    params: dict[str, float] = {}
    for key, label, default in cls.PARAM_SPECS:
        params[key] = st.sidebar.number_input(label, value=float(default), key=f"p_{type_id}_{key}")

    if st.sidebar.button("➕ Añadir al gráfico", use_container_width=True):
        st.session_state.functions.append(create_function(type_id, params))
        st.rerun()

    if st.session_state.functions and st.sidebar.button(
        "🗑 Vaciar gráfico", use_container_width=True
    ):
        st.session_state.functions = []
        st.rerun()

    st.sidebar.divider()
    glow = st.sidebar.checkbox("Efecto glow", value=False)
    animate = st.sidebar.checkbox("Modo animación", value=False)
    progress: float | None = None
    if animate and st.session_state.functions:
        progress = st.sidebar.slider("Progreso", 0.0, 1.0, 1.0, 0.02)

    return glow, progress


def main() -> None:
    _init_state()
    glow, progress = _sidebar()

    st.title("Math Animator")
    st.caption("Grafica funciones, compara curvas y explora los ejemplos.")

    functions = st.session_state.functions

    if not functions:
        st.info(
            "Elige un **ejemplo** en la barra lateral o **añade una función** para empezar."
        )
        demo = create_functions_from_example("seno_coseno")
        fig = _render_figure(demo, glow=glow)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        return

    col_plot, col_info = st.columns([2.2, 1])

    with col_plot:
        fig = _render_figure(
            functions,
            glow=glow,
            progress=progress if progress is not None and progress < 1.0 else None,
        )
        st.pyplot(fig, use_container_width=True)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", facecolor=fig.get_facecolor(), dpi=150)
        buf.seek(0)
        plt.close(fig)
        st.download_button(
            "Descargar PNG",
            data=buf,
            file_name="math_animator.png",
            mime="image/png",
            use_container_width=True,
        )

    with col_info:
        st.subheader("Funciones activas")
        for i, fn in enumerate(functions):
            with st.expander(f"{i + 1}. {fn.formula_text()}", expanded=(i == len(functions) - 1)):
                _show_info(fn, functions)
                if st.button("Quitar", key=f"rm_{i}"):
                    st.session_state.functions.pop(i)
                    st.rerun()


if __name__ == "__main__":
    main()
