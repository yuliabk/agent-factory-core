# G3 Host Remediation Evidence

```yaml
gate: G3-Host-Remediation
date: 2026-08-22
branch: codex/g3-hotelbeds-store-provisioning
windows_edition: Windows-11-Home
wsl_before: 2.5.10.0
wsl_after: 2.7.12.0
wsl_update_available: 2.7.12
wsl_update_result: direct-official-msi-installed
windows_restart_1: owner-approved-completed
windows_restart_2: owner-approved-completed
windows_installer_reregister: completed-exit-0
official_msi_sha256: a460d4560215f2efe003c136244b78ea3415d773824d7a688ea9ded36dbe9145
official_msi_signature: valid-microsoft-corporation
docker_desktop_restart: completed
docker_desktop_status_after_restart: starting
docker_daemon_ready: false
docker_desktop_version: 4.86.0.236216
docker_installer_validation: pass
docker_desktop_wsl_flags: 15
bitlocker_status: pass-fully-encrypted-protection-on
bitlocker_recovery_key_observed: false
n8n_container_created: false
n8n_volume_created: false
n8n_network_created: false
encryption_key_value_observed: false
hotelbeds_credential_materialized: false
provider_network_calls: 0
decision: reinstall-and-restore-pass-host-blocked-separate-remediation-decision-required
docker_vmm_pilot_approved: true
docker_vmm_install_in_place_result: no-change-exit-minus-5
docker_vmm_ui_selection: selected-apply-invoked
docker_vmm_full_restart: completed
docker_backend_after_vmm_pilot: linux-wsl
docker_vmm_pilot_result: fail-backend-not-persisted
docker_upgrade_pilot_approved: true
docker_upgrade_source: official-docker-release-4.87.0-build-236836
docker_upgrade_sha256: 9ac03d4e900c0fdee981d4bde083a55fdfb28ffba2cae77726eff2a437254822
docker_upgrade_checksum_match: true
docker_upgrade_signature: valid-docker-inc
docker_upgrade_mode: in-place-per-user
docker_desktop_version_after_upgrade: 4.87.0.236836
docker_data_disk_preserved: true
docker_backend_system_disk_regenerated: true
docker_backend_after_upgrade: linux-wsl
docker_daemon_ready_after_upgrade: false
docker_upgrade_pilot_result: upgrade-pass-data-disk-preserved-host-blocked
docker_vmm_retry_4_87_approved: true
docker_vmm_retry_4_87_ui_selection: selected-apply-invoked
docker_vmm_retry_4_87_full_restart: completed
docker_backend_after_vmm_retry_4_87: linux-wsl
docker_vmm_system_disk_created: false
docker_vmm_retry_4_87_result: fail-vmm-backend-blocked
docker_offline_backup_approved: true
docker_offline_backup_source: docker_data.vhdx
docker_offline_backup_target_drive: D
docker_offline_backup_target_filesystem: FAT
docker_offline_backup_target_encrypted: false-owner-accepted-risk
docker_offline_backup_overwrite: false
docker_offline_backup_bytes: 51380224
docker_offline_backup_checksum_match: true
docker_offline_backup_result: pass
docker_reinstall_approved: true
docker_reinstall_preflight_backup_checksum_match: true
docker_reinstall_preflight_installer_checksum_match: true
docker_reinstall_preflight_installer_signature: valid-docker-inc
docker_reinstall_uninstall_result: completed
docker_reinstall_install_version: 4.87.0.236836
docker_reinstall_install_result: completed-exit-0
docker_reinstall_restore_checksum_match_before_start: true
docker_reinstall_daemon_ready: false
docker_reinstall_local_disk_hash_after_start_matches_backup: false-runtime-wrote-local-disk
docker_reinstall_backup_retained: true
docker_reinstall_result: reinstall-pass-restore-pass-host-blocked
windows_integrity_remediation_approved: true
windows_integrity_backup_d_available_before_start: true
dism_restorehealth_result: pass-s-ok
dism_reboot_required: false
sfc_scannow_result: pass-repaired-system-drivers
sfc_repaired_files: rndismp6.sys,usb80236.sys
standard_reboot_registry_markers: absent
pending_file_rename_operations: present
windows_restart_after_integrity_repair: owner-completed
windows_integrity_boundaries: no-factory-reset-no-wsl-unregister-no-vhdx-delete-no-n8n-no-provider-network
post_restart_wsl_version: 2.7.12.0
post_restart_virtualization_services: wslservice-vmcompute-hns-running
post_restart_docker_desktop_started_for-readiness-check: true
post_restart_docker_desktop_wsl_distro: running-v2
post_restart_docker_version_check: timeout
post_restart_docker_log: socketforwarder-receive-fds-missing-and-engine-ping-timeout
post_restart_result: windows-integrity-pass-docker-host-blocked
n8n_resources_created_during_integrity_remediation: false
provider_network_calls_during_integrity_remediation: 0
vsock_repair_assessment_approved: true
vsock_assessment_mode: read-only
docker_desktop_distro_running_during_assessment: true
docker_desktop_host_c_share_exists: true
docker_desktop_host_c_share_windows_visible: false
vsock_failure_point: drvfs-mount-c-port-50002
virtualization_services_during_assessment: wslservice-vmcompute-hns-running
owner_account_admin_group_membership: true
owner_current_token_elevated: false
vsock_assessment_result: wsl-drive-share-host-blocked-privilege-pilot-candidate
docker_privilege_pilot_approved: true
docker_privilege_pilot_normal_shutdown_command: blocked
docker_privilege_pilot_window_close_request: sent-no-exit
docker_privilege_pilot_force_stop_performed: false
docker_privilege_pilot_elevated_relaunch_attempted: false
docker_privilege_pilot_result: normal-quit-blocked-elevated-relaunch-not-attempted
docker_forced_quit_pilot_approved: true
docker_forced_quit_preflight_backup_d_exists: true
docker_forced_quit_preflight_backup_bytes: 51380224
docker_forced_quit_processes_stopped: true
docker_forced_quit_wsl_shutdown: true
docker_forced_quit_distro_state_before_elevated_launch: stopped
docker_forced_quit_elevated_launch: completed
docker_forced_quit_daemon_check: timeout
docker_forced_quit_elevated_log: utilconnectvsock-plan9-socketforwarder-missing-engine-ping-timeout
docker_forced_quit_postcheck_processes_stopped: true
docker_forced_quit_postcheck_wsl_distro_state: stopped
docker_forced_quit_backup_d_retained: true
docker_forced_quit_result: elevated-docker-fail-host-plan9-vsock-blocked
wsl_feature_repair_approved: true
wsl_feature_check_elevated: true
wsl_feature_microsoft_windows_subsystem_linux: enabled
wsl_feature_virtual_machine_platform: enabled
wsl_feature_hypervisor_platform: enabled
wsl_feature_toggle_performed: false
wsl_feature_repair_restart_performed: false
wsl_feature_repair_result: features-pass-plan9-vsock-remains-blocked
wsl_feature_cycle_approved: true
wsl_feature_cycle_preflight_backup_d_exists: true
wsl_feature_cycle_preflight_docker_wsl_stopped: true
wsl_feature_cycle_stage_1_disable_wsl: invoked
wsl_feature_cycle_stage_1_disable_virtual_machine_platform: invoked
wsl_feature_cycle_restart_1: pending
wsl_feature_cycle_boundaries: no-vhdx-delete-no-docker-reset-or-uninstall-no-n8n-no-credential-no-provider-network
```

## אבחון ופעולות

- WSL פעיל בגרסה `2.5.10.0`, kernel `6.6.87.2`, ו-`docker-desktop` הוא distro מסוג WSL 2.
- Hypervisor זמין. `WslService`, `vmcompute` ו-`hns` היו פעילים בזמן האבחון.
- Docker Desktop ו-`docker-desktop` נעצרו והופעלו מחדש באופן ממוקד, ללא reset, unregister או מחיקת data. Docker נשאר ב-`starting` ו-`docker info` לא החזיר תשובה בתוך timeout.
- לוג Docker חזר על `UtilConnectVsock:606: connect port 50002 failed 110` ועל המתנה ל-`socketforwarder-receive-fds.sock`.
- `wsl --update` מצא גרסה `2.7.12`, אך נכשל עם Windows Installer code `1618`.
- בזמן הכשל הראשון היה פתוח מתקין חיצוני `AbacusAI Setup`. ה-Owner סגרה אותו באופן רגיל, אך ניסיון עדכון נוסף עדיין נכשל ב-`1618`.
- תהליך השירות `msiexec` נשאר פעיל, ללא Registry marker מסוג `Installer\\InProgress`. ניסיון עצירה רגיל ולא-מוגבה נדחה; התהליך לא נהרג והשירות לא שונה.
- ה-Owner אישרה Windows restart, והוא בוצע. לאחריו `1618` נפתר אך `wsl --update` נכשל ב-`Wsl/CallMsi/Install/REGDB_E_CLASSNOTREG`.
- Windows Installer נרשם מחדש ב-elevated session עם exit `0`. משום ש-CallMsi עדיין נכשל, הורדה חבילת `wsl.2.7.12.0.x64.msi` מה-release הרשמי של Microsoft.
- גודל החבילה היה `258998272` bytes, ה-SHA-256 התאים ל-asset metadata הרשמי, וה-Authenticode signature הייתה Valid עבור Microsoft Corporation. התקנת MSI מוגבהת הסתיימה ב-exit `0`.
- `wsl --version` מאשר `2.7.12.0` ו-kernel `6.18.33.2-2`.
- Docker bootstrap עדיין נעצר ב-DrvFS mount של `C:`; `socketforwarder-receive-fds.sock` לא נוצר ו-Docker daemon אינו מוכן גם לאחר `wsl --shutdown` ו-restart ממוקד.
- בדיקת BitLocker מוגבהת החזירה PASS רק כאשר `VolumeStatus=FullyEncrypted`, `ProtectionStatus=On` ו-`EncryptionPercentage=100`. הבדיקה לא קראה או הציגה Recovery Key.
- ה-Owner אישרה Windows restart שני והוא בוצע. לאחריו Docker חזר לאותו כשל `UtilConnectVsock` port `50002` בזמן DrvFS mount.
- `docker-desktop` רשום עם Flags `15`; אין ראיה ש-Drive mounting או interoperability הושבתו. Docker Desktop installer validation הסתיים ב-exit `0`.
- `Get-BitLockerVolume` ו-`manage-bde` אינם מספקים אימות סמכותי ב-session הלא-מוגבה. לא שונה מצב ההצפנה.

## פעולת Owner נדרשת

1. ה-`Docker VMM Beta` Pilot הסתיים ללא מעבר אפקטיבי. repair/reinstall, upgrade או עריכת settings דורשים החלטת Owner נפרדת עם הגנה על data disk קיים.
2. אין לבצע Factory Reset, uninstall, `wsl --unregister`, מחיקת VHDX או יצירת n8n Volume ללא אישור מפורש נוסף.

## Docker VMM Pilot

- ה-Owner אישרה שינוי backend ויצירת Docker data disk בלבד, תוך שמירת כל גבולות ה-Provisioning.
- ניסיון install-in-place עם `--backend=docker-vmm` החזיר `-5` במהירות ולא שינה את ההתקנה או יצר משאב n8n.
- `Docker VMM BETA` נבחר ו-`Apply` הופעלו דרך ה-UI הרשמי. Codex לא קרא ולא ערך `settings-store.json`.
- לאחר סגירה מלאה של תהליכי Docker, `wsl --shutdown` והפעלה מחדש, `docker-desktop` שוב רץ כ-WSL 2 והלוג דיווח `starting engine linux/wsl` ו-`WSL engine enabled`.
- ה-daemon נשאר לא מוכן. תוצאת ה-Pilot: `FAIL / BACKEND-NOT-PERSISTED`; לא נוצר Docker VMM data disk מאומת.

## Docker Upgrade Pilot

- ה-Owner אישרה שדרוג in-place בלבד תוך שמירת data קיים, ללא Reset, uninstall, n8n או Provider Network.
- חבילת Docker Desktop `4.87.0.236836` הורדה מהקישור הרשמי. ה-SHA-256 המאומת הוא `9ac03d4e900c0fdee981d4bde083a55fdfb28ffba2cae77726eff2a437254822`, בהתאם ל-release הרשמי, וה-Authenticode היה Valid עבור Docker Inc.
- השדרוג per-user הסתיים במקום. `wsl/disk/docker_data.vhdx`, דיסק נתוני ה-containers/images, נשאר באותו נתיב עם אותו זמן יצירה וגודל. `wsl/main/ext4.vhdx`, דיסק מערכת ה-backend, נבנה מחדש בזמן startup של הגרסה החדשה. לא בוצעו mount, export, copy או קריאת תוכן.
- לאחר ההפעלה Docker נשאר ב-`linux/wsl`, ה-daemon לא החזיר version בתוך timeout, והלוג חזר על `UtilConnectVsock` port `50002` בזמן DrvFS mount.
- תוצאה: `UPGRADE-PASS / DATA-DISK-PRESERVED / HOST-BLOCKED`. לא הופעלה פקודת יצירת משאב ולא הייתה Provider Network או API call.

## Docker VMM Retry 4.87

- ה-Owner אישרה ניסיון חוזר בגרסת Docker Desktop `4.87.0` בלבד, ללא Reset, uninstall, n8n, Credential או Provider Network.
- `Docker VMM BETA` נבחר ו-`Apply` הופעלו דרך `Settings > General > Virtual Machine Manager`; `settings-store.json` לא נקרא ולא נערך.
- לאחר full quit, `wsl --shutdown` והפעלה מחדש, הלוג דיווח שוב `starting engine linux/wsl` ו-`WSL engine enabled`.
- לא נוצר Docker VMM system disk; `docker_data.vhdx` נשאר באותו נתיב, זמן יצירה וגודל.
- תוצאה: `FAIL / VMM-BACKEND-BLOCKED`. לא הופעלה פקודת יצירת משאב ולא הייתה Provider Network או API call.

## Docker Offline Backup

- ה-Owner אישרה העתקה מאומתת של `docker_data.vhdx` בלבד ובחרה במפורש ביעד `D:` הנשלף, FAT ובלתי מוצפן, לאחר גילוי הסיכון.
- Docker Desktop ו-WSL נעצרו לפני ההעתקה. היעד היה חדש ולא היה קיים קובץ יעד, ולכן לא בוצע overwrite.
- גודל המקור והעותק היה `51380224` bytes, ו-SHA-256 תאם.
- אין בכך אישור ל-repair, reinstall, restore, reset או מחיקת מקור. לא נוצרו n8n resources ולא הייתה Provider Network או API call.

## Docker Reinstall

- ה-Owner אישרה uninstall, התקנה מחדש של Docker Desktop `4.87.0` ושחזור מעותק D.
- לפני uninstall ה-SHA-256 של העותק ב-D תאם למקור, והמתקין הרשמי תאם ל-checksum המפורסם ונשא חתימת Docker Inc תקפה.
- Docker הוסר בהצלחה, הותקן מחדש per-user עם exit `0`, ו-`docker_data.vhdx` שוחזר מהעותק. לפני startup ה-SHA-256 של העותק והדיסק המשוחזר תאם.
- ניסיון daemon ראשון נכשל שוב ב-DrvFS עם `UtilConnectVsock` port `50002`; Docker ו-WSL נעצרו ללא repair נוסף.
- לאחר ניסיון העלייה ה-hash של הדיסק המקומי שונה, מפני שה-runtime כתב אליו. לא בוצע overwrite שני; עותק D נשאר קיים ושלם וממשיך להיות נקודת השחזור המאומתת.
- אין Factory Reset, `wsl --unregister`, n8n resource, Credential, Provider Network או API call.

אין לבצע Docker factory reset, `wsl --unregister`, מחיקת VHDX, יצירת n8n Volume או Provider connection במסגרת ראיה זו.
