# -*- coding: utf-8 -*-
"""WebSocket message contract shared by the robot bridge and laptop clients.

This module stays valid on Python 2.7 and Python 3. The robot runs the same
file; the laptop installs it as the ``nao-websocket-bridge-protocol`` package.
"""

from __future__ import print_function

import json

SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH_BYTES = 2
FRONT_MIC = 3
AUDIO_ENCODING = "pcm_s16le"
AUDIO_STREAM = "audio"


def websocket_url(ip, port, token=""):
    """WebSocket URL for the robot bridge, including a path token when set."""
    base = "ws://%s:%s" % (ip, port)
    secret = (token or "").strip().strip("/")
    if not secret:
        return base
    return "%s/%s" % (base, secret)


def path_is_authorized(path, token):
    """Accept every path when ``token`` is empty, otherwise require ``/token``."""
    if not token:
        return True
    if not path:
        return False
    raw = path.split("?", 1)[0]
    if len(raw) > 1 and raw.endswith("/"):
        raw = raw[:-1]
    return raw == "/" + token


def audio_format_payload():
    """JSON object sent before the first PCM frame."""
    return {
        "type": "audio_format",
        "encoding": AUDIO_ENCODING,
        "sample_rate": SAMPLE_RATE,
        "channels": CHANNELS,
        "sample_width": SAMPLE_WIDTH_BYTES,
    }


def audio_format_message():
    return json.dumps(audio_format_payload())


def status_message(dropped_chunks, subscribed):
    """JSON text frame sent to the laptop so it can see mic health."""
    return json.dumps({
        "type": "status",
        "dropped_chunks": int(dropped_chunks),
        "subscribed": bool(subscribed),
    })


def validate_audio_format(audio_format):
    """Raise ``ValueError`` when a format object is not front-mic PCM."""
    expected = audio_format_payload()
    for key in expected:
        actual_value = audio_format.get(key)
        expected_value = expected[key]
        if actual_value != expected_value:
            raise ValueError(
                "Unexpected audio format for %s: %r (expected %r)"
                % (key, actual_value, expected_value)
            )
    return audio_format


def message_type(message):
    """Return the ``type`` of a decoded JSON object."""
    if not isinstance(message, dict):
        raise ValueError("text frame must be a JSON object")
    kind = message.get("type")
    if not kind:
        raise ValueError("text frame is missing type")
    return kind
