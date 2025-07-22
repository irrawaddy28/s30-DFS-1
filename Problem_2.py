'''
542 01 Matrix
https://leetcode.com/problems/01-matrix/description/

Given an m x n binary matrix mat, return the distance of the nearest 0 for each cell. The distance between two cells sharing a common edge is 1.


Example 1:
Input: mat = [[0,0,0],[0,1,0],[0,0,0]]
Output: [[0,0,0],[0,1,0],[0,0,0]]

Example 2:
Input: mat = [[0,0,0],[0,1,0],[1,1,1]]
Output: [[0,0,0],[0,1,0],[1,2,1]]

Constraints:
m == mat.length
n == mat[i].length
1 <= m, n <= 104
1 <= m * n <= 104
mat[i][j] is either 0 or 1.
There is at least one 0 in mat.

Solution:
1. DFS traversal
Maintain a distance matrix (init to +inf) and visited matrix (init to False). Mark all 0-cells with distance = 0. Perform a new DFS for each cell containing  1. The DFS recursion on a cell returns the least distance from a 0. That is,
DFS(cell) = min distance(Cell, 0)

In the DFS(SC) recursion, mark the SC (starting cell) as visited. For each neighbor, do a DFS again. Update the distance matrix for the SC using the distances of neighbors. That is,
distance(SC) = 1 + min(dist(nbr1,0), dist(nbr2,0), ...)
Mark SC as unvisited and return distance(SC)
https://youtu.be/2AZvtk6UThs?t=884

Time: O(MN), Space: O(MN)

2. BFS traversal by tracking level
We mutate the matrix to generate a distance matrix.
Step 1: Enqueue all the independent components (0s) first. Mark all dependent components (1s) as -1 to indicate unvisited
Step 2: At level=0, pop the queue. Popped elements should have all cells containing 0s which are at a distance of 0 from 0. Hence, don't update the values of the matrix. Enque the neighbors (level 1 nodes) whose values are - 1.
Step 3: At lvl 1, pop the queue. Popped elements should have all cells containing -1s which are at a dist 1. Set the values of these cells to 1. If the cell value is not -1, then it means it was visited.
Step 4: At lvl 2, pop the queue. Popped elements should have all cells containing -1s which are at a dist 2. Set the values of these cells to 2.
Thus, at each level, the distance of the cells  from the nearest 0 is basically the level of that cell.

Note: In BFS, each cell is visited only once. Hence, mark it as visited when you are enqueing that cell in the queue. Do not wait to mark it as visited when that element is poppped from the queue.
https://youtu.be/2AZvtk6UThs?t=884

Time: O(MN), Space: O(MN)

3. BFS traversal without tracking level (level agnostic)
We mutate the matrix to generate a distance matrix.
Although we don't track level, it is implict that
    at level 0, queue should have all cells containing 0s
    at level 1, queue should have all cells containing -1s at a dist 1
    at level 2, queue should have all cells containing -1s at a dist 2

Step 1: Enqueue all the independent components (0s) first. Mark all dependent components (1s) as -1 to indicate unvisited

Step 2: Pop the queue. Since we don't track the level, the level information is hidden. Since the popped elements are 0s, then they are at a distance 0 from 0. Don't touch these cells.

Now, enque the neighbors. Let nbr of popped 0, if it contains a -1 be X. Then X must be at a distance 1 from 0s. Update the value of the X using this logic:
    If mat[nbr X] == -1: then mat[nbr X] = mat[cell containing 0]+1=0+1=1
    Enque nbr X so that we can find nbrs of X

Step 3: Pop the queue. Since we don't track the level, the level information is hidden. The popped elements must have a value of 1 (from Step 2) and they are at a distance 1 from 0.

Let nbr of X which contains a -1 be Y. Then Y is at a dist 1 from X
and X is at a dist 2 from 0. Thus, Y is at a dist 2 from 0.
Update Y using this logic:
    If mat[Y] == -1: then mat[Y] = mat[X]+1=1+1=2

Step 4: Pop the queue. Since we don't track the level, the level information is hidden. The popped elements must have a value of 2 (from Step 3) and they are at a distance 2 from 0.

Let nbr of Y which contains a -1 be Z. Then Z is at a dist 1 from Y
and Y is at a dist 2 from 0. Thus, Y is at a dist 3 from 0.
Update Y using this logic:
    If mat[Y] == -1: then mat[Y] = mat[X]+1=2+1=3

Continue doing this until the queue is empty

Note: In BFS, each cell is visited only once. Hence, mark it as visited when you are enqueing that cell in the queue. Do not wait to mark it as visited when that element is poppped from the queue.
https://youtu.be/2AZvtk6UThs?t=884

Time: O(MN), Space: O(MN)
'''
from copy import deepcopy as dcp
from collections import deque

def updateMatrix_dfs(mat):
    def dfs(mat, i, j, visited):
    # dfs(i,j) returns the shortest distance from mat[i][j] to 0
        if mat[i][j] == 0:
            return 0

        visited[i][j] = True
        for dir in dirs:
            x_, y_ = i + dir[0], j + dir[1]
            if 0 <= x_ <= M-1 and 0 <= y_ <= N-1 and not visited[x_][y_]:
                d = dfs(mat, x_, y_, visited)
                distance[i][j] = min(distance[i][j], d + 1)
        visited[i][j] = False
        return distance[i][j]

    if not mat:
        return None
    M = len(mat)
    N = len(mat[0])
    distance = [[float('inf')]*N for _ in range(M)]
    visited =  [[False]*N for _ in range(M)]
    dirs = [[-1,0],[1,0],[0,-1],[0,1]] # U, D, L, R

    for i in range(M):
        for j in range(N):
            if mat[i][j] == 0:
                distance[i][j] = 0

    for i in range(M):
        for j in range(N):
            if mat[i][j] == 1:
                distance[i][j] = dfs(mat, i,j, dcp(visited))
    return distance

def updateMatrix_bfs(mat):
    if not mat:
         return None
    M = len(mat)
    N = len(mat[0])
    dirs = [[-1,0],[1,0],[0,-1],[0,1]] # U, D, L, R
    q = deque()

    # We mutate the 0-1 matrix to get a distance matrix
    # Enqueue all the independent components (0s) first
    # Mark all dependent components (1s) as -1 to indicate unvisited
    for i in range(M):
        for j in range(N):
            if mat[i][j] == 0:
                q.append((i,j))
            else:
                mat[i][j] == -1

    # At each level, enque all cells containing -1 (originally 1s). These cells are at a distance level+1 from 0.
    # At lvl 0, queue should have all cells containing 0s
    # At lvl 1, queue should have all cells containing 1s at a dist 1
    # At lvl 2, queue should have all cells containing 1s at a dist 2
    lvl = 0
    while q:
        K = len(q)
        for i in range(K):
            curr = q.popleft()
            for dir in dirs:
                x_, y_ = curr[0] + dir[0], curr[1] + dir[1]
                if 0 <= x_ <= M-1 and 0 <= y_ <= N-1 and mat[x_][y_] == -1:
                    mat[x_][y_] = lvl + 1
                    q.append((x_,y_))
        lvl += 1
    return mat

def updateMatrix_bfs_level_agnostic(mat):
    if not mat:
         return None
    M = len(mat)
    N = len(mat[0])
    dirs = [[-1,0],[1,0],[0,-1],[0,1]] # U, D, L, R
    q = deque()

    # We mutate the 0-1 matrix to get a distance matrix
    # Enqueue all the independent components (0s) first
    # Mark all dependent components (1s) as -1 to indicate unvisited
    for i in range(M):
        for j in range(N):
            if mat[i][j] == 0:
                q.append((i,j))
            else:
                mat[i][j] = -1

    # Although we don't track level, it is implict that
    # at level 0, queue should have all cells containing 0s
    # at level 1, queue should have all cells containing -1s at a dist 1
    # at level 2, queue should have all cells containing -1s at a dist 2
    #
    # Since we don't track the level, the level information is hidden.
    # Update the value of the a child using this logic:
    # if mat[child] == -1 (unvisited): then mat[child] = mat[parent]+1
    while q:
        curr = q.popleft()
        x, y = curr[0], curr[1]
        for dir in dirs:
            x_, y_ = x + dir[0], y + dir[1]
            if 0 <= x_ <= M-1 and 0 <= y_ <= N-1 and mat[x_][y_] == -1:
                mat[x_][y_] = mat[x][y] + 1
                q.append((x_,y_))
    return mat

def run_updateMatrix():
    tests = [([[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,0],[0,0,0]]),
             ([[0,0,0],[0,1,0],[1,1,1]],[[0,0,0],[0,1,0],[1,2,1]]),
             ([ [1,0,1,1,0,0,1,0,0,1],
                [0,1,1,0,1,0,1,0,1,1],
                [0,0,1,0,1,0,0,1,0,0],
                [1,0,1,0,1,1,1,1,1,1],
                [0,1,0,1,1,0,0,0,0,1],
                [0,0,1,0,1,1,1,0,1,0],
                [0,1,0,1,0,1,0,0,1,1],
                [1,0,0,0,1,1,1,1,0,1],
                [1,1,1,1,1,1,1,0,1,0],
                [1,1,1,1,0,1,0,0,1,1]],
              [ [1,0,1,1,0,0,1,0,0,1],
                [0,1,1,0,1,0,1,0,1,1],
                [0,0,1,0,1,0,0,1,0,0],
                [1,0,1,0,1,1,1,1,1,1],
                [0,1,0,1,1,0,0,0,0,1],
                [0,0,1,0,1,1,1,0,1,0],
                [0,1,0,1,0,1,0,0,1,1],
                [1,0,0,0,1,2,1,1,0,1],
                [2,1,1,1,1,2,1,0,1,0],
                [3,2,2,1,0,1,0,0,1,1]]
            ),]
    tests = [([[0,0,0],[0,1,0],[1,1,1]],[[0,0,0],[0,1,0],[1,2,1]])]
    for test in tests:
        mat, ans = test[0], test[1]
        for method in ['dfs', 'bfs', 'bfs_level_agnostic']:
            if method == 'dfs':
                distance = updateMatrix_dfs(dcp(mat))
            elif method == 'bfs':
                distance = updateMatrix_dfs(dcp(mat))
            elif method == 'bfs_level_agnostic':
                distance = updateMatrix_bfs_level_agnostic(dcp(mat))
            print(f"\n0-1 Matrix: {mat}")
            print(f"{method}: Distance from nearest 0 = {distance}")
            print(f"Pass: {ans == distance}")

run_updateMatrix()