import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        maxConsecutiveMoves = 100
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))

            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            if i >= maxConsecutiveMoves and currentNumberOfAttacks == 0:
                # reach max consecutive moves or goal state
                break

            i += 1
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            if currentNumberOfAttacks <= newNumberOfAttacks:
                # reach local minimal, need to randomly initialize current state
                newBoard = Board()

        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        costBoard = self.getCostBoard()
        costBoardTranspose = list(map(list, zip(*costBoard.squareArray)))

        allNeighbourCost = [cost for row in costBoard.squareArray for cost in row]
        minNeighbourCost = min(allNeighbourCost)
        currentAttackCount = self.getNumberOfAttacks()

        if minNeighbourCost >= currentAttackCount:
            # already in local minimal, return current board with the first queen we meet
            for x, row in enumerate(costBoard.squareArray):
                for y, cost in enumerate(row):
                    if cost == 9999:
                        return (self, currentAttackCount, x, y)
        else:
            boardSize = len(self.squareArray)
            minNeighbourIdx = allNeighbourCost.index(minNeighbourCost)
            newRow, newCol = minNeighbourIdx // boardSize, minNeighbourIdx % boardSize
            # find the queen in corresponding column and move it to minimal neighbour (newRow, newCol)
            queenRow = costBoardTranspose[newCol].index(9999)
            self.squareArray[queenRow][newCol] = 0
            self.squareArray[newRow][newCol] = 1

            return (self, self.getNumberOfAttacks(), newRow, newCol)

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        def attackCount(queenCount):
            # given the number of queens in a row/column/diagonal, return corresponding number of attacks
            return queenCount * (queenCount - 1) / 2 if queenCount > 1 else 0

        attacks = 0
        # get row attack
        for row in self.squareArray:
            attacks += attackCount(sum(row))
        # get column attack
        for col in list(map(list, zip(*self.squareArray))):
            attacks += attackCount(sum(col))
        # get diagonal attack
        # TODO: refactor this part
        size = len(self.squareArray)
        diagonals = [[self.squareArray[i - j][j] for j in range(max(i - size + 1, 0), min(i + 1, size))] for i in range(size * 2 - 1)]
        diagonals.extend([[self.squareArray[size - i + j - 1][j] for j in range(max(i - size + 1, 0), min(i + 1, size))] for i in range(size * 2 - 1)])
        for diagonal in diagonals:
            attacks += attackCount(sum(diagonal))

        return int(attacks)


if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
