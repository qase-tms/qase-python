import pytest
from qaseio.commons import QaseUtils

def test_build_tree_empty_items():
    items = {}
    tree = QaseUtils.build_tree(items)
    assert tree == {}

def test_build_tree_no_parent():
    items = {
        '1': {'name': 'step1'},
        '2': {'name': 'step2'}
    }
    tree = QaseUtils.build_tree(items)
    assert tree == items

def test_build_tree_with_parent():
    items = {
        '1': {'name': 'step1', 'steps': {}},
        '2': {'name': 'step2', 'parent_id': '1', 'steps': {}}
    }
    tree = QaseUtils.build_tree(items)
    expected_tree = {
        '1': {
            'name': 'step1',
            'steps': {
                '2': {
                    'name': 'step2',
                    'parent_id': '1',
                    'steps': {}
                }
            }
        }
    }
    assert tree == expected_tree

def test_build_tree_multiple_levels():
    items = {
        '1': {'name': 'step1', 'steps': {}},
        '2': {'name': 'step2', 'parent_id': '1', 'steps': {}},
        '3': {'name': 'step3', 'parent_id': '2', 'steps': {}}
    }
    tree = QaseUtils.build_tree(items)
    expected_tree = {
        '1': {
            'name': 'step1',
            'steps': {
                '2': {
                    'name': 'step2',
                    'parent_id': '1',
                    'steps': {
                        '3': {
                            'name': 'step3',
                            'parent_id': '2',
                            'steps': {}
                        }
                    }
                }
            }
        }
    }
    assert tree == expected_tree