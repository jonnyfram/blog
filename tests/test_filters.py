import os
import unittest
import datetime

#configure app to use testing config

if not "CONFIG_PATH" in os.environ:
    os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"
    
import blog #why does this return "Import Error: No module named 'blog'"
from blog.filters import *

class FilterTests(unittest.TestCase):
    def test_date_format(self):
        #party time
        date = datetime.date(1999, 12, 31)
        formatted = dateformat(date, "%y/%m/%d")
        self.assertEqual(formatted, "99/12/31")
        
    def test_date_format_none(self):
        formatted = dateformat(None, "%y/%m/%d")
        self.assertEqual(formatted, None)

if __name__ == "__main__":
    unittest.main()