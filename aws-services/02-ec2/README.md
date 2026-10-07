# EC2 — compute

**Suhani Awasthi · 24BCS10260**

EC2 provides virtual servers called instances. An AMI supplies the operating-system image and launch configuration; choose an architecture compatible with the instance type. Instance families target general-purpose, compute, memory, storage or accelerator workloads; sizes set CPU/memory capacity. This coursework uses x86_64 Amazon Linux on the t3 family.

Key pairs support SSH access to compatible Linux AMIs; the private key stays with the operator. An IAM instance role is different: it supplies temporary AWS API credentials to software. Session Manager can provide access without opening inbound SSH when its agent, IAM permissions and connectivity are configured.

Security Groups are stateful allow-rule firewalls attached to network interfaces. Return traffic for an allowed connection is tracked. EBS supplies persistent block volumes within an availability zone; encryption protects stored data, and snapshots support recovery. Root volumes can be configured for deletion at termination.

A private IP identifies the instance within its network. A public IPv4 enables internet routing only when routes and firewall rules also permit it. A normal auto-assigned public address can change after stop/start; an Elastic IP is a separately allocated static address with its own lifecycle and charges.

Lifecycle: pending → running → stopping → stopped → starting/running, or shutting-down → terminated. Reboot differs from stop/start. Termination is not the same as deleting every related resource: volumes, snapshots and other assets may remain. CPU credits matter for burstable T instances under sustained load.

Use cases: web hosting, build agents, batch work and single-node coursework Kubernetes. Inspect instance status, cloud-init logs, Security Groups and `curl` the actual application endpoint. A running EC2 state does not prove the application started.

Reference: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html
