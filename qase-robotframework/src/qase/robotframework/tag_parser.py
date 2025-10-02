import json
import re

from .models import TestMetadata


class TagParser:
    @staticmethod
    def parse_tags(tags: list[str], logger=None) -> TestMetadata:
        metadata = TestMetadata()
        for tag in tags:
            if tag.lower().startswith("q-"):
                qase_id = TagParser.__extract_ids(tag)
                if qase_id is not None:
                    metadata.qase_ids.append(qase_id)

            if tag.lower() == "qase.ignore":
                metadata.ignore = True

            if tag.lower().startswith("qase.fields"):
                metadata.fields = TagParser.__extract_fields(tag, logger)

            if tag.lower().startswith("qase.params"):
                metadata.params = TagParser.__extract_params(tag, logger)

        return metadata

    @staticmethod
    def __extract_ids(tag: str) -> int or None:
        qase_id = re.compile(r"Q-(\d+)", re.IGNORECASE)
        if qase_id.fullmatch(tag):
            return int(qase_id.match(tag).groups()[0])

        return None

    @staticmethod
    def __extract_fields(tag: str, logger=None) -> dict:
        value = tag.split(':', 1)[-1].strip()
        try:
            return json.loads(value)
        except ValueError as e:
            # Use logger if available, otherwise fallback to print for critical errors
            if logger:
                logger.log_error(f"Error parsing fields from tag '{tag}': {e}")
            else:
                print(f"CRITICAL: Error parsing fields from tag '{tag}': {e}")
            return {}

    @staticmethod
    def __extract_params(tag: str, logger=None) -> list[str]:
        value = tag.split(':', 1)[-1].strip()
        try:
            # Remove square brackets and split by comma
            if value.startswith('[') and value.endswith(']'):
                params_str = value[1:-1]
                return [item.strip() for item in params_str.split(",") if item.strip()]
            else:
                # Handle case without brackets
                return [item.strip() for item in value.split(",") if item.strip()]
        except (ValueError, IndexError) as e:
            # Use logger if available, otherwise fallback to print for critical errors
            if logger:
                logger.log_error(f"Error parsing params from tag '{tag}': {e}")
            else:
                print(f"CRITICAL: Error parsing params from tag '{tag}': {e}")
            return []
