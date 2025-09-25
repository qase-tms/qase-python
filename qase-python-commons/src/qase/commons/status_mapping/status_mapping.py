"""
Status mapping utilities for Qase Python Commons.

This module provides functionality to map test result statuses from one value to another
based on configuration. This is useful for standardizing status values across different
testing frameworks or for custom status transformations.
"""

from typing import Dict, Optional, List
import os
import logging


class StatusMappingError(Exception):
    """Exception raised when status mapping encounters an error."""
    pass


class StatusMapping:
    """
    Handles mapping of test result statuses.
    
    This class provides functionality to:
    - Parse status mapping from configuration
    - Validate status mappings
    - Apply status mappings to test results
    - Support both JSON configuration and environment variables
    """
    
    # Valid statuses that can be mapped
    VALID_STATUSES = {
        'passed', 'failed', 'skipped', 'disabled', 'blocked', 'invalid'
    }
    
    def __init__(self, mapping: Optional[Dict[str, str]] = None):
        """
        Initialize StatusMapping with optional mapping dictionary.
        
        Args:
            mapping: Dictionary mapping source status to target status
        """
        self.mapping = mapping or {}
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_dict(cls, mapping_dict: Dict[str, str]) -> 'StatusMapping':
        """
        Create StatusMapping from dictionary.
        
        Args:
            mapping_dict: Dictionary with status mappings
            
        Returns:
            StatusMapping instance
            
        Raises:
            StatusMappingError: If mapping contains invalid statuses
        """
        instance = cls()
        instance.set_mapping(mapping_dict)
        return instance
    
    @classmethod
    def from_env_string(cls, env_string: str) -> 'StatusMapping':
        """
        Create StatusMapping from environment variable string.
        
        Expected format: "source1=target1,source2=target2"
        
        Args:
            env_string: Environment variable string
            
        Returns:
            StatusMapping instance
            
        Raises:
            StatusMappingError: If string format is invalid
        """
        instance = cls()
        instance.parse_env_string(env_string)
        return instance
    
    def set_mapping(self, mapping_dict: Dict[str, str]) -> None:
        """
        Set status mapping from dictionary.
        
        Args:
            mapping_dict: Dictionary with status mappings
            
        Raises:
            StatusMappingError: If mapping contains invalid statuses
        """
        if not isinstance(mapping_dict, dict):
            raise StatusMappingError("Mapping must be a dictionary")
        
        # Validate all statuses in the mapping
        for source_status, target_status in mapping_dict.items():
            if source_status not in self.VALID_STATUSES:
                raise StatusMappingError(f"Invalid source status: {source_status}")
            if target_status not in self.VALID_STATUSES:
                raise StatusMappingError(f"Invalid target status: {target_status}")
        
        self.mapping = mapping_dict.copy()
        self.logger.debug(f"Status mapping set: {self.mapping}")
    
    def parse_env_string(self, env_string: str) -> None:
        """
        Parse status mapping from environment variable string.
        
        Expected format: "source1=target1,source2=target2"
        
        Args:
            env_string: Environment variable string
            
        Raises:
            StatusMappingError: If string format is invalid
        """
        if not env_string or not env_string.strip():
            self.mapping = {}
            return
        
        mapping_dict = {}
        pairs = env_string.split(',')
        
        for pair in pairs:
            pair = pair.strip()
            if not pair:
                continue
                
            if '=' not in pair:
                raise StatusMappingError(f"Invalid mapping format: {pair}. Expected 'source=target'")
            
            source_status, target_status = pair.split('=', 1)
            source_status = source_status.strip()
            target_status = target_status.strip()
            
            if not source_status or not target_status:
                raise StatusMappingError(f"Empty status in mapping: {pair}")
            
            mapping_dict[source_status] = target_status
        
        self.set_mapping(mapping_dict)
    
    def apply_mapping(self, status: str) -> str:
        """
        Apply status mapping to a given status.
        
        Args:
            status: Original status
            
        Returns:
            Mapped status if mapping exists, otherwise original status
        """
        if not status:
            return status
        
        if status in self.mapping:
            mapped_status = self.mapping[status]
            self.logger.debug(f"Status mapped: {status} -> {mapped_status}")
            return mapped_status
        
        return status
    
    def get_mapping(self) -> Dict[str, str]:
        """
        Get current status mapping.
        
        Returns:
            Dictionary with current status mappings
        """
        return self.mapping.copy()
    
    def is_empty(self) -> bool:
        """
        Check if mapping is empty.
        
        Returns:
            True if no mappings are defined
        """
        return len(self.mapping) == 0
    
    def validate(self) -> List[str]:
        """
        Validate current mapping and return any issues.
        
        Returns:
            List of validation error messages
        """
        errors = []
        
        for source_status, target_status in self.mapping.items():
            if source_status not in self.VALID_STATUSES:
                errors.append(f"Invalid source status: {source_status}")
            if target_status not in self.VALID_STATUSES:
                errors.append(f"Invalid target status: {target_status}")
        
        return errors
    
    def __str__(self) -> str:
        """String representation of the mapping."""
        return str(self.mapping)
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"StatusMapping({self.mapping})"


def create_status_mapping_from_config(config_value: Optional[Dict[str, str]]) -> StatusMapping:
    """
    Create StatusMapping from configuration value.
    
    Args:
        config_value: Configuration dictionary or None
        
    Returns:
        StatusMapping instance
    """
    if config_value is None:
        return StatusMapping()
    
    return StatusMapping.from_dict(config_value)


def create_status_mapping_from_env(env_var_name: str = 'STATUS_MAPPING') -> StatusMapping:
    """
    Create StatusMapping from environment variable.
    
    Args:
        env_var_name: Name of environment variable
        
    Returns:
        StatusMapping instance
    """
    env_value = os.getenv(env_var_name)
    if env_value:
        return StatusMapping.from_env_string(env_value)
    return StatusMapping()
