import csv
import sys
if len(sys.argv) > 1:

    '''
        This proyect is divided in several functions to obtain the desired results
        The functiones are:
            S = Match or MisMatch of letters
            init = Initialize and returns a matrix given two sequences
            fillMatrix = Fills the matrix obtained from init with the calculated scores
            backTracking and backTrackingHelper = Does the necessary calculations to select the correct allingment for each sequence
            and returns the resultant sequences and scoring
            main = Reads the input csv file and calls every function to obtain results and prints them
    '''

    d = -2 # Gap Penalty
    
    # Match or MisMatch
    def S(a, b):
        if a == b: return 1
        return -1
    
    # Initialize matrix
    def init(s1, s2):
        s1_len = len(s1)
        s2_len = len(s2)
    
        # Create empty matrix
        matrix = [[0 for i in range(s1_len + 1)] for j in range(s2_len + 1)]

        # Initialization Step
        for i in range(s2_len+1):
            for j in range(s1_len+1):
                matrix[0][j] = d * j
                matrix[i][0] = d * i
    
        return matrix
    
    # Fill matrix
    def fillMatrix(s1, s2, matrix):
        
        for i in range(1, len(matrix)):
            for j in range(1, len(matrix[i])):
                diagonal = matrix[i-1][j-1]
    
                scoring = diagonal + S(s1[j-1], s2[i-1]) # diagonal score
    
                gapj = matrix[i][j-1] + d # left score
                gapi = matrix[i-1][j] + d # up score
    
                matrix[i][j] = max(scoring, gapj, gapi) # inputs to the matrix max between diagonal, left or up score
    
    # BackTracking function
    def backTracking(s1, s2, matrix):
    
        n = len(matrix) - 1 # length of columns
        m = len(matrix[n-1]) - 1 # length of rows
        scoring = matrix[n][m]  # last index that corresponds to the scoring
        res1 = '' # resultant sequence for sequence 1
        res2 = '' # resultant sequence for sequence 2
    
        # Recursive BackTracking helper
        def backTrackingHelper(s1, s2, matrix, res1, res2, i, j):
            # base case
            if i == 0 and j == 0:
                return res1[::-1], res2[::-1] # When it has reached the first index it returns the both sequences reversed

            up = matrix[i-1][j] + d
            left = matrix[i][j-1] + d
            diagonal = matrix[i-1][j-1] + S(s1[j-1], s2[i-1])

            maxNum = max(up, left, diagonal) # max number between up, left and diagonal scores
            
            # if all scores are equal it moves to the left
            if (maxNum == diagonal == left == up):
                res1 += s1[j-1]
                res2 += '-'
                return backTrackingHelper(s1, s2, matrix, res1, res2, i, j-1)
            
            # if the diagonal and left scores are equal it moves to the left
            if (maxNum == diagonal == left):
                res1 += s1[j-1]
                res2 += '-'
                return backTrackingHelper(s1, s2, matrix, res1, res2, i, j-1)
            
            # if the diagonal and up scores are equal it moves up
            if (maxNum == diagonal == up):
                res1 += '-'
                res2 += s2[i-1]
                return backTrackingHelper(s1, s2, matrix, res1, res2, i-1, j)

            # if max score is diagonal it moves to the diagonal score
            if maxNum == diagonal:
                res1 += s1[j-1]
                res2 += s2[i-1]
                return backTrackingHelper(s1, s2, matrix, res1, res2, i-1, j-1)

            # if max score is left it moves to the left score
            elif maxNum == left:
                res1 += s1[j-1]
                res2 += '-'
                return backTrackingHelper(s1, s2, matrix, res1, res2, i, j-1)

            # if max score is up it moves up
            res1 += '-'
            res2 += s2[i-1]
            return backTrackingHelper(s1, s2, matrix, res1, res2, i-1, j)
        
        # backTracking function returns both sequence and the scoring in a tuple
        return backTrackingHelper(s1, s2, matrix, res1, res2, n, m), scoring
    
    
    def main(csvFile):
        
        # list to store file data
        rows = []
        with open(csvFile, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                rows.append(row)
        file.close()
        
        # Iterates through input data to obtain sequences
        for row in range(1, len(rows)):
            matrix = init(rows[row][0], rows[row][1])   # Initialize matrix
            fillMatrix(rows[row][0], rows[row][1], matrix)  # Fills the matrix
            resTup = backTracking(rows[row][0], rows[row][1], matrix)   # Results Tuple
        
            sequence1 = resTup[0][0]
            sequence2 = resTup[0][1]
            scoring = resTup[1]
        
            print(sequence1, sequence2, scoring)
    
    main(sys.argv[1]) # Calls main function to read file and print results




