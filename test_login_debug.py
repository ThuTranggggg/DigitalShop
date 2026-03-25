#!/usr/bin/env python
import requests
import json
import sys

def test_login():
    """Test login endpoint with different configurations"""
    
    tests = [
        {
            "name": "Test 1: With explicit Content-Type",
            "url": "http://localhost:8002/customers/login/",
            "payload": {"username": "customer01", "password": "customer123"},
            "headers": {"Content-Type": "application/json"},
            "use_json": True
        },
        {
            "name": "Test 2: Via api-gateway proxy",
            "url": "http://localhost:8000/api/customers/login/",
            "payload": {"username": "customer01", "password": "customer123"},
            "headers": {"Content-Type": "application/json"},
            "use_json": True
        },
        {
            "name": "Test 3: With wrong password",
            "url": "http://localhost:8002/customers/login/",
            "payload": {"username": "customer01", "password": "wrong"},
            "headers": {"Content-Type": "application/json"},
            "use_json": True
        }
    ]
    
    for test in tests:
        print(f"\n{'='*60}")
        print(f"{test['name']}")
        print(f"{'='*60}")
        
        try:
            if test["use_json"]:
                r = requests.post(test["url"], json=test["payload"], headers=test["headers"], timeout=5)
            else:
                r = requests.post(test["url"], data=json.dumps(test["payload"]), headers=test["headers"], timeout=5)
            
            print(f"Status Code: {r.status_code}")
            print(f"Headers: {dict(r.headers)}")
            print(f"Response Body:")
            try:
                resp_json = r.json()
                print(json.dumps(resp_json, indent=2))
            except:
                print(r.text)
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_login()
