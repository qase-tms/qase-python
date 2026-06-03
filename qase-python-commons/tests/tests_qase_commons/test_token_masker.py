"""Tests for token_masker — config logging must never leak the API token."""

import json

import pytest

from qase.commons.util.token_masker import mask_token, sanitize_config_for_log


class TestMaskToken:
    def test_long_token_keeps_first_three_and_last_four(self):
        token = "daa20e2e5dd9246712faa2ba3767a8f4f20d5060fea696e6a94734f845be93f3"
        masked = mask_token(token)

        assert masked.startswith("daa")
        assert masked.endswith("93f3")
        assert "****" in masked
        # The original token must not survive anywhere inside the masked form.
        assert token not in masked
        # The mask hides the bulk: only 3+4=7 visible characters out of 64.
        assert len(masked) == len("daa****93f3")

    def test_eight_char_token_is_masked(self):
        assert mask_token("abcd1234") == "abc****1234"

    def test_seven_char_token_fully_hidden(self):
        assert mask_token("1234567") == "*******"

    def test_empty_token_returns_empty(self):
        assert mask_token("") == ""

    def test_non_string_token_is_returned_as_is(self):
        # Defensive: a misconfigured object should not crash the logger.
        assert mask_token(None) is None
        assert mask_token(12345) == 12345


class TestSanitizeConfigForLog:
    def _sample_payload(self, token):
        return {
            "mode": "testops",
            "testops": {
                "api": {
                    "host": "qase.io",
                    "token": token,
                },
                "batch": {"size": 1},
            },
        }

    def test_masks_token_in_serialised_config(self):
        payload = self._sample_payload(
            "daa20e2e5dd9246712faa2ba3767a8f4f20d5060fea696e6a94734f845be93f3"
        )
        out = sanitize_config_for_log(json.dumps(payload))

        parsed = json.loads(out)
        assert parsed["testops"]["api"]["token"] == "daa****93f3"
        # Host and other fields must remain intact.
        assert parsed["testops"]["api"]["host"] == "qase.io"
        assert parsed["mode"] == "testops"
        # The original token must not appear anywhere in the log line.
        assert payload["testops"]["api"]["token"] not in out

    def test_returns_string_when_token_absent(self):
        payload = {"mode": "off", "testops": {"api": {"host": "qase.io"}}}
        out = sanitize_config_for_log(json.dumps(payload))

        # Token missing -> nothing to mask, but still valid JSON output.
        parsed = json.loads(out)
        assert "token" not in parsed["testops"]["api"]

    def test_handles_null_token_without_mutating(self):
        payload = self._sample_payload(None)
        out = sanitize_config_for_log(json.dumps(payload))

        parsed = json.loads(out)
        assert parsed["testops"]["api"]["token"] is None

    def test_falls_back_to_str_for_unparseable_input(self):
        class Weird:
            def __str__(self):
                return "<not json>"

        # Must not raise — logging must keep working even on a serialisation bug.
        assert sanitize_config_for_log(Weird()) == "<not json>"

    def test_accepts_object_with_json_str(self):
        class Cfg:
            def __str__(self):
                return json.dumps(
                    {"testops": {"api": {"token": "abcdefghij", "host": "qase.io"}}}
                )

        out = sanitize_config_for_log(Cfg())
        parsed = json.loads(out)
        assert parsed["testops"]["api"]["token"] == "abc****ghij"
