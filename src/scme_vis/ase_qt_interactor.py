from pyvistaqt import QtInteractor
import warnings

import numpy as np  # type: ignore
import pyvista
import ase

try:
    from pyvista.core.utilities import conditional_decorator, threaded
except ImportError:  # PV < 0.40
    from pyvista.utilities import conditional_decorator, threaded
from qtpy import QtCore, QtGui
from qtpy.QtCore import QSize, QTimer, Signal

from ase import Atoms
from ase.io import read

import visualize_atoms

from pyvistaqt.window import MainWindow
from typing import Union, Any


class ASEQtInteractor(QtInteractor):
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        parent: MainWindow = None,
        title: str = None,
        off_screen: bool = None,
        multi_samples: int = None,
        line_smoothing: bool = False,
        point_smoothing: bool = False,
        polygon_smoothing: bool = False,
        auto_update: Union[float, bool] = 5.0,
        **kwargs: Any,
    ) -> None:

        super().__init__(
            parent,
            title,
            off_screen,
            multi_samples,
            line_smoothing,
            point_smoothing,
            polygon_smoothing,
            auto_update,
        )

        self.atoms = None

    # pylint: disable=invalid-name,useless-return
    def dropEvent(self, event: QtCore.QEvent) -> None:
        """Event is called after dragEnterEvent."""
        try:
            for url in event.mimeData().urls():
                self.url = url
                filename = self.url.path()
                self.atoms = read(filename)
                print(self.atoms)

                colors = {1: "lightgrey", 8: "red"}
                radii = {1: 0.1, 8: 0.15}

                visualize_atoms.add_atoms_as_spheres(
                    self, self.atoms, radii=radii, colors=colors
                )

        except IOError as exception:  # pragma: no cover
            warnings.warn(f"Exception when dropping files: {str(exception)}")
