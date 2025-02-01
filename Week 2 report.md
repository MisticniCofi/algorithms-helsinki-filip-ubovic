#Week 2 report

This week I have spent most of the time visualizing the problem. At first I thought I had to use OpenStreetMaps to visualize the problem, but realized that a simple graph will be sufficient. Then I wanted to import information from OpenStreetMaps, because I had no idea how to actually find the neighboring nodes on a graph.
	
Suddenly, I figured that I could just randomly generate points in a rectangle whose sides present coordinates of longitude and latitude, get the distances from every node to all the others, creating a distance matrix, by subtracting the coordinates and applying Pythagora’s theorem, and then select an arbitrary number of closest ones for neighbors.
	
I decided on doing a project in Python for the sake of simplicity and plethora of available libraries. I picked RustworkX for graph visualization, which is similar to NetworkX, but is implemented in Rust making it much quicker. I also had to recall how to write in Python. Next week I will start implementing the algorithm. I left some pictures of the graph and code.

Time spent: 

~10 hours thinking of how to visualize

~10 hours recalling Python and playing around with the library

