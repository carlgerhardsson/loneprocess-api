#!/usr/bin/env python3
"""
Generate Firebase custom token for Frontend Team X
"""
import os
from pathlib import Path
from firebase_admin import credentials, auth, initialize_app

# Setup credentials
credentials_dir = Path(__file__).parent / "credentials"
credential_files = list(credentials_dir.glob("*.json"))

if not credential_files:
    print("❌ No credentials found!")
    print("Please place your Firebase service account key in credentials/")
    exit(1)

# Initialize Firebase
cred = credentials.Certificate(str(credential_files[0]))
try:
    initialize_app(cred)
except ValueError:
    pass  # Already initialized

# Generate custom token for frontend-team-x
uid = "frontend-team-x"
custom_claims = {
    "team": "frontend-team-x",
    "role": "external",
    "access_level": "read-only"
}

try:
    # Create custom token
    custom_token = auth.create_custom_token(uid, custom_claims)
    
    print("=" * 70)
    print("🔑 FIREBASE CUSTOM TOKEN GENERATED")
    print("=" * 70)
    print(f"\nUID: {uid}")
    print(f"Claims: {custom_claims}")
    print(f"\n📋 TOKEN (copy this to Frontend Team X):\n")
    print(custom_token.decode('utf-8'))
    print("\n" + "=" * 70)
    print("⚠️  SECURITY:")
    print("- Send via secure channel (NOT email)")
    print("- Token expires after exchange for ID token (1 hour)")
    print("- Read-only access enforced by Firestore rules")
    print("=" * 70)
    print("\n💡 USAGE:")
    print("Frontend Team X should exchange this token for an ID token:")
    print("https://firebase.google.com/docs/auth/admin/create-custom-tokens")
    print("=" * 70)
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
