# DynamoDB and RDS — databases

**Suhani Awasthi · 24BCS10260**

DynamoDB is a managed NoSQL key-value/document database. Tables contain items; items contain attributes. The partition key distributes and identifies data; an optional sort key distinguishes and orders items sharing a partition key. Design keys around access patterns, avoid hot partitions, and use secondary indexes when alternate queries are needed. Query selects items through keys; Scan reads across the table and can be expensive. Good uses include session state, device events and predictable high-scale lookup workloads.

RDS manages relational database instances and operational tasks such as backups and maintenance. Common engines include PostgreSQL, MySQL, MariaDB, Oracle, SQL Server and Db2; Aurora is a related AWS relational service. Choose an engine for SQL semantics, ecosystem, licensing and workload requirements rather than treating engines as interchangeable.

Secure RDS through private networking, Security Groups, encrypted storage, TLS, database permissions and managed credentials. Automated backups and point-in-time recovery provide recovery options; manual snapshots have their own retention lifecycle. Test restores rather than only checking that backups exist.

Multi-AZ deployments improve availability and failover; read replicas primarily support read scaling and commonly replicate asynchronously. Their exact capabilities depend on the engine and deployment type. A standby in a classic Multi-AZ DB instance deployment is not the same as a readable replica. Use cases include transactional business systems, inventory and relational reporting.

| Decision | DynamoDB | RDS |
|---|---|---|
| Data model | Items/attributes and explicit access-pattern design | Tables, relations, joins and constraints |
| Query | Key-oriented operations and indexes | SQL and engine-specific query planning |
| Scaling | Managed partitioning with capacity modes | Instance/storage choices, replicas and engine features |
| Typical fit | High-scale keyed lookups | Relational transactions and joins |

The assignments request research, not provisioning these databases. No DynamoDB/RDS resources or charges are introduced by the coursework Terraform.

Reference: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
RDS: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html
