import unittest
import ctypes
import tkinter
import os
user32 = ctypes.windll.user32
from brick_mason.home.modules import SourceImporter, BricksCreator, ContentAnalyzer, ContentGenerator

'''=========================== ENABLE AWS TESTS ==========================='''
enable_aws = False
'''========================================================================'''

class Source_Importer_Check_Docx_Tests(unittest.TestCase):
    test_text = ""
    text_filepath1 = os.getcwd() + r"\testfiles\testdoc1.docx"
    test_text2 = "Buffers are important for maintaining life. They keep pH conditions stable. \
Some biochemical processes can only happen in very specific reaction conditions. \
In unstable environments, chaos would occur. Proteins would denature. \
Anything could react with anything and produce all kinds of useless junk. \
The organism would die.BufferslifepH conditionsSome biochemical processesvery \
specific reaction conditionsunstable environmentschaosProteinsall kindsuseless \
junkThe organismBufferslifepH conditionsSome biochemical processesvery specific \
reaction conditionsunstable environmentschaosProteinsall kindsuseless junkThe \
organismconditionsSome biochemical processesveryspecific reaction conditionsunstable"   
    text_filepath2 = os.getcwd() + r"\testfiles\testdoc2.docx"
    test_text3 = "She gave a second example where she helped the show runners accurately \
portray a meth synthesis reaction with 30 gallons of methylamine precursor. The P2P \
method was used for synthesis. To stay true to the illegal nature of character’s \
actions, she looked up illegal syntheses and gave the show runners a list of \
reduction methods to choose from .\n\t\
They chose aluminum mercury because it was easy to say. Here Dr. Nelson noted that \
the priorities of chemists versus show creators differed she would never have chosen \
a reagent based on its ease of pronunciation.\n\n\
Synthesis Reaction\n\
A synthesis reaction occurs when two or more reactants combine to form a single \
product. This type of reaction is represented by the general equation: A + B → AB. • An \
example of a synthesis reaction is the combination of sodium(Na) and chlorine(Cl) to \
produce sodium chloride(NaCl)."
    text_filepath3 = os.getcwd() + r"/testfiles/testdoc2.docx"
    
    def test_file_opcheck(self):
        wrong_extension = "./testfiles/testdoc1.txt"
        fake_path = "./testfiles/testdoc1.docx"
        self.assertFalse(SourceImporter.opCheck(fake_path))
        self.assertFalse(SourceImporter.opCheck(wrong_extension))
    
    def test_file_opcheck(self):
        self.assertTrue(SourceImporter.opCheck(self.text_filepath1))
        self.assertTrue(SourceImporter.opCheck(self.text_filepath2))
        self.assertTrue(SourceImporter.opCheck(self.text_filepath3))
        
    def test_docx_text_extraction_emptyfile(self):
        text_rtn = SourceImporter.extract_from_docx(self.text_filepath1)
        self.assertEqual(self.test_text, text_rtn)
    
    def test_docx_text_extraction_regular_para(self):
        text_rtn = SourceImporter.extract_from_docx(self.text_filepath1)
        self.assertEqual(self.test_text, text_rtn)
    
    def test_docx_text_extraction_fancydoc(self):
        text_rtn = SourceImporter.extract_from_docx(self.text_filepath1)
        self.assertEqual(self.test_text, text_rtn)

    # Checks word count for empty file containing no words.
    def test_docx_word_count_empty(self):
        self.assertEquals(
            0, SourceImporter.get_text_word_count(self.text_filepath1))
    
    # Checks word count for file containing a few paragraphs.
    def test_docx_word_count(self):
        self.assertEquals(
            71, SourceImporter.get_text_word_count(self.text_filepath2))
    
    # Checks word count for document containing words of disparate formats     
    def test_docx_word_count_fancy(self):
        self.assertEquals(
            146, SourceImporter.get_text_word_count(self.text_filepath3))

    # Check selectFiles cancel button
    #@patch('yourmodule.selectFiles', return_value='cancel')
    def test_select_file_cancel(self):
        tkinter.messagebox.showinfo(title='Required Test Action',
                                    message='A file dialog window will open. To perform this test, you will select cancel')
        file_list = SourceImporter.selectFiles()
        self.assertEquals('', file_list)
        
    # Check selectFiles select testdoc1
    def test_select_file_single(self):
        tkinter.messagebox.showinfo(
            title='Required Test Action',
            message='A file dialog window will open. \
To perform this test, you will select the file at ' + r'.\testfiles\testdoc1.docx')
        file_list = SourceImporter.selectFiles()
        self.assertEquals(self.text_filepath1, file_list)

    # Check selectFiles select testdoc1
    def test_select_file_single(self):
        tkinter.messagebox.showinfo(
            title='Required Test Action',
            message='A file dialog window will open. To perform this test, \
you will select the files testdoc1.docx and testdoc2.docx at' + r'.\testfiles')
        file_list = SourceImporter.selectFiles()
        self.assertEquals(self.text_filepath1, file_list)

    # Check selectFiles select testdoc1 and testdoc2
    def test_select_file_single(self):
        store = (self.text_filepath1, self.text_filepath2)
        tkinter.messagebox.showinfo(
            title='Required Test Action',
            message='A file dialog window will open. To perform this test, \
you will select the files testdoc1.docx and testdoc2.docx at' + r'.\testfiles')
        file_list = SourceImporter.selectFiles()
        self.assertEquals(store, file_list)

    # Check selectFiles select testdoc1 and testdoc2
    def test_select_file_single(self):

        SourceImporter.addSourceFile()

'''       
SourceImporter.duplicate_file_exists(t) #RDS/S3
SourceImporter.addSourceFile() #RDS/S3
SourceImporter.set_ktops(file, ktop_list) # RDS/S3
SourceImporter.get_ktops_by_file(file) # RDS/S3
SourceImporter.set_word_count(file, word_count) # RDS/S3
SourceImporter.set_image_tags(image)  # RDS/S3
SourceImporter.getObjectList(image, bucket)  # RDS/S3/Rekognition
SourceImporter.get_text_key_phrases(rtnd_text) # Comprehend
SourceImporter.get_text_syntax(rtnd_text) # Comprehend
SourceImporter.text_analysis(file) # Comprehend
SourceImporter.preprocess() # Comprehend/RDS/S3/Rekognition
'''

class Content_Analyzer_Check_Docx_Tests(unittest.TestCase):
        
    def test_query_Source_Files(self):
        rtn_query = ContentAnalyzer.query_SourceFiles(exts, sDate, eDate)
        num_query = rtn_query.count()
        self.assertEquals(0, num_query)


# ==== Sample Tests ====

# functions generated for testing
def getStr1():
    return "Hello World"
def getStr2():
    return "Hello World?"
def getNum():
    return 3
def tbool(x):
    if x == 0:
        return True
    else:
        return False

class Sample_Testing(unittest.TestCase):

    def test_text_Hello_World(self):
        self.assertEqual(getStr1(), 'Hello World')

    def test_mismatched_text_Hello_World(self):
        self.assertFalse(getStr2() == 'Hello World', "Test Value Not False")

    def test_bool(self):
        self.assertTrue(tbool(0))

    def test_bool2(self):
        self.assertFalse(tbool(1))

class Sample_Testing2(unittest.TestCase):
    def test_num_equal(self):
        self.assertEqual(3, getNum())

    def test_num_not_equal(self):
        self.assertNotEqual(2, getNum())
# ==== End Sample Tests ====


#if __name__ == '__main__':
#    unittest.main()
