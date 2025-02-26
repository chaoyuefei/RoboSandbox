from robosandbox.visualization.plotly_Figure3D import Figure3D
from robosandbox.geometry.mesh_utilities import stack_meshes


class Link3D(Figure3D):
    def __init__(self):
        # self.points, self.faces = self.get_outer_mesh()
        super().__init__()

    def add_mesh(self, points, faces, fig, outline=False):
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

        fig = Figure3D()
        # outer profile mesh
        outer_points, outer_faces = self.get_outer_mesh()
        inner_points, inner_faces = self.get_inner_mesh()
        start_points, start_faces = self.get_side_mesh(side="start")
        end_points, end_faces = self.get_side_mesh(side="end")
        points, faces = stack_meshes(
            (outer_points, outer_faces),
            (inner_points, inner_faces),
            (start_points, start_faces),
            (end_points, end_faces),
        )
        fig = self.add_mesh(points, faces, fig, outline)

        return fig.draw()
