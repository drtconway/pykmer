import pykmer.file as file

import os
import os.path

def test_autoremove_0():
    nm = file.tmpfile('wibble')
    assert not os.path.isfile(nm)

def test_autoremove_1():
    nm = file.tmpfile('wibble')
    with open(nm, 'w') as f:
        print >> f, 'hello world'
    assert os.path.isfile(nm)
    os.remove(nm)

def test_autoremove_2():
    with file.autoremove():
        nm = file.tmpfile()
        with open(nm, 'w') as f:
            print >> f, 'hello world'
        assert os.path.isfile(nm)
    assert not os.path.isfile(nm)

def test_autoremove_3():
    with file.autoremove():
        nm = file.tmpfile()
        with open(nm, 'w') as f:
            print >> f, 'hello world'
        assert os.path.isfile(nm)
        os.remove(nm)
        assert not os.path.isfile(nm)
    assert not os.path.isfile(nm)

def test_autoremove_3():
    try:
        with file.autoremove():
            nm = file.tmpfile()
            with open(nm, 'w') as f:
                print >> f, 'hello world'
            assert os.path.isfile(nm)
            raise StopIteration
        assert False
    except StopIteration:
        pass
    assert not os.path.isfile(nm)

