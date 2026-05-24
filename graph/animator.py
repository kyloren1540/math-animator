"""Animation controller using matplotlib FuncAnimation."""

from __future__ import annotations

from typing import Callable

import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from graph.renderer import GraphRenderer


class DrawAnimator:
    """Left-to-right progressive draw animation."""

    def __init__(
        self,
        canvas: FigureCanvasQTAgg,
        renderer: GraphRenderer,
        get_functions: Callable[[], list],
        on_frame: Callable[[float], None] | None = None,
    ):
        self.canvas = canvas
        self.renderer = renderer
        self.get_functions = get_functions
        self.on_frame = on_frame
        self._anim: FuncAnimation | None = None
        self._progress = 0.0
        self.speed = 1.0
        self.paused = False
        self.loop = True
        self._frame_step = 0.02

    @property
    def progress(self) -> float:
        return self._progress

    def is_running(self) -> bool:
        return self._anim is not None

    def start(self) -> None:
        self.stop()
        self._progress = 0.0
        self.paused = False
        self.renderer.clear()
        interval = max(16, int(50 / max(0.1, self.speed)))

        def update(_frame: int):
            if self.paused:
                return ()
            step = self._frame_step * self.speed
            self._progress += step
            if self._progress >= 1.0:
                if self.loop:
                    self._progress = 0.0
                    self.renderer.clear()
                else:
                    self._progress = 1.0
            funcs = self.get_functions()
            if not funcs:
                return ()
            self.renderer.draw_partial(funcs, self._progress)
            if self.on_frame:
                self.on_frame(self._progress)
            self.canvas.draw_idle()
            return ()

        self._anim = FuncAnimation(
            self.renderer.figure,
            update,
            interval=interval,
            blit=False,
            cache_frame_data=False,
        )
        self.canvas.draw_idle()

    def stop(self) -> None:
        if self._anim is not None:
            self._anim.event_source.stop()
            self._anim = None
        self._progress = 0.0

    def pause(self) -> None:
        self.paused = True

    def resume(self) -> None:
        self.paused = False

    def toggle_pause(self) -> bool:
        self.paused = not self.paused
        return self.paused

    def restart(self) -> None:
        was_running = self.is_running()
        self.stop()
        if was_running:
            self.start()
        else:
            self._progress = 0.0

    def set_speed(self, speed: float) -> None:
        self.speed = max(0.1, min(5.0, speed))
        if self.is_running():
            running = True
            self.stop()
            if running:
                self.start()
