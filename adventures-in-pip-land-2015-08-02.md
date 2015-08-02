## Adventures in pip land

Slides at https://github.com/rbtcollins/reveal.js

<small>Robert Collins  
rbtcollins@hp.com  
@rbtcollins (Twitter)</small>



## Take this positively

Humourous talk.

I respect all the folk that have built up pip and the packaging ecosystem.

It took a decade to get here.



## pyinstall


## Part of pyinstaller


## Split out in 2008: 7 years ago

```
commit 97c152c463713bdaa0c1531a910eeae681035489
Author: Ian Bicking <ianb@colorstudy.com>
Date:   Wed Oct 15 17:24:00 2008 -0500

    [svn r20975] Rename occurrance of pyinstall to pip
```


## > 4000 commits


## 70% of downloads from PyPI
https://caremad.io/2015/04/a-year-of-pypi-downloads/

=> 24M downloads a week using pip

![PyPI clients](adventures-in-pip-land/stacked-installer-pct.png)


## YOU ARE RUNNING MY CODE
Note:
be afraid


## pip is a moving target
* 7.1.0 &nbsp; 2015-06-30
* 7.0.0 &nbsp; 2015-05-21
* 6.1.0 &nbsp; 2015-04-07
* 6.0.0 &nbsp; 2014-12-22
* 1.5.6 &nbsp; 2014-05-16
* 1.5.0 &nbsp; 2014-01-02
* 1.4.1 &nbsp; 2013-08-07
* 1.4.0 &nbsp; 2013-07-23


## People upgrade slowly
![PyPI pip breakdown](adventures-in-pip-land/stacked-pip-ver-pct.png)


## Installs from
* directories
* VCSs
* Wheels
* SDists

* NOT bdist_eggs etc


## Installs into
* system
* user
* isolated directories
* virtual environments
* as eggs[*]
Note:
Deprecated, oh so deprecated


## Installs itself


## Runs under
* Python 2.6, 2.7
* Python 3.2, 3.3, 3.4, 3.5, 3.6
* pypy
* Jython(ish)
* IronPython



## pip uninstall

1. Lookup name in local DB <!-- .element: class="fragment" -->
2. Read DB of installed files <!-- .element: class="fragment" -->
3. Delete <!-- .element: class="fragment" -->


## Horror #1


## Overlaid environments

* --system-side-packages
* --user


## Horror #2


## develop mode

* python setup.py develop
* pip install -e
* easy_install.pth <!-- .element: class="fragment" -->

Note:
Try this:
make a virtualenv
pip install .
pip install -e .
pip uninstall mock
pip uninstall mock
Locking


## Horror #3


## 6 different DBs

* flat egg-info
* namespaced egg-info
* distutils 'egg'
* egg
* develop eggs
* dist-info

Note:
And when someone proposes a new format...


![Angry Dad](adventures-in-pip-land/Picture_2_c.jpg)



## pip install

1. Find the package to install <!-- .element: class="fragment" -->
2. Find its dependencies <!-- .element: class="fragment" -->
3. Repeat recursively <!-- .element: class="fragment" -->
4. Install <!-- .element: class="fragment" -->



## Finding

* Name <!-- .element: class="fragment" -->
* Find links <!-- .element: class="fragment" -->

Note:
PEP 426 describes a replacement that allows the same functionality, no better...


## Horror #4


* Name
* Find links
* Direct references

pip @ file:///localbuilds/pip-1.3.1.zip


## Horror #5


Pip does not resolve versions
Note:
It FINDS versions


1. URLs
2. Find links and indices
   https://pypi.python.org/simple/NAME
3. Already installed
4. Choose between them


## Sidebar

Working resolver

https://github.com/pypa/pip/issues/988

https://github.com/rbtcollins/pip/tree/issue-988



## Dependencies


## Query the index?


## Wheels

* Download
* Unpack
* Examine the metadata file


## Everything else

* Download
* Unpack
* Run ```setup.py egg_info```
* Look in the metadata file egg_info creates


## Horror #6


PasteScript

```
egg_info.writers = paste.script.epdesc:EggInfoWriters
```

See pip/req/req_install.py

```
__file__ = __SETUP_PY__
from setuptools.command import egg_info
....
egg_info.egg_info.run = replacement_run
exec(compile(
    getattr(tokenize, 'open', open)
    (__file__).read().replace('\\r\\n', '\\n'),
    __file__,
    'exec'
))
```

Note:
PasteScript has its own entry point
But its not installed yet... and neither are its dependencies.


## Horror #7


Two words


## Easy Install


```
setup(
  ...
  setup_requires=["py2app"],
  )
```


## Issues

* no pip cache (wheel and http)
* no pip http proxy configuration
* no pip find-links configuration
* build numpy etc twice


## Declarative dependencies

* Coming soon(tm)
* Static machine readable in setup.cfg
* Fallback to procedural generation



## Recurse


## See under recursion


## Recurse


## See under recursion



## Install

1. Order by dependencies
2. Build wheels
3. Install in order


## Horror #8


## Setuptools


## Distribute?

https://pythonhosted.org/setuptools/merge.html

Note:
setuptools 0.6 forked as distribute.
then distribute merged back as 0.7.
Last setuptools before that was 0.6c12


Setuptools 0.6.36 ... is distribute

Distribute 0.7.3 ... gets you setuptools


```
from setuptools import setup
```


## details
```
distribute-0.6.49$ ls
CHANGES (links).txt
...
distribute.egg-info
setuptools
```


## Support removed in 7.0.0

```
rmadison python-setuptools
 python-setuptools | 0.6.24-1ubuntu1 | precise        | all
```


```
$ mkvirtualenv test
$ pip install -U pip
$ pip install -U setuptools
$ pip list
distribute (0.6.24)
pip (7.1.0)
setuptools (18.0.1)
```


Forks, the gift that keeps on giving


PR 2767

3 different cross checks for distribute<->setuptools

Changes to setuptools or distribute pulled to front of the list
Note:
otherwise, we would uninstall distribute, and boom


## Ordering #2

* Cycles A->B->A
* User order
Note:
Thats right: we let users tell us the order to install packages to workaround
bugs in metadata/build scripts. 78000 packages on PyPI



## Wheel building

```
try:
  setup.py bdist_wheel
except:
  pass
else:
  add_to_cache
```



## Installation

* Unpack wheels
* Otherwise run setup.py install


## Horror #9


```
"""import setuptools, tokenize;__file__=%r;
exec(compile(
  getattr(tokenize, 'open', open)
      (__file__).read().replace(
          '\\r\\n', '\\n'),
  __file__, 'exec'))""" % self.setup_py
```


* Record files
* Egg vs single-version-externally-managed



## Questions?

* Robert Collins
* @rbtcollins
* lifeless on freenode
* rbtcollins@hp.com
