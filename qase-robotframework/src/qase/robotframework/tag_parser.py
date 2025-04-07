import json
import logging
import re

from .models import TestMetadata


class TagParser:
    __logger = logging.getLogger("qase-robotframework")

    @staticmethod
    def parse_tags(tags: list[str]) -> TestMetadata:
        metadata = TestMetadata()
        for tag in tags:
            if tag.lower().startswith("q-"):
                qase_id = TagParser.__extract_ids(tag)
                if qase_id is not None:
                    metadata.qase_ids.append(qase_id)

            if tag.lower() == "qase.ignore":
                metadata.ignore = True

            if tag.lower().startswith("qase.fields"):
                metadata.fields = TagParser.__extract_fields(tag)

            if tag.lower().startswith("qase.params"):
                metadata.params = TagParser.__extract_params(tag)

        return metadata

    @staticmethod
    def __extract_ids(tag: str) -> int or None:
        qase_id = re.compile(r"Q-(\d+)", re.IGNORECASE)
        if qase_id.fullmatch(tag):
            return int(qase_id.match(tag).groups()[0])

        return None

    @staticmethod
    def __extract_fields(tag: str) -> dict:
        value = tag.split(':', 1)[-1].strip()
        try:
            return json.loads(value)
        except ValueError as e:
            TagParser.__logger.error(f"Error parsing fields from tag '{tag}': {e}")
            return {}

    @staticmethod
    def __extract_params(tag: str) -> list[str]:
        value = tag.split(':', 1)[-1].strip()
        try:
            return [item.strip() for item in value[1:-1].split(",")]
        except ValueError as e:
            TagParser.__logger.error(f"Error parsing params from tag '{tag}': {e}")
            return []
