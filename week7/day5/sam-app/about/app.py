import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "course": "Week 7",
            "topic": "Deployment with AWS SAM",
            "status": "Learning"
        })
    }

