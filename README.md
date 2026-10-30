# nao-websocket-bridge-protocol

WebSocket message contract for the microphone bridge between a NAO and a laptop. No third-party imports and no type annotations, so the same file loads on the robot's Python 2.7 and as this package on Python 3.10+.

The [bridge install](https://github.com/icampus-wildau/nao-websocket-bridge#install) copies the package onto the robot next to `audio_bridge.py`. Laptops install it from PyPI. [nao-websocket-bridge-client](https://github.com/icampus-wildau/nao-websocket-bridge-client) is the async reader.

```bash
uv add nao-websocket-bridge-protocol
```

Run `uv add` inside an existing Python project, or install into an activated
Python 3.10+ environment on Linux or Windows with
`python -m pip install nao-websocket-bridge-protocol`. Python 2.7 on the NAO
uses the copied source, not this Python 3 package installation.

## Messages

The first frame is text JSON:

```json
{"type": "audio_format", "encoding": "pcm_s16le", "sample_rate": 16000, "channels": 1, "sample_width": 2}
```

Every later binary frame is that PCM: 16 kHz, mono, signed 16-bit little-endian. The bridge also sends status frames:

```json
{"type": "status", "dropped_chunks": 0, "subscribed": true}
```

`dropped_chunks` counts microphone buffers the bridge could not queue. `subscribed` is whether the front microphone is subscribed. `validate_audio_format` checks the keys above and ignores any other fields. `message_type` returns the `type` of a decoded JSON object.

```python
from nao_websocket_bridge_protocol import (
    audio_format_message,
    status_message,
    validate_audio_format,
    websocket_url,
)

websocket_url("192.168.2.50", 8765)             # ws://192.168.2.50:8765
websocket_url("192.168.2.50", 8765, "secret")   # ws://192.168.2.50:8765/secret
```

`path_is_authorized` accepts every path when the token is empty. Otherwise the path must be `/` plus the token.

`SAMPLE_RATE` is 16000, `CHANNELS` is 1, `SAMPLE_WIDTH_BYTES` is 2, and `FRONT_MIC` is 3 (the ALAudioDevice channel the bridge subscribes).

## Local development

With this checkout next to another project:

```bash
uv add --editable ../nao-websocket-bridge-protocol
```

Restore that project's `pyproject.toml` and lockfile before committing. The bridge install copies these files onto the robot on its own.
