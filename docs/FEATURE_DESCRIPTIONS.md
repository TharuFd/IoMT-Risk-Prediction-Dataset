# Feature Descriptions / Data Dictionary

This dictionary documents the **28 input telemetry features**, alongside the timestamp and two labels. Interpret operational definitions as intended semantics; exact generator rules and collection mappings need verification against the original generation scripts.

| Column | Group | Data type | Meaning | Unit / range |
|---|---|---|---|---|
| `timestamp` | Index | object | Observation time. Each row represents a five-minute step; timezone is not encoded. | YYYY-MM-DD HH:MM:SS |
| `hour` | Temporal | int64 | Hour of observation, local recording clock (0–23). | integer; 0–23 |
| `is_off_hours` | Temporal | int64 | Binary indicator for generator-defined non-working/off-hours period; exact policy must be confirmed from generation code. | 0/1 |
| `dicom_c_store_count` | DICOM | float64 | Count of observed DICOM C-STORE operations in the observation window. | count |
| `dicom_c_find_count` | DICOM | float64 | Count of DICOM C-FIND query operations. | count |
| `dicom_c_move_count` | DICOM | float64 | Count of DICOM C-MOVE retrieval operations. | count |
| `dicom_failed_assoc_count` | DICOM | float64 | Count of failed DICOM association attempts. | count |
| `dicom_bytes_mb` | DICOM | float64 | Estimated DICOM traffic volume during the window. | MB |
| `dicom_external_dst_count` | DICOM | float64 | Count of DICOM destinations classified external by the generator/collector. | count |
| `flow_count` | Network | float64 | Number of observed network flows in the window. | count |
| `unique_dst_ip_count` | Network | float64 | Number of distinct destination IP addresses. | count |
| `tcp_syn_count` | Network | float64 | Number of TCP SYN observations. | count |
| `tcp_rst_count` | Network | float64 | Number of TCP RST observations. | count |
| `smb_flow_count` | Network | float64 | Number of SMB-related network flows. | count |
| `winrm_flow_count` | Network | float64 | Number of WinRM-related network flows. | count |
| `wmi_rpc_flow_count` | Network | float64 | Number of WMI/RPC-related network flows. | count |
| `outbound_connection_count` | Network | float64 | Number of outbound connection observations. | count |
| `network_entropy` | Network | float64 | Generator/collector-derived network variability/entropy metric; exact formula and base require source verification. | unitless; definition pending |
| `powershell_event_count` | Endpoint | float64 | Number of PowerShell execution-related events. | count |
| `encoded_command_count` | Endpoint | float64 | Count of PowerShell encoded-command indicators. | count |
| `iex_count` | Endpoint | float64 | Count of Invoke-Expression/IEX indicators. | count |
| `downloadstring_count` | Endpoint | float64 | Count of DownloadString indicators. | count |
| `suspicious_keyword_count` | Endpoint | float64 | Count of suspicious command/token indicators according to detector rules. | count |
| `wmi_exec_count` | Endpoint | float64 | Number of detected WMI execution activities. | count |
| `psexec_exec_count` | Endpoint | float64 | Number of detected PsExec execution activities. | count |
| `process_create_count` | Endpoint | float64 | Number of observed process creation events. | count |
| `suspicious_parent_count` | Endpoint | float64 | Number of events with suspicious parent process relationships. | count |
| `remote_logon_count` | Authentication | float64 | Number of remote logon observations. | count |
| `failed_logon_count` | Authentication | float64 | Number of failed logon observations. | count |
| `future_risk_score_24h` | Target | float64 | Numeric generated/derived risk score for the next-24-hour prediction target; do not treat as independently observed incident outcome. | 0–100 |
| `future_risk_level_24h` | Target | object | Categorical risk level derived from the numeric risk score. | LOW / MEDIUM / HIGH / CRITICAL |

## Label bands, verified from the file

| Risk level | Observed score interval |
|---|---|
| LOW | 0.00–29.99 |
| MEDIUM | 30.00–49.99 |
| HIGH | 50.00–69.99 |
| CRITICAL | 70.00–100.00 |

**Important:** `future_risk_score_24h` must not be used as an input feature when predicting `future_risk_level_24h`: the label is exactly recoverable from it. `timestamp` is a time index, not one of the 28 model inputs. Numeric count fields are serialized as floating-point values; observed integer-like values should not be mistaken for fractional events.

## Collector alignment

Live inference must produce these exact 28 feature names, time-window definitions, ordering and preprocessing. `hour` and `is_off_hours` must use the same timezone and off-hours policy as the training dataset. Any unavailable feature must be handled with a documented missing-data policy rather than silently substituted.
