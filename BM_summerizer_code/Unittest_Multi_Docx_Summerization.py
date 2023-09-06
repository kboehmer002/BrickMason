import unittest
from unittest.mock import patch, mock_open
from Multi_Docx_Summerization import summarize_file


class TestSummarizeFile(unittest.TestCase):
    def test_summarize_txt_file(self):
        m = mock_open(read_data="This is a test text file.")
        with patch("builtins.open", m):
            summary = summarize_file("test.txt", sentences_count=2)
        self.assertEqual(summary, "This is a test text file.")

    def test_summarize_docx_file(self):
        with patch("Multi_Docx_Summerization.docx2txt.process") as mock_process:
            mock_process.return_value = "This is a test docx file."
            summary = summarize_file("test.docx", sentences_count=2)
        self.assertEqual(summary, "This is a test docx file.")

    def test_unsupported_file_type(self):
        with self.assertRaises(ValueError):
            summarize_file("test.pdf", sentences_count=2)


if __name__ == "__main__":
    unittest.main()