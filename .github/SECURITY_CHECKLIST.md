# Security Checklist - Pre-Deployment

**Run through this checklist before deploying to staging or giving external access.**

---

## ✅ **Authentication & Authorization**

- [ ] Firebase Authentication enabled
- [ ] Custom claims configured (`team: 'frontend-team-x'`)
- [ ] Token expiration set (1 hour default)
- [ ] No password-based auth (token-only)
- [ ] Test token generation works

---

## ✅ **Firestore Security**

- [ ] Security rules deployed
- [ ] Read-only access for external teams verified
- [ ] Write access blocked for external teams
- [ ] Service account has admin access
- [ ] Test security rules with Firebase Emulator:
   ```bash
   firebase emulators:start --only firestore
   ```

---

## ✅ **Secrets Management**

- [ ] `credentials/` folder in .gitignore
- [ ] No `*.json` files in Git (except firebase.json)
- [ ] `FIREBASE_TOKEN` in GitHub Secrets
- [ ] Service account key downloaded and stored securely
- [ ] Old tokens revoked

---

## ✅ **Code Security**

- [ ] No hardcoded secrets in code
- [ ] No production URLs in staging code
- [ ] Input validation via Pydantic models
- [ ] Error messages don't leak sensitive info
- [ ] Dependencies updated:
   ```bash
   pip list --outdated
   ```

---

## ✅ **Data Protection**

- [ ] Only test data in Firestore
- [ ] No real personnummer
- [ ] No real email addresses
- [ ] Swedish names are fake (generated)
- [ ] Verified no PII in test data

---

## ✅ **Network Security**

- [ ] CORS configured correctly
- [ ] HTTPS enforced (Firebase default)
- [ ] Rate limiting enabled (Firebase built-in)
- [ ] No open ports beyond Firebase defaults

---

## ✅ **Monitoring & Alerts**

- [ ] Budget alert set to $0 in Firebase
- [ ] Usage monitoring enabled
- [ ] Email alerts configured
- [ ] GitHub Actions notifications enabled

---

## ✅ **Documentation**

- [ ] SECURITY.md created
- [ ] API documentation reviewed
- [ ] No sensitive info in documentation
- [ ] External team onboarding guide ready
- [ ] Incident response plan documented

---

## ✅ **Testing**

- [ ] All endpoints tested locally
- [ ] Security rules tested
- [ ] Token authentication tested
- [ ] Read-only access verified
- [ ] Rate limiting tested

---

## ✅ **Deployment**

- [ ] CI/CD pipeline tested
- [ ] Firestore rules deployed
- [ ] Firestore indexes deployed
- [ ] GitHub Actions workflow runs successfully
- [ ] Staging URL accessible

---

## ✅ **External Access**

- [ ] Token generated for Frontend Team X
- [ ] Token sent securely (not via email)
- [ ] Onboarding documentation sent
- [ ] Support contact provided
- [ ] Expected usage communicated

---

## ✅ **Post-Deployment**

- [ ] Monitor first 24h of external access
- [ ] Review Firebase logs
- [ ] Check for unusual activity
- [ ] Verify costs remain at $0
- [ ] Collect feedback from external team

---

## 🔴 **Security Incident Response**

If you need to revoke access immediately:

```bash
# 1. Update Firestore rules to block all external access
firebase deploy --only firestore:rules

# 2. Revoke all tokens (requires manual deletion in Firebase Console)
# Go to: Authentication → Users → Delete user

# 3. Rotate GitHub Secrets
firebase login:ci  # Generate new token
# Update FIREBASE_TOKEN in GitHub Secrets

# 4. Review logs
# Firebase Console → Usage & Billing → Usage

# 5. Notify security team
# Email: carl.gerhardsson@cgi.com
```

---

**Last Review:** 2026-03-10  
**Reviewed By:** Carl Gerhardsson  
**Next Review:** Before Phase 6 (External Access)
