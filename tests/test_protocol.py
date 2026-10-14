from __future__ import annotations

import json
import unittest

from nao_websocket_bridge_protocol import (
    audio_format_message,
    message_type,
    path_is_authorized,
    status_message,
    validate_audio_format,
    websocket_url,
)


class ProtocolTests(unittest.TestCase):
    def test_websocket_url_appends_a_token_path(self) -> None:
        self.assertEqual(websocket_url("10.0.0.5", 8765, ""), "ws://10.0.0.5:8765")
        self.assertEqual(
            websocket_url("10.0.0.5", 8765, " booth-secret/ "),
            "ws://10.0.0.5:8765/booth-secret",
        )

    def test_path_token(self) -> None:
        self.assertTrue(path_is_authorized("/anything", ""))
        self.assertTrue(path_is_authorized("/secret/", "secret"))
        self.assertFalse(path_is_authorized("/other", "secret"))

    def test_status_and_format_round_trip(self) -> None:
        status = json.loads(status_message(4, True))
        self.assertEqual(
            status,
            {"type": "status", "dropped_chunks": 4, "subscribed": True},
        )
        self.assertEqual(message_type(status), "status")
        audio_format = json.loads(audio_format_message())
        self.assertEqual(validate_audio_format(audio_format)["sample_rate"], 16000)

    def test_format_rejects_a_different_rate(self) -> None:
        audio_format = json.loads(audio_format_message())
        audio_format["sample_rate"] = 8000
        with self.assertRaises(ValueError):
            validate_audio_format(audio_format)


if __name__ == "__main__":
    unittest.main()
