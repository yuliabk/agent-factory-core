# G3 Hotelbeds Store Provisioning Evidence

```yaml
gate: G3-Hotelbeds-Store-Provisioning
date: 2026-08-22
branch: codex/g3-hotelbeds-store-provisioning
tenant_id: travel-poc-synthetic
store_type: n8n-self-hosted-community
n8n_version: 2.35.7
image_platform: linux/amd64
image_digest: sha256:f410270e715c795b4935eb16f94c099f7aee8da81c340c9842e76f0d5e716ff3
docker_desktop_installed: true
docker_daemon_ready: false
full_disk_encryption_verified: false
container_created: false
volume_created: false
network_created: false
encryption_key_value_observed: false
hotelbeds_credential_materialized: false
provider_network_calls: 0
decision: partial-host-prerequisite-blocked-no-go-to-volume
```

## ראיות וכשלים

- Docker CLI זמין, אך Docker Desktop נשאר ב-`starting`; לוגי ה-host מצביעים על כשל WSL/vsock בחיבור ל-backend.
- `manage-bde -status` לא סיפק סטטוס הצפנה משום שהפקודה דורשת הרשאת Administrator. לכן Full-disk encryption אינה נחשבת מאומתת.
- פורטים `5678`, `5679` ו-`5680` היו פנויים בעת ה-preflight.
- לא נוצרו קובצי Key/Certificate, לא נקרא `.env`, ולא נצפה שום Secret או Credential.
- לא בוצעה קריאת Hotelbeds API ולא הוגדר Provider endpoint.

## החלטת Gate

חבילת baseline לא-סודית הוכנה וננעלה, אך ה-Provisioning האפקטיבי אינו Complete. אסור ליצור Volume או להפעיל Runtime עד ש-Docker daemon תקין ו-Full-disk encryption מאומת. פעולות תיקון host דורשות אישור נפרד משום שהן שינוי מערכת מעבר ל-baseline המקומי המאושר.

מקורות גרסה: [n8n 2.35.7 release](https://github.com/n8n-io/n8n/releases/tag/n8n%402.35.7), [n8n security advisories](https://github.com/n8n-io/n8n/security/advisories).
