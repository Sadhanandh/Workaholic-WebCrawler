Workaholic Webcrawler 
===================== 

An extensible multi-threaded Web crawler.
Useful in a multinode system where DB is centralized or clustered. 


Features: 
========= 

*Uses sqlite database. 
*Batch Processing of DB query. 
*Efficiently uses two queues 

    *raw queue -> which the slave pulls out of. 
    *final queue -> which the manager pulls out of and verifies it using DB calls 

*Each node has 1 manager and x slaves 
*The manager queries the central database 
*The database also stores "backlinks" -> the number of backlinks to a particular page. 
*User-Agent Header is customizable. 
*Switch Between urllib2 (Good socks support) or the requests library. 


Requirements: 
============= 

python-lxml (can also do a regex search instead) 
optional( python-requests ) 


Usage: 
====== 

```
git clone https://github.com/Sadhanandh/Workaholic-WebCrawler.git
```

If you dont have the lxml library already then: 
On Ubuntu/Debian: 
```
sudo apt-get install python-lxml
```
or 
On Windows/Mac/*nix 
```
pip install lxml
```


```
./webcrawl.py --urls "http://github.com http://twitter.com" 
```

Other options-- 

```
-d / --depth "depth of crawling" 
-t / threads "number of threads ie number of slaves per node " 
-b / batch   "batch query limit" 
```


TODO: 
======= 
* Use Multi-clustered MySql DB server co-operating with a Node community 
* Separate IO bound slaves  (that uses threading library) and CPU bound slaves (that uses multiprocessing library) to  maximize the throughput. 
*Respect Robot.txt (DB) 
*Support Multi-Proxy IP's and also every page of the base url should be crawled through the same proxy (DB) 

CANDO: 
====== 
* Find all the links in the readable area(excluding the usually user ignored header,footer and irrelevant areas of the page) 
