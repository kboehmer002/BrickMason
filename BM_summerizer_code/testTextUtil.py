import textUtil
import unittest

class testTextUtil(unittest.TestCase):
    def test_findWords(self):
        self.assertEqual(textUtil.findWords('This is a test'), ['This', 'is', 'a', 'test'])
    
    def test_isRedundantSentence(self):
        self.assertEqual(textUtil.isRedundantSentence('The cat in the hat is black.', 'The cat in the hat is dark black.', 0.9), True)
        self.assertEqual(textUtil.isRedundantSentence('This is a test', 'This is a test', 0.9), True)
        self.assertNotEqual(textUtil.isRedundantSentence('This is a test', 'This is not a test', 0.9), True)
        self.assertEqual(textUtil.isRedundantSentence('This is a test', 'This is a quiz', 0.85), True)
        self.assertEqual(textUtil.isRedundantSentence('This is a test', 'This is a quiz', 0.99), False)
        self.assertEqual(textUtil.isRedundantSentence('Pam ate a potato', 'This is a quiz', 0.9), False)
        
        
    def test_returnRedundantSentences(self):
        document = "The cat in the hat is black. The cat in the hat is also furry."
        threshold = 0.8

        result = textUtil.returnRedundantSentences(document, threshold)
        expected_output = [['The cat in the hat is black.', 'The cat in the hat is also furry.']]

        
if __name__ == '__main__':
    unittest.main()
