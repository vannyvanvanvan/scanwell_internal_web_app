from flask import Blueprint, Response
from app.functions.redis_config import redis_client
from app.functions.events import CHANNEL_NAME


sse_routes = Blueprint("sse", __name__)


@sse_routes.route("/events")
def sse_stream():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(CHANNEL_NAME)

    def event_stream():
        try:
            for message in pubsub.listen():
                if message and message.get("type") == "message":
                    data = message.get("data")
                    yield f"data: {data}\n\n"
        finally:
            try:
                pubsub.close()
            except Exception:
                pass

    return Response(event_stream(), mimetype="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    })