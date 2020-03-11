# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 09:14:41 2017

@author: galdal-gibbsj

Credit for game rules: # https://bitstorm.org/gameoflife/

User notes
play with starting config (0=binomial,1=GLider,2=small exploder),
probability (for config=0),
grid size (nrows, ncols)

"""

# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--starting_config", default=0, type=int)
parser.add_argument("--topology", default="m0", type=str)

args = parser.parse_args()

starting_config = args.starting_config
topology = args.topology

print(starting_config, topology)

nrows, ncols = 100, 100

# Function to initiate grid (default is random 15% alive)
def setup_grid(starting_config=0):
    if starting_config == 0:                
        # Random 15% alive
        prob = 0.10
        # Initialise grid
        data=np.random.binomial(n=1, p=prob, size=(nrows,ncols))
        # data=np.random.randint(low=0, high=2, size=(nrows,ncols))
                            
    elif starting_config == 1:
        # Glider
        data = np.zeros((nrows, ncols))
        data[10,10]=1
        data[10,11]=1
        data[10,12]=1
        data[9,12]=1
        data[8,11]=1
    
    elif starting_config == 2:
        # Small exploder
        data = np.zeros((nrows, ncols))
        data[8,10]=1
        data[9,9]=1
        data[9,10]=1
        data[9,11]=1
        data[10,9]=1
        data[10,11]=1
        data[11,10]=1
    
    return data
    
# Update function, used in animation (non-wrap-around)
def update(data, topology="m0"):
    global grid
    neighbour_grid = np.zeros_like(grid)
    data_temp = np.zeros_like(grid) # don't modify 'data' while iterating thru it!
       
    # Perform an iteration & plot new setup
    for i in range(nrows):
        for j in range(ncols):
            
            ## torus
            if topology == "m0":
                i_list = [(i-1)%(nrows-0),(i)%(nrows-0),(i+1)%(nrows-0)]
                j_list = [(j-1)%(ncols-0),(j)%(ncols-0),(j+1)%(ncols-0)]
            ## Mobius order 1 (need 2 laps to get back to start)
            elif topology == "m1":
                i_list = [(i-1),(i),(i+1)]
                j_list = [(j-1),(j),(j+1)]
                for ind_dum in len(i_list):
                    if i_list[ind_dum]<0 and j_list[ind_dum]<0:
                        pass
                for index, el in enumerate(i_list):
                    if el < 0: 
                        i_list[index] = nrows + el

            # Count neighbours
            neighbour_count = 0
            for p in i_list:
                for q in j_list:
                    if not (p==i and q==j): # self not neighbour nor non-neighbour  
                        try:
                            if grid[p,q]==1:
                                neighbour_count+=1
                        except IndexError:
                            pass

            # If alive
            if grid[i,j] == 1:
                # If 1 or fewer buddies
                if neighbour_count < 2 or neighbour_count>3:
                    # Cell dies
                    dummy = 0
                else: dummy = 1
                    # data[i,j] = 0 ## spoke too soon

            # If dead
            if grid[i,j] == 0:
                # if 3 
                if neighbour_count == 3:
                    # Call revives
                    dummy = 1
                    # data[i,j] = 1 ## spoke too soon
                else: dummy = 0

            data_temp[i,j] = dummy
            neighbour_grid[i,j] = int(neighbour_count)
    
    mat.set_data(data_temp)
    grid = data_temp
    pop_list.append(np.mean(data_temp))
    return [mat]

# Set up population trajectory animation
pop_list = []
# Set up animation
grid = setup_grid(starting_config=starting_config)
fig, ax = plt.subplots()
mat = ax.matshow(grid)
ani = animation.FuncAnimation(fig, update, interval=0, save_count=5000)
plt.show()

# Plot population trajectory
plt.plot(pop_list)
plt.ylabel('Population / %')
plt.xlabel('Time / itns')
plt.title('Population History')
plt.show()
plt.savefig("Popn.jpg")