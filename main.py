from utils import *
import os

os.chdir("/Users/aleclock/Desktop/uni/TLN/mazzei/progettoTLN_Mazzei")

def main():
    sentences = loadSentences("./resources/sentences.txt")
    for s in sentences:
        print (s)

main()