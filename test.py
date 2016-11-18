import unittest
import unittest.mock as mock

import setup


class TestPlatform(unittest.TestCase):

    @mock.patch('sys.platform', 'linux2')
    def test_linux_detected_correctly(self):
        self.assertEqual(setup.platform(), 'linux')

    @mock.patch('sys.platform', 'darwin')
    def test_darwin_dected_correctly(self):
        self.assertEqual(setup.platform(), 'mac')

    @mock.patch('sys.platform', 'windows')
    def test_unsupported_platform_exception_raised_on_windows(self):
        self.assertRaises(setup.UnsupportedPlatformException, setup.platform)
