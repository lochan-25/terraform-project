import boto3

def get_ec2_instances(ec2):
    return ec2.describe_instances()['Reservations']

def get_ebs_volumes(ec2):
    return ec2.describe_volumes()['Volumes']

def get_elastic_ips(ec2):
    return ec2.describe_addresses()['Addresses']

def get_snapshots(ec2):
    return ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

def has_tag(tags, key, value):
    return any(tag.get('Key') == key and tag.get('Value') == value for tag in tags or [])

def cleanup_tagged_ec2_instances(ec2, instances, tag_key, tag_value, dry_run=False):
    matching = [inst for reservation in instances for inst in reservation['Instances'] if has_tag(inst.get('Tags'), tag_key, tag_value)]

    for instance in matching:
        print(f"Terminating EC2 Instance ID: {instance['InstanceId']} (state={instance['State']['Name']})")
        if not dry_run:
            ec2.terminate_instances(InstanceIds=[instance['InstanceId']])
            print(f"Terminated EC2 Instance ID: {instance['InstanceId']}")

def cleanup_tagged_ebs_volumes(ec2, volumes, tag_key, tag_value, dry_run=False):
    matching = [vol for vol in volumes if has_tag(vol.get('Tags'), tag_key, tag_value)]

    for volume in matching:
        if volume.get('Attachments'):
            print(f"Skipping attached EBS Volume ID: {volume['VolumeId']}")
            continue

        print(f"Deleting EBS Volume ID: {volume['VolumeId']}")
        if not dry_run:
            ec2.delete_volume(VolumeId=volume['VolumeId'])
            print(f"Deleted EBS Volume ID: {volume['VolumeId']}")

def cleanup_tagged_elastic_ips(ec2, elastic_ips, tag_key, tag_value, dry_run=False):
    for ip in elastic_ips:
        if has_tag(ip.get('Tags'), tag_key, tag_value):
            allocation_id = ip['AllocationId']
            if ip.get('InstanceId') and ip.get('AssociationId'):
                print(f"Disassociating Elastic IP: {allocation_id} from instance {ip['InstanceId']}")
                if not dry_run:
                    ec2.disassociate_address(AssociationId=ip['AssociationId'])
            print(f"Releasing Elastic IP Allocation ID: {allocation_id}")
            if not dry_run:
                ec2.release_address(AllocationId=allocation_id)
                print(f"Released Elastic IP Allocation ID: {allocation_id}")

def cleanup_tagged_snapshots(ec2, snapshots, tag_key, tag_value, dry_run=False):
    matching = [snap for snap in snapshots if has_tag(snap.get('Tags'), tag_key, tag_value)]

    for snapshot in matching:
        print(f"Deleting Snapshot ID: {snapshot['SnapshotId']}")
        if not dry_run:
            ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            print(f"Deleted Snapshot ID: {snapshot['SnapshotId']}")

def main():
    session = boto3.Session()
    ec2 = session.client('ec2')

    instances = get_ec2_instances(ec2)
    volumes = get_ebs_volumes(ec2)
    elastic_ips = get_elastic_ips(ec2)
    snapshots = get_snapshots(ec2)

    dry_run = input("Perform dry run? (yes/no): ").strip().lower() == 'yes'
    tag_key = 'Name'
    tag_value = 'terraform-example'

    cleanup_tagged_ec2_instances(ec2, instances, tag_key, tag_value, dry_run=dry_run)
    cleanup_tagged_ebs_volumes(ec2, volumes, tag_key, tag_value, dry_run=dry_run)
    cleanup_tagged_elastic_ips(ec2, elastic_ips, tag_key, tag_value, dry_run=dry_run)
    cleanup_tagged_snapshots(ec2, snapshots, tag_key, tag_value, dry_run=dry_run)

if __name__ == "__main__":
    main()