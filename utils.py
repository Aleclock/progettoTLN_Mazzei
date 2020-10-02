
"""
Load document in path line by line
Input:
    path: file path
Output:
    sentences: list of sentences
"""
def loadSentences(path):
    sentences = []
    with open(path) as file:
        for line in file.readlines():
            sentences.append(line.replace("\n", ""))
    file.close()
    return sentences