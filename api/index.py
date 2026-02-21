import json

def handler(request, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "status": "ok",
            "version": "39.0-HANDSHAKE-SUCCESS",
            "message": "Python Runtime Handshake Successful",
            "method": request.get('method', 'GET') if isinstance(request, dict) else 'Unknown'
        })
    }
