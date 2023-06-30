# -*- coding: utf-8 -*-
import json
import os

from jiant.utils import config_handlers

BASE_PATH = os.path.dirname(__file__)

def load_json(path):
    with open(path, 'r') as file:
        return json.load(file)

def test_json_merge_patch():
    """Tests that JSON Merge Patch works as expected (https://tools.ietf.org/html/rfc7396)"""
    target = {
        "title": "Goodbye!",
        "author" : {
            "givenName" : "John",
            "familyName" : "Doe"
        },
        "tags": [ "example", "sample" ],
        "content": "This will be unchanged"
    }
    
    patch = {
        "title": "Hello!",
        "phoneNumber": "+01-123-456-7890",
        "author": {
            "familyName": None
        },
        "tags": [ "example" ]
    }
    
    merged = config_handlers.json_merge_patch(json.dumps(target), json.dumps(patch))
    
    expected = {
        "title": "Hello!",
        "author" : {
            "givenName" : "John"
        },
        "tags": [ "example" ],
        "content": "This will be unchanged",
        "phoneNumber": "+01-123-456-7890"
    }
    
    assert json.dumps(json.loads(merged), sort_keys=True) == json.dumps(expected, sort_keys=True)


def test_merging_multiple_json_configs():
    base_config = load_json(os.path.join(BASE_PATH, "config/base_config.json"))
    override_config_1 = load_json(os.path.join(BASE_PATH, "./config/first_override_config.json"))
    override_config_2 = load_json(os.path.join(BASE_PATH, "./config/second_override_config.json"))
    
    merged_config = config_handlers.merge_jsons_in_order(
        [json.dumps(base_config), json.dumps(override_config_1), json.dumps(override_config_2)]
    )
    
    expected_config = load_json(os.path.join(BASE_PATH, "./config/final_config.json"))
    
    assert json.dumps(json.loads(merged_config), sort_keys=True) == json.dumps(expected_config, sort_keys=True)
