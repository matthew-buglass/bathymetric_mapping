import json


class VertexPoint:
    def __init__(self, x=0.0, y=0.0, z=0.0, visited=False, created=False, adjacent_vertices=None, adjacent_edges=None,
                 adjacent_in_order_indices=None):
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.visited: bool = visited
        self.created: bool = created
        if adjacent_vertices is None:
            self.adjacent_vertices: list[VertexPoint] = []
            self.adjacent_edges: list[bool] = []
            self.adjacent_in_order_indices = []
        else:
            self.adjacent_vertices: list[VertexPoint] = adjacent_vertices
            self.adjacent_edges: list[bool] = adjacent_edges
            self.adjacent_in_order_indices = adjacent_in_order_indices

    def set_x(self, x: float):
        self.x = x

    def set_y(self, y: float):
        self.y = y

    def set_z(self, z: float):
        self.z = z

    def set_coordinates(self, x: float, y: float, z: float):
        self.set_x(x)
        self.set_y(y)
        self.set_z(z)

    def set_visited(self):
        self.visited = True

    def set_created(self):
        self.created = True

    def add_vertex(self, vert, in_order_index):
        self.adjacent_vertices.append(vert)
        self.adjacent_edges.append(False)
        self.adjacent_in_order_indices.append(in_order_index)

    def set_connected(self, vert):
        idx = self.adjacent_vertices.index(vert)
        self.adjacent_edges[idx] = True

    def remove_vertex(self, vert):
        """
        Removes a vert from the collection of adjacent vertices.
        :param vert: The vertex to remove
        :return: 0 if successful, 1 if IndexError, 2 if ValueError
        """
        try:
            index = self.adjacent_vertices.index(vert)
            self.adjacent_vertices.remove(vert)
            self.adjacent_edges.pop(index)
            self.adjacent_in_order_indices.pop(index)
            return 0
        except IndexError:
            return 1
        except ValueError:
            return 2

    def set_connected(self, vert):
        try:
            index = self.adjacent_vertices.index(vert)
            self.adjacent_edges[index] = True
            return 0
        except IndexError:
            return 1
        except ValueError:
            return 2

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def get_z(self) -> float:
        return self.z

    def get_coordinates(self) -> (float, float, float):
        """
        :return: (x, y, z)
        """
        return self.get_x(), self.get_y(), self.get_z()

    def get_adjacent(self):
        return [(self.adjacent_vertices[x], self.adjacent_edges[x], self.adjacent_in_order_indices[x])
                for x in range(len(self.adjacent_vertices))]

    def to_dict(self) -> dict:
        temp_adj_vert = self.adjacent_vertices
        temp_adj_edge = self.adjacent_edges
        temp_adj_ind = self.adjacent_in_order_indices

        self.adjacent_vertices = []
        self.adjacent_edges = []
        self.adjacent_in_order_indices = []

        out = self.__dict__.copy()

        self.adjacent_vertices = temp_adj_vert
        self.adjacent_edges = temp_adj_edge
        self.adjacent_in_order_indices = temp_adj_ind

        return out

    def to_json(self) -> json:
        temp_adj_vert = self.adjacent_vertices
        temp_adj_edge = self.adjacent_edges
        temp_adj_ind = self.adjacent_in_order_indices

        self.adjacent_vertices = []
        self.adjacent_edges = []
        self.adjacent_in_order_indices = []

        json_out = json.dumps(self)

        self.adjacent_vertices = temp_adj_vert
        self.adjacent_edges = temp_adj_edge
        self.adjacent_in_order_indices = temp_adj_ind

        return json_out

    def to_pretty_json(self) -> json:
        self_dict = self.to_dict()

        json_out = json.dumps(self_dict, indent=4)

        return json_out

    @classmethod
    def from_json(cls, j):
        return VertexPoint(**json.loads(j))

