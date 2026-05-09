#!/usr/bin/env python3
"""
API Security Scanner - A CLI tool for basic API security testing
"""
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin

# Security headers to check
SECURITY_HEADERS = [
    'Content-Security-Policy',
    'X-Frame-Options',
    'Strict-Transport-Security',
    'X-Content-Type-Options'
]

class APIScanner:
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.results = []
    
    def scan_endpoint(self, endpoint):
        """Scan a single endpoint for security issues"""
        url = urljoin(self.base_url, endpoint)
        result = {
            'endpoint': endpoint,
            'url': url,
            'status_code': None,
            'auth_required': False,
            'missing_headers': [],
            'present_headers': [],
            'warnings': []
        }
        
        try:
            response = requests.get(url, timeout=self.timeout, allow_redirects=False)
            result['status_code'] = response.status_code
            
            # Check authentication requirement
            if response.status_code in [401, 403]:
                result['auth_required'] = True
            
            # Check security headers
            for header in SECURITY_HEADERS:
                if header in response.headers:
                    result['present_headers'].append(header)
                else:
                    result['missing_headers'].append(header)
            
            # Detect warnings
            if response.status_code == 200 and not result['auth_required']:
                if 'admin' in endpoint.lower() or 'config' in endpoint.lower():
                    result['warnings'].append('Sensitive endpoint publicly accessible')
                else:
                    result['warnings'].append('Public endpoint exposed')
            
            if response.status_code == 500:
                result['warnings'].append('Server error - possible misconfiguration')
                
        except requests.exceptions.Timeout:
            result['warnings'].append('Request timeout')
        except requests.exceptions.ConnectionError:
            result['warnings'].append('Connection failed')
        except Exception as e:
            result['warnings'].append(f'Error: {str(e)}')
        
        return result
    
    def scan_endpoints(self, endpoints, max_workers=5):
        """Scan multiple endpoints concurrently"""
        print("\nScanning endpoints...\n")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_endpoint = {
                executor.submit(self.scan_endpoint, endpoint): endpoint 
                for endpoint in endpoints
            }
            
            for future in as_completed(future_to_endpoint):
                result = future.result()
                self.results.append(result)
                self.print_result(result)
    
    def print_result(self, result):
        """Print scan result for an endpoint"""
        print(f"[+] {result['endpoint']}")
        
        if result['status_code']:
            print(f"    Status Code: {result['status_code']}")
        
        print(f"    Auth Required: {'Yes' if result['auth_required'] else 'No'}")
        
        if result['missing_headers']:
            headers_str = ', '.join(result['missing_headers'])
            print(f"    Security Headers Missing: {headers_str}")
        else:
            print(f"    Security Headers: OK")
        
        if result['warnings']:
            for warning in result['warnings']:
                print(f"    Warning: {warning}")
        
        print()

def main():
    print("=== API Security Scanner ===\n")
    
    # Get user input
    base_url = input("Enter API base URL: ").strip()
    if not base_url:
        print("Error: Base URL is required")
        return
    
    endpoints_input = input("Enter endpoints (comma separated): ").strip()
    if not endpoints_input:
        print("Error: At least one endpoint is required")
        return 
    # Parse endpoints
    endpoints = [e.strip() for e in endpoints_input.split(',')]
    endpoints = [e if e.startswith('/') else f'/{e}' for e in endpoints]
    
    # Create scanner and run
    scanner = APIScanner(base_url)
    start_time = time.time()
    scanner.scan_endpoints(endpoints)
    elapsed_time = time.time() - start_time
    
    print(f"Scan Completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()


