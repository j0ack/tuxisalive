import unittest
import os

import filesCache

class testFilesCache(unittest.TestCase):
    """A test class for filesCache module.
    """

    def setUp(self):
        """Create objects
        """
        self.cfContainer = filesCache.CachedFilesContainer("cache_unittest")

    def test00TempDirCache(self):
        """Test the presence of the temp directory of the cache.
        """
        cacheDir = self.cfContainer.getCacheDir()
        self.assertNotEqual(cacheDir, "")
        self.assertTrue(os.path.isdir(cacheDir))

    def test01CreateFileCacheFromDisk(self):
        """Test the creation of a cached file from the hard drive.
        """
        # Create cached file with existing file
        fc = self.cfContainer.createFileCache(__file__)
        # fc object must be != than None
        self.assertNotEqual(fc, None)
        # md5Tag must exists
        self.assertNotEqual(fc.getMd5Tag(), "")
        # Output filename must exists
        self.assertTrue(os.path.isfile(fc.getOutputFilePath()))
        # Destroy the cached file
        fc.destroy()
        # Create cached file with unexisting file
        fc = self.cfContainer.createFileCache("c:\\inconnu.bidule")
        # fc object must be == None
        self.assertEqual(fc, None)

    def test02CreateFileCacheFromURL(self):
        """Test the creation of a cached file from an url.
        """
        # Create cached file with existing url
        fc = self.cfContainer.createFileCache("http://www.kysoh.com/download/test.html")
        # fc object must be != than None
        self.assertNotEqual(fc, None)
        # md5Tag must exists
        self.assertNotEqual(fc.getMd5Tag(), "")
        # Output filename must exists
        self.assertTrue(os.path.isfile(fc.getOutputFilePath()))

    def test03DestroyContainer(self):
        """Test the destroying of the cached files container.
        """
        cacheDir = self.cfContainer.getCacheDir()
        # Destroy the container
        self.cfContainer.destroy()
        # Temp dir cache must not exists
        self.assertFalse(os.path.isdir(cacheDir))



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testFilesCache))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

