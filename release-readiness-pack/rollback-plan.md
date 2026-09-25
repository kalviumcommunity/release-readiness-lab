### **4. `release-readiness-pack/rollback-plan.md`**
markdown
# Rollback Plan

## Recovery Information
**Target Release:** checkout-api:v2.5
**Known-Good Rollback Target:** checkout-api:v2.3 (Deployment Hash: 76f6c99df)
**Target Recovery Time Objective (RTO):** < 3 Minutes

## Rollback Execution Steps
1. Execute rolling undo via kubectl:
   
bash
   kubectl rollout undo deployment/checkout-api

---