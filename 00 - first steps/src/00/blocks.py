import argparse

parser = argparse.ArgumentParser()
parser.add_argument("times", help="ammount of iterations programm will do")
args = parser.parse_args()

iterations: int = int(args.times)
s: str
while (iterations):
    s = input()
    if (s.startswith("00000") and not s[5] == '0' and len(s) == 32):
        print(s)
    iterations -= 1