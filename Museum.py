class Museum:
    """
    Represents a collection of artifcats with assciated values and weights to find the optimal subset.
    The optimal subset will maximize the total value while staying within a given capacity constraint. 

    Attributes:
        __value (list[int]): List of artifact values where index i corresponds to item i (index 0 is None)
        __weight (list[int]): List of artifact weights where index i corresponds to item i (index 0 is None)
        __capacity_max (int): Maximum weight capcity
        __n (int): Number of items in the collection 
    """

    def __init__(self, value: list[int], weight: list[int], capacity_max: int):
        """
        Museum instance with artifacts and capacity constraint

        Args: 
            value (list[int]): List of item values where value[i] is the value of item i for i >= 1
            weight (list[int]): List of item weights where weight[i] is the weight of item i for i >= 1
            capacity_max (int): Maximum weight capacity for sack?
            n (int): Number of items in the collection
        """
        self.__value = value
        self.__weight = weight
        self.__capacity_max = capacity_max
        self.__n = len(value) - 1


    def __optimal_subset_value(self, value:list[int], weight:list[int], Cmax:int) -> list[list[int]]:
        """
        Pseudocode for S
        Initialize array with n+1 rows and Cmax+1 columns
        Set first row and first column to 0
        for row = 1 to n inclusive:
        for avail_capacity = 1 to Cmax inclusive:
           ... etc etc ...

        Builds the 2d table to find the optimal subset values 
        S[i][] represents the biggest value possible using the first i items considering the constraint r. 

        Args: 
            value (list[int]): List of item values
            weight (list[int]): List of item weights 
            Cmax (int): Maximum capacity constraint   

        Returns:
            list[list[int]]: 2d table ((n+1)x(Cmax+1)) containing maximum values achievable using items 
            1 to i considering capacity r.
            Bottom right cell = optimal solution      
        """
        n = len(value) - 1 # index 0 is none 
        # Create table : items(n + 1) x capacity(Cmax +1)
        S = [[0 for _ in range(Cmax + 1)] for _ in range(n + 1)]
        # Fill table 
        for i in range(1, n + 1):
            for j in range(1, Cmax + 1):
                # check if item is too heavy for capacity 
                if weight[i] > j:
                    # can't carry item i so the best value is the same as without it.
                    S[i][j] = S[i-1][j]
                # item fits     
                else: 
                    # option to not take the item 
                    dont_take = S[i-1][j]
                    # option to take the item 
                    take = S[i-1][j - weight[i]] + value[i]
                    # pick whichever option has higher value 
                    S[i][j] = max(dont_take, take)
        return S


    def __build_subset(self, S: list[list[int]], value: list[int], weight: list[int], Cmax: int) -> list[int]:
        """
        Start from bottom right cell of 2d table and backtrack to determine what items were selected for 
        optimal solution.
        
        Args:
            S (list(list[int])): the complete table from __optimal_subset_value
            value (list[int]): list of item values 
            weight (list[int]): list of item weights
            Cmax(int): maximum capacity constraint

        Returns: 
            list[int]: list of item indicies that are the optimal subset
        """
        subset = []
        # iterate backwards through S to find which items are included
        # ... your code here ...
        n = len(value) - 1
        r = Cmax
        # last > first
        for i in range(n, 0, -1):
            # compare cell with the cell above it 
            # if not equal, item i was included 
            if S[i][r] != S[i-1][r]:
                # item is in subset 
                subset.append(i)
                # subtract the items weight from the remaining capacity 
                r = r - weight[i]
        return subset

    def solve(self) -> None:
        """
        Solves the problem by building 2d table, identifies the optimal subset of museum artifacts,
        and displays statistics regarding the solution(number of possible subsets, table dimensions,
        selected items, and total weight and value).

        Returns:
            None: results are just printed output 

        Prints:
            * Total num of possible subsets 
            * Size of the 2d table
            * Num of items in optimal subset
            * Items in the optimal subset
            * Total weight of optimal subset
            * Capacity constraint 
            * Capacity utilization
            * Total value of optimal subset     
        """
        # build the table
        S = self.__optimal_subset_value(self.__value, self.__weight, self.__capacity_max)
        # find which items are in the optimal subset 
        optimal_items = self.__build_subset(S, self.__value, self.__weight, self.__capacity_max)
        # calculate how many subsets are theoretically possible 
        total_possible_subsets = 2 ** self.__n
        # calculate the size of matrix S
        matrix_size = (self.__n + 1) * (self.__capacity_max + 1)
        # calculate how many items in the optimal subset 
        amt_items_in_subset = len(optimal_items)
        # calculate total weight of items in optimal subset 
        total_weight = sum(self.__weight[i] for i in optimal_items)
        # calculate the total value (bottom right corner)
        total_value = S[self.__n][self.__capacity_max]

        print(f"Total possible subsets: {total_possible_subsets:,}")
        print(f"Size of matrix: {matrix_size:,}")
        print(f"Number of items in optimal subset: {amt_items_in_subset:,}")
        print(f"Items in optimal subset: {sorted(optimal_items, reverse=True)}")
        print(f"Total weight of optimal subset: {total_weight}")
        print(f"Capacity constaint: {self.__capacity_max}")
        print(f"Capacity utilization: {total_weight}/{self.__capacity_max} ({(total_weight/self.__capacity_max)*100:.1f}%)")
        print(f"Total value of optimal subset: {total_value}")
