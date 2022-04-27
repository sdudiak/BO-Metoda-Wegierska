from cmath import inf

class Hungarian():
    def __init__(self,matrix):
        self.matrix = matrix # matrix[task][machine] = cost
        self.theta = 0 # total matrix reduction
    

    def reduce_matrix(self): # method subtracting lowest values from rows and columns
        # rows:
        for i,_ in enumerate(self.matrix):
            self.theta += min(self.matrix[i])
            self.matrix[i] = [elem - min(self.matrix[i]) for elem in matrix[i]]
        # cols:
        for j,_ in enumerate(self.matrix):
            min_col_val = inf
            for i,_ in enumerate(self.matrix[i]): # find minimal value
                if self.matrix[i][j] < min_col_val : min_col_val = self.matrix[i][j]
            
            self.theta += min_col_val

            for i,_ in enumerate(self.matrix[i]): # subtract minimal value
                self.matrix[i][j] -= min_col_val
        
            





