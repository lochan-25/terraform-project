import boto3
import sys

ec2 = boto3.client('ec2')
s3 = boto3.client('s3')


def delete_ec2(dry_run=False):
    print("Fetching EC2 instances...")
    instances = ec2.describe_instances()

    instance_ids = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])

    if not instance_ids:
        print("No EC2 instances found.")
        return

    print(f"Instances found: {instance_ids}")

    if dry_run:
        print("Dry run enabled. Skipping EC2 deletion.")
    else:
        print("Deleting EC2 instances...")
        ec2.terminate_instances(InstanceIds=instance_ids)


def delete_ebs(dry_run=False):
    print("Fetching EBS volumes...")
    volumes = ec2.describe_volumes()

    volume_ids = [v['VolumeId'] for v in volumes['Volumes']]

    if not volume_ids:
        print("No EBS volumes found.")
        return

    print(f"Volumes found: {volume_ids}")

    if dry_run:
        print("Dry run enabled. Skipping EBS deletion.")
    else:
        for vol in volume_ids:
            print(f"Deleting volume: {vol}")
            try:
                ec2.delete_volume(VolumeId=vol)
            except Exception as e:
                print(f"Error deleting {vol}: {e}")


def delete_s3(dry_run=False):
    print("Fetching S3 buckets...")
    buckets = s3.list_buckets()

    for bucket in buckets['Buckets']:
        name = bucket['Name']
        print(f"Bucket found: {name}")

        if dry_run:
            print(f"Dry run: skipping bucket {name}")
            continue

        print(f"Deleting bucket: {name}")

        # delete all objects
        objects = s3.list_objects_v2(Bucket=name)
        if 'Contents' in objects:
            for obj in objects['Contents']:
                s3.delete_object(Bucket=name, Key=obj['Key'])

        try:
            s3.delete_bucket(Bucket=name)
        except Exception as e:
            print(f"Error deleting bucket {name}: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python cleanup.py <ec2|ebs|s3> [dryrun]")
        sys.exit(1)

    resource = sys.argv[1].lower()
    dry_run = False

    if len(sys.argv) > 2:
        dry_run = sys.argv[2].lower() == "true"

    print(f"Running cleanup for: {resource}, dry_run={dry_run}")

    if resource == "ec2":
        delete_ec2(dry_run)
    elif resource == "ebs":
        delete_ebs(dry_run)
    elif resource == "s3":
        delete_s3(dry_run)
    else:
        print("Invalid resource type. Use ec2 | ebs | s3")


if __name__ == "__main__":
    main()
