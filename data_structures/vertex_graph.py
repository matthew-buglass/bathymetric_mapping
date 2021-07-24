import json
from importlib.machinery import SourceFileLoader

# from data_structures.vertex_point import vp.VertexPoint
vp = SourceFileLoader("vertex_point", "D:\\Bathymetric Mapping\\bathymetric_mapping_scripts\\data_structures\\vertex_point.py").load_module()


class VertexGraph:
    def __init__(self, head=None, right=None, left=None):
        self.head: vp.VertexPoint = head
        self.right: VertexGraph = right
        self.left: VertexGraph = left

        if self.head is not None:
            self.head = vp.VertexPoint.from_json(json.dumps(head))

            if left is not None:
                self.left = VertexGraph.from_json(json.dumps(left))

            if right is not None:
                self.right = VertexGraph.from_json(json.dumps(right))


    @classmethod
    def from_list(cls, l):
        def from_list_helper(vert_list, depth: int) -> VertexGraph:
            if len(vert_list) == 0:     # base case 1, empty list
                return None
            elif len(vert_list) == 1:   # base case 2, list of one element
                g = VertexGraph()
                g.set_head(vert_list[0])
                return g
            else:                       # recursive case
                # sorting the list based on the dimension that we are looking for
                if depth % 3 == 0:
                    vert_list.sort(key=lambda v: v.get_x())
                elif depth % 3 == 1:
                    vert_list.sort(key=lambda v: v.get_y())
                else:
                    vert_list.sort(key=lambda v: v.get_z())

                mid_point = len(vert_list) // 2

                mid_val = vert_list[mid_point]

                left_list = vert_list[:mid_point]
                right_list = vert_list[mid_point+1:]

                g = VertexGraph()

                g.set_head(mid_val)
                g.set_left(from_list_helper(left_list, depth+1))
                g.set_right(from_list_helper(right_list, depth+1))

                return g

        return from_list_helper(l, 0)

    def is_empty(self) -> bool:
        return self.head is None

    def get_head(self) -> vp.VertexPoint:
        return self.head

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def set_head(self, vert: vp.VertexPoint):
        self.head = vert

    def set_left(self, graph):
        self.left = graph

    def set_right(self, graph):
        self.right = graph

    def to_string_coordinates(self, order: int):
        """

        :param order: 0 = in order; 1 = pre order; 2 = post order
        :return:
        """
        output = ""
        if order == 0:
            output += "In order coordinates:\n"
            for c in self.get_in_order_coordinates():
                output += str(c) + " "
        elif order == 1:
            output += "Pre order coordinates:\n"
            for c in self.get_pre_order_coordinates():
                output += str(c) + " "
        else:
            output += "Post order coordinates:\n"
            for c in self.get_post_order_coordinates():
                output += str(c) + " "

        return output.rstrip()

    def get_order_coordinates(self, order: int):
        """

        :param order: 0 = in order; 1 = pre order; 2 = post order
        :return:
        """
        if order == 0:
            return self.get_in_order_coordinates()
        elif order == 1:
            return self.get_pre_order_coordinates()
        else:
            return self.get_post_order_coordinates()

    def get_vertices(self):
        if self.left is None and self.right is None:
            return [self.head]
        elif self.left is None:
            out = [self.head]
            out.extend(self.right.get_vertices())
            return out
        elif self.right is None:
            out = self.left.get_vertices()
            out.extend([self.head])
            return out
        else:
            out = self.left.get_vertices()
            out.extend([self.head])
            out.extend(self.right.get_vertices())
            return out

    def get_in_order_coordinates(self):
        if self.left is None and self.right is None:
            return [self.head.get_coordinates()]
        elif self.left is None:
            out = [self.head.get_coordinates()]
            out.extend(self.right.get_in_order_coordinates())
            return out
        elif self.right is None:
            out = self.left.get_in_order_coordinates()
            out.extend([self.head.get_coordinates()])
            return out
        else:
            out = self.left.get_in_order_coordinates()
            out.extend([self.head.get_coordinates()])
            out.extend(self.right.get_in_order_coordinates())
            return out


    def get_post_order_coordinates(self):
        if self.left is None and self.right is None:
            return [self.head.get_coordinates()]
        elif self.left is None:
            out = self.right.get_post_order_coordinates()
            out.extend([self.head.get_coordinates()])
            return out
        elif self.right is None:
            out = self.left.get_post_order_coordinates()
            out.extend([self.head.get_coordinates()])
            return out
        else:
            out = self.left.get_post_order_coordinates()
            out.extend(self.right.get_post_order_coordinates())
            out.extend([self.head.get_coordinates()])
            return out

    def get_pre_order_coordinates(self):
        if self.left is None and self.right is None:
            return [self.head.get_coordinates()]
        elif self.left is None:
            out = [self.head.get_coordinates()]
            out.extend(self.right.get_pre_order_coordinates())
            return out
        elif self.right is None:
            out = [self.head.get_coordinates()]
            out.extend(self.left.get_pre_order_coordinates())
            return out
        else:
            out = [self.head.get_coordinates()]
            out.extend(self.left.get_pre_order_coordinates())
            out.extend(self.right.get_pre_order_coordinates())
            return out

    def range_search(self, x_range: (float, float)=None,
                     y_range: (float, float)=None,
                     z_range: (float, float)=None):
        """
        Returns a list of vertices that are within the range that was given
        :param x_range: (low, high) inclusive of the x coordinate range for the search
        :param y_range: (low, high) inclusive of the y coordinate range for the search
        :param z_range: (low, high) inclusive of the z coordinate range for the search
        :return: Returns a list of vertices that are within the range that was given
        """
        def range_search_helper(obj: VertexGraph, depth: int, x_range: (float, float)=None,
                                y_range: (float, float)=None,
                                z_range: (float, float)=None):
            if obj is None:  # base case if not an actual object
                return []
            else:  # recursive case
                # checking to see if this vertex is in the range
                valid = True
                if x_range is not None:
                    valid = valid and x_range[0] <= obj.get_head().get_x() <= x_range[1]
                if y_range is not None:
                    valid = valid and y_range[0] <= obj.get_head().get_y() <= y_range[1]
                if z_range is not None:
                    valid = valid and z_range[0] <= obj.get_head().get_z() <= z_range[1]

                # adding the vertex if it's valid
                if valid:
                    output = [obj.get_head()]
                else:
                    output = []

                # getting the value and next range to determine the recursion direction
                if depth % 3 == 0:
                    value = obj.get_head().get_x()
                    next_range = x_range
                elif depth % 3 == 1:
                    value = obj.get_head().get_y()
                    next_range = y_range
                else:
                    value = obj.get_head().get_z()
                    next_range = z_range

                # going down to the appropriate sub tree
                if next_range is None:
                    output.extend(range_search_helper(obj.get_left(), depth + 1, x_range, y_range, z_range))
                    output.extend(range_search_helper(obj.get_right(), depth + 1, x_range, y_range, z_range))
                elif value < next_range[0]:
                    output.extend(range_search_helper(obj.get_right(), depth+1, x_range, y_range, z_range))
                elif value > next_range[1]:
                    output.extend(range_search_helper(obj.get_left(), depth+1, x_range, y_range, z_range))
                else:
                    output.extend(range_search_helper(obj.get_left(), depth+1, x_range, y_range, z_range))
                    output.extend(range_search_helper(obj.get_right(), depth+1, x_range, y_range, z_range))

                return output

        return range_search_helper(self, 0, x_range, y_range, z_range)

    def get_adjacent_within(self, vertex: vp.VertexPoint, x_radius=-1, y_radius=-1, z_radius=-1):
        x_range = None
        y_range = None
        z_range = None

        if x_radius > 0:
            x_range = (vertex.get_x()-1, vertex.get_x()+1)
        if y_radius > 0:
            y_range = (vertex.get_y()-1, vertex.get_y()+1)
        if z_radius > 0:
            z_range = (vertex.get_z()-1, vertex.get_z()+1)

        points = self.range_search(x_range, y_range, z_range)
        points.remove(vertex)

        return points

    def get_xy_euclidean_adjacent(self, vert, distance):
        prox = self.get_adjacent_within(vert, distance, distance)
        duds = []

        for p in prox:
            euclidean_distance = ((vert.get_x() - p.get_x())**2 + (vert.get_y() - p.get_y())**2) ** 0.5

            if euclidean_distance > distance:
                duds.append(p)

        for d in duds:
            prox.remove(d)

        return prox

    def get_blender_vertices(self):
        return self.get_in_order_coordinates()

    def get_blender_edges(self):
        out = []
        verts = self.get_vertices()

        for i in range(len(verts)):
            edges = [(i, x[2]) for x in verts[i].get_adjacent()]

            for edge in edges:
                edge = tuple(sorted(edge))

                if edge not in out:
                    out.append(edge)

        return out

    def get_blender_faces(self):
        return []

    def get_blender_data(self):
        return self.get_blender_vertices(), self.get_blender_edges(), self.get_blender_faces()

    def establish_proximity_xy(self, distance):
        verts = self.get_vertices()

        for v in verts:
            prox = self.get_adjacent_within(v, distance, distance)

            for p in prox:
                p_idx = verts.index(p)
                v.add_vertex(p, p_idx)

    def establish_euclidean_proximity_xy(self, distance):
        verts = self.get_vertices()

        for v in verts:
            prox = self.get_xy_euclidean_adjacent(v, distance)

            for p in prox:
                p_idx = verts.index(p)
                v.add_vertex(p, p_idx)

    def to_dict(self) -> dict:
        if self.left is None and self.right is None:
            old_head = self.get_head()
            self.head = self.get_head().to_dict()
            out = self.__dict__.copy()
            self.head = old_head
            return out
        elif self.right is None:
            old_head = self.get_head()
            old_left = self.get_left()

            left_dict = self.left.to_dict()

            self.head = self.get_head().to_dict()
            self.left = left_dict

            out = self.__dict__.copy()

            self.head = old_head
            self.left = old_left

            return out
        elif self.left is None:
            old_head = self.get_head()
            old_right = self.get_right()

            right_dict = self.right.to_dict()

            self.head = self.get_head().to_dict()
            self.right = right_dict

            out = self.__dict__.copy()

            self.head = old_head
            self.right = old_right

            return out
        else:
            old_head = self.get_head()
            old_left = self.get_left()
            old_right = self.get_right()

            left_dict = self.left.to_dict()
            right_dict = self.right.to_dict()

            self.head = self.get_head().to_dict()
            self.left = left_dict
            self.right = right_dict

            out = self.__dict__.copy()

            self.head = old_head
            self.left = old_left
            self.right = old_right

            return out

    def to_pretty_json(self) -> json:
        self_dict = self.to_dict()

        json_out = json.dumps(self_dict, indent=4)

        return json_out

    @classmethod
    def from_json(cls, j):
        return VertexGraph(**json.loads(j))
