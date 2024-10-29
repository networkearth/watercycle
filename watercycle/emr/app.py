import boto3 

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless/client/create_application.html

def create_emr_application(config):
    client = boto3.client('emr-serverless')
    response = client.list_applications()
    collisions = []
    for application in response['applications']:
        if application['name'] == config['name']:
            collisions.append(application['id'])
    if collisions:
        answer = None
        while answer not in ['Y', 'n']:
            answer = input("Name Collisions Found. Overwrite Existing Applications? (Y/n): ")
        if answer == 'Y':
            while collisions:
                client.delete_application(applicationId=collisions.pop(0))
    if not collisions:
        print("Creating Application...")
        response = client.create_application(
            name=config['name'],
            releaseLabel='emr-6.6.0',
            type="SPARK",
            maximumCapacity={
                'cpu': str(config['max_vcpus']),
                'memory': str(config['max_memory']),
                'disk': f"{config['max_disk']}GB",
            },
        )
    else:
        print("Not Creating Application...")
    
