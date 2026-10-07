# Kubernetes object comparisons

| Property | Deployment | ReplicaSet |
|---|---|---|
| Purpose | Manage stateless application releases | Maintain desired replica count |
| Pod management | Owns ReplicaSets that own Pods | Creates and replaces matching Pods |
| Scaling | Change Deployment replicas or HPA | Change ReplicaSet replicas |
| Updates | RollingUpdate/Recreate, history and rollback | No release orchestration |
| Relationship | Creates a new ReplicaSet when Pod template changes | Normally controlled by Deployment; avoid editing managed replicas directly |

| Property | Deployment | DaemonSet | StatefulSet |
|---|---|---|---|
| Use case | Stateless HTTP/API | Node logging/network agents | Stateful databases |
| Creation | Interchangeable replicas | One per eligible node | Ordinal identities such as database-0 |
| Scaling | Replica count or HPA | Eligible node count | Replica count; ordered behavior by default |
| Networking | Service selects disposable Pods | Node-local access or Service | Stable Pod DNS, commonly headless Service |
| Storage | Optional volumes without stable replica identity | Often mounts node paths | Per-Pod PVCs through volumeClaimTemplates |
| Example | Web frontend | Log collector | Database replicas |

A ReplicaSet keeps Pods alive but does not give clients a stable address. A Service selects ready endpoints and gives clients stable discovery and, normally, a virtual IP. Client → DNS → Service port → selected Pod target port. Headless Services return Pod addresses directly. Services neither create Pods nor replace a ReplicaSet. StatefulSet provides identity and storage ordering, not database replication by itself.

References: https://kubernetes.io/docs/concepts/workloads/controllers/ and https://kubernetes.io/docs/concepts/services-networking/service/
