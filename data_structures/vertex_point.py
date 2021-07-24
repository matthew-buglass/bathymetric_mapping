class VertexPoint:
    def __init__(self):
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
        self.visited: bool = False
        self.adjacent_vertices: list[VertexPoint] = []
        self.adjacent_edges: list[bool] = []

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

    def add_vertex(self, vert):
        self.adjacent_vertices.append(vert)
        self.adjacent_edges.append(False)

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
        return [(self.adjacent_vertices[x], self.adjacent_edges[x]) for x in range(len(self.adjacent_vertices))]