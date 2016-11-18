import sys
import os
from distutils.core import setup


class UnsupportedPlatformException(Exception):
    pass


def install_tensorflow():
    # are we python3 or python2
    # do we have a cpu
    # mac or linux
    pass


def pythonversion():
    return sys.version[:2]


def hasgpu():
    return not os.system('which nvidia-smi')


def platform():
    platform_name = sys.platform
    if platform_name.startswith('linux'):
        return 'linux'
    elif platform_name.startswith('darwin'):
        return 'mac'
    else:
        raise UnsupportedPlatformException(
            'Only linux and mac are supported, but you are on "{}"'
            .format(platform_name))


def create_fuzzyness(platform_name, python_version):
    if platform_name == 'mac':
        return 'py{}-none-any'.format(python_version[0])
    elif platform_name == 'linux':
        cpstring = '{}{}'.format(*python_version)
        if cpstring == '27':
            return 'cp27-none-linux_x86_64'
        else:
            return 'cp{}-cp{}m-linux_x86_64'.format(cpstring, cpstring)


def build_url(tf_version, python_version, processing_unit, platform_name):
    kwargs = {
        'platform_name': platform_name,
        'processing_unit': processing_unit,
        'tf_version': tf_version,
        'kladderadatsch': create_fuzzyness
    }
    return ('https://storage.googleapis.com/tensorflow/'
            '{platform_name}/{processing_unit}/'
            'tensorflow-{tf_version}-{kladderadatsch}.whl'
            .format(**kwargs))


if __name__ == '__main__':
    install_tensorflow()

    setup(
        name='tnt',
        version='0.0.0',
    )
