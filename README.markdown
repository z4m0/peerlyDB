#PeerlyDB
PeerlyDB is the database of [Peerly](https://github.com/z4m0/peerly).
PeerlyDB is a fork of [bmuller/kademlia](https://github.com/bmuller/kademlia).

##Diferences with Kademlia right now
* It can contain several versions of the same key and all of them are retrieved on GET

##Ideas
This is a list of planned features or ideas. Feel free to discuss them and propose more.

* Voting system: Each user can vote up or vote down an entry. The most voted entries should remain more time. The user can see what the comunity things about this entry. The votes won't be stored in the same location as the value. This means that the kademlia protocol should be extended.


* Add the option to subscribe. A peer subscribes to a key. Each time an unpdate is recieved the peer is notified. It has the problem if there are too many subscriptors.

* Allow signatures.

