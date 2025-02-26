import robosandbox as rsb

# import robosandbox.geometry.Link.CylinderLink as cl
import numpy as np
from robosandbox.geometry.Link.CylinderLink import CylinderLink as cl


def test_CylinderLink():
    cylinder_link = rsb.geometry.Link.CylinderLink(
        length=0.4,
        E=70e6,
        rho=2700,
        Rout=25e-3,
        parameters=[25e-3, 2e-3],
        method="linear",
    )
    print(f"Link Length: {cylinder_link.len} m")
    print(np.round(cylinder_link.I_tensor, 5))
    print(f"Center of mass: {np.round(cylinder_link.get_center_of_mass(), 4)}")
    print(f"I Tensor: {np.round(cylinder_link.I_tensor[0, 0], 4)}")
    print(f"Center of mass: {np.round(cylinder_link.COM[-1], 4)}")
    print(f"Mass: {cylinder_link.mass} kg")


def test_CylinderLink_plot():
    cylinder_link = cl(
        length=0.4,
        E=70e6,
        rho=2700,
        Rout=25e-3,
        parameters=[25e-3, 2e-3],
        method="linear",
    )
    cylinder_link.plot_discretized_points()


def test_get_outer_mesh():
    link = cl(
        length=0.4,
        E=70e6,
        rho=2700,
        Rout=25e-3,
        inner_profile={"params": [20e-3, 5e-3], "method": "linear"},
        resolutions={"axial": 80, "radial": 10, "angular": 360},
    )
    points, faces = link.get_outer_mesh()
    print(f"len of outer points: {len(points)}")
    print(f"len of outer faces: {len(faces)}")


def test_get_inner_mesh():
    link = cl(
        length=0.4,
        E=70e6,
        rho=2700,
        Rout=25e-3,
        inner_profile={"params": [20e-3, 5e-3], "method": "linear"},
        resolutions={"axial": 80, "radial": 10, "angular": 360},
    )
    points, faces = link.get_inner_mesh()
    print(f"len of inner points: {len(points)}")
    print(f"len of inner faces: {len(faces)}")


def test_get_side_mesh():
    link = cl(
        length=0.4,
        E=70e6,
        rho=2700,
        Rout=25e-3,
        inner_profile={"params": [20e-3, 5e-3], "method": "linear"},
        resolutions={"axial": 80, "radial": 10, "angular": 360},
    )
    points, faces = link.get_side_mesh(side="start")
    print(f"len of side points: {len(points)}")
    print(f"len of side faces: {len(faces)}")


def test_stack_meshes():
    from robosandbox.geometry.mesh_utilities import stack_meshes

    link = cl(
        length=0.4,
        E=70e6,
        rho=2700,
        Rout=25e-3,
        inner_profile={"params": [20e-3, 5e-3], "method": "linear"},
        resolutions={"axial": 80, "radial": 30, "angular": 360},
    )
    outer_points, outer_faces = link.get_outer_mesh()
    inner_points, inner_faces = link.get_inner_mesh()
    start_side_points, start_side_faces = link.get_side_mesh(side="start")
    end_side_points, end_side_faces = link.get_side_mesh(side="end")
    # outer_points = np.array(outer_points)
    # inner_points = np.array(inner_points)
    # start_side_points = np.array(start_side_points)
    # end_side_points = np.array(end_side_points)
    # outer_faces = np.array(outer_faces)
    # inner_faces = np.array(inner_faces)
    # start_side_faces = np.array(start_side_faces)
    # end_side_faces = np.array(end_side_faces)

    points, faces = stack_meshes(
        (outer_points, outer_faces),
        (inner_points, inner_faces),
        (start_side_points, start_side_faces),
        (end_side_points, end_side_faces),
    )
    print(f"len of points: {len(points)}")
    print(f"len of faces: {len(faces)}")


def test_mesh_export():
    from robosandbox.geometry.mesh_utilities import stack_meshes
    from stl import mesh

    link = cl(
        length=0.4,
        E=70e6,
        rho=2700,
        Rout=25e-3,
        inner_profile={"params": [20e-3, 5e-3], "method": "linear"},
        resolutions={"axial": 80, "radial": 30, "angular": 360},
    )
    outer_points, outer_faces = link.get_outer_mesh()
    inner_points, inner_faces = link.get_inner_mesh()
    start_side_points, start_side_faces = link.get_side_mesh(side="start")
    end_side_points, end_side_faces = link.get_side_mesh(side="end")
    points, faces = stack_meshes(
        (outer_points, outer_faces),
        (inner_points, inner_faces),
        (start_side_points, start_side_faces),
        (end_side_points, end_side_faces),
    )
    # points, faces = stack_meshes((start_side_points, start_side_faces))

    # Function to convert quads to triangles
    def quads_to_triangles(quads):
        triangles = []
        for quad in quads:
            # Split each quad into two triangles
            triangles.append([quad[0], quad[1], quad[2]])
            triangles.append([quad[2], quad[3], quad[0]])
        return np.array(triangles)

    # Get the triangles from the quads
    triangles = quads_to_triangles(faces)

    # Create the mesh data
    example = mesh.Mesh(np.zeros(triangles.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(triangles):
        # Assign points to vertices directly
        for j in range(3):
            example.vectors[i][j] = points[f[j], :]
    example.save("robosandbox/geometry/test_geometry/output_mesh.stl")

    # for i, f in enumerate(faces):
    #     for j in range(3):
    #         cube.vectors[i][j] = vertices[f[j], :]

    # Write the mesh to file "cube.stl"
    # robosandbox/geometry/test_geometry
    # cube.save("robosandbox/geometry/test_geometry/cube.stl")


def test_cy_plot():
    link = cl(
        length=0.4,
        E=70e6,
        rho=2700,
        Rout=25e-3,
        inner_profile={"params": [20e-3, 5e-3], "method": "linear"},
        resolutions={"axial": 80, "radial": 10, "angular": 360},
    )
    link.plot(outline=True)


if __name__ == "__main__":
    # test_CylinderLink()
    # test_get_outer_mesh()
    # test_get_inner_mesh()
    # test_get_side_mesh()
    # test_stack_meshes()
    # test_mesh_export()
    test_cy_plot()
