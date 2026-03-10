# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 3.0.x   | :white_check_mark: |
| < 3.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please email:
**carl.gerhardsson@cgi.com**

**Do NOT open a public GitHub issue for security vulnerabilities.**

---

## Security Measures

### 1. Firebase Authentication
- ✅ Custom tokens with team claims
- ✅ Token expiration: 1 hour
- ✅ Token refresh required
- ✅ No password-based auth (token-only)

### 2. Firestore Security Rules
- ✅ Read-only access for external teams
- ✅ Explicit collection whitelisting
- ✅ Team-based access control via custom claims
- ✅ No write access from external clients
- ✅ Service account required for writes

### 3. API Security
- ✅ CORS restricted (configurable)
- ✅ Rate limiting via Firebase
- ✅ Input validation via Pydantic
- ✅ No SQL injection (Firestore is NoSQL)

### 4. Data Protection
- ✅ Test data only (no production data)
- ✅ No PII in staging environment
- ✅ Swedish test names (realistic but fake)
- ✅ No real personnummer

### 5. Secret Management
- ✅ Service account keys in .gitignore
- ✅ Firebase tokens in GitHub Secrets
- ✅ No secrets in code
- ✅ Credentials folder excluded from Git

### 6. Access Control

**What External Teams CAN access:**
- ✅ API documentation (public GitHub branch)
- ✅ Staging API endpoints (with valid token)
- ✅ Test data (read-only)

**What External Teams CANNOT access:**
- ❌ Source code (private branches)
- ❌ Firebase Console
- ❌ Service account keys
- ❌ GitHub Secrets
- ❌ Write access to database
- ❌ Production environment

### 7. Monitoring
- ✅ Firebase usage monitoring
- ✅ GitHub Actions logs
- ✅ Budget alerts at $0
- ✅ No auto-upgrade to paid plans

---

## Security Checklist

Before giving external access:

- [ ] Service account key NOT in Git
- [ ] Firestore rules deployed and tested
- [ ] Firebase token stored in GitHub Secrets
- [ ] Budget alert set to $0
- [ ] Test data verified (no real PII)
- [ ] CORS configured correctly
- [ ] Token expiration tested
- [ ] Read-only access verified
- [ ] Documentation reviewed
- [ ] External team onboarding documented

---

## Incident Response

If a security incident occurs:

1. **Immediately revoke all external tokens**
   ```bash
   firebase auth:export users.json
   # Review and delete compromised tokens
   ```

2. **Update Firestore rules**
   ```bash
   firebase deploy --only firestore:rules
   ```

3. **Rotate GitHub Secrets**
   - Generate new FIREBASE_TOKEN
   - Update in GitHub Secrets

4. **Audit logs**
   - Check Firebase Console → Usage
   - Review GitHub Actions logs

5. **Notify affected parties**
   - Email external teams
   - Provide new tokens if needed

---

## Security Best Practices

### For Developers:
1. Never commit credentials
2. Use environment variables
3. Review Firestore rules regularly
4. Keep dependencies updated
5. Test security rules before deploy

### For External Teams:
1. Keep tokens secure
2. Don't share tokens between teams
3. Report suspicious activity
4. Use HTTPS only
5. Rotate tokens periodically

---

## Compliance

- ✅ GDPR: Test data only, no real PII
- ✅ Data residency: europe-west region
- ✅ Encryption: TLS 1.3 in transit, AES-256 at rest
- ✅ Audit trail: Firebase logs

---

**Last Updated:** 2026-03-10
**Next Review:** 2026-06-10
