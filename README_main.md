# Week 1 Projects: Cloud Computing Internship

**Role:** Cloud Computing Intern (Infrastructure & DevOps Track)

**Organization:** WeIntern Pvt Ltd

**Intern:** Rahul Lengare

This repository holds the work completed in **Week 1** of the internship: cloud account setup, infrastructure mapping, static site hosting with a CDN, cost automation, and basic monitoring. Each project has its own README that explains the steps in detail.

---

## Projects

| # | Project | What I did | Tools | Details |
|---|---------|------------|-------|---------|
| 1 | Cloud Account Onboarding | Set up a secure IAM login with MFA, installed and configured the AWS CLI, and verified access to the dev sandbox. | IAM, MFA, AWS CLI | [README_task1.md](README_task1.md) |
| 2 | Infrastructure Map | Explored the dev environment and drew its architecture: VPCs, subnets, services and how they connect. | VPC, draw.io | [README_task2.md](README_task2.md) |
| 3 | Static Site with CDN | Hosted the front end of my DayFlow task tracker on a private S3 bucket behind CloudFront, using a bucket policy that only allows CloudFront to read it. | S3, CloudFront | [README_task3.md](README_task3.md) |
| 4 | Automation Script | Wrote a script that lists running instances, filters them by tag, and prints a cost estimate. | Python (boto3), Git | [README_task4.md](README_task4.md) |
| 5 | Cloud Alerts | Created alarms for high CPU usage and a cost threshold, and tested that they trigger. | CloudWatch | [README_task5.md](README_task5.md) |
| 6 | Tech Debrief | Summarized the week and described one problem I hit and how I solved it. | Documentation | [README_task6.md](README_task6.md) |

---

## Repository Structure

```text
internship-week1-tasks/
├── README.md                       # This file: project overview
├── README_task1.md                 # Cloud Account Onboarding
├── README_task2.md                 # Infrastructure Map
├── README_task3.md                 # Static Site with CDN
├── README_task4.md                 # Automation Script
├── README_task5.md                 # Cloud Alerts
├── README_task6.md                 # Tech Debrief
└── screenshots/                    # All screenshots for every project
```

All screenshots are stored in the `screenshots/` folder, and the project READMEs link to them.


## Tools Used

- **Cloud:** AWS (IAM, VPC, S3, CloudFront, EC2, CloudWatch)
- **Scripting and CLI:** AWS CLI, Python (boto3)
- **Diagrams and version control:** draw.io, Git, GitHub

