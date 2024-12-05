import python_learnable_webcrawler as crawler
import unittest



class TestGettingLinks(unittest.TestCase):

    def testConnectingUrls(self):
        crawler.get_connecting_and_current("uci.edu")
        self.assertTrue(True)

    def testsimilarity(self): 
        document = "this is a set of words and a keyword: pasta"
        keywords = "pasta"
        print(crawler.similarity(keywords, document))
        self.assertTrue(True)

    




if __name__ == "__main__":
    unittest.main()