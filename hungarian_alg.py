from cmath import inf

class Hungarian():
    def __init__(self,matrix):
        self.matrix = matrix # matrix[task][machine] = cost
        self.theta = 0 # total matrix reduction
    

    def reduce_matrix(self): # method subtracting lowest values from rows and columns
        # rows:
        for i,_ in enumerate(self.matrix):
            self.theta += min(self.matrix[i])
            self.matrix[i] = [elem - min(self.matrix[i]) for elem in self.matrix[i]]
        # cols:
        for j,_ in enumerate(self.matrix):
            min_col_val = inf
            for i,_ in enumerate(self.matrix[i]): # find minimal value
                if self.matrix[i][j] < min_col_val : min_col_val = self.matrix[i][j]
            
            self.theta += min_col_val

            for i,_ in enumerate(self.matrix[i]): # subtract minimal value
                self.matrix[i][j] -= min_col_val
            
    def get_more_independent_zeros(self): # method for further matrix reduction
        min_matrix_val = inf
        crossed_rows = [] # temporary arrays, while proper ones are being developed
        crossed_cols = []

        for i,_ in enumerate(self.matrix): # find minimal value uncrossed value in matrix
            for j in enumerate(self.matrix[i]):
                if i not in crossed_rows and j not in crossed_cols and self.matrix[i][j] < min_matrix_val:
                    min_matrix_val = self.matrix[i][j]
        # add minval
        multiplicator = 1 # how many times multiply min value
        for i,_  in enumerate(self.matrix): # subtract minimal value from uncrossed elems
            if i in crossed_rows : continue
            for j,_ in enumerate(self.matrix[i]):
                if i in crossed_rows and j in crossed_cols: 
                    self.matrix[i][j] += min_matrix_val # add minimal value to double crossed elements
                    multiplicator -= 1
                if j in crossed_cols : continue
                self.matrix[i][j] -= min_matrix_val
                multiplicator += 1
        self.theta += multiplicator * min_matrix_val

        
        


        




