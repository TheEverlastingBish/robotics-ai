### Workshop 1 - Data Structures in Python
import sys
from tracemalloc import start
sys.path.append('../../../')
from utils import util
import time
from datetime import datetime, timedelta


## Stacks
### Task 1: Stack Operations
def task1():
    s = util.Stack()

    ## Operations
    s.push('a')
    s.push('b')
    s.push('c')
    s.pop()
    s.pop()
    s.push('d')
    s.push('e')
    s.pop()
    s.push('f')

    print(s.list)
    # ['a', 'd', 'f']



### Task 2: Custom Stack Operations
def task2():
    s2 = util.Stack()
    s2.list = ['dog', 'cat', 'bird', 'porcupine', 'hedgehog', 'antelope', 'orca']

    ## Operations
    s2.push('unicorn')
    print(s2.list)
    # ['dog', 'cat', 'bird', 'porcupine', 'hedgehog', 'antelope', 'orca', 'unicorn']

    s2.sort_list(reverse=False)
    print(s2.list)
    # ['antelope', 'bird', 'cat', 'dog', 'hedgehog', 'orca', 'porcupine', 'unicorn']

    s2.pop()
    print(s2.list)
    # # ['antelope', 'bird', 'cat', 'dog', 'hedgehog', 'orca', 'porcupine']

    print(s2.peek())
    # # porcupine

    print(s2.count())
    # # 7

    print("Does 'hedgehog' exist? ", s2.isExists('hedgehog'))
    # # Does 'hedgehog' exist?  True

    s2 = util.Stack()  # To reset, simply set to a new instance
    print(s2.list)

    print("Is the stack now empty?", s2.isEmpty())

    print("Peek?", s2.peek())



### Task 3: Checking Bracket Sequence
def check_bracket_sequence(expr):
    opening_brackets = ( '{', '[', '(' )
    closing_brackets = ( '}', ']', ')' )

    if len(expr) == 0:
        return False
    
    sx = util.Stack()

    for char in expr:
        if char in opening_brackets:
            sx.push(char)
            print("Adding element '{}'".format(char))
        else:
            if not sx:
                print("Empty stack")
                return False
            current_char = sx.pop()

            if char in closing_brackets:
                if current_char != opening_brackets[closing_brackets.index(char)]:
                    print("Mismatched brackets")
                    return False

    # Check empty Stack
    if not sx.isEmpty():
        return False
    else:
        return True



## Queues
### Task 4: Queue Operations
def task4():
    q1 = util.Queue()

    q1.push('a')
    q1.push('b')
    q1.push('c')
    q1.pop()
    q1.pop()
    q1.push('d')
    q1.push('e')
    q1.pop()
    q1.push('f')

    print(q1.list)



### Task 5: Additional Queue Operations
def task5():
    q = util.Queue()

    start_time = datetime.now()
    print("{}: Starting...".format(start_time))

    for i in range(100000):
        q.push(i)

    finish_time = datetime.now()
    print("{}: Finished.".format(finish_time))
    print("Time taken: {:.5f}s.".format((finish_time - start_time).total_seconds()))
    print("Queue Count: {:,}".format(len(q.list)))
    return q



# Task 6: Reverse a Queue
def reverse_queue(q):
    qx = util.Queue()
    qx = q
    print("Original Queue - First element: {:,}, Last element: {:,}".format(q.list[0], q.list[-1]))
    qx.reverse()
    print("Reversed Queue - First element: {:,}, Last element: {:,}".format(q.list[0], q.list[-1]))
    return qx


# Task 7: Dictionary Operations
def dictionary_ops():
    pass


# Task 8: Graphs
def graph_ops():
    pass



# Ops
if __name__ == '__main__':

    menu = input("""#######  Menu ######\n
    1. Task 1: Stack Operations
    2. Task 2: Custom Stack Operations
    3. Task 3: Check Bracket Sequence
    4. Task 4: Queue Operations
    5. Task 5: Additional Queue Operations
    6. Task 6: Reverse a Queue
    7. Task 7: Dictionary Operations
    8. Task 8: Graph Operations
    \nEnter selection: $ """).strip()

    if   menu == '1':
        task1()
    elif menu == '2':
        task2()
    elif menu == '3':
        br_seq = input("Enter bracket sequence:\n$ ")
        print(check_bracket_sequence(br_seq))
    elif menu == '4':
        task4()
    elif menu == '5':
        task5()
    elif menu == '6':
        reverse_queue(task5())
    elif menu == '7':
        dictionary_ops()
    elif menu == '8':
        graph_ops()
    else:
        print("ERR: Invalid selection.")

