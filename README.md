# Week 1 Projects: Cloud Computing Internship

**Name:** Rahul Lengare
**Role:** Cloud Computing Intern (Infrastructure & DevOps Track)
**Company:** WeIntern Pvt Ltd

This is my work from **Week 1** of my cloud internship.

In this week I learned how to:
- set up a safe cloud account,
- draw a map of a cloud system,
- put a website online,
- write a small script that checks cost,
- and set up alerts that send me an email.

Each project has its own page with every step. Click the link in the last column to open it.

## The 6 Projects

| # | Project | What I did | What I learned | Steps |
|---|---------|------------|----------------|-------|
| 1 | Cloud Account Setup | Made a safe login for AWS with a second check (MFA) and connected my computer to AWS. | Why a safe login matters, and how to use AWS from the terminal. | [Open](README_task1.md) |
| 2 | Cloud Map | Drew a picture of what runs in our cloud and how the parts connect. | How a cloud network is built, with public and private parts. | [Open](README_task2.md) |
| 3 | Website Online | Put a web page online using S3 (storage) and CloudFront (fast delivery). The storage is private, and only CloudFront can read it. | How websites are hosted cheaply and safely. | [Open](README_task3.md) |
| 4 | Cost Script | Wrote a Python script that finds running servers with a tag and estimates what they cost. | How to use Python with AWS, and how to spot cost early. | [Open](README_task4.md) |
| 5 | Alerts | Set alarms that send me an email when a server is too busy or the cost goes up. | How to watch the cloud so problems are found early. | [Open](README_task5.md) |
| 6 | Weekly Summary | Wrote what I did this week and one problem I solved. | How to explain technical work in a clear way. | [Open](README_task6.md) |

---

## What I Learned This Week

- **Safety first.** Use your own login, turn on MFA, and keep things private.
- **Labels help.** Tags (like `Env=Dev`) let a script find the right servers.
- **Cost matters.** A small server still costs money while it runs, so check and clean up.
- **Write it down.** Clear steps and screenshots let anyone repeat the work.


## Words You May Not Know

| Word | Simple meaning |
|------|----------------|
| **Cloud / AWS** | Computers you rent over the internet from Amazon, instead of owning them. |
| **Server (EC2)** | One rented computer in the cloud. |
| **S3** | A place in the cloud to store files. |
| **CloudFront** | A service that delivers a website fast to people all over the world. |
| **IAM** | The tool that controls who can do what in the cloud account. |
| **MFA** | A second check when you log in, like a code on your phone. |
| **Tag** | A label on a cloud item, such as `Env=Dev`. |
| **Alarm** | A rule that warns you, for example by email, when something goes wrong. |


## Files in This Repository

```text
internship-week1-tasks/
├── README.md                       
├── README_task1.md                 # Project 1 
├── README_task2.md                 # Project 2 
├── README_task3.md                 # Project 3  
├── README_task4.md                 # Project 4 
├── README_task5.md                 # Project 5 
├── README_task6.md                  
├── infrastructure-diagram.drawio          
├── cost_estimator.py                              
├── screenshots/                    
└── index.html  
```

## Tools I Used

- **Cloud:** AWS (IAM, VPC, S3, CloudFront, EC2, CloudWatch)
- **Code and terminal:** AWS CLI, Python (boto3)
- **Drawing and saving work:** draw.io, Git, GitHub


## Safety Note

This repository has no passwords, secret keys or `.env` files. Account numbers and other private details are hidden in the pictures and pages.
