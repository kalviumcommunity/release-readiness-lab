### **2. `release-readiness-pack/config-verification.md`**
markdown
# Configuration & Environment Verification

## Audit Matrix
| Setting / Secret | Target Value / Secret Reference | Verified in Staging? | Status |
| :--- | :--- | :--- | :--- |
| DB_PORT | ConfigMap: checkout-config (5432) | Yes | OK |
| DB_USER | Secret: db-credentials (DB_USER) | Yes | OK |
| DB_PASSWORD | Secret: db-credentials (DB_PASSWORD) | Yes | OK |
| APP_PORT | ContainerPort 80 (Aligned with Nginx) | Yes | OK |

## Environment Parity Check
ConfigMap and Secret keys matched target environment definitions.
Health probes updated to point to / on port 80.


