### Workshop 1 - Data Structures in Python
import sys
sys.path.append('../../../')
from utils import util


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
    pass


# Ops
if __name__ == '__main__':

    menu = input("Menu:\n1. Task 1\n2. Task 2\n3. Task 3: Check Bracket Sequence\n$ ").strip()

    if menu == '1':
        task1()
    elif menu == '2':
        task2()
    elif menu == '3':
        br_seq = input("Enter bracket sequence:\n$ ")
        print(check_bracket_sequence(br_seq))
    else:
        print("Invalid selection.")

