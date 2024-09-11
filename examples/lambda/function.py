def handler(event, context):
    print("Hello, CDK!")
    return {
        'statusCode': 200,
        'body': 'Hello, World!'
    }