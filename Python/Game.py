from queue import Queue
from Sudoku import Sudoku
from Field import Field

class Game:

    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

    def show_sudoku(self):
        print(self.sudoku)

    def solve(self) -> bool:
        """
        Enhanced AC-3 algorithm with MRV heuristic and prioritization of finalized fields.
        @return: True if a solution is found; False otherwise.
        """
        arc_queue = Queue()  
        
        
        for row in self.sudoku.board:
            for field in row:
                if field.value == 0:  
                    for neighbour in field.neighbours:
                        if neighbour.value == 0:
                            priority = self.calculate_priority(field, neighbour)
                            arc = (field.row, field.col, neighbour.row, neighbour.col)
                            arc_queue.put((priority, arc))

        while not arc_queue.empty():
            _, arc = arc_queue.get()

            if self.process_arc(arc[0], arc[1], arc[2], arc[3]):
                field = self.sudoku.board[arc[0]][arc[1]]

                if len(field.domain) == 0:
                    return False

                
                for neighbour in field.neighbours:
                    if neighbour.value == 0:  
                        priority = self.calculate_priority(field, neighbour)
                        temp_arc = (neighbour.row, neighbour.col, field.row, field.col)
                        arc_queue.put((priority, temp_arc))

        
        for row in self.sudoku.board:
            for field in row:
                if len(field.domain) == 1:
                    field.value = field.domain[0]

        return True

    def calculate_priority(self, field1: Field, field2: Field) -> int:
        """
        Calculate priority for an arc between two fields based on MRV and finalized fields.
        Lower values indicate higher priority.

        Priority :
        - Fields with a single value (finalized) get the highest priority (value 0).
        - Otherwise, prioritize based on the size of their domains (MRV).
        """
        
        if len(field1.domain) == 1:
            return 0  

        # Check MRV for the first field
        return len(field1.domain)  

    def process_arc(self, f1_row, f1_col, f2_row, f2_col):
        """
        Process the arc between two fields, f1 and f2, removing values from f1's domain.
        @return: True if f1's domain was modified; False otherwise.
        """
        domain_changed = False
        f1 = self.sudoku.board[f1_row][f1_col]
        f2 = self.sudoku.board[f2_row][f2_col]

        for val1 in f1.domain[:]:  
            valid_option = any(val1 != val2 for val2 in f2.domain)

            if not valid_option:
                f1.domain.remove(val1)
                domain_changed = True

        return domain_changed

    def valid_solution(self, verbose=True) -> bool:
        """
        Checks the validity of a Sudoku solution.
        @return: True if the solution is valid; False otherwise.
        """
        for row in self.sudoku.board:
            for field in row:
                for n in field.neighbours:
                    if field.value == n.value and field.value != 0:
                        if verbose:
                            print(f"Duplicate number ({field.value}) at ({field.row + 1}, {field.col + 1}) and ({n.row + 1}, {n.col + 1})")
                        return False
        return True
