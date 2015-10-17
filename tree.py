R = 75
C = 300
A = 8
L = 2250
V = 7
B = 53
T = 400

class Node(object):
    def __init__(self, balloons, sky, prev_action):
        self.children = []
        self.balloons = balloons
        self.sky = sky
        self.prev_action = prev_action
        self.heuristic_value = 0

    def apply_action(self):
        start_pos = self.prev_action[0]
        new_pos = self.prev_action[2]
        if 0<=start_pos[0]<R:
            for i in range(-V, V+1):
                for j in range(-V, V+1):
                    if i*i+j*j<=V*V and 0 <= start_pos[0]+i < R:
                        self.sky[start_pos[0]+i][(start_pos[1]+j)%C] -= 1
        if 0<=new_pos[0]<R:
            for i in range(-V, V+1):
                for j in range(-V, V+1):
                    if i*i+j*j<=V*V and 0 <= new_pos[0]+i < R:
                        self.sky[new_pos[0]+i][(new_pos[1]+j)%C] += 1

    def remove_action(self):
        start_pos = self.prev_action[0]
        new_pos = self.prev_action[2]
        if 0<=new_pos[0]<R:
            for i in range(-V, V+1):
                for j in range(-V, V+1):
                    if i*i+j*j<=V*V and 0 <= new_pos[0]+i < R:
                        self.sky[new_pos[0]+i][(new_pos[1]+j)%C] -= 1
        if 0<=start_pos[0]<R:
            for i in range(-V, V+1):
                for j in range(-V, V+1):
                    if i*i+j*j<=V*V and 0 <= start_pos[0]+i < R:
                        self.sky[start_pos[0]+i][(start_pos[1]+j)%C] += 1

def expand_tree(root_node, current_B, depth, expand_function, heuristic):
    root_node.heuristic_value = heuristic(root_node)
    if depth > 0:
        children = expand_function(root_node, current_B)
        root_node.children = children
        for child in root_node.children:
            expand_tree(child, current_B, depth - 1, expand_function, heuristic)
        if root_node.children:
            root_node.heuristic_value += 0*max(root_node.children, key=lambda x: x.heuristic_value).heuristic_value