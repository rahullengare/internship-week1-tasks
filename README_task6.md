# Task 6: Week 1 Tech Debrief

## 1. About This Task

**What the task is:** Present my infrastructure map, the static-site deployment and my automation script to my mentor, and describe one challenge I hit and how I solved it.

**Why it matters:** The debrief pulls the whole week together. It shows what I built, that I understand it, and what I learned from a real problem.

**Deliverable:** A 1-page written summary (this README) and a 10-minute talk using the plan in Section 5.

---

## 2. Week 1 Summary

| # | Task | What I delivered | Result | Details |
|---|------|------------------|--------|---------|
| 1 | Cloud Account Onboarding | IAM user, MFA, AWS CLI configured, sandbox access verified, tagging rules read | Access works with MFA, signed in as an IAM user (not root) | [README_task1.md](README_task1.md) |
| 2 | Infrastructure Map | Architecture diagram of the dev environment (VPC, subnets, services, connections) | `infrastructure-diagram.png` and the editable `.drawio` file | [README_task2.md](README_task2.md) |
| 3 | Static Site with CDN | Student Portal page on a **private** S3 bucket behind CloudFront, readable only through a bucket policy for CloudFront | Live URL: `https://<your-domain>.cloudfront.net` | [README_task3.md](README_task3.md) |
| 4 | Automation Script | `cost_estimator.py` lists running EC2 instances with the tag `Env=Dev` and estimates their cost | Found `dev-test-instance` (`t3.micro`, Mumbai): about $8.18 per month | [README_task4.md](README_task4.md) |
| 5 | Cloud Alerts | CloudWatch alarms for CPU (>= 70%) and estimated charges (> $0.01), with an SNS email notification | The CPU alert email arrived after I forced the alarm state | [README_task5.md](README_task5.md) |

---

## 3. The Challenge I Solved

### What happened
When I first ran `cost_estimator.py`, it stopped with `AuthFailure`. A direct check with `aws sts get-caller-identity` then gave `InvalidClientTokenId`. The same AWS CLI had worked earlier in Command Prompt, so the account and permissions were fine.

### How I found the cause
1. The error meant AWS rejected the **credentials**, not a missing permission. My script's first error message wrongly said "check your permissions", so I changed it to show where the credentials come from and the last 4 characters of the access key.
2. The new message showed that this terminal (MSYS2) was using a key that did not match the active key in IAM.
3. Cause: each terminal can keep its own saved credentials. The MSYS2 terminal had an old key in its own `~/.aws` folder, which was different from the one saved by `aws configure` in Command Prompt.

### How I fixed it
I ran `aws configure` in the same terminal with a valid access key, confirmed it with `aws sts get-caller-identity` (it showed my IAM user), and ran the script again. It then listed the instance and the cost.

### What I learned
- `AuthFailure` or `InvalidClientTokenId` means the **key** is wrong or inactive. `UnauthorizedOperation` or `AccessDenied` means the key is fine but a **permission** is missing.
- Run `aws sts get-caller-identity` first, in the same terminal where the script will run.
- `aws configure` shows the keys on screen while you type, so never screenshot it. A key that has been shown anywhere should be deleted and replaced.
- Good error messages save time. A message that says where the credentials came from made the problem obvious.

---

## 4. What I Learned This Week

- **Security first:** an IAM user with MFA, a private bucket, and only the permissions each task needs.
- **Tagging matters:** the script finds the right resources only because they carry the `Env=Dev` tag.
- **Cost awareness:** even a small test server costs money while it runs, so I check what is running and clean up when a task is reviewed.
- **Documentation:** a README with steps, screenshots and a cleanup section makes the work easy for someone else to repeat.

### What I would improve
- Use the Pricing API in the script instead of a small price table, so the estimate is correct in any region.
- Add an email action to the cost alarm, which needs an SNS topic in the same region as the alarm.
- Test the CPU alarm with real load, not only with a forced alarm state.

---

## 5. 10-Minute Presentation Plan

| Time | Topic | What to show |
|------|-------|--------------|
| 1 min | Introduction | The week at a glance (the table in Section 2) |
| 2 min | Infrastructure map | The diagram: VPC, subnets, services and how they connect |
| 2 min | Static site | Open the live CloudFront URL, then show the private bucket and the bucket policy |
| 2 min | Automation script | Run `python cost_estimator.py --region ap-south-1 --price t3.micro=0.0112` live |
| 1 min | Alerts | The two alarms and the email I received |
| 2 min | The challenge | Section 3: problem, cause, fix, lesson |

**Before I present**
- [ ] The CloudFront URL opens over HTTPS and the form works
- [ ] The test EC2 instance is still running, so the script has something to list
- [ ] `aws sts get-caller-identity` works in the terminal I will use
- [ ] The diagram, the email screenshot and the READMEs are open in tabs

---

## 6. Cleanup After the Mentor Review

Once my mentor has reviewed Week 1, I remove the resources I created so nothing keeps costing money:

| Resource | From | How |
|----------|------|-----|
| Test EC2 instance `dev-test-instance` | Task 4 | EC2 → Instances → Instance state → **Terminate** |
| CloudFront distribution, then the S3 bucket | Task 3 | Disable and delete the distribution, then empty and delete the bucket |
| CloudWatch alarms and the SNS topic | Task 5 | Delete them (see Task 5 cleanup) |
| Access keys I no longer use | Task 1 | IAM → Security credentials → Deactivate, then Delete |

**I do not delete** the API Gateway, Lambda function or DynamoDB table used by the Student Portal. They were not created for this internship.
**I keep** the repository (READMEs, scripts, screenshots) as the record of Week 1.

---

## 7. Folder Structure

```
internship-week1-tasks/
├── README.md
├── README_task1.md ... README_task5.md
├── README_task6.md                 # This file
├── infrastructure-diagram.drawio
├── bucket-policy.json
├── cost_estimator.py
├── task3-site/
│   └── index.html
└── screenshots/
```
