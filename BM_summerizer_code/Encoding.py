import chardet  
import os  
file_size = os.path.getsize('ScholorRX_Provided.docx') 
if file_size == 0:    
    print('File is empty')
with open('ScholorRX_Provided.docx', 'rb') as f:    
    result = chardet.detect(f.read(100000))    
    print(result['encoding'])