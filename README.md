# nao-websocket-bridge-protocol

Dependency-free contract for the WebSocket bridge between a NAO and a laptop.

The same source is copied onto the robot (Python 2.7) by `nao-websocket-bridge`'s install script and installed on the laptop as this package. It has no third-party imports and no type annotations, so both interpreters can load it.

Text frames are JSON objects. Binary frames are the payload of one stream. Audio is the only binary stream: 16 kHz mono PCM S16LE. A later stream can add a `stream` field; parsers ignore fields they do not know.

Until that second stream exists, the audio format and status objects keep their current keys (`type`, `encoding`, `sample_rate`, `channels`, `sample_width`, `dropped_chunks`, `subscribed`).

## Local development

From the other project, with the checkouts side by side:

```bash
uv add --editable ../nao-websocket-bridge-protocol
```

Restore that project's `pyproject.toml` and lockfile before committing. The committed dependency stays the PyPI release. The copy onto the robot is still a file copy, not this install.
