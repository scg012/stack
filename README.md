# Stack

Fifth is a new stack-based language. A stack is a data structure which can only have elements added to the top.
Fifth stores a stack of integers and supports commands to manipulate that stack.
Operations always apply to the top of the stack.

Fifth supports the following arithmetic operators:

`+`, `-`, `*`, `/`
      which act upon the top of the stack.

Fifth also supports arithmetic operators that act upon the bottom of the stack, i.e. in the reverse manner:
* `r+`
* `r-`
* `r*`
* `r/`


Fifth also supports the following commands:

* `PUSH x` - push x onto the top of the stack, where x is a valid integer
* `POP` - remove the top element of the stack
* `SWAP` - swap the top two elements of the stack
* `DUP` - duplicate the top element of the stack

Fifth also supports arithmetic operators that act upon the bottom of the stack, i.e. in the reverse manner:
* `rPUSH x` - push x onto the bottom of the stack, where x is a valid integer
* `rPOP` - remove the bottom element of the stack
* `rSWAP` - swap the bottom two elements of the stack
* `rDUP` - duplicate bottom top element of the stack

Stack is a python program which works as a fifth interpreter. Each line of input to the program
represents a single fifth command.  The result of each command is output to the terminal.

Example:
```
stack is []
PUSH 3
stack is [3]
PUSH 11
stack is [3, 11]
+
stack is [14]
DUP
stack is [14, 14]
PUSH 2
stack is [14, 14, 2]
*
stack is [14, 28]
SWAP
stack is [28, 14]
/
stack is [2]
+
ERROR

rPUSH 11
stack is [11, 3]

rPUSH 5
stack is [5, 11, 3]


```

## Requirements:
Minimum Python version is `3.10`.


##Run Tests:
```commandline
export PYTHONPATH=$PYTHONPATH:src
pytest tests
```
Code coverage results will be in `./htmlcov/index.html`.

# Run Program
From the base directory:

Option 1:
```commandline
python3 ./
```

Option 2:
```commandline
cd src
python3 ./
```

Option 3:
```commandline
cd src
python3 stack.py
```

Option 3:
```commandline
cd src
chmod +x stack.py
./stack.py
```

## To Exit the Program:
Enter an empty new line / carriage return.