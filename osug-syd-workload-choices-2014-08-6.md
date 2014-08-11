## Workload choices


<small>Robert Collins  
rbtcollins@hp.com  
@rbtcollins (Twitter)</small>



## compute types


### Baremetal
* Ironic
* Nova-bm (deprecated)
Note:
No hypervisor, no fancy features - image on, image off
Low Agility
Highest performance
High vulnerability - root on your hardware, enough said; but wait there is more... no network virtualisation, no storage virt yet etc.


### Containers
* libvirt/lxc
* docker
* openvz
Note:
No hypervisor, hardware isolation via kernel and namespaces, some fancy features depending on specific container (e.g. suspend/live migration etc)
Medium Agility
High performance
Medium vulnerability - overlay network, neutron policy etc, but have kernel surface are to defend against


### Virtual machines
* KVM
* Xen
* HyperV
* VMWare
Note:
Full hypervisor, full range of fancy features - live migration etc
Fully agile
Medium performance - e.g. databases can suffer
Least vulnerable - narrow surface area, network virtualised. muahahaha side channel attacks



## Workload types


### Dynamic
* API frontends
* service tiers
* ...
Note:
Really looking at things where quick reaction is key - e.g. you have 10m from load starting to skyrocket to having new capacity online - containers or vms. If they are in your surface area for attack - vms.


### Performance constrained
* DBs
* Big data - e.g. hadoop clusters
* singleton services
* load balancers (in extreme cases)
Note:
Baremetal - entire capacity of machine
then lxc - get flexability


### Jitter sensitive
* NTP
* some crypto systems
Note:
Baremetal


### Non-linux
* Windows
* BSD...
Note: BM or hypervisor - or possibly that OS specific jail etc as a container driver


### Security
* Domain controllers (KDC, AD, etc)
* Puppet master/ chefserver
* Keystone
* Package signing servers
Note: Baremetal! Or a dedicated cloud / hypervisor via aggregate



## Deployment styles



## Precious Pets


Cloud image
Note: even Windows


Bootable ISO and do an install by-hand.

Eeek.


Evolution by hand


Pick if you have:

* Windows vendor apps
* Other unautomatable installs
Note: Suitable for truely one-offs only.



## Persistent pets
aka configuration management

* Chef
* Puppet
* cfengine


cloud-init bootstrap
Note: e.g. hands off to chef / puppet


Foreman


Adhoc scripts
Note: e.g. ssh in, apt-get install chef, run it.


Typically evolve by local agents and packages


Pick if:

* Existing investment in e.g. Chef, Puppet
* Deploying other existing topology
* Evolving from non-cloud



## Cluster orchestration tools
* Heat
* Juju
* Eve (part of HP Helion Commercial edition)
* (other TOSCA servers)
Note: Eve is not yet available, not a forward looking statement :)


Have automated bring-up built in


Evolve via API calls
Note: version the structure locally


Lifecycle management
Note: varies between service etc - bring up, scale down, automated


Pick if:

* Dynamic workloads
* Complex topologies
* Automatic recovery



## Immutable servers
* Docker
* Heat w/Golden images
* NFS roots... <!-- .element: class="fragment" -->
Note: Popularised by Netflix, but actually quite old - see NASA bringup-of-infrastructure paper


Very very good for large scale


Reduced window for entropy


Complete confidence that what you tested is what you are deploying


Complete confidence that you can recreate the state of your servers from scratch


Pick if:

* Super dynamic
* Long lived servers (less room for entropy)
* Want to reach CI/CD Nirvana
Note: (latency is lower)



## Questions?

* Robert Collins
* @rbtcollins
* lifeless on freenode
* rbtcollins@hp.com
