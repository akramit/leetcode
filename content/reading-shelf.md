# Reading Shelf

System design and engineering papers worth reading alongside interview prep.

### 1. Scaling Architecture & Infrastructure

* [Hypertext Transfer Protocol](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol)
* [Should you go Beyond Relational Databases?](https://blog.teamtreehouse.com/should-you-go-beyond-relational-databases)
* [Database Replication](https://en.wikipedia.org/wiki/Replication_(computing))
* [Multi-master replication](https://en.wikipedia.org/wiki/Multi-master_replication)
* [NDB Cluster Replication: Multi-Master and Circular Replication](https://dev.mysql.com/doc/refman/5.7/en/mysql-cluster-replication-multi-master.html)
* [Caching Strategies and How to Choose the Right One](https://codeahoy.com/2017/08/11/caching-strategies-and-how-to-choose-the-right-one/)
* [Single point of failure](https://en.wikipedia.org/wiki/Single_point_of_failure)
* [Amazon CloudFront Dynamic Content Delivery](https://aws.amazon.com/cloudfront/dynamic-content/)
* [Configure Sticky Sessions for Your Classic Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html)
* [Active-Active for Multi-Regional Resiliency](https://netflixtechblog.com/active-active-for-multi-regional-resiliency-c47719f6685b)
* [Amazon EC2 High Memory Instances](https://aws.amazon.com/ec2/instance-types/high-memory/)
* [What it takes to run Stack Overflow](http://nickcraver.com/blog/2013/11/22/what-it-takes-to-run-stack-overflow)
* [What The Heck Are You Actually Using NoSQL For](http://highscalability.com/blog/2010/12/6/what-the-heck-are-you-actually-using-nosql-for.html)

### 2. Capacity Estimation & Benchmarks

* [Google Pro Tip: Use Back-Of-The-Envelope-Calculations To Choose The Best Design](http://highscalability.com/blog/2011/1/26/google-pro-tip-use-back-of-the-envelope-calculations-to-choo.html)
* [System design primer](https://github.com/donnemartin/system-design-primer)
* [Latency Numbers Every Programmer Should Know](https://colin-scott.github.io/personal_website/research/interactive_latency.html)
* [Amazon Compute Service Level Agreement](https://aws.amazon.com/compute/sla/)
* [Compute Engine Service Level Agreement (SLA)](https://cloud.google.com/compute/sla)
* [SLA summary for Azure services](https://azure.microsoft.com/en-us/support/legal/sla/summary/)

### 3. Rate Limiting & Traffic Throttling

* [Rate-limiting strategies and techniques](https://cloud.google.com/solutions/rate-limiting-strategies-techniques)
* [Twitter rate limits](https://developer.twitter.com/en/docs/basics/rate-limits)
* [Google docs usage limits](https://developers.google.com/docs/api/limits)
* [IBM microservices](https://www.ibm.com/cloud/learn/microservices)
* [Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)
* [Stripe rate limiters](https://stripe.com/blog/rate-limiters)
* [Shopify REST Admin API rate limits](https://help.shopify.com/en/api/reference/rest-admin-api-rate-limits)
* [Better Rate Limiting With Redis Sorted Sets](https://engineering.classdojo.com/blog/2015/02/06/rolling-rate-limiter/)
* [System Design - Rate limiter and Data modelling](https://medium.com/@saisandeepmopuri/system-design-rate-limiter-and-data-modelling-9304b0d18250)
* [How we built rate limiting capable of scaling to millions of domains](https://blog.cloudflare.com/counting-things-a-lot-of-different-things/)
* [Redis website](https://redis.io/)
* [Lyft rate limiting](https://github.com/lyft/ratelimit)
* [Scaling your API with rate limiters](https://gist.github.com/ptarjan/e38f45f2dfe601419ca3af937fff574d#request-rate-limiter)
* [What is edge computing](https://www.cloudflare.com/learning/serverless/glossary/what-is-edge-computing/)
* [Rate Limit Requests with Iptables](https://blog.programster.org/rate-limit-requests-with-iptables)
* [OSI model](https://en.wikipedia.org/wiki/OSI_model#Layer_architecture)

### 4. Distributed Data Hashing & Partitioning

* [Consistent hashing](https://en.wikipedia.org/wiki/Consistent_hashing)
* [Consistent Hashing - Tom White](https://tom-e-white.com/2007/11/consistent-hashing.html)
* [Dynamo: Amazon's Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
* [Cassandra - A Decentralized Structured Storage System](http://www.cs.cornell.edu/Projects/ladis2009/papers/Lakshman-ladis2009.PDF)
* [How Discord Scaled Elixir to 5,000,000 Concurrent Users](https://blog.discord.com/scaling-elixir-f9b8e1e7c29b)
* [CS168: The Modern Algorithmic Toolbox - Consistent Hashing](http://theory.stanford.edu/~tim/s16/l/l1.pdf)
* [Maglev: A Fast and Reliable Software Network Load Balancer](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/44824.pdf)

### 5. Key-Value & Storage Engines

* [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
* [Memcached](https://memcached.org/)
* [Redis](https://redis.io/)
* [Dynamo: Amazon’s Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
* [Apache Cassandra](https://cassandra.apache.org/)
* [Bigtable: A Distributed Storage System for Structured Data](https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf)
* [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree)
* [Cassandra architecture](https://cassandra.apache.org/doc/latest/architecture/)
* [SSTable and Log-Structured Storage](https://www.igvita.com/2012/02/06/sstable-and-log-structured-storage-leveldb/)
* [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter)

### 6. Unique ID Generation

* [Universally unique identifier](https://en.wikipedia.org/wiki/Universally_unique_identifier)
* [Ticket Servers: Distributed Unique Primary Keys on the Cheap](https://code.flickr.net/2010/02/08/ticket-servers-distributed-unique-primary-keys-on-the-cheap/)
* [Announcing Snowflake](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake.html)
* [Network time protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol)

### 7. Web APIs & URL Shorteners

* [A RESTful Tutorial](https://www.restapitutorial.com/index.html)
* [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter)

### 8. Web Crawling & Indexing

* [US Library of Congress](https://www.loc.gov/websites/)
* [EU Web Archive](http://data.europa.eu/webarchive)
* [Digimarc Piracy Intelligence](https://www.digimarc.com/products/digimarc-services/piracy-intelligence)
* [Web Crawling Survey (Christopher Olston, Marc Najork)](http://infolab.stanford.edu/~olston/publications/crawling_survey.pdf)
* [29% Of Sites Face Duplicate Content Issues](https://tinyurl.com/y6tmh55y)
* [Donald J. Patterson, Web Crawling Slides](https://www.ics.uci.edu/~lopes/teaching/cs221W12/slides/Lecture05.pdf)
* [Google Dynamic Rendering](https://developers.google.com/search/docs/guides/dynamic-rendering)

### 9. Notification Systems & Messaging

* [Twilio SMS](https://www.twilio.com/sms)
* [Nexmo SMS](https://www.nexmo.com/products/sms)
* [SendGrid](https://sendgrid.com/)
* [Mailchimp](https://mailchimp.com/)
* [You Cannot Have Exactly-Once Delivery](https://bravenewgeek.com/you-cannot-have-exactly-once-delivery/)
* [Security in Push Notifications](https://cloud.ibm.com/docs/services/mobilepush?topic=mobile-pushnotification-security-in-push-notifications)
* [RabbitMQ Queued Messages](https://bit.ly/2sotIa6)

### 10. News Feed & Social Graph Systems

* [How News Feed Works - Facebook](https://www.facebook.com/help/327131014036297/)
* [Friend of Friend recommendations with Neo4j and SQL Server](http://geekswithblogs.net/brendonpage/archive/2015/10/26/friend-of-friend-recommendations-with-neo4j.aspx)

### 11. Real-Time Chat & Communications

* [Erlang at Facebook](https://www.erlang-factory.com/upload/presentations/31/EugeneLetuchy-ErlangatFacebook.pdf)
* [Messenger and WhatsApp process 60 billion messages a day](https://www.theverge.com/2016/4/12/11415198/facebook-messenger-whatsapp-number-messages-vs-sms-f8-2016)
* [Long tail distribution](https://en.wikipedia.org/wiki/Long_tail)
* [The Underlying Technology of Messages - Facebook](https://www.facebook.com/notes/facebook-engineering/the-underlying-technology-of-messages/454991608919/)
* [How Discord Stores Billions of Messages](https://blog.discordapp.com/how-discord-stores-billions-of-messages-7fa6ec7ee4c7)
* [Apache ZooKeeper](https://zookeeper.apache.org/)
* [The evolution of WeChat background system](https://www.infoq.cn/article/the-road-of-the-growth-weixin-background)
* [End-to-end encryption - WhatsApp](https://faq.whatsapp.com/en/android/28030015/)
* [Flannel: An Application-Level Edge Cache to Make Slack Scale](https://slack.engineering/flannel-an-application-level-edge-cache-to-make-slack-scale-b8a6400e2f6b)

### 12. Search Autocomplete & Stream Processing

* [The Life of a Typeahead Query - Facebook](https://www.facebook.com/notes/facebook-engineering/the-life-of-a-typeahead-query/389105248919/)
* [How We Built Prefixy: A Scalable Prefix Search Service](https://medium.com/@prefixyteam/how-we-built-prefixy-a-scalable-prefix-search-service-for-powering-autocomplete-c20f98e2eff1)
* [Prefix Hash Tree: An Indexing Data Structure over Distributed Hash Tables](https://people.eecs.berkeley.edu/~sylvia/papers/pht.pdf)
* [MongoDB](https://en.wikipedia.org/wiki/MongoDB)
* [Unicode Frequently Asked Questions](https://www.unicode.org/faq/basic_q.html)
* [Apache Hadoop](https://hadoop.apache.org/)
* [Spark Streaming](https://spark.apache.org/streaming/)
* [Apache Storm](https://storm.apache.org/)
* [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
