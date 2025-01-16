# Design a Rate Limiter 

## What is a rate limiter
* limits the rate at which requests, accesses, etc. can be handled by the central service. rate limiters can be implemented at mulitple levels of architecture, but the most common is at the HTTP level, where we limit clients' rate at which they can make API calls to our servers.
* why do we rate limit?
  * prevent denial of service (Dos) attacks
  * reduce cost
  * ensure servers aren't overloaded 
* two primary components to a rate limiter: algorithm and rules

## Step 1: understand the problem, identify the scope
* what does typical traffic look like? how far should we scale? do we plan on using a distributed system? **how do we inform users that they've been limited?**

## Step 2: high-level design
* client-side vs server-side rate limiter: client-side generally not preferred, since we can't guarantee the client implementation; server-side has less overhead and we have complete control
* should we use a third-party rate limiter or middleware? should we implement it in the server-side?
  * generally, middleware is preferred. a name that is constantly brought up is **Redis**
  * things to consider: is adding middleware and/or a third part cost-effective for the company? will implementing our own rate limiter take too much time? 
* algorithms:
  * token bucket: 
    * a bucket has an associated refiller that refills its tokens at a constant rate
    * each request uses one token; if there are no tokens left, the request is dropped
    * pros: easy to implement, memory efficient, handles bursts of traffic well
    * cons: only two parameters, perhaps overly simple 
  * leaking bucket: 
    * algorithm handles requests at a constant rate (instead of adding tokens at a constant rate)
    * if a request is added while the queue is full, the request gets dropped
    * pros: useful if a constant throughput is important
    * cons: handles bursts poorly
  * fixed window counter:
    * break time scale into constant-sized windows (eg. minute-long windows)
    * each window gets a counter and a limit; if in any given time window, the counter reaches the limit, any requests added during that window get dropped
    * pros: there may be some particular use cases where this kind of constant time windowing is preferred
    * cons: bursts of traffic at edges of windows: bursts of traffic that should exceed the limit may not be limited if the burst is split across two different windows, bypassing the limit entirely
  * sliding window log:
    * solves the burst issue of the fixed window algorithm by using a sliding window, based on the timestamp of requests
    * using the timestamp of the "first" request and some expiration length to determine which requests are in the queue
    * limit is the number of requests in the log; log is determined by sliding window of time based on non-expired logs 
    * pros: solves the burst issue
    * cons: memory inefficient, since we have to store all request timestamps, maybe even including those of dropped requests
  * sliding window counter:
    * solves both the burst issue and memory issues of other window algorithms
    * determines the limit of the current window using the current algorithm: # of requests in current window + (# of requests in previous window * % of time into the current window at the time of the current request)
    * pros: uses the average number of requests in the previous window to determine how many requests in the current window we can use
    * cons: only works for no-so-strict look back windows (?) 
* where should we store counters in general? usuing in cache, because fast  
* dropped requests are usually handled in two ways: completely dropped with HTTP header return of error 429, or put into a message queue to be handled later 

## Step 3: Design deep dive
* how and where are rules created/stored?
  * typically stored as json files using `domain`, `descriptors`, `liimt`, etc
  * typically stored on disk, which are moved to cache by workers to be accessed by the rate limited (server-side or middleware)
* distributed case?
  * primary issues:
    * race conditions: incrementing counter correctly when multiple rate limiters must working simultaneously; could be solved with locks, but locks significantly slow the system down; solved instead with either Lua scripts or sorted sets data structure by Redis 
    * synchronization: synchronizing counter and limits between multiple rate limiters is crucial for limiters to work properly; solved by using a centralized data storage system like Redis, where all limiters access a single storage for tracking counters 
* performance:
  * want multiple geographically spread data centers to maximize performance globally; **multi-data center setup**
  * eventual consistency is better for low-latency priority systems (as opposed to strong consistency, which is more reliable but slower)
* monitoring:
  * want to know how our rate limiters are performing, specifically (1) whether algorithms are working effectively and (2) whether rules are working effectively 

## Step 4: Wrap up 
* hard (absolutely no going over the limit) vs soft (can go over the limit if contained in a small time frame) rate limiting
* rate limiting at different levels:
  * not just HTTP, but also at the physical layer, transport layer, IP layer, etc.
* avoid rate limiting from the server software side:
  * design of client cache
  * exception/error catching code
  * retry logic 


## References 

* https://medium.com/@saisandeepmopuri/system-design-rate-limiter-and-data-modelling-9304b0d18250 