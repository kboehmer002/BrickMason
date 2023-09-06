import boto3


# Read the text from the file (buffers.txt in this case)
'''
with open("./BM_simplePrograms/TextFilePrograms/buffers.txt", "r") as buffers:
    buffers = buffers.read()

print(buffers)
print(type(buffers))
'''
# -------------------------------------------------------------------------
    
'''Passes in a set or list of strings. Returns list of dictionaries with string index and list of associated keywords for each string.'''

def batchDetectKeyPhrases(textStrings):
    
    # boto3 client
    comprehend = boto3.client('comprehend')
    
    # create a list to store each strings kps dictionaries 
    kpsDictionaries = []
    
    # iterates over each string and keeps track of index 
    i = 0
    for string in textStrings:
        
        # Detect key phrases with Comprehend, which will return a dictionary that contains key phrases
        compKP_result = comprehend.detect_key_phrases(Text=string, LanguageCode='en')
        
        # Extract the key phrases. Uses list comprehension syntax [expression for item in iterable if condition]
        keyPhrases = [keyPhrase['Text'] for keyPhrase in compKP_result['KeyPhrases']]
        
        # Create dictionary to store index number of each string and ass. keyPhrases
        index_and_kps = {'index': i, 'key_phrases': keyPhrases}
        
        # Add dictionary for each string to the list of dictionaries for all strings
        kpsDictionaries.append(index_and_kps)
        
        # increment the index
        i += 1
        
    return kpsDictionaries
    
# -----------------------------------------------------------------------------------------------------

'''Given a string of text, returns a set of key phrases, using comprehend'''
def getKeyPhrases(text):
    comprehend = boto3.client('comprehend')
    keyPhrases = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
    keyPhraseSet = set()
    for phrase in keyPhrases['KeyPhrases']:
        keyPhraseSet.add(phrase['Text'])
    return keyPhraseSet

#------------------------------------------------------------------------------------------------------------------

'''Function to compare two sets of word (use to compare user query to AWS generated keywords) - returns set of matching words'''
def searchForKeyPhraseMatch(userQueryWordSet, documentKeyWordSet):
    keyWordMatches = userQueryWordSet.intersection(documentKeyWordSet)
    return keyWordMatches

#----------------------------------------------------------------------------------------------------------------

'''Returns the percent of query words found within the doc's keywords'''
def findPercentMatch(userQueryWordSet, documentKeyWordSet):
    keyWordMatches = searchForKeyPhraseMatch(userQueryWordSet, documentKeyWordSet)
    kWM_length = len(keyWordMatches)
    uQWS_length= len(userQueryWordSet)
    percentMatch = (kWM_length/uQWS_length)*100
    return percentMatch



# ----------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------

'''
# Do stuff with the set - make some more functions later
key_phrases = getKeyPhrases(buffers)
print(key_phrases)
'''

#--------------------------------------------------------------------------------------------------------------------

# Test searchForKeyPhraseMatch and findPercentMatch
if __name__ == '__main__':
    set1 = {'cat', 'dog', 'bird'}
    set2 = {'dolphin', 'steak', 'cat', 'dog'}
    matches = searchForKeyPhraseMatch(set1, set2)
    print(matches)
    percentMatch = findPercentMatch(set1, set2)
    print(percentMatch)

    