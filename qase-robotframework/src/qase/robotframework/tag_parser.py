import json
import re

from .models import TestMetadata


class TagParser:
    @staticmethod
    def parse_tags(tags: list[str], logger=None) -> TestMetadata:
        metadata = TestMetadata()
        for tag in tags:
            tag_lower = tag.lower()
            
            # Check for project IDs first: Q-PROJECT.PROJ1-123,124
            if tag_lower.startswith("q-project."):
                project_result = TagParser.__extract_project_ids(tag)
                if project_result:
                    project_code, testops_ids = project_result
                    if project_code not in metadata.qase_multi_ids:
                        metadata.qase_multi_ids[project_code] = []
                    metadata.qase_multi_ids[project_code].extend(testops_ids)
                continue

            if tag_lower.startswith("q-") and not tag_lower.startswith("q-project."):
                qase_id = TagParser.__extract_ids(tag)
                if qase_id is not None:
                    metadata.qase_ids.append(qase_id)

            if tag_lower == "qase.ignore":
                metadata.ignore = True

            if tag_lower.startswith("qase.fields"):
                metadata.fields = TagParser.__extract_fields(tag, logger)

            if tag_lower.startswith("qase.params"):
                metadata.params = TagParser.__extract_params(tag, logger)

        return metadata

    @staticmethod
    def __extract_ids(tag: str) -> int or None:
        qase_id = re.compile(r"Q-(\d+)", re.IGNORECASE)
        if qase_id.fullmatch(tag):
            return int(qase_id.match(tag).groups()[0])

        return None

    @staticmethod
    def __extract_project_ids(tag: str) -> tuple or None:
        """
        Extract project IDs from tag.
        Format: Q-PROJECT.PROJ1-123,124 or Q-PROJECT.PROJ1-123
        Returns: (project_code, [testops_ids]) or None
        """
        # Pattern: Q-PROJECT.PROJECT_CODE-ID1,ID2,ID3
        pattern = re.compile(r"Q-PROJECT\.([A-Za-z0-9_]+)-([\d,]+)", re.IGNORECASE)
        match = pattern.fullmatch(tag)
        if match:
            project_code = match.group(1)
            ids_str = match.group(2)
            testops_ids = [int(id.strip()) for id in ids_str.split(',') if id.strip()]
            if project_code and testops_ids:
                return (project_code, testops_ids)
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
