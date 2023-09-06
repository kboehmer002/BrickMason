import argparse
import os
import docx2txt
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

#

def summarize_file(file_path, sentences_count=3):
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext == ".txt":
        with open(file_path, "r", encoding="iso-8859-1") as file:
            text = file.read()
    elif file_ext == ".docx":
        text = docx2txt.process(file_path)
    else:
        raise ValueError("Unsupported file type: {}".format(file_ext))
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences_count=sentences_count)
    return " ".join([str(sentence) for sentence in summary])


if __name__ == "__main__":

    # Get the list of file names from user input
    file_names = []
    with open("input_file_names.txt", "r") as file:
        for line in file:
            file_names.append(line.strip())

    # Get the number of sentences for the summary from user input
    sentences_count = input("Enter the number of sentences for the summary: ")
    try:
        sentences_count = int(sentences_count)
    except ValueError:
        print("Invalid input: number of sentences must be an integer")
        exit()

    # Summarize each file and print the summary to the console
    for file_name in file_names:
        try:
            summary = summarize_file(
                file_name, sentences_count=sentences_count)
            print("Summary of {}: {}".format(file_name, summary))
            print("-" * 80)  # Print a separation line
        except Exception as e:
            print("Error summarizing file {}: {}".format(file_name, str(e)))