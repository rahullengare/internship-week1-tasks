#!/usr/bin/env python3
"""
cost_estimator.py

Lists running EC2 instances that have a given tag (default: Env=Dev)
and prints an estimated cost summary.

This script is READ-ONLY: it only calls ec2:DescribeInstances.
It never creates, changes or deletes anything.

The prices are APPROXIMATE On-Demand Linux prices for us-east-1.
They do not include EBS storage, data transfer, taxes or discounts.
Always check the AWS pricing page for exact numbers.
"""

import argparse
import sys
from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

# Approximate On-Demand Linux prices in USD per hour (us-east-1).
# Add more instance types here, or use --price TYPE=PRICE on the command line.
PRICES = {
    "t3.nano": 0.0052,
    "t3.micro": 0.0104,
    "t3.small": 0.0208,
    "t3.medium": 0.0416,
    "t3.large": 0.0832,
    "t2.micro": 0.0116,
    "t2.small": 0.0230,
    "t2.medium": 0.0464,
}

HOURS_PER_MONTH = 730  # average hours in one month

# Error codes that mean "the credentials themselves were not accepted".
BAD_CREDENTIAL_CODES = {
    "AuthFailure",
    "InvalidClientTokenId",
    "SignatureDoesNotMatch",
    "ExpiredToken",
    "RequestExpired",
}


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="List running EC2 instances with a tag and estimate their cost."
    )
    parser.add_argument("--tag-key", default="Env", help="tag key to filter by (default: Env)")
    parser.add_argument("--tag-value", default="Dev", help="tag value to filter by (default: Dev)")
    parser.add_argument("--region", help="AWS region (default: from your AWS CLI config)")
    parser.add_argument("--profile", help="AWS CLI profile name (default: default profile)")
    parser.add_argument(
        "--price",
        action="append",
        default=[],
        metavar="TYPE=PRICE",
        help="extra or custom hourly price, e.g. --price m5.large=0.096 (can be repeated)",
    )
    return parser.parse_args(argv)


def build_price_table(extra_prices):
    """Return the built-in prices plus any --price overrides."""
    prices = dict(PRICES)
    for item in extra_prices:
        try:
            instance_type, value = item.split("=", 1)
            prices[instance_type.strip()] = float(value)
        except ValueError:
            sys.exit(f"Invalid --price value '{item}'. Use the form TYPE=PRICE, e.g. m5.large=0.096")
    return prices


def get_running_instances(ec2, tag_key, tag_value):
    """Return a list of running instances that have the given tag."""
    filters = [
        {"Name": "instance-state-name", "Values": ["running"]},
        {"Name": f"tag:{tag_key}", "Values": [tag_value]},
    ]
    instances = []
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate(Filters=filters):
        for reservation in page["Reservations"]:
            instances.extend(reservation["Instances"])
    return instances


def describe_credentials(session):
    """Say where the credentials came from (never prints the secret key)."""
    creds = session.get_credentials()
    if creds is None:
        return f"Region: {session.region_name}. No credentials found."
    return (f"Region: {session.region_name}. Credentials source: {creds.method}. "
            f"Access key ends with: ...{creds.access_key[-4:]}")


def instance_name(instance):
    """Return the value of the Name tag, or '-' if there is none."""
    for tag in instance.get("Tags", []):
        if tag["Key"] == "Name":
            return tag["Value"]
    return "-"


def main(argv=None):
    args = parse_args(argv)
    prices = build_price_table(args.price)

    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    region = session.region_name
    if not region:
        sys.exit("No region set. Use --region <name> or run 'aws configure'.")

    ec2 = session.client("ec2")

    try:
        instances = get_running_instances(ec2, args.tag_key, args.tag_value)
    except NoCredentialsError:
        sys.exit("No AWS credentials found. Run 'aws configure' first.")
    except ClientError as error:
        code = error.response["Error"]["Code"]
        message = error.response["Error"].get("Message", "")
        if code in BAD_CREDENTIAL_CODES:
            sys.exit(f"AWS rejected your credentials ({code}).\n"
                     f"  {describe_credentials(session)}\n"
                     f"Check that these are the credentials you expect, that the access key is "
                     f"Active in IAM, and that 'aws sts get-caller-identity' works in this same terminal.")
        if code in ("UnauthorizedOperation", "AccessDenied"):
            sys.exit(f"Permission denied ({code}). Ask your mentor to allow "
                     f"ec2:DescribeInstances for your IAM user.")
        sys.exit(f"AWS error ({code}): {message}")
    except BotoCoreError as error:
        sys.exit(f"Could not connect to AWS: {error}")

    tag_text = f"{args.tag_key}={args.tag_value}"
    print(f"\nRunning EC2 instances with tag {tag_text} (region: {region})")
    print("=" * 84)

    if not instances:
        print("No running instances found. Check the region, the tag and the instance state.\n")
        return 0

    header = f"{'Name':<20} {'Instance ID':<20} {'Type':<11} {'Hours up':>9} {'$/hour':>8} {'$/month':>9}"
    print(header)
    print("-" * 84)

    now = datetime.now(timezone.utc)
    total_hourly = 0.0
    total_monthly = 0.0
    unknown_types = set()

    for instance in instances:
        instance_type = instance["InstanceType"]
        hours_up = (now - instance["LaunchTime"]).total_seconds() / 3600
        price = prices.get(instance_type)

        if price is None:
            unknown_types.add(instance_type)
            price_text, monthly_text = "n/a", "n/a"
        else:
            monthly = price * HOURS_PER_MONTH
            total_hourly += price
            total_monthly += monthly
            price_text, monthly_text = f"{price:.4f}", f"{monthly:.2f}"

        print(f"{instance_name(instance)[:20]:<20} {instance['InstanceId']:<20} "
              f"{instance_type:<11} {hours_up:>9.1f} {price_text:>8} {monthly_text:>9}")

    print("-" * 84)
    print(f"Running instances : {len(instances)}")
    print(f"Estimated cost    : ${total_hourly:.4f} per hour, about ${total_monthly:.2f} per month "
          f"({HOURS_PER_MONTH} hours)")

    if unknown_types:
        print(f"No price known for: {', '.join(sorted(unknown_types))} "
              f"(left out of the total; add one with --price TYPE=PRICE)")
    if region != "us-east-1":
        print(f"Note: prices are for us-east-1. Prices in {region} can be different.")
    print("Note: estimate only. EBS storage, data transfer and taxes are not included.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())