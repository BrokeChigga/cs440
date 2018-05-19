import Queue
import heapq
import copy

#load the maze into double list
#ret:
#double list containing maze
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

#do dfs	search on the maze
#starting from start node to end node
#return path and number of node expand
def dfs(maze, start, end):
	stack = []
	stack.append([start]);
	expand_count = 0

	explored = []
	for i in range(len(maze)):
		explored_row = []
		for j in range(len(maze[0])):
			explored_row.append(False)
		explored.append(explored_row)

	while (len(stack)!=0):
		path = stack.pop();
		(x,y) = path[-1]
		if(explored[x][y]):
			continue
		explored[x][y] = True

		if(x == end[0] and y == end[1]):
			return path, expand_count
		expand_count += 1
		if x-1>=0 and maze[x-1][y]!='%' and not explored[x-1][y]:
			new_path = list(path)
			new_path.append((x-1, y))
			stack.append(new_path)
		if x+1<len(maze) and maze[x+1][y]!='%' and not explored[x+1][y]:
			new_path = list(path)
			new_path.append((x+1, y))
			stack.append(new_path)
		if y-1>0 and maze[x][y-1]!='%' and not explored[x][y-1]:
			new_path = list(path)
			new_path.append((x,y-1))
			stack.append(new_path)
		if y+1<len(maze[0]) and maze[x][y+1]!='%' and not explored[x][y+1]:
			new_path = list(path)
			new_path.append((x,y+1))
			stack.append(new_path)

#do bfs	search on the maze
#starting from start node to end node
#return path and number of node expand
def bfs(maze, start, end):
	q = Queue.Queue()
	q.put([start])
	expand_count = 0

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
			return path, expand_count
		expand_count += 1
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


def manhattan(node1, node2):
	return abs(node1[0]-node2[0]) + abs(node1[1] - node2[1])

#made for greedy_best_first and A* methods
#node comaparison based on its priority
class node:
    #def __init__(self, list, end):
    def __init__(self, list, priority):
        self.list = list
        self.priority = priority
        #self.priority = manhattan(list[-1], end)

    def __cmp__(self, other):
         return cmp(self.priority, other.priority)

#do greedy best first search on the maze
#starting from start node to end node
#return path and number of node expand
def greedy_best_first(maze, start, end):
	front_list = []
	heapq.heappush(front_list, node([start], manhattan([start][-1], end)))
	expand_count = 0

	explored = []
	for i in range(len(maze)):
		explored_row = []
		for j in range(len(maze[0])):
			explored_row.append(False)
		explored.append(explored_row)

	while (len(front_list) !=0):
		path = heapq.heappop(front_list).list
		(x,y) = path[-1]
		if(explored[x][y]):
				continue
		explored[x][y] = True
		if(x == end[0] and y == end[1]):
			return path, expand_count	
		expand_count += 1
		if x-1>=0 and maze[x-1][y]!='%' and not explored[x-1][y]:
			new_path = list(path)
			new_path.append((x-1, y))
			heapq.heappush(front_list, node(new_path, manhattan(new_path[-1], end)))
		if x+1<len(maze) and maze[x+1][y]!='%' and not explored[x+1][y]:
			new_path = list(path)
			new_path.append((x+1, y))
			heapq.heappush(front_list, node(new_path, manhattan(new_path[-1], end)))
		if y-1>0 and maze[x][y-1]!='%' and not explored[x][y-1]:
			new_path = list(path)
			new_path.append((x,y-1))
			heapq.heappush(front_list, node(new_path, manhattan(new_path[-1], end)))
		if y+1<len(maze[0]) and maze[x][y+1]!='%' and not explored[x][y+1]:
			new_path = list(path)
			new_path.append((x,y+1))
			heapq.heappush(front_list, node(new_path, manhattan(new_path[-1], end)))


#do A* search on the maze
#starting from start node to end node
#return path and number of node expand
def a_star(maze, start, end):
	front_list = []
	heapq.heappush(front_list, node([start], manhattan([start][-1], end)))
	expand_count = 0

	explored = []
	for i in range(len(maze)):
		explored_row = []
		for j in range(len(maze[0])):
			explored_row.append(False)
		explored.append(explored_row)

	while (len(front_list) !=0):
		path = heapq.heappop(front_list).list
		(x,y) = path[-1]
		if(explored[x][y]):
				continue
		explored[x][y] = True
		if(x == end[0] and y == end[1]):
			return path, expand_count	
		expand_count += 1
		if x-1>=0 and maze[x-1][y]!='%' and not explored[x-1][y]:
			new_path = list(path)
			new_path.append((x-1, y))
			heapq.heappush(front_list, node(new_path, manhattan(new_path[-1], end)+len(path)))
		if x+1<len(maze) and maze[x+1][y]!='%' and not explored[x+1][y]:
			new_path = list(path)
			new_path.append((x+1, y))
			heapq.heappush(front_list, node(new_path, manhattan(new_path[-1], end)+len(path)))
		if y-1>0 and maze[x][y-1]!='%' and not explored[x][y-1]:
			new_path = list(path)
			new_path.append((x,y-1))
			heapq.heappush(front_list, node(new_path, manhattan(new_path[-1], end)+len(path)))
		if y+1<len(maze[0]) and maze[x][y+1]!='%' and not explored[x][y+1]:
			new_path = list(path)
			new_path.append((x,y+1))
			heapq.heappush(front_list, node(new_path, manhattan(new_path[-1], end)+len(path)))

#find start and end of the maze
def find_ends(maze):
	start = ()
	end = ()
	for row in range(len(maze)):
		for col in range(len(maze[row])):
			if(maze[row][col] == 'P'):
				start = (row, col)
			elif(maze[row][col] == '.'):
				end = (row, col)
	return (start, end)

#write solution to file
#denote path using '.'
def write_solution_to_file(filename, solved_maze):
	out_file = open(filename, 'w+')
	for i in range(len(solved_maze)):
		for j in range(len(solved_maze[0])):
			if(solved_maze[i][j] == 'P'):
				out_file.write('P')
			if(solved_maze[i][j] == '%'):
				out_file.write('%')
			if(solved_maze[i][j] == ' '):
				out_file.write(' ')
			if(solved_maze[i][j] == '.'):
				out_file.write('.')
		out_file.write('\n')
	out_file.close()


def part_1():
	out_dir = 'output/'
	maze_name = 'mediumMaze.txt'
	maze = load_maze(maze_name)
	start, end = find_ends(maze)

	#dfs
	path, expand_count = dfs(maze, start, end)
	print 'DFS path:', path
	print 'DFS path cost:', len(path)-1
	print 'DFS expand node:', expand_count
	print '-------------------------------'

	ret_maze = copy.deepcopy(maze)
	for item in path:
		ret_maze[item[0]][item[1]] = '.'
	ret_maze[start[0]][start[1]] = 'P'
	write_solution_to_file(out_dir + 'DFS_' + maze_name, ret_maze)

	#bfs
	path, expand_count = bfs(maze, start, end)
	print 'BFS path:', path
	print 'BFS path cost:', len(path)-1
	print 'BFS expand node:', expand_count
	print '-------------------------------'

	ret_maze = copy.deepcopy(maze)
	for item in path:
		ret_maze[item[0]][item[1]] = '.'
	ret_maze[start[0]][start[1]] = 'P'
	write_solution_to_file(out_dir + 'BFS_' + maze_name, ret_maze)

	#greedy
	path, expand_count = greedy_best_first(maze, start, end)
	print 'Greedy Best First path:', path
	print 'Greedy Best First path cost:', len(path)-1
	print 'Greedy Best First expand node:', expand_count
	print '-------------------------------'

	ret_maze = copy.deepcopy(maze)
	for item in path:
		ret_maze[item[0]][item[1]] = '.'
	ret_maze[start[0]][start[1]] = 'P'
	write_solution_to_file(out_dir + 'Greedy_' + maze_name, ret_maze)

	#A*
	path, expand_count = a_star(maze, start, end)
	print 'A* path:', path
	print 'A* path cost:', len(path)-1
	print 'A* expand node:', expand_count
	print '-------------------------------'

	ret_maze = copy.deepcopy(maze)
	for item in path:
		ret_maze[item[0]][item[1]] = '.'
	ret_maze[start[0]][start[1]] = 'P'
	write_solution_to_file(out_dir + 'A*_' + maze_name, ret_maze)




def main():
	#print('part1:bigMaze')
	#part_1()
	print('part1')
main()