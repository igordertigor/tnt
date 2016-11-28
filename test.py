import os
import tempfile
import shutil
import stat
import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import setup


def remove_nvidia_smi_from_path(target_path):
    return ':'.join([directory for directory in target_path.split(':')
                     if os.path.exists(directory) and
                     'nvidia-smi' not in os.listdir(directory)])


class TestHasGPU(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp(prefix='tnt-test-')
        filename = os.path.join(self.tempdir, 'nvidia-smi')
        with open(filename, 'w') as fp:
            fp.write('mock nvidia-smi')
        new_mode = stat.S_IXUSR ^ stat.S_IRUSR ^ stat.S_IWUSR
        os.chmod(filename, new_mode)
        self.old_path = os.environ['PATH']

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        os.environ['PATH'] = self.old_path

    def test_has_gpu_succeeds(self):
        os.environ['PATH'] += ':{}'.format(self.tempdir)
        self.assertTrue(setup.hasgpu())

    def test_has_gpu_fails(self):
        os.environ['PATH'] = remove_nvidia_smi_from_path(os.environ['PATH'])
        self.assertFalse(setup.hasgpu())


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


class TestWheeltags(unittest.TestCase):

    def test_mac_27(self):
        wheeltags = setup.create_wheeltags('mac', (2, 7))
        self.assertEqual(wheeltags, 'py2-none-any')

    def test_mac_34(self):
        wheeltags = setup.create_wheeltags('mac', (3, 4))
        self.assertEqual(wheeltags, 'py3-none-any')

    def test_mac_35(self):
        wheeltags = setup.create_wheeltags('mac', (3, 5))
        self.assertEqual(wheeltags, 'py3-none-any')

    def test_linux_27(self):
        wheeltags = setup.create_wheeltags('linux', (2, 7))
        self.assertEqual(wheeltags, 'cp27-none-linux_x86_64')

    def test_linux_34(self):
        wheeltags = setup.create_wheeltags('linux', (3, 4))
        self.assertEqual(wheeltags, 'cp34-cp34m-linux_x86_64')

    def test_linux_35(self):
        wheeltags = setup.create_wheeltags('linux', (3, 5))
        self.assertEqual(wheeltags, 'cp35-cp35m-linux_x86_64')


class TestBuildURL(unittest.TestCase):

    @mock.patch("setup.create_wheeltags")
    def test_build_url_assembles_correctly(self, wheeltags_mock):
        wheeltags_mock.return_value = 'ANY_WHEELTAGS'
        expected = ("https://storage.googleapis.com/tensorflow/"
                    "ANY_PLATFORM_NAME/ANY_PROCESSING_UNIT/"
                    "tensorflow-ANY_TF_VERSION-ANY_WHEELTAGS.whl")
        result = setup.build_url(
            "ANY_TF_VERSION",
            "ANY_PYTHON_VERSION",
            "ANY_PROCESSING_UNIT",
            "ANY_PLATFORM_NAME",
        )
        self.assertEqual(result, expected)
        wheeltags_mock.assert_called_once_with("ANY_PLATFORM_NAME",
                                               "ANY_PYTHON_VERSION")
