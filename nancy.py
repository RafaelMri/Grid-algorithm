import matplotlib.pyplot as plt

class Grid(object):

    def __init__(self, arr, n):
        self.nodes = arr
        self.max_key = None
        self.n = n
    
    def add_node(self, node):
        self.nodes.append(node)

    def find_row_neighbor(self, node):
        for n in self.nodes:
            if n.row == node.row and n.col != node.col:
                return n

        return None

    def find_col_neighbor(self, node):
        for n in self.nodes:
            if n.col == node.col and n.row != node.row:
                return n

        return None

    def midgrid(self):
        for cur_key in xrange(self.max_key, -1, -1):
            for node in self.nodes:
                if node.col_key == cur_key:
                    i = node.col
                    if node.out_orientation == "up":
                        to_shift = node


            for node in self.nodes:
                node.row += 1
                if node.col > i:
                    node.col += 1

            to_shift.col += 1

            self.add_node(Node(1, i))
            self.add_node(Node(1, self.n + 2))
            self.add_node(Node(self.n + 2, i + 1))
            self.add_node(Node(self.n + 2, self.n + 2))

            self.n += 2


    def order_up_cols(self):
        key = 0
        
        temp_arr = []
        for node in self.nodes:
            if node.out_orientation == "up":
                temp_arr.append(node)

        temp_arr = sorted(temp_arr, key = lambda x: x.col)

        for node in temp_arr:
            node.col_key = key
            self.find_col_neighbor(node).col_key = key
            key += 1

        self.max_key = key - 1

    def orient(self):
        assert len(self.nodes) > 0
        start = self.nodes[0]
        rn = self.find_row_neighbor(start)
        cn = self.find_col_neighbor(start)

        if rn.col > start.col:
          start.set_out_orientation("right")
        else:
          start.set_out_orientation("left")

        prevnode = start
        curnode = rn
        while True:
            if prevnode.row == curnode.row:
                if prevnode.col > curnode.col:
                    curnode.set_in_orientation("left")
                else:
                    curnode.set_in_orientation("right")

                next = self.find_col_neighbor(curnode)
                if next.row > curnode.row:
                    curnode.set_out_orientation("down")
                else:
                    curnode.set_out_orientation("up")


            elif prevnode.col == curnode.col:
                if prevnode.row > curnode.row:
                    curnode.set_in_orientation("up")
                else:
                    curnode.set_in_orientation("down")

                next = self.find_row_neighbor(curnode)
                if next.col > curnode.col:
                    curnode.set_out_orientation("right")
                else:
                    curnode.set_out_orientation("left")

            if curnode == start:
                break
            
            temp = curnode
            curnode = next
            prevnode = temp
        
        return None


    def graph(self):
        col_pairs = []
        row_pairs = []
        for node in self.nodes:
            col_n = self.find_col_neighbor(node)
            row_n = self.find_row_neighbor(node)

            col_pairs.append(([node.col, col_n.col],[self.n - node.row + 1, self.n - col_n.row + 1]))
            col_pairs.append(([node.col, row_n.col],[self.n - node.row + 1, self.n - row_n.row + 1]))


        for col_pair in col_pairs:
            plt.plot(col_pair[0], col_pair[1])
        for row_pair in row_pairs:
            plt.plot(row_pair[0], row_pair[1])


        plt.xlim ([0, self.n + 1])
        plt.ylim([0, self.n + 1])
        plt.show()


    def __str__(self):
        s = ''
        for node in self.nodes:
            s += str(node) + '\n'

        return s


class Node(object):

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.out_orientation = "None"
        self.in_orientation = "None"
        self.col_key = None
    
    def set_out_orientation(self, out_orientation):
        self.out_orientation = out_orientation
    
    def set_in_orientation(self, in_orientation):
        self.in_orientation = in_orientation

    def __eq__(self, other):
        return (self.row, self.col) == (other.row, other.col)

    def __str__(self):
        return "row: {}, col: {}, in: {}, out: {}, key: {}".format(self.row, self.col,
         self.in_orientation, self.out_orientation, self.col_key)



nodes = []
n = int(raw_input().strip())
grid = Grid([], n / 2)


for _ in xrange(n):
    row, col = [int(val) for val in raw_input().strip().split(' ')]
    grid.add_node(Node(row, col))

grid.graph()
grid.orient()
grid.order_up_cols()
grid.midgrid()
grid.graph()
