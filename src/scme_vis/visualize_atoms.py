import pyvista as pv
from pydantic import BaseModel
from typing import Optional
from ase import Atoms


class HullMeshOptions(BaseModel):
    line_width: float = 3
    show_edges: bool = False
    opacity: float = 0.5
    metallic: bool = True
    specular: float = 0.7
    ambient: float = 0.3
    show_scalar_bar: bool = False
    pickable: bool = False


class AtomSphereOptions(BaseModel):
    show_edges: bool = False
    metallic: bool = True
    smooth_shading: bool = True
    specular: float = 0.7
    ambient: float = 0.3
    show_scalar_bar: bool = False
    radius: float = 0.1


def add_atoms_as_spheres(
    plotter,
    atoms: Atoms,
    options: AtomSphereOptions = AtomSphereOptions(),
    colors: dict[int, str] = dict(),
    name: Optional[str] = None,
):
    # Go over all the points inside pointset
    for i, atom in enumerate(atoms):

        color = colors.get(atom.number, "grey")
        sphere = pv.Sphere(radius=options.radius, center=atom.position)

        if name is None:
            actor_name = "p_" + str(i)
        else:
            actor_name = "p_" + name + str(i)

        # Add the actor
        plotter.add_mesh(
            sphere,
            color=color,
            name=actor_name,
        )
