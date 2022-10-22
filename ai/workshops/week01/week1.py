### Workshop 1 - Data Structures in Python
import sys
from tracemalloc import start
sys.path.append('../../../')
from utils import util
import time
from datetime import datetime, timedelta


## Stacks
### Task 1: Manipulating a Stack
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



### Task 2: Custom Stack
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
### Task 4: Manipulating Queue
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



### Task 5: Additional Operations in Queues
def task5():
    q2 = util.Queue()

    start_time = datetime.now()
    print("{}: Starting...".format(start_time))
    # time.sleep(4)
    for i in range(100000):
        q2.push(i)

    finish_time = datetime.now()
    print("{}: Finished.".format(finish_time))
    print("Time taken: {:.5f}s.".format((finish_time - start_time).total_seconds()))
    print("Queue Count: {:,}".format(len(q2.list)))



# Ops
if __name__ == '__main__':

    menu = input("""#######  Menu ######\n
    1. Task 1
    2. Task 2
    3. Task 3: Check Bracket Sequence
    4. Task 4
    5. Task 5
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
    else:
        print("ERR: Invalid selection.")

