# VPC — networking

**Suhani Awasthi · 24BCS10260**

A VPC is a logically isolated AWS network. CIDR defines its IP range: 10.42.0.0/16 contains the smaller coursework subnet 10.42.1.0/24. Subnets belong to one availability zone. Avoid overlapping ranges when connecting networks or choosing Kubernetes Pod/Service CIDRs.

Route tables choose a next hop by destination prefix. A public subnet has a route to an Internet Gateway; a workload also needs a public address and permissive security rules to exchange IPv4 internet traffic. A private subnet lacks that direct internet-gateway route. An Internet Gateway connects the VPC to the internet. A NAT Gateway can provide outbound IPv4 access for private-subnet workloads without allowing unsolicited inbound internet connections; it incurs charges and requires appropriate routing.

| Control | Scope | Behavior |
|---|---|---|
| Security Group | Network interface | Stateful allow rules; return traffic is tracked |
| Network ACL | Subnet boundary | Stateless ordered allow/deny rules; return/ephemeral ports must be considered |
| Route table | Associated subnet/gateway | Selects the destination path; does not replace firewall rules |

The lab provisions one public subnet, a route table, Internet Gateway and restricted Security Group. No NAT Gateway is needed for this small single-subnet design. HTTP and optional Kubernetes API access are limited to the operator's /32; SSH is optional. A production multi-tier design commonly places only load balancers in public subnets and application/databases in private subnets.

Troubleshooting: confirm destination IP and route, subnet association, Security Group, NACL, DNS and application listener. VPC Flow Logs help examine accepted/rejected network flows; they do not contain full packet payloads.

Reference: https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html
