import Queue
import heapq
import copy
import part1
import time

#struture to use in building priority queue in mult
#store path, current path cost and priority culculated by using heuristic function
#comparison based on priority
class path:
	def __init__(self, lst, cost, priority):
		self.path = lst
		self.cost = cost
		self.priority = priority

	def __cmp__(self, other):
         return cmp(self.priority, other.priority)

# This function starts the process of solving a maze for multiple dots.
# Params:
#   start - Node that signifies the starting position in the maze
#   goals - Array of nodes that are all goal states
# Returns:
#   The order of the goals accessed by coordinates, and the total number of node it expand
def mult(maze, start, goals):
	goal_edges = []		#priority queue for all edges bewteen goal states and start
	goals.append(start)
	#determines the optimal distance btw any two goal nodes
	#store each pair in priority queue
	for i in range(len(goals)):
		for j in range(len(goals)):
			if(i<j):
				dist = bfs_distance(maze, goals[i], goals[j])
				heapq.heappush(goal_edges, (dist, goals[i], goals[j]))

	front_list = []
	heapq.heappush(front_list, path([start], 0, 0))

	expand_count = 0
	#search loop
	while (len(front_list)!=0):
		curr = heapq.heappop(front_list)
		curr_path = curr.path 	#only include goal node
		curr_cost = curr.cost   #total cost

		#if all goal state have been visited, return path
		if len(curr_path) == len(goals):
			return curr_path, curr_cost, expand_count
		#generate mst for current path
		sum_edge, curr_mst = mst(goal_edges, goals, curr_path)
		for goal in goals:
			if goal not in curr_path:
				#print(curr_path)
				base_dist = find_dist(curr_path[-1], goal, goal_edges)
				curr_priority = curr_cost + base_dist + sum_edge
				ret_path, ret_count = part1.a_star(maze, curr_path[-1], goal)
				next_path = list(curr_path)		
				for node in ret_path:
					if node not in curr_path and node in goals:
						next_path.append(node)
				next_cost = len(ret_path)-1 + curr_cost
				
				expand_count += ret_count		#add expand node count
				#print(next_path)
				heapq.heappush(front_list, path(next_path, next_cost, curr_priority))

#given a pair of node, return optimal distance
def find_dist(node1, node2, edges):
	curr_edge = [edge for edge in edges if (edge[1]==node1 and edge[2]==node2) or (edge[1]==node2 and edge[2]==node1)]

	return (curr_edge[0][0])
#param:
#edges: List of edges in graph(increasing order)
#goals:	List of goals
#ret: List of edges representing mst
def mst(edges, goals, visited):
	mst_edges = []
	goal_set = []
	sum_edge = 0
	for goal in goals:
		goal_set.append([goal])

	for edge in sorted(list(edges)):
		u = edge[1]
		v = edge[2]
		if u not in visited and v not in visited:
			start_idx = find_set(u, goal_set)
			end_idx = find_set(v, goal_set)
			if start_idx != end_idx:
				# u.neighbors.append(v)
				# v.neighbors.append(u)
				union(start_idx, end_idx, goal_set)
				mst_edges.append(edge)
				sum_edge += edge[0]
	return (sum_edge, mst_edges)

#helper function for mst
def find_set(node, goal_set):
	for i in range(len(goal_set)):
		if node in goal_set[i]:
			return i
#helper function for mst
def union(idx1, idx2, goal_set):
	goal_set[idx1] += goal_set[idx2]
	goal_set.remove(goal_set[idx2])


#bfs for culculating the distance bewteen goals
#return length of path
def bfs_distance(maze, start, end):
	q = Queue.Queue()
	q.put([start])
	explored = []
	for i in range(len(maze)):
		explored_row = []
		for j in range(len(maze[0])):
			explored_row.append(False)
		explored.append(explored_row)
	while not q.empty():
		path = q.get()
		(x,y) = path[-1]
		if(explored[x][y]):
			continue
		explored[x][y] = True
		if(x == end[0] and y == end[1]):
			return len(path)-1
		if x-1>=0 and maze[x-1][y]!='%' and not explored[x-1][y]:
			new_path = list(path)
			new_path.append((x-1, y))
			q.put(new_path)
		if x+1<len(maze) and maze[x+1][y]!='%' and not explored[x+1][y]:
			new_path = list(path)
			new_path.append((x+1, y))
			q.put(new_path)
		if y-1>0 and maze[x][y-1]!='%' and not explored[x][y-1]:
			new_path = list(path)
			new_path.append((x,y-1))
			q.put(new_path)
		if y+1<len(maze[0]) and maze[x][y+1]!='%' and not explored[x][y+1]:
			new_path = list(path)
			new_path.append((x,y+1))
			q.put(new_path)

#load maze into double lists
def load_maze(filename):
	ret = []
	with open(filename) as inputfile:
		for line in inputfile:
			line = line.strip()
			row = []
			for i in range(len(line)):
				row.append(line[i])
			ret.append(row)
	return ret

#find start point and goals in maze
def find_goals(maze):
	start = ()
	end = []
	for row in range(len(maze)):
		for col in range(len(maze[row])):
			if(maze[row][col] == 'P'):
				start = (row, col)
			elif(maze[row][col] == '.'):
				end.append((row, col))
	return (start, end)

def write_solution_to_file(filename, solved_maze):
	out_file = open(filename, 'w+')
	for i in range(len(solved_maze)):
		for j in range(len(solved_maze[0])):
			out_file.write(solved_maze[i][j])
		out_file.write('\n')
	out_file.close()

def part_2():
	out_dir = 'output/'
	maze_name = 'tinySearch.txt'
	maze = load_maze(maze_name)
	start, end = find_goals(maze)
	path, cost, count = mult(maze, start, end)
	print 'A* MST solution path:', path
	print 'A* MST heuristic path cost:', cost
	print 'A* MST heuristic expand node:', count

	ret_maze = copy.deepcopy(maze)
	goal_list = ['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m',
	'n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M',
	'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	idx = 0
	for i in range(1, len(path)):
		ret_maze[path[i][0]][path[i][1]] = goal_list[idx]
		idx +=1
	ret_maze[start[0]][start[1]] = 'P'
	write_solution_to_file(out_dir + 'A*_MST_' + maze_name, ret_maze)

def main():
	print('part2:tinySearch')
	start_time = time.time()
	part_2()
	end_time = time.time()
	elapsed_time = end_time - start_time
	print'time elapsed: ', elapsed_time
	
main()