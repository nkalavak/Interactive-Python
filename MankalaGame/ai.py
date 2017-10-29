################### EE562 ####################
############ Niveditha Kalavakonda ###########
############ HW3 - KALAH GAME IMPL.###########

import time
import random
import io
import copy

from PyQt4.QtCore import QElapsedTimer

global timer
global timeElapsed
global totalMoves

timer = None
timeElapsed = 0
totalMoves = 0

class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"

MAX = float("inf")
MIN = -float("inf")

""" # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating your move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately
    def move(self, a, b, a_fin, b_fin, t):
        #For test only: return a random move
        r = []
        for i in range(6):
            if a[i] != 0:
                r.append(i)
        # To test the execution time, use time and file modules
        # In your experiments, you can try different depth, for example:
        f = open('time.txt', 'a') #append to time.txt so that you can see running time for all moves.
        # Make sure to clean the file before each of your experiment
        for d in [3, 5, 7]: #You should try more
            f.write('depth = '+str(d)+'\n')
            t_start = time.time()
            self.minimax(depth = d)
            f.write(str(time.time()-t_start)+'\n')
        f.close()
        return r[random.randint(0, len(r)-1)]
        #But remember in your final version you should choose only one depth according to your CPU speed (TA's is 3.4GHz)
        #and remove timing code.

        #Comment all the code above and start your code here

    # calling function
    def minimax(self, depth):
        #example: doing nothing but wait 0.1*depth sec
        time.sleep(0.1*depth)"""

class ai:
    def __init__(self):
        pass

    class state:
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a
            self.b = b
            self.a_fin = a_fin
            self.b_fin = b_fin

    """
    This function generates a single child for c particular pit (given by holeNum)
    It returns a boolean (secondMove) by checking if a second move exists or not
    It does this by checking if the move lands in the Kalah
    Returns: a tuple consisting of the 'state' object child and the boolean secondMove
    """

    def updateLocalState_childrenGeneration(self, holeNumber, a, b, a_fin, b_fin):

        a_copy = copy.copy(a)
        b_copy = copy.copy(b)
        a_fin_copy = a_fin
        b_fin_copy = b_fin

        secondMove = False #Checks for second move
        takeAcross = False #checks if it can eat seeds from opposite side

        numPebbles = a[holeNumber]
        a_copy[holeNumber] = 0 #empties the current hole by emptying existing seeds

        # if the number of seeds is less than 5, increment a until we run out of seeds
        if numPebbles <= (5 - holeNumber):
            for i in range(numPebbles):
                a_copy[holeNumber + i + 1] += 1
                # checking if last pebble slot  is 0
                if a_copy[holeNumber + i + 1] == 1 and (numPebbles - i - 1) == 0:
                    takeAcross = True
                    a_fin_copy += b_copy[5 - (holeNumber + i + 1)] # take seeds from opposite hole and place into Kalah
                    b_copy[5 - (holeNumber + i + 1)] = 0 # empty opposite hole

        # if the number of seeds is more than 5
        else:
            IncrA = 5 - holeNumber # number of times we increment a (5 - current index)
            # increment a
            for i in range(IncrA):
                a_copy[holeNumber + i + 1] += 1
                # check if the last pebble slot is 0
                if a_copy[holeNumber + i + 1] == 1 and (numPebbles - i - 1) == 0:
                    takeAcross = True
                    a_fin_copy   += b_copy[5 - (holeNumber + i + 1)]
                    b_copy[5 - (holeNumber + i + 1)] = 0
            numPebbles -= IncrA

            # if there are still some seeds, increment a_fin
            if (numPebbles > 0):
                a_fin_copy += 1
                numPebbles -= 1
                # check if eligible for second move
                if numPebbles == 0:
                    secondMove = True

            while (numPebbles > 0):
                # if we only have less than 6 seeds, increment b only
                if numPebbles <= 6:
                    for i in range(numPebbles):
                        b_copy[i] += 1
                        numPebbles -= 1
                # if we have more than 6 seeds
                else:
                    # first increment all the 6 holes in b
                    for i in range(6):
                        b_copy[i] += 1
                        numPebbles -= 6
                    # if we now have 6 or less than 6 seedss, increment the remaining holes in a
                    if numPebbles <= 6:
                        for i in range(numPebbles):
                            a_copy[i] += 1
                            numPebbles -= 1
                            # check if the last pebble lands in an empty slot
                            if a_copy[i] == 1 and numPebbles == 0:
                                takeAcross = True
                                a_fin_copy += b_copy[5 - i]
                                b_copy[5 - i] = 0
                    # if we now have 7 seeds remaining
                    elif numPebbles == 7:
                        # increment all the 6 holes in a
                        for i in range(6):
                            a_copy[i] += 1
                            # check if the last pebble lands in an empty slot
                            if a_copy[i] == 1 and (numPebbles - i - 1) == 0:
                                takeAcross = True
                                a_fin_copy += b_copy[5 - i]
                                b_copy[5 - i] = 0
                        # and also increment a_fin
                        a_fin_copy += 1
                        numPebbles -= 7
                        # check if eligible for second move
                        if numPebbles == 0:
                            secondMove = True

                    # if we now have more than 7 seeds remaining
                    else:
                        # increment all the 6 holes in a
                        for i in range(6):
                            a_copy[i] += 1
                        numPebbles -= 6
                        if numPebbles > 0:
                            a_fin_copy += 1
                            numPebbles -= 1
                            # check if the last pebble lands in an empty slot
                            if a_copy[i] == 1 and numPebbles == 0:
                                takeAcross = True
                                a_fin_copy += b_copy[5 - i]
                                b_copy[5 - i] = 0
                            # check if eligible for second move
                            if numPebbles == 0:
                                secondMove = True

        child = self.state(a_copy, b_copy, a_fin_copy, b_fin_copy)
        # return a tuple with child object of class 'state' and secondMove boolean
        return (child, secondMove)

    """
    This function generates all possible children from one state condition
    All children are appended into the list 'children'(also considering their index value)
    Returns: a list that contains tuples of each child (object and second move) with its index
    """

    def setChildrenIndex(self, a, b, a_fin, b_fin):
        # copy a and b to avoid mutation during passing / operations
        a_copy = copy.copy(a)
        b_copy = copy.copy(b)
        children = list()
        # generating all possible children by moving stones from index 0 to 6
        for i in range(6):
            if a_copy[i] != 0:
                child = self.updateLocalState_childrenGeneration(i, a_copy, b_copy, a_fin, b_fin)
                children.append((child, i)) #appends children to list
        # return the children list
        return children

        """
        FUNCTION FOR taking MAX or MIN in consecutive steps

        for i in range(6):
            if a[i] != 0:
                (child, secondMove) = self.updateLocalState_childrenGeneration(i, a, b, a_fin, b_fin)
                if secondMove:
                    for j in range(6):
                        if a[j] != 0:
                            (child, secondMove) = self.updateLocalState_childrenGeneration(j, a, b, a_fin, b_fin)
                            children.append(((child, secondMove), i))
                else:
                    children.append(((child, secondMove), i))
        return children"""

    """
    This function extracts all possible children from the function
    Returns: a list of each child (object and second move)
    """

    def getChildren(self, a, b, a_fin, b_fin):
        children = self.setChildrenIndex(a, b, a_fin, b_fin)
        result = list()
        for child in children:
            result.append((child[0][0], child[0][1]))
        return result

    """
    Pre-defined function written to communicate with the UI, by taking into account the moves
    Returns: index value of best move index
    """

    def move(self, a, b, a_fin, b_fin, t):
        # For test only: return a random move
        global timer
        global timeElapsed
        global totalMoves

        totalMoves +=1 #To keep track of all the moves
        # defining the alpha, beta, and depth parameters to be used
        alpha = MIN
        beta = MAX
        depth = 7 #Also tried with 3 and 7
        machine = ai()
        # timing variables
        timer = QElapsedTimer()
        timer.start()
        t_start = time.time()

        val_found = False #To set priorities
        for i in range(6):
            if a[i] >= 13: #Highest priority is when a pit has more than 13 pebbles -- Heuristic 1
                bestMove = i
                val_found = True
        if not val_found:
            children = self.setChildrenIndex(a, b, a_fin, b_fin) # generating all children
            bestMove = -1
            bestValue = -float("inf")
            # evaluate every child to find the ultimate best move index
            for child in children:
                # obtaining the weighted value of child from the alpha-beta minimax algorithm
                value = machine.minimax(child[0][0].a, child[0][0].b, child[0][0].a_fin, child[0][0].b_fin, depth,
                                     False, child[0][1], child[0][1], alpha, beta, t_start, t)
                # check if the child value returned by minimax is valid (i.e.: larger than -infinity)
                if value > bestValue:
                    bestMove = child[1] # if valid, set the new best move to the index that produces current child
                    bestValue = max(value, bestValue) # update best value to the maximum between the old and the current child value

            for j in range(6): #Heuristic 5
                if b[j] == 0:
                    (ch1,sec1) = machine.updateLocalState_childrenGeneration(bestMove, b, a, b_fin, a_fin)
                    if(ch1.a_fin - a_fin < 3 and a[5-j] != 0): #Condition for checking
                        bestMove = 5-j #Makes avoiding being eaten the best move
        if bestMove == -1:
            bestMove = 0 #Arbitrary

        timeElapsed = timeElapsed + timer.elapsed()
        print "Time This Move: %f ms" % timer.elapsed()
        print "Total Time Elapsed: %f ms" % timeElapsed
        print "Average Time per Move: %f ms" % (timeElapsed / totalMoves)
        print "Total Moves: %d" % totalMoves
        print "------------------------\n"
        return bestMove


    """
    This function checks if the game has ended
    This happens if number of stones in a's or b's kalah is more than or equal to 37 (a_fin or b_fin >= 37)
    or if a or b run out of stone (a or b = [0,0,0,0,0,0])
    Returns: Boolean based on whether game ended or not
    """
    def isEndGame(self, a, b, a_fin, b_fin):
        if a_fin >= 37 or b_fin >= 37 or a == [0, 0, 0, 0, 0, 0] or b == [0, 0, 0, 0, 0, 0]:
            return True
        return False

    """
    This function checks if current state is game end condition or leaf condition
    This is determined if game reaches end conditions, or
    Depth is greater than depth limit set or
    Time elapsed is greater than time limit set (only for tournament)
    Returns: Boolean based on whether terminal condition or not
    """
    def isTerminal(self, a, b, a_fin, b_fin, depth, t_start, t):
        #time check done for tournament
        #if (time.time()- t_start)*1000 > t:
        #   return True
        if self.isEndGame(a, b, a_fin, b_fin) or depth <= 0: #or timer.hasExpired(t) :
            return True
        return False

    """Heuristic Function definition
    The heuristics are set to be:
    1. number of seeds in a's kalah - b's kalah
    2. number of all possible subsequent moves
    3. sum of seeds in a's holes - sum of seeds in b's holes
    Returns: Integer based on weights and heuristics
    """
    def heuristicFunc(self, numSecondMove, a, b, a_fin, b_fin):
        diffOfKalahs = a_fin - b_fin #heuristic 2
        totalDiff = sum(a) - sum(b) #heuristic 3
        playablePebbles = sum(a) + sum(b) #heuristic 4

        # if there are more than or equal to 15 playable stones, heuristic is only kalahDiff and numSecondMove
        if playablePebbles >= 15:
            heuristic = 0.7 * diffOfKalahs + 0.3 * numSecondMove
        # else if there are less than 15 playable stones, heuristic also takes into account stonesDiff
        elif playablePebbles < 15:
            heuristic = 0.5 * diffOfKalahs + 0.3 * numSecondMove + 0.2 * totalDiff
        return heuristic

    """
    This is the Minimax Algorithm with Alpha-Beta Pruning
    """
    def minimax(self, a, b, a_fin, b_fin, depth, Maxmin, numSecondMove, secMove, alpha, beta, t_start, t):
        # copy a and b to avoid mutation during passing / operations
        a_copy = copy.copy(a)
        b_copy = copy.copy(b)
        a_fin_copy = a_fin
        b_fin_copy = b_fin
        # check for terminal condition (game ends or leaf node)
        if self.isTerminal(a_copy, b_copy, a_fin_copy, b_fin_copy, depth, t_start, t):
            return self.heuristicFunc(numSecondMove, a_copy, b_copy, a_fin_copy, b_fin_copy)
        # (the player to be optimized by the AI)
        if Maxmin:
            bestValue = -float("inf")
            for (child, secMove) in self.getChildren(a_copy, b_copy, a_fin_copy, b_fin_copy):  # Need to define getting children
                numSecMove = numSecondMove + secMove
                # if current player is eligible for second move,
                # run minimax again without switching player and without decrementing level
                if secMove:
                    value = self.minimax(child.a, child.b, child.a_fin, child.b_fin, depth, Maxmin, numSecMove,
                                         secMove, alpha, beta, t_start, t)
                    bestValue = max(bestValue, value)
                # if not second move, run minimax, switch player and decrement level
                else:
                    value = self.minimax(child.a, child.b, child.a_fin, child.b_fin, depth - 1, not Maxmin, numSecMove,
                                         secMove, alpha, beta, t_start, t)
                    bestValue = max(bestValue, value)
                    if bestValue >= beta:
                        return bestValue
                    alpha = max(bestValue, alpha)
            return bestValue
        # (the player the AI is playing against)
        else:
            bestValue = float("inf")
            for (child, secMove) in self.getChildren(b_copy, a_copy, b_fin_copy,
                                                     a_fin_copy):  # Need to define getting children
                numSecMove = numSecondMove
                # if current player is eligible for second move,
                # run minimax again without switching player and without decrementing level
                if secMove:
                    value = self.minimax(child.a, child.b, child.a_fin, child.b_fin, depth, Maxmin, numSecMove,
                                         secMove, alpha, beta, t_start, t)
                    bestValue = min(bestValue, value)
                # if not second move, run minimax, switch player and decrement level
                else:
                    value = self.minimax(child.a, child.b, child.a_fin, child.b_fin, depth - 1, not Maxmin, numSecMove,
                                         secMove, alpha, beta, t_start, t)
                    bestValue = min(bestValue, value)
                    if bestValue <= alpha:
                        return bestValue
                    beta = min(bestValue, beta)
            return bestValue