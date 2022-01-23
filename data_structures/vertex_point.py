import json


class VertexPoint:
    def __init__(self, x=0.0, y=0.0, z=0.0, visited=False, created=False, adjacent_vertices=None, adjacent_edges=None,
                 adjacent_in_order_indices=None):
        """
        Create a VertexPoint
        
        :param x: a float of the x co-ordinate
        :param y: a float of the y co-ordinate
        :param z: a float of the z co-ordinate
        :param visited: a boolean of whether the vertex has been visited during a graph traversal
        :param created: a boolean of whether teh vertex has been created and added to a graph
        :param adjacent_verticies: a list of the verticies that are adjacent in a graph
        :param adjacent_edges: a list booleans marking whether the edges to adjacent verticies have been traversed
        :param adjacent_in_order_indices: a list of the indicies of adjacent verticies from an in-order traversal of their graph
        """
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
    
    @classmethod
    def from_json(cls, j):
        """
        Instatiates a vertex from a json object
        """
        return VertexPoint(**json.loads(j))

    def set_x(self, x: float):
        """
        Sets the x co-ordinate of the vertex
        
        :param x: a float of the x co-ordinate
        """
        self.x = x

    def set_y(self, y: float):
        """
        Sets the y co-ordinate of the vertex
        
        :param y: a float of the y co-ordinate
        """
        self.y = y

    def set_z(self, z: float):
        """
        Sets the z co-ordinate of the vertex
        
        :param z: a float of the z co-ordinate
        """
        self.z = z

    def set_coordinates(self, x: float, y: float, z: float):
        """
        Sets the co-ordinates of the vertex
        
        :param x: a float of the x co-ordinate
        :param y: a float of the y co-ordinate
        :param z: a float of the z co-ordinate
        """
        self.set_x(x)
        self.set_y(y)
        self.set_z(z)

    def set_visited(self):
        """
        Marks the vertex as visited when doing a graph traversal
        """
        self.visited = True

    def set_created(self):
        """
        Marks the vertex as visited when doing a graph traversal
        """
        self.created = True

    def add_vertex(self, vert, in_order_index):
        """
        Marks the provided vertex as adjacent
        
        :param vert: the vertex to mark as adjacent
        :param in_order_vertex: the in-order traversal index of hte vertex to mark as adjacent
        """
        self.adjacent_vertices.append(vert)
        self.adjacent_edges.append(False)
        self.adjacent_in_order_indices.append(in_order_index)

#     def set_connected(self, vert):
#         """
#         Marks ednge to the provided vertex as traversed
        
#         :param vert: the vertex to which's edge is to be traversed
#         """
#         idx = self.adjacent_vertices.index(vert)
#         self.adjacent_edges[idx] = True

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
        """
        Marks ednge to the provided vertex as traversed
        
        :param vert: the vertex to which's edge is to be traversed
        
        :return: 0 if successful, 1 if IndexError, 2 if ValueError
        """
        try:
            index = self.adjacent_vertices.index(vert)
            self.adjacent_edges[index] = True
            return 0
        except IndexError:
            return 1
        except ValueError:
            return 2

    def get_x(self) -> float:
        """
        Returns the x co-ordinate of the vertex
        
        :return float: the vertex's x co-ordinate
        """
        return self.x

    def get_y(self) -> float:
        """
        Returns the y co-ordinate of the vertex
        
        :return float: the vertex's y co-ordinate
        """
        return self.y

    def get_z(self) -> float:
        """
        Returns the z co-ordinate of the vertex
        
        :return float: the vertex's z co-ordinate
        """
        return self.z

    def get_coordinates(self) -> (float, float, float):
        """
        Gets a tuple of teh vertex's co-ordinates
        
        :return (float, float, float): (x, y, z) co-ordinates
        """
        return self.get_x(), self.get_y(), self.get_z()

    def get_adjacent(self):
        """
        Returns list of tuples with data pertaining to adjacent verticies
        
        :return [(VertexPoint, bool, int)]: A list of adjacent vertex data (VertexPoint, was_endge_travesed, in_order_index)
        """
        return [(self.adjacent_vertices[x], self.adjacent_edges[x], self.adjacent_in_order_indices[x])
                for x in range(len(self.adjacent_vertices))]

    def to_dict(self) -> dict:
        """
        Creates a dictionary prepresentation of the vertex, without adjecent verticies
        
        :return dict: a dictionary of the vertex without it's adjacent verticies
        """
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
        """
        Creates a json representation of the vertex, without adjecent verticies
        
        :return json: a json object of the vertex without it's adjacent verticies
        """
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
        """
        Creates a pretty-printable json representation of the vertex, without adjecent verticies
        
        :return json: a pretty-printable json object of the vertex without it's adjacent verticies
        """
        self_dict = self.to_dict()

        json_out = json.dumps(self_dict, indent=4)

        return json_out
