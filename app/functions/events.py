from typing import Any, Dict, Optional
import json
from app.functions.redis_config import redis_client


CHANNEL_NAME = "realtime_updates"


def publish_update(event_type: str, payload: Optional[Dict[str, Any]] = None, actor_id: Optional[int] = None) -> None:
    message = {"type": event_type}
    if payload:
        message["payload"] = payload
    if actor_id is not None:
        message["actor_id"] = actor_id
    try:
        redis_client.publish(CHANNEL_NAME, json.dumps(message))
    except Exception:
        pass