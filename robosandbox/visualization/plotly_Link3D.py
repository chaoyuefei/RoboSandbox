from robosandbox.visualization.plotly_Figure3D import Figure3D
from robosandbox.geometry.mesh_utilities import stack_meshes
from stl import mesh
import numpy as np


class Link3D(Figure3D):
    def __init__(self):
        # self.points, self.faces = self.get_outer_mesh()
        super().__init__()

    def add_mesh(self, points, faces, method, fig, outline=False):
        if method == "tri":
            for face in faces:
                fig.add_tri(
                    [
                        points[face[0]],
                        points[face[1]],
                        points[face[2]],
                    ],
                    outline=outline,
                )
        if method == "quad":
            for face in faces:
                fig.add_quad(
                    [
                        points[face[0]],
                        points[face[1]],
                        points[face[2]],
                        points[face[3]],
                    ],
                    outline=outline,
                )
        return fig

    # def plot(self, *args, **kwargs):
    #     super().__init__()
    #     outline = kwargs.get("outline", False)

    #     fig = Figure3D()
    #     # outer profile mesh
    #     outer_points, outer_faces = self.get_outer_mesh()
    #     fig = self.add_mesh(outer_points, outer_faces, fig, outline)
    #     # inner profile mesh
    #     inner_points, inner_faces = self.get_inner_mesh()
    #     fig = self.add_mesh(inner_points, inner_faces, fig, outline)
    #     # two sides mesh
    #     start_points, start_faces = self.get_side_mesh(side="start")
    #     fig = self.add_mesh(start_points, start_faces, fig, outline)
    #     end_points, end_faces = self.get_side_mesh(side="end")
    #     fig = self.add_mesh(end_points, end_faces, fig, outline)
    #     return fig.draw()

    def plot(self, *args, **kwargs):
        super().__init__()
        outline = kwargs.get("outline", False)
        method = kwargs.get("method", "tri")
        save_path = kwargs.get("save_path", None)

        fig = Figure3D()
        # outer profile mesh
        outer_points, outer_faces = self.get_outer_mesh(method=method)
        inner_points, inner_faces = self.get_inner_mesh(method=method)
        start_points, start_faces = self.get_side_mesh(method=method, side="start")
        end_points, end_faces = self.get_side_mesh(method=method, side="end")
        points, faces = stack_meshes(
            (outer_points, outer_faces),
            (inner_points, inner_faces),
            (start_points, start_faces),
            (end_points, end_faces),
        )
        print(f"len of points: {len(points)}")
        print(f"len of faces: {len(faces)}")
        print(points)
        fig = self.add_mesh(points, faces, method, fig, outline)
        if save_path is not None:
            self.get_stl_export(points, faces, save_path)
        return fig.draw()

    def get_stl_export(self, points, faces, save_path):
        link_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                link_mesh.vectors[i][j] = points[f[j], :]
                # print(points[f[j], :])
                # floatarrary = points[f[j], :].astype(float)
                # print(points[f[j], :])
                # print(floatarrary)
                # print("+++++++++++")
                # exit()
        link_mesh.save(save_path)
