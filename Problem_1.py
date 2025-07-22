'''
733 Flood Fill
https://leetcode.com/problems/flood-fill/description/

You are given an image represented by an m x n grid of integers image, where image[i][j] represents the pixel value of the image. You are also given three integers sr, sc, and color. Your task is to perform a flood fill on the image starting from the pixel image[sr][sc].

To perform a flood fill:
Begin with the starting pixel and change its color to color.
Perform the same process for each pixel that is directly adjacent (pixels that share a side with the original pixel, either horizontally or vertically) and shares the same color as the starting pixel.
Keep repeating this process by checking neighboring pixels of the updated pixels and modifying their color if it matches the original color of the starting pixel.
The process stops when there are no more adjacent pixels of the original color to update.

Return the modified image after performing the flood fill.

Example 1:
Input: image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2
Output: [[2,2,2],[2,2,0],[2,0,1]]
Explanation: From the center of the image with position (sr, sc) = (1, 1) (i.e., the red pixel), all pixels connected by a path of the same color as the starting pixel (i.e., the blue pixels) are colored with the new color.

Note the bottom corner is not colored 2, because it is not horizontally or vertically connected to the starting pixel.

Example 2:
Input: image = [[0,0,0],[0,0,0]], sr = 0, sc = 0, color = 0
Output: [[0,0,0],[0,0,0]]
Explanation: The starting pixel is already colored with 0, which is the same as the target color. Therefore, no changes are made to the image.

Solution:
1. BFS traversal of graph
https://youtu.be/oSvkTfsqwko?t=4234

Time: O(MN), Space: O(MN)

2. DFS traversal of graph
https://www.youtube.com/watch?v=2AZvtk6UThs

Time: O(MN), Space: O(MN)
'''
from collections import deque
from copy import deepcopy as dcp

def flood_fill_bfs(image, sr, sc, color):
    if not image or len(image) == 0 or image[sr][sc] == color:
        return image

    M = len(image)
    N = len(image[0])
    dirs = [[-1,0],[1,0],[0,-1],[0,1]] # U, D, L, R

    rows = deque()
    cols = deque()
    rows.append(sr)
    cols.append(sc)
    old_color = image[sr][sc]
    image[sr][sc] = color
    while rows:
        row = rows.pop()
        col = cols.pop()
        # For each neighboring cell containing the old color, change the old color to the desired color and enque the cell.
        for dir in dirs:
            x_, y_ = row + dir[0], col + dir[1]
            if 0 <= x_ <= M-1 and 0 <= y_ <= N-1 and image[x_][y_] == old_color:
                rows.append(x_)
                cols.append(y_)
                image[x_][y_] = color
    return image


def flood_fill_dfs(image, sr, sc, color):
    def dfs(sr, sc, color):
        if image[sr][sc] == old_color: image[sr][sc] = color
        # For each neighboring cell containing the old color, change the old color to the desired color. Do a recursion on the neighbor.
        for dir in dirs:
            x_, y_ = sr + dir[0], sc + dir[1]
            if 0 <= x_ <= M-1 and 0 <= y_ <= N-1 and image[x_][y_] == old_color:
                dfs(x_, y_, color)

        # # -------- code below from class (minor restructuring) ---------
        # # base
        # if not (0 <= sr <= M-1 and 0 <= sc <= N-1 and image[sr][sc] == old_color):
        #     return

        # # logic
        # if image[sr][sc] == old_color: image[sr][sc] = color
        # # For each neighboring cell containing the old color, change the old color to the desired color. Do a recursion on the neighbor.
        # for dir in dirs:
        #     x_, y_ = sr + dir[0], sc + dir[1]
        #     dfs(x_, y_, color)
        # # -------------------------------

    if not image or len(image) == 0 or image[sr][sc] == color:
        return image
    M = len(image)
    N = len(image[0])
    dirs = [[-1,0],[1,0],[0,-1],[0,1]] # U, D, L, R
    old_color = image[sr][sc]
    dfs(sr, sc, color)
    return image


def run_flood_fill():
    tests = [ ([[1,1,1],[1,1,0],[1,0,1]],1,1,2,[[2,2,2],[2,2,0],[2,0,1]]),
              ([[0,0,0],[0,0,0]],0,0,0,[[0,0,0],[0,0,0]]),
    ]
    for test in tests:
        image, sr, sc, color, ans = test[0], test[1], test[2], test[3], test[4]
        print(f"\nOriginal image = {image}")
        print(f"sr, sc = {sr, sc}, color = {color}")
        for method in ['bfs', 'dfs']:
            if method == 'bfs':
                new_image = flood_fill_bfs(dcp(image), sr, sc, color)
            elif method == 'dfs':
                new_image = flood_fill_dfs(dcp(image), sr, sc, color)
            print(f"{method}: Flood-fill image = {new_image}")
            print(f"Pass: {ans == new_image}")

run_flood_fill()