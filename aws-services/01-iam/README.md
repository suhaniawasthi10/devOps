# IAM — identity and access

**Suhani Awasthi · 24BCS10260**

IAM controls who can perform which actions on AWS resources. Authentication establishes identity; authorization evaluates applicable policies. An explicit deny overrides an allow, and access without an applicable allow is implicitly denied.

| Component | Meaning and use |
|---|---|
| User | Long-lived identity; can have console credentials or access keys. Avoid long-lived keys when federation is available. |
| Group | Collection of IAM users receiving common permissions; it is not an assumable identity. |
| Role | Assumable identity with temporary credentials; suitable for EC2, workloads and federated users. |
| Policy | JSON statements describing Effect, Action, Resource and optional Condition. |
| Permissions | Effective allowed actions after identity/resource policies, boundaries and organization restrictions are considered. |

A role's trust policy determines who may assume it; its permissions policy determines what the assumed role can do. Least privilege means only required actions, on required resources, under appropriate conditions. The coursework EC2 role can list its own bucket and get/put that bucket's objects; it does not grant access to every bucket.

Prefer IAM Identity Center/federation for people, instance/workload roles for applications, MFA for sensitive accounts and protected root credentials. Review unused permissions and access keys, use CloudTrail for auditing and IAM Access Analyzer for policy review. Never commit access keys or use the root account for routine labs.

Use cases: read-only support access, CI assuming a deployment role, EC2 accessing S3 without embedded credentials. For verification, `aws sts get-caller-identity` identifies the current principal; test allowed and denied operations with a scoped lab identity. It does not itself prove every permission is safe.

Reference: https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html
