import argparse

parser = argparse.ArgumentParser()
parser.add_argument("cypher", help="incoming cypher massage")
args = parser.parse_args()

decyphered: str = ""
for word in args.cypher.split(): decyphered += word[0]
print(decyphered)