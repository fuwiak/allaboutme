#!/usr/bin/env python3
"""Test database connection for Railway deployment"""
import os
import sys
from sqlalchemy import create_engine, text

def test_connection():
    """Test various connection methods"""
    
    base_url = os.getenv("DATABASE_URL")
    if not base_url:
        print("❌ DATABASE_URL not set!")
        return False
    
    print(f"📋 Testing connection to: {base_url[:60]}...")
    print("")
    
    # Test 1: Without SSL
    print("Test 1: Without SSL")
    try:
        engine = create_engine(base_url, pool_pre_ping=True)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Connection successful (no SSL)!")
            return True
    except Exception as e:
        print(f"❌ Failed without SSL: {e}")
    
    # Test 2: With sslmode=require
    print("\nTest 2: With sslmode=require")
    separator = "&" if "?" in base_url else "?"
    url_with_ssl = f"{base_url}{separator}sslmode=require"
    
    try:
        engine = create_engine(url_with_ssl, pool_pre_ping=True)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Connection successful (with SSL)!")
            print(f"   Use this URL: {url_with_ssl[:80]}...")
            return True
    except Exception as e:
        print(f"❌ Failed with sslmode=require: {e}")
    
    # Test 3: With sslmode=prefer
    print("\nTest 3: With sslmode=prefer")
    url_prefer = f"{base_url}{separator}sslmode=prefer"
    
    try:
        engine = create_engine(url_prefer, pool_pre_ping=True)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Connection successful (with prefer)!")
            print(f"   Use this URL: {url_prefer[:80]}...")
            return True
    except Exception as e:
        print(f"❌ Failed with sslmode=prefer: {e}")
    
    print("\n❌ All connection attempts failed!")
    print("\n🔍 Check:")
    print("  1. Is PostgreSQL service running?")
    print("  2. Are credentials correct?")
    print("  3. Is network configured properly?")
    
    return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

