import boto3
from tabulate import tabulate

# Function to save data to a file
def save_data_to_file(filename, data):
    with open(filename, 'w') as file:
        for item in data:
            file.write("%s\n" % item)

# Prompt for AWS Access Key ID and Secret Access Key
aws_access_key_id = input("Enter your AWS Access Key ID: ")
aws_secret_access_key = input("Enter your AWS Secret Access Key: ")
aws_region = input("Enter your AWS Region: ")  # Prompt for the AWS Region

# Create a Boto3 IAM client with the provided credentials and region
iam = boto3.client('iam', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

try:
    # First Scan: List all IAM users and save the results to a file
    first_scan_response = iam.list_users()
    first_scan_data = []

    for user in first_scan_response['Users']:
        username = user['UserName']
        access_keys = iam.list_access_keys(UserName=username)['AccessKeyMetadata']
        last_activity = max(key['CreateDate'] for key in access_keys) if access_keys else "N/A"
        creation_time = user['CreateDate'].strftime('%Y-%m-%d %H:%M:%S')
        first_scan_data.append([username, last_activity, creation_time])

    first_scan_file = "first_scan_results.txt"
    save_data_to_file(first_scan_file, first_scan_data)
    print(f"First scan results saved to {first_scan_file}")

    # Prompt for permission to perform the second scan
    input("Press Enter to perform the second scan...")

    # Second Scan: List all IAM users again and save the results to a different file
    second_scan_response = iam.list_users()
    second_scan_data = []

    for user in second_scan_response['Users']:
        username = user['UserName']
        access_keys = iam.list_access_keys(UserName=username)['AccessKeyMetadata']
        last_activity = max(key['CreateDate'] for key in access_keys) if access_keys else "N/A"
        creation_time = user['CreateDate'].strftime('%Y-%m-%d %H:%M:%S')
        second_scan_data.append([username, last_activity, creation_time])

    second_scan_file = "second_scan_results.txt"
    save_data_to_file(second_scan_file, second_scan_data)
    print(f"Second scan results saved to {second_scan_file}")

    # Compare the two files and show the differences in a table
    with open(first_scan_file, 'r') as file1, open(second_scan_file, 'r') as file2:
        first_scan_lines = set(file1.readlines())
        second_scan_lines = set(file2.readlines())

    differences = list(second_scan_lines - first_scan_lines)
    
    if differences:
        print("Differences between the two scans:")
        print(tabulate(differences, headers=["Username", "Last Activity", "Creation Time"], tablefmt="grid"))
    else:
        print("No differences found between the two scans.")

except Exception as e:
    print(f"An error occurred: {str(e)}")
