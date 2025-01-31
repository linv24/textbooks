# Scale From Zero to Millions of Users

## Summary

<p align="center">
  <img src="static/ch1/ch1_fig.png" width=500>
</p>

### Web Server Structure

* single server setup: user accesses the web via some device(s) (computer, phone) using a domain name; domain name is resolved to an IP address by DNS server; IP address is returned to device and inputted to web server to return page content 
* load balancer: distributes users across available servers based on request load; improves availability in case of server failures; improves security
  * may use private IPs of web servers, better security and scalability 
  * supports horizontal scaling of web tier by adding more web servers to be handled by load balancer 
* key concept: decoupling components to scale them individually 

### Vertical vs Horiztonal Scaling
* vertical scaling: increasing power of a single device (increasing CPU/RAM/memory)
  * drawbacks: hardware limit to how much vertical scaling, more expensive to scale higher, not necessarily helpful for higher demand 
* horizontal scaling: adding additional devices to a component (more servers, more databases, etc) to improve availability and load handling
  * drawbacks: more complexity in managing devices, higher risk of inconsistency across devices 

### Databases
* relational vs non-relational databases 
  * tabular vs non-tabular
  * simplicity vs scalability
  * integrity vs performance 
  * generic tabular structure vs use case-specific 
  * stricter regulation for data integrity and ACID vs fewer or more complex systems for integrity
  * suffers from join complexity vs may be optimized for complex joins 
* master-slave structure: master handles all write operations, slaves handle (in parallel) all read operations 
  * availability: master also capable of reads, slaves may be promoted to master, in cause of failure
  * data is **replicated** across slaves for data reliability 

### Caching
* cache assist database for fasting retrieval of data
* important to specify expiry times, time-to-live, caching policies for evicting data, consistency methods (eg. LRU, FIFO), etc.
* content delivery network:
  * acts as a cache for web servers, where CDNs cache and retrieve static content (more complex CDNs handle HTML as well) and deliver it to the user 
  * CDNs are distributed geographically, so that query performance improvements are maximized by location 
  * CDNs are managed by third parties

### Scaling the Web Tier
* stateful web:
  * each web server stores data (eg. session data, user authentication) of user state in-memory
  * much simpler, but comes with several drawbacks: user redirection may result in data inconsistency; higher risk of a SPOF; difficult to scale
* stateless web:
  * move state/session data to a database decoupled from the servers
  * allows for horizontal scaling of web servers, which can all access the state database
  * now commonly use nosql database to store state
* message queue: 
  * more robust method of fetching HTML data with web servers
  * web servers (**producers**) publish message in the message queue, which are read asynchronously by workers (**consumers**) to fetch the data 

### Scaling the Data Tier 
* sharding: split data across several devices that share the same schema but share the data load
  * important to specify a good sharding strategy: evenly distributed hashing function
  * common problems: shard redirection (in case of shard failure or shard overload), celebrity problem (frequently accessed shards may be located on the same device), joining & de-normalization (should be able to handle complex joins)
  * example of horizontal scaling
* data centers:
  * multiple geographically-spread data centers to distribute load, improve reliability & availability
  * requires some system to redirect users based on location (eg. geoDNS)
  * each data center has its own (1) web servers, (2) databases, and (3) caches, but all data centers may share a single noSQL state database
* tools: useful data for large-scale applications in terms of insights, diagnostics, etc
  * logging, metrics, monitoring, automation 



## Unknowns

* relational vs non-relational databases 
  * relational:
    * aka SQL database 
    * RDBMS: Relational DataBase Management Systems
    * CRUD: create, read, update delete operations
    * store data in rows and columns in tables, tabular format 
    * each row gets a unique primary key
    * rows in other tables can be referenced using a foreign key (which is the primary key in the referenced row's original table)
    * benefits over non-relational dbs:
      * intuitive, logical, and well-worn design
      * built-in security using roles
      * flexibility in operations without widespread side effects
      * easy collaboration/synchronization 
      * data consistency: usually employ some sort of data redundancy to account for data failures 
  * non-relational:
    * aka NoSQL (not only SQL) database 
    * flexible data structure, not necessarily tabular 
    * five types of non-relational databases:
      * key-value: 
        * each datum has a key, and value for associated data
        * keys and values can both be simple or complex objects
        * schema is defined per-row 
      * document: 
        * for semi-structured data like json, where data is stored as entire objects for reference
      * graph:
        *  data is stored as nodes in a graph to emphasize relationships between data points 
      * column-oriented: 
        * similar to tabular format of SQL databases, except column names may vary between rows; much less strict that relational columns/tables (not ACID)
      * in-memory: 
        * data stored in memory for ultra fast, low-latency data fetching 
      * benefits over relational dbs: 
        * flexibility in data, not necessary to tabularize data
        * faster development bc of flexibility in data format
        * massive data storage, bc designed for large quantities of flexible, complex data
        * faster queries, since designed not to have a hierarchy of relationships and optimized for fast fetching of data
        * scalability: horizontal scaling instead of vertical scaling
        * availability: unlike with relational dbs, there generally no single point of failure if data failures arise
      * disadvantages: 
        * no single language, like SQL for relational dbs
        * much newer, not as mature or widely used
        * case-by-case basis for deciding which database/data format to use per use case
        * not great for complex queries or joins 
        * not as robust systems for data consistency/integrity as SQL databases
  * primary differences between relational vs non-relational:
    * data integrity: ACID vs other non-ACID mechanisms
    * performance: relational typically sacrifice performance for higher data integrity
    * scale: non-relational typically designed per-use case to encourage high scalability 
  * ACID: atomicity, consistency, isolation, durability 
    * atomicity: operations are all-or-none, treated as individual units
    * consistency: operation transforms the database consistently across states, one valid state to another
    * isolation: operations have the same result, whether they were performed in series, in parallel, or separately from other operations 
    * durability: once transactions are committed, they are guaranteed to have the correct result (through logging, recovery mechanisms, redundancies, etc)
  * strong vs eventual consistency:
    * strong: data reads are always synchronized/up to date, at the cost of more storage
      * better where data integrity/reliability/consistency are important (e-commerce, finance)
    * eventual: data reads may be stale in small time-scale use cases, but saves much more storage 
      * better where latency, availability, and scalability are important (social media platforms, collaboration platforms)
* database normalization & de-normalization
  * normalization: 
    * transform a database to adhere to "normal forms"
    * best for **reducing data redundancy and improving data integrity** by normalizing table structure and ensuring that database operations are ACID
    * first normal form (NF1): all columns are atomic and all rows are unique (splitting large table into smaller table)
    * second normal form: satisfy NF1 and make sure all rows depend fully on primary key
    * third normal form: satisfy NF2 and remove transient dependencies (ie. non-key columns shouldn't depend on other non-key columns)
    * ... (more normal forms )
  * denormalization: 
    * combine smaller tables when **read performance is prioritized over write performance**, at the cost of risk of data inconsistency and storage usage 
    * increases data redundancy to improve query time, for when database is read-heavy and/or uses complex joins that normalized databases struggle with

## References 

* https://cloud.google.com/learn/what-is-a-relational-database
* https://cloud.google.com/discover/what-is-nosql 
* https://aws.amazon.com/compare/the-difference-between-relational-and-non-relational-databases/ 
* https://medium.com/@abhirup.acharya009/strong-consistency-vs-eventual-consistency-19ce6f87c112 