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
1. DFS
All 1s are initially marked as -1 to flag them as unprocessed cells.
We start a separate DFS from every 0, assigning increasing distance values to reachable cells. The DFS only updates a cell if it's unvisited or if the new path offers a smaller distance.
Time: O(M^2 N^2), Space: O(MN)
https://youtu.be/3e3VoSOjQNo?t=2241

2. DFS with Memoization (more optimal in TC than the regular dfs)
For each cell with a 1, we use DFS to search its neighbors until we find the nearest 0.
If a neighbor has already been processed (distance not 0), we reuse it to save work.
Then we return 1 + the minimum distance from all four directions to update the result.
(JS solution)
Time: O(MN), Space: O(MN)
https://youtu.be/3e3VoSOjQNo?t=3211


3. BFS traversal by tracking level
We mutate the matrix to generate a distance matrix.
Step 1: Enqueue all the independent components (0s) first. Mark all dependent components (1s) as -1 to indicate unvisited
Step 2: At level=0, pop the queue. Popped elements should have all cells containing 0s which are at a distance of 0 from 0. Hence, don't update the values of the matrix. Enque the neighbors (level 1 nodes) whose values are - 1.
Step 3: At lvl 1, pop the queue. Popped elements should have all cells containing -1s which are at a dist 1. Set the values of these cells to 1. If the cell value is not -1, then it means it was visited.
Step 4: At lvl 2, pop the queue. Popped elements should have all cells containing -1s which are at a dist 2. Set the values of these cells to 2.
Thus, at each level, the distance of the cells  from the nearest 0 is basically the level of that cell.

Note: In BFS, each cell is visited only once. Hence, mark it as visited when you are enqueing that cell in the queue. Do not wait to mark it as visited when that element is poppped from the queue.
Time: O(MN), Space: O(MN)
https://youtu.be/2AZvtk6UThs?t=884


4. BFS traversal without tracking level (level agnostic)
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
Time: O(MN), Space: O(MN)
https://youtu.be/2AZvtk6UThs?t=884
'''
from copy import deepcopy as dcp
from collections import deque

def updateMatrix_dfs(mat):
    def dfs(mat, i, j, dist):
        # print(f"dfs({i}, {j}, {dist})")
        # base case
        if i < 0 or i == M or j < 0 or j == N:
            return

        for dir in dirs:
            x, y = i + dir[0], j + dir[1]
            if 0 <= x <= M-1 and 0 <= y <= N-1:
                if mat[x][y] == -1:
                    #print(f"mat[{x}][{y}] = {mat[x][y]}")
                    mat[x][y] = dist
                    dfs(mat, x, y, dist + 1)
                elif mat[x][y] > dist:
                    #print(f"mat[{x}][{y}] = {mat[x][y]}")
                    mat[x][y] = dist
                    dfs(mat, x, y, dist + 1)
                elif mat[x][y] == 0:
                    continue

                # Compress above if-elif-elif into a single if
                # if mat[x][y] > dist or mat[x][y] == -1:
                #     mat[x][y] = dist
                #     dfs(mat, x, y, dist + 1)

    if not mat:
        return None
    M, N = len(mat), len(mat[0])

    for i in range(M):
        for j in range(N):
            if mat[i][j] == 1:
                mat[i][j] = -1 # unvisited

    dirs = [[-1,0],[1,0],[0,-1],[0,1]] # U, D, L, R
    for i in range(M): # O(NM)
       for j in range(N): # O(N)
           if mat[i][j] == 0:
               dfs(mat, i, j, 1) # O(NM)
    return mat


def updateMatrix_dfs_memoization(mat):
    def dfs(mat, i, j):
            # base case: if we find a 0 in the neighbor
            # we set the nearest distance to a 0-cell as 1
            if i > 0 and mat[i-1][j] == 0:
                return 1
            if i < m-1 and mat[i+1][j] == 0:
                return 1
            if j > 0 and mat[i][j-1] == 0:
                return 1
            if j < n-1 and mat[i][j+1] == 0:
                return 1

            top = 9999
            left = 9999
            bottom = 9999
            right = 9999

            # (i-1,j) top cell: if top doesn't have valid distance, skip
            # if it has valid distance, use DP matrix
            if i > 0 and result[i-1][j] != -1:
                top = result[i-1][j]

            # (i,j-1) left cell: if left doesn't have valid distance, skip
            # if it has valid distance, use DP matrix
            if j > 0 and result[i][j-1] != -1:
                left = result[i][j-1]

            # (i,j+1) right cell: if right doesn't have valid distance, call dfs
            # if it has valid distance, use DP matrix
            if j < n-1:
                if result[i][j+1] == -1:
                    result[i][j+1] = dfs(mat, i, j+1)
                right = result[i][j+1]

            # (i,j+1) bottom cell: if bottom doesn't have valid dist, call dfs
            # if it has valid distance, use DP matrix
            if i < m-1:
                if result[i+1][j] == -1:
                    result[i+1][j] = dfs(mat, i+1, j)
                bottom = result[i+1][j]

            return 1 + min(top, left, bottom, right)

    if not mat:
        return None
    m = len(mat)
    n = len(mat[0])
    result = [[-1]*n for _ in range(m)] # DP matrix

    for i in range(m):
        for j in range(n):
            if mat[i][j] == 1:
                result[i][j] = dfs(mat, i, j)
    return result


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
                mat[i][j] = -1

    # At each level, enque all cells containing -1 (originally 1s). These cells are at a distance level+1 from 0.
    # At lvl 0, queue should have all cells containing 0s
    # At lvl 1, queue should have all cells containing 1s at a dist 1
    # At lvl 2, queue should have all cells containing 1s at a dist 2
    lvl = 1
    while q:
        K = len(q)
        for _ in range(K):
            x, y = q.popleft()
            for dir in dirs:
                x_, y_ = x + dir[0], y + dir[1]
                if 0 <= x_ <= M-1 and 0 <= y_ <= N-1 and mat[x_][y_] == -1:
                    mat[x_][y_] = lvl
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

#O1 Matrix Bottom Up DP Solution

def updateMatrix_dp(mat):
    m, n = len(mat), len(mat[0])
    INF = m + n  # larger than any possible distance
    dist = [[0 if mat[i][j] == 0 else INF for j in range(n)] for i in range(m)]

    # Pass 1: top-left -> bottom-right
    for i in range(m):
        for j in range(n):
            if dist[i][j] != 0:
                if i > 0:
                    dist[i][j] = min(dist[i][j], dist[i-1][j] + 1)
                if j > 0:
                    dist[i][j] = min(dist[i][j], dist[i][j-1] + 1)

    # Pass 2: bottom-right -> top-left
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if dist[i][j] != 0:
                if i < m - 1:
                    dist[i][j] = min(dist[i][j], dist[i+1][j] + 1)
                if j < n - 1:
                    dist[i][j] = min(dist[i][j], dist[i][j+1] + 1)
    return dist

def run_tests():
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
            ),
    ]
    for test in tests:
        mat, ans = test[0], test[1]
        for method in ['bfs', 'bfs_level_agnostic', 'dfs', 'dfs_memoization', 'dp']:
            if method == 'dfs':
                distance = updateMatrix_dfs(dcp(mat))
            elif method == 'bfs':
                distance = updateMatrix_bfs(dcp(mat))
            elif method == 'bfs_level_agnostic':
                distance = updateMatrix_bfs_level_agnostic(dcp(mat))
            elif method == "dp":
                distance = updateMatrix_dp(dcp(mat))
            print(f"\n0-1 Matrix: {mat}")
            print(f"{method}: Distance from nearest 0 = {distance}")
            passed = (ans == distance)
            assert passed == True, f"Test case failed"
            print(f"Pass: {passed}")
    print(f"\nDONE")

run_tests()