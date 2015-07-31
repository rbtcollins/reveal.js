## Reliable testing with pip constraints

aka repeatable builds made better

<small>Robert Collins  
rbtcollins@hp.com  
@rbtcollins (Twitter)</small>



## The problem


## Testing your code

Note:
what do you do after you test it? You deploy it... and you want to know that
that will work.


## Deploying your code...

* Linux  <!-- .element: class="fragment" -->
* Docker <!-- .element: class="fragment" -->
* Pip <!-- .element: class="fragment" -->
* Updates break things <!-- .element: class="fragment" -->

Note:
Linux - ancient; docker - just distro, no better; pip - latest but... its the latest


## Other projects

* Loose coupling
* Mistakes
* Major versions



## Existing solutions


### Be an island

Don't use other projects at all


### Build distro packages
Note:
Not very useful: high friction, parallel toolchain.


### Manual mirrors
Note:
Fragile: need to gate changes, no guarantee that what comes in is backwards comaptible.


### Tight bounds
```
lxml>=3.4,<3.4
lxmlproc<=0.2
```
Note:
Bad: your releases are now transitively controlling common plumbing but
when one server releases, its now incompatible with your other.


### Vendoring

all your dependencies in e.g. my_tree/_vendor/
Note:
Breaks exactly the same when you have multiple projects.
Also gosh - don't even think about the impact when you pass objects from
vendors libraries to standalone ones.


### Requirements files


```
lxml==3.4.0
lxmlproc==0.2
```
Note:
Pins the dependencies precisely. Doesn't depend on mirror fragility.
But installs the world every time: describes DEPLOYMENT.


### Buildout

**easy_install**

Note:
Same issue with multiple projects



## The new shiny


### Constraints files


```
lxml==3.4.0
lxmlproc==0.2
```


```
pip install -c my-constraints.txt my-project
```

Note: Describes a consistent universe of packages.



## When to use it


### All the time


### More usefully
* You have multiple projects  <!-- .element: class="fragment" -->
* You have some optional dependencies  <!-- .element: class="fragment" -->



## When to use something else
* Single project  <!-- .element: class="fragment" -->
* Fixed set of dependencies  <!-- .element: class="fragment" -->
* Special cases <!-- .element: class="fragment" -->


**Your project is not a special case**


**(Unless your name is Donald Stufft, or Jason R. Coombs)**



## Caveats


### Use pip-compile
Note:
At least until pip's recursive resolver is landed


### Put pip-compile in cron
Note:
Because you do want to keep up to date with security fixes etc


### Mixed Python versions
Could use generate-constraints from https://git.openstack.org/openstack/requirements


### Loosen your dependencies

Record known-bad, not presumed-broken.
Note:
Otherwise you'll wedge yourself during releases


### Unlisted/unknown deps
* Unconstrained
* Can install any version



## Internals


### History
Pip has a lot of legacy and corner case code
Note: come see my talk on sunday morning!


### Constraints inject requirements


### But don't schedule them to install



## OpenStack


### devstack
```
export USE_CONSTRAINTS=True
```
Note:
will Just Work.


### tox
```
[tox]
minversion = 1.8
...
[testenv]
install_command =
	constraints: pip install -U --force-reinstall \
	             -c{env:UPPER_CONSTRAINTS_FILE:\
		     {toxinidir}/upper-constraints.txt}\
		     {opts} {packages}
	pip install -U --force-reinstall {opts} {packages}
```


```tox -e py27-constraints```


### constraints checked out separately
http://git.openstack.org/cgit/openstack/requirements/tree/upper-constraints.txt
Note:
Current thing designed for CI



## Questions?

* Robert Collins
* @rbtcollins
* lifeless on freenode
* rbtcollins@hp.com
