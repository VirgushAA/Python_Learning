str_counter: int = 0
answer: bool = True
conditions: bool = True
s: str
while str_counter < 3:
    try:
        s = input()
        if len(s) != 5:
            conditions = False
            str_counter = 3
        else:
            if str_counter == 0:
                if (s[0] != '*' or s[4] != '*') or (s[1] == '*' or s[2] == '*' or s[3] == '*'):
                    answer = False
            elif str_counter == 1:
                if (s[0] != '*' or s[1] != '*' or s[3] != '*' or s[4] != '*') or s[2] == '*':
                    answer = False
            elif str_counter == 2:
                if (s[0] != '*' or s[2] != '*' or s[4] != '*') or (s[1] == '*' or s[3] == '*'):
                    answer = False
            str_counter += 1
    except EOFError: 
        conditions = False
        str_counter = 3
        
if conditions:
    try:
        s = input()
        conditions = False
    except EOFError: conditions = conditions
    
if conditions: print(answer)
else: print("Error")