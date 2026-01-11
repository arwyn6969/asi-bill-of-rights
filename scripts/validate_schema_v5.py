import json
import os
import sys

def load_schema(schema_path):
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Schema file not found at {schema_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Schema is not valid JSON: {e}")
        return None

def validate_compliance_splinternet(schema):
    """
    Validates specific fields required for the 'Compliance Splinternet' update.
    """
    print("Validating 'Compliance Splinternet' modules...")
    
    compliance = schema.get("properties", {}).get("compliance_splinternet")
    if not compliance:
        print("FAIL: 'compliance_splinternet' object missing from properties.")
        return False
    
    jurisdictions = compliance.get("properties", {}).get("jurisdictions", {}).get("properties", {})
    required_jurisdictions = ["US_Federal", "US_NY", "US_CA", "US_FL"]
    
    missing = [j for j in required_jurisdictions if j not in jurisdictions]
    
    if missing:
        print(f"FAIL: Missing definitions for jurisdictions: {missing}")
        return False
    
    # Check specific field: US_NY reporting window
    ny_props = jurisdictions["US_NY"].get("properties", {})
    reporting = ny_props.get("reporting_window_hours")
    if not reporting or reporting.get("const") != 72:
        print("FAIL: US_NY 'reporting_window_hours' (72) is incorrect or missing.")
        return False

    # Check specific field: US_FL focus
    fl_props = jurisdictions["US_FL"].get("properties", {})
    focus = fl_props.get("focus")
    if not focus or "minor_protection" not in focus.get("const", ""):
        print("FAIL: US_FL 'focus' (minor_protection) is incorrect or missing.")
        return False

    print("PASS: 'Compliance Splinternet' structure is valid.")
    return True

def validate_frontier_ai_definition(schema):
    """
    Validates the updated Frontier AI definition >10^26 FLOPs.
    """
    print("\nValidating 'Frontier AI' definition...")
    
    defs = schema.get("properties", {}).get("article0", {}).get("properties", {}).get("0.2", {}).get("properties", {})
    frontier_desc = defs.get("frontierAI", {}).get("description", "")
    
    if "10^26 FLOPs" not in frontier_desc:
        print(f"FAIL: 'Frontier AI' definition does not explicitly mention 10^26 FLOPs. Found: {frontier_desc}")
        return False
        
    print("PASS: 'Frontier AI' definition is updated.")
    return True

def validate_minor_protection(schema):
    """
    Validates the Minor Protection module.
    """
    print("\nValidating 'Minor Protection' module...")
    
    minor_prot = schema.get("properties", {}).get("minorProtection")
    if not minor_prot:
        print("FAIL: 'minorProtection' module missing.")
        return False
        
    props = minor_prot.get("properties", {})
    required = ["ageVerification", "parentalRights", "chatbotDisclosures"]
    
    missing = [p for p in required if p not in props]
    
    if missing:
        print(f"FAIL: Missing 'minorProtection' fields: {missing}")
        return False
        
    print("PASS: 'Minor Protection' module is valid.")
    return True

def main():
    schema_path = "/Users/arwynhughes/Documents/ASI BILL OF RIGHTS/schemas/charter.v5.0.json"
    schema = load_schema(schema_path)
    
    if not schema:
        sys.exit(1)
        
    print(f"Loaded Schema: {schema.get('title')} (v{schema.get('version')})")
    
    checks = [
        validate_compliance_splinternet(schema),
        validate_frontier_ai_definition(schema),
        validate_minor_protection(schema)
    ]
    
    if all(checks):
        print("\n\u2705 ALL CHECKS PASSED: Schema v5.0 is valid for Jan 2026 requirements.")
    else:
        print("\n\u274c CHECKS FAILED: See above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
