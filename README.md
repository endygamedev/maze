<p align="center"><img src="/assets/logo.gif" alt="logo" width="150"></p>
<h1 align="center">Maze solver or pathfinding algorithm</h1>
<p align="center">This repository contains the implementation and visualization of the primitive pathfinding algorithm.</p>

<h2>Problem</h2>
<p>Given a space with passages and walls, an entry point and an exit point are also given, you must find a path from start to finish through free cells.</p>
<p>We can divide this task into 3 subtasks:
  <ol>
    <li>Generate given space (maze)</li>
    <li>Implement a pathfinding algorithm</li>
    <li>Create visualization of this algorithm</li>
  </ol>
</p>

<p align="center"><img src="/assets/maze_example.png"><br>
<i>(1) Maze example</i>
</p>

<p><i>Description to image (1)</i><br>
<ul>
  <li>black — walls</li>
  <li>white — passages</li>
  <li>green — entry point (start)</li>
  <li>magenta — exit point (finish)</li>
</ul>
</p>

<h2>Algorithms</h2>
<h3>1. Generate maze</h3>
<p>Given the <code><i>width</i></code> and <code><i>height</i></code> of the maze we want to create.<br>
So, to begin with, randomly generate an entry point (<code><i>start</i></code>) and an exit point (<code><i>finish</i></code>).<br>
Then we create a matrix of ones (<code><i>maze</i></code>), in the further implementation we will denote 0 as a passage, and 1 as a wall, roughly speaking, we set a labyrinth of some walls.<br>
Set the matrix element <code><i>maze<sub>start.x start.y</sub></i> = 0</code> and also denote by <code><i>(current.x, current.y)</sub></i></code> the current position in the maze matrix.<br>
Until we reach the finish line <code><i>(current.x, current.y) != (finish.x, finish.y)</i></code>, then we take a random cell from the list of passed cells and a random direction of movement: up, down, left, right; we check whether we can go in this direction, if not, then we change the direction of movement until the desired direction is found, we move in the chosen direction.<br>
Thus, at each iteration, we move in a random direction of a random cell until we find the finish, roughly speaking, we destroy the walls. 
</p>
