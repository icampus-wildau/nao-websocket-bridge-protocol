# nao-websocket-bridge-protocol

*WebSocket message contract for the microphone bridge between a NAO and a laptop.*

![PyPI](https://img.shields.io/pypi/v/nao-websocket-bridge-protocol?style=flat-square)
![Python](https://img.shields.io/badge/python-2.7%20%7C%203.10%2B-blue?style=flat-square)
![CI](https://img.shields.io/github/actions/workflow/status/icampus-wildau/nao-websocket-bridge-protocol/pypi.yml?style=flat-square&label=CI)
![License: Apache 2.0](https://img.shields.io/badge/license-Apache%20License%202.0-blue)

No third-party imports and no type annotations, so the same file loads on the robot's Python 2.7 and on Python 3. The [bridge install](https://github.com/icampus-wildau/nao-websocket-bridge#install-from-a-laptop) copies the package onto the robot next to `audio_bridge.py`. Laptops install it from PyPI. [nao-websocket-bridge-client](https://github.com/icampus-wildau/nao-websocket-bridge-client) is the async reader.

## Install

```bash
uv add nao-websocket-bridge-protocol
# or, in an activated Python 3.10+ environment:
python -m pip install nao-websocket-bridge-protocol
```

Python 2.7 on the NAO uses the copied source, not this install.

## Messages

The first frame is text JSON. Later binary frames are that PCM. Status is another text frame, about every 5 seconds on the bridge. `version` is omitted when empty.

```json
{"type": "audio_format", "encoding": "pcm_s16le", "sample_rate": 16000, "channels": 1, "sample_width": 2}
{"type": "status", "dropped_chunks": 0, "subscribed": true}
```

`dropped_chunks` counts microphone buffers the bridge could not queue. `subscribed` is whether the front microphone is subscribed.

```python
from nao_websocket_bridge_protocol import (
    audio_format_message,
    status_message,
    validate_audio_format,
    websocket_url,
)

websocket_url("192.168.2.50", 8765)            # ws://192.168.2.50:8765
websocket_url("192.168.2.50", 8765, "secret")  # ws://192.168.2.50:8765/secret

announce = audio_format_message()
# Raises ValueError when a key disagrees. Extra keys are ignored.
validate_audio_format({"type": "audio_format", "encoding": "pcm_s16le",
                       "sample_rate": 16000, "channels": 1, "sample_width": 2})

status_message(0, True)          # no version field
status_message(0, True, "1.1.0") # adds "version"
```

`path_is_authorized` accepts every path when the token is empty. Otherwise the path must be `/` plus the token.

`SAMPLE_RATE` is 16000, `CHANNELS` is 1, `SAMPLE_WIDTH_BYTES` is 2, and `FRONT_MIC` is 3 (the ALAudioDevice channel the bridge subscribes).

## Local development

```bash
uv add --editable ../nao-websocket-bridge-protocol
```

Restore that project's `pyproject.toml` and lockfile before committing. The bridge install copies these files onto the robot on its own.
