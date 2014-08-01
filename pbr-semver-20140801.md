## pbr and semver

aka Python Build Reasonableness and Semantic Versioning

<small>Robert Collins  
rbtcollins@hp.com  
@rbtcollins (Twitter)</small>



## Setuptools

Note:
"Anthony baxter" - Very clever code written by very clever people


## OpenStack
* Dozens of projects <!-- .element: class="fragment" -->
* Identical infrastructure code <!-- .element: class="fragment" -->
* Maintenance nightmare <!-- .element: class="fragment" -->

Note: Lots of simple code in a complex environment...


## Refactor

* New project <!-- .element: class="fragment" -->
* Setuptools plugin <!-- .element: class="fragment" -->
* Used by all OpenStack projects <!-- .element: class="fragment" -->

Note: 
What do we do to fix DRY problems? We add an abstraction. What problem cannot be solved by adding abstractions?



## PBR
Consistent setuptools integration glue for all OpenStack projects.

Depends on git and a recent pip for installation support.


## Testing

* testr
```
python setup.py test
```

Note:
testr integration, driven through tox


## git integration
Hard requirement but....
* automatically picks up all versioned files
* scans history for changelog and authors file contents


## PyPI integration

Generates a rich summary from README.rst + changelog


## Documentation

Sphinx API glue, and Sphinx manpage output.


## PIP

Pulls requirements from requirements*.txt

Note: This is another DRY situation


## Versioning

Generates pre-release version numbers for you from tags and or config settings

Note:
blank.. lets talk about consistency a little. You know, that thing where you do the same thing.. openstack and API servers (2012.1) vs clients (1.2.3).



## Semantic versioning
[semver](http://semver.org) is a simple and clear set of rules for versioning
software to clearly indicate compatibility interactions.
Note:
Which we adopted. And then realised it didn't quite work. So we changed it :).


## [openstack-semver](http://docs.openstack.org/developer/pbr/semver.html)
"This is a fork of Semantic Versioning 2.0. The specific changes have to do with the format of pre-release and build labels, specifically to make them not confusing when co-existing with Linux Distribution packaging. Inspiration for the format of the pre-release and build labels came from Python's PEP440."



## Issues


## dev builds
* 1.3.2 tagged
* 5 local commits <!-- .element: class="fragment" -->
* 1.3.2.5.g$sha <!-- .element: class="fragment" -->

Note:
1.3.2 tagged, 1.3.2.N.g$sha - counts as a full release


## PEP-440
Developers don't know PEP-440:

* tag 1.3.2.a2 <!-- .element: class="fragment" -->
* should be 1.3.2.0a2 <!-- .element: class="fragment" -->
Note:
1.3.2.a2
-> 1.3.2.0a2


## CD
1.3.2.0a1 cannot be sorted vs 1.3.2.dev5
Note:
Folk pulling trunk want monotonic versions but dev versions have no precedence vs alpha/beta/rc in semver


## Binary Packaging
Turns out everyone reinvents the same integration and version translation glue... differently.
Note:
mention Debian vs Ubuntu, Redhat vs third parties... touch on sort-before


## Sort-before
1.3.2.0a1 sorts before 1.3.2 - versions are special. dpkg has ~ rpm has nothing



## [pbr-semver](https://git.openstack.org/cgit/openstack/oslo-specs/tree/specs/juno/pbr-semver.rst)
* new <!-- .element: class="fragment" -->
* shiny <!-- .element: class="fragment" -->
* magic <!-- .element: class="fragment" -->



## Strict PEP-440 mode
Enforce PEP-440 compatible version numbers


Epic fail on existing versions


Have to parse every version we ever accepted:
```
1.2b1
1.2.b1
1.2.3.4.g123
```



## History scanning
Scan git history for pseudo headers and calculate new release versions


Before: pbr-0.10.1.dev5.gaada1d1


```
Look for and process sem-ver pseudo headers in git

At the moment careful changelog review is needed by humands to
determine the next version number. Semantic versioning means that all
we need to know to get a reasonable default next version (and a lower
bound on the next version) is a record of bugfix/deprecation/feature
work and api-breaking commits. In this patch we start scanning for
such headers from the git history to remove this burden from
developers/project release managers. Higher versions can of course
be used either via pre-versioning or by tagging the desired version.

implements: blueprint pbr-semver
sem-ver: feature
Change-Id: Id5e8cd723d5186d1bd8c01599eae8933e6f7ea6d
```


After: pbr-0.11.0.dev5.gaada1d1


```
sem-ver: feature
sem-ver: api-break
sem-ver: deprecation
sem-ver: bugfix
sem-ver: bugfix, api-break
```
Note:
no line == sem-ver:bugfix



## Doing releases
Wrap git tag to make releases trivial
```
python setup.py tag-release
```



## Doing binary (distro) builds
Provide helpers to generate dpkg and RPM versions from a semver version
```
setup.py deb-version
1.2.0~0b1
setup.py rpm-version
1.1.9999.1
```



## Exporting versions as version_info tuples
```
import pbr.version
...
version_info = pbr.version.Version('MYPACKAGENAME').version_info()

```



## Allow disabling pre-release versions for CD folk
```
python setup.py sdist
...
1.3.2.0a1
python setup.py sdist
1.3.2.dev34.g$sha
```



## Getting started with PBR


## setup.py
```
#!/usr/bin/env python

import setuptools
setuptools.setup(
    setup_requires=['pbr'],
    pbr=True)
```


## setup.cfg
```
[metadata]
name = os-apply-config
author = OpenStack
author-email = openstack-dev@lists.openstack.org
summary = Config files from cloud metadata
description-file = 
        README.rst
home-page = http://git.openstack.org/cgit/openstack/os-apply-config
classifier = 
        Development Status :: 4 - Beta
....
        Programming Language :: Python

[files]
packages = 
        os_apply_config

[entry_points]
console_scripts =
        os-apply-config = os_apply_config.apply_config:main
```



## Questions?

* Robert Collins
* @rbtcollins
* lifeless on freenode
* rbtcollins@hp.com
