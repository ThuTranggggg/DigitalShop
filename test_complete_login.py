#!/usr/bin/env python3
"""
Simulates complete login flow with detailed logging
"""
import requests
import json
from datetime import datetime

def log(msg, level="INFO"):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [{level}] {msg}")

def test_complete_login_flow():
    """Simulate complete customer login flow"""
    
    BASE_URL = "http://localhost:8000"
    credentials = {"username": "customer01", "password": "customer123"}
    
    log("="*70, "TEST")
    log("SIMULATING COMPLETE CUSTOMER LOGIN FLOW", "TEST")
    log("="*70, "TEST")
    
    # Step 1: Login
    log(f"Step 1: POST /api/customers/login/ with credentials: {credentials['username']}/***")
    try:
        r = requests.post(
            f"{BASE_URL}/api/customers/login/",
            json=credentials,
            timeout=5
        )
        log(f"Response Status: {r.status_code}", "HTTP")
        login_response = r.json()
        log(f"Response Keys: {list(login_response.keys())}", "DEBUG")
        
        if r.status_code != 200:
            log(f"ERROR: Login failed with status {r.status_code}", "ERROR")
            log(f"Response: {json.dumps(login_response, indent=2)}", "ERROR")
            return False
            
        # Extract data
        if login_response.get('success') != True:
            log("ERROR: success field is not True", "ERROR")
            return False
            
        login_data = login_response.get('data', {})
        if not login_data:
            log("ERROR: No data field in response", "ERROR")
            return False
            
        token = login_data.get('access')
        customer = login_data.get('customer')
        
        if not token:
            log("ERROR: No access token in response", "ERROR")
            return False
            
        log(f"✓ Login successful, got token: {token[:50]}...", "SUCCESS")
        log(f"✓ Customer profile: {customer.get('full_name')} ({customer.get('username')})", "SUCCESS")
        
    except requests.exceptions.Timeout:
        log("ERROR: Login request timeout (5 seconds)", "ERROR")
        return False
    except Exception as e:
        log(f"ERROR: {type(e).__name__}: {e}", "ERROR")
        return False
    
    # Step 2: Ensure cart
    log(f"\nStep 2: POST /api/customers/cart/ (ensureCart)")
    try:
        r = requests.post(
            f"{BASE_URL}/api/customers/cart/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        log(f"Response Status: {r.status_code}", "HTTP")
        cart_response = r.json()
        
        if r.status_code != 201 and r.status_code != 200:
            log(f"WARNING: Unexpected status {r.status_code}", "WARN")
            log(f"Response: {cart_response}", "DEBUG")
        else:
            log("✓ Cart ensured successfully", "SUCCESS")
            
    except requests.exceptions.Timeout:
        log("ERROR: Cart request timeout (5 seconds)", "ERROR")
        return False
    except Exception as e:
        log(f"ERROR: {type(e).__name__}: {e}", "ERROR")
        return False
    
    # Step 3: Fetch cart summary
    log(f"\nStep 3: GET /api/customers/cart/summary/")
    try:
        r = requests.get(
            f"{BASE_URL}/api/customers/cart/summary/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        log(f"Response Status: {r.status_code}", "HTTP")
        cart_summary = r.json()
        
        if r.status_code != 200:
            log(f"ERROR: Failed to fetch cart summary", "ERROR")
            return False
        
        cart_data = cart_summary.get('data', {})
        log(f"✓ Cart summary fetched", "SUCCESS")
        log(f"  - Total items: {cart_data.get('total_items', 0)}", "DEBUG")
        log(f"  - Total amount: {cart_data.get('total_amount', 0)}", "DEBUG")
            
    except requests.exceptions.Timeout:
        log("ERROR: Cart summary request timeout (5 seconds)", "ERROR")
        return False
    except Exception as e:
        log(f"ERROR: {type(e).__name__}: {e}", "ERROR")
        return False
    
    # Step 4: Fetch customer products
    log(f"\nStep 4: GET /api/customers/laptops/")
    try:
        r = requests.get(
            f"{BASE_URL}/api/customers/laptops/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        log(f"Response Status: {r.status_code}", "HTTP")
        
        if r.status_code != 200:
            log(f"ERROR: Failed to fetch products", "ERROR")
            products_response = r.json()
            log(f"Response: {products_response}", "DEBUG")
            return False
        
        products_response = r.json()
        products = products_response.get('data', [])
        log(f"✓ Products fetched successfully", "SUCCESS")
        log(f"  - Total products: {len(products)}", "DEBUG")
        if products:
            log(f"  - First product: {products[0].get('name', 'N/A')}", "DEBUG")
            
    except requests.exceptions.Timeout:
        log("ERROR: Products request timeout (5 seconds)", "ERROR")
        return False
    except Exception as e:
        log(f"ERROR: {type(e).__name__}: {e}", "ERROR")
        return False
    
    log("\n" + "="*70, "TEST")
    log("✓ COMPLETE LOGIN FLOW SUCCESS", "SUCCESS")
    log("="*70, "TEST")
    return True

if __name__ == "__main__":
    success = test_complete_login_flow()
    exit(0 if success else 1)
