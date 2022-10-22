import util
s = util.Stack()

# Postfix notation: operation goes after the operands
# Instead of 1 + 2 we write 1 2 +
# Instead of 1 + (2 + 3) we write 1 2 3 + +
# Instead of (1 + 2) + 3 we write 1 2 + 3 +
# Instead of (2 * 3) + 4 we write 2 3 * 4 +

expr = input("Enter expression: ")

tokens = expr.split()

def isNumber(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

# Scan the tokens from left to right
# If a token is a number, then push it into the stack
# If a token is an operation ('+' or '*'), then pop its operands,
# compute the result, and push it onto the stack


for token in tokens:
    if isNumber(token) :
        s.push(int(token))
    elif token == '+':
        x = s.pop()
        y = s.pop()
        s.push(x + y)
    elif token == '*':
        x = s.pop()
        y = s.pop()
        s.push(x * y)

print(s.pop())

