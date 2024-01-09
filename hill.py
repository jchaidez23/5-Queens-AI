from board import Board
import random
import time

#updates the rows to provide a neighbor to each iteration
def update_row(board,row,row_index):
    #print("UPDATED ROWS")
    board.get_map()[row_index] = row
    #board.show_map()
    return board

#Creates the neighbor to each row
#initializes two rows full of 0's 
#and then replaces the necessary index by 1 allowing for it to wrap around using the modulus

def get_new_row(row):
   # print("NR")
    queen = None
    for i in range(5):
        if row[i] == 1:
            queen = i

    
    neighbor1 = [0,0,0,0,0]
    neighbor2 = [0,0,0,0,0]
    right = (queen + 1) % 5
    left = (queen - 1) % 5
    neighbor1[left] = 1
    neighbor2[right] = 1
    neighbors = [neighbor1,neighbor2]
    #print(neighbors)
    return neighbors

#Creates the original board
start_time = time.perf_counter()
current = Board(5)
current.show_map()
print(current.get_fitness())

#creates a tries counter to randomly restart on a random row
tries = 0
while current.get_fitness() != 0:
    while tries < 100:
        #ends program if the condition is met
        #finding the optimal solution
        if current.get_fitness() == 0:
            current.show_map()
            end_time = time.perf_counter()
            total_time = end_time - start_time
            print("Running time:", total_time, "ms")
            break
            
        
        #iterates over the board and updates to a neighbor if it has a 
        #lower number of attacking pairs using the get fitness function
        for row in range(5):
            new_rows = get_new_row(current.get_map()[row])
            left_neighbor = update_row(current,new_rows[1],row)
                #print(left_neighbor.get_fitness())
            right_neighbor = update_row(current,new_rows[0],row)
                #print(right_neighbor.get_fitness())
            if left_neighbor.get_fitness() < current.get_fitness():
                current = left_neighbor
            elif right_neighbor.get_fitness() < current.get_fitness():
                current = right_neighbor
        tries += 1

        #if we reach 99 tries we randomly select a row and get its neigbors in order to prevent
        #being stuck in a local minima
        if tries == 99:
            random_num = random.randint(0,4)
            random_row = get_new_row(current.get_map()[random_num])
            left_neighbor = update_row(current,random_row[1],random_num)
                #print(left_neighbor.get_fitness())
            right_neighbor = update_row(current,random_row[0],random_num)
            if left_neighbor.get_fitness() < current.get_fitness():
                current = left_neighbor
            elif right_neighbor.get_fitness() < current.get_fitness():
                current = right_neighbor
            tries = 0


