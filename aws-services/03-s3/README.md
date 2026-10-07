# S3 — object storage

**Suhani Awasthi · 24BCS10260**

S3 stores objects in buckets. An object contains bytes plus metadata and a key; slash-separated key prefixes resemble folders but are not a POSIX filesystem. General-purpose bucket names are globally unique within an AWS partition and buckets are created in a region.

Storage classes balance access frequency, resilience characteristics, retrieval behavior and cost. Standard suits frequently accessed data; Intelligent-Tiering can move eligible objects between access tiers; Standard-IA/One Zone-IA suit infrequent access with different resilience tradeoffs; Glacier classes support archive use with varying retrieval modes and timing. Check current service documentation and pricing before choosing a class.

Versioning preserves successive object versions and uses delete markers for normal deletes. It helps recovery but is not a substitute for access controls or independent backups. Lifecycle rules can transition objects and expire current/noncurrent versions; incorrect rules can delete valuable data.

Server-side encryption protects stored objects. SSE-S3 uses S3-managed keys; SSE-KMS integrates with KMS controls and policies. TLS protects data in transit. A bucket policy is a resource-based policy; identity policies also participate in authorization. Block Public Access helps prevent accidental exposure, and BucketOwnerEnforced disables ACL-based ownership management for the lab bucket.

Use cases: static assets, backups, logs, data lakes and build artifacts. In the S3 assignment, verify the bucket name, encryption, versioning and public-access block; upload a harmless object, replace it, list versions, and recover the older one. Remove all versions/delete markers before destroying a versioned lab bucket unless explicitly choosing destructive cleanup.

Reference: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html
