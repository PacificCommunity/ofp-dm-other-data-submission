---
description: "Electronic Monitoring Longline CSV data templates and field specifications"
# Do not edit manually - regenerate with: python scripts/generate_templates.py
---

## Electronic Monitoring (EM) Longline CSV Data Format

Electronic Monitoring (EM) data provide detailed records of fishing operations and catch events derived from onboard video cameras, sensors, and EM analysis systems. These data are produced through a structured review process conducted by trained EM analysts and, in some cases, supported by automated or artificial intelligence tools.

EM data capture information related to fishing activities, including trip metadata, gear deployment, catch events, species identification, and potential compliance observations. They support both **scientific monitoring** (for example, species composition, catch characterisation and fishing effort) and **compliance monitoring** (for example, mitigation measures, protected-species interactions and operational practices).

The EM Longline CSV templates provide a structured tabular format for submitting EM data to SPC/OFP. The templates incorporate the [WCPFC Interim Electronic Monitoring Minimum Data Fields](https://meetings.wcpfc.int/node/24512), together with additional fields required to support regional data management and submission processes. Field names, definitions, formats, codes and field order are aligned, where applicable, with the [EM Longline JSON standard](https://pacificcommunity.github.io/tufman2-json-standard/longline-em/). This alignment provides consistency between the CSV and JSON submission formats and supports future transition to direct JSON submission.

### Which template should I use?

Two CSV template options are provided for each EM data table:

- **WCPFC minimum CSV** – recommended as the starting point for EM data providers. It contains the WCPFC Interim Electronic Monitoring Minimum Data Fields together with additional relationship, structural, or conditionally required fields needed to submit the data as linked CSV tables.
- **Comprehensive CSV** – contains the WCPFC minimum fields plus additional fields drawn from the SPC/FFA/PNA Data Collection Committee (DCC) standard and other fields supported by the EM Longline JSON standard.

Data providers may begin with the WCPFC minimum templates and add fields from the comprehensive templates where those data are available or required by their national EM programme.

### Data submission workflow

The CSV format is intended for national EM programmes and data providers that currently produce tabular data. The submitted data follow this workflow:

1. An EM data provider submits EM data to SPC/OFP using the CSV templates.
2. The CSV tables are converted into the corresponding JSON structured format.
3. The converted JSON formatted data are submitted to the **Tufman2 Data Quality Control (DQC) API** for validation.
4. Validation errors are corrected by EM data providers before resubmission.
5. Data that pass the applicable DQC checks can then be submitted to Tufman2.

---

### Field formatting details

The following formatting rules apply to values supplied in the CSV templates:

- **Datetime values** must use ISO 8601 format in UTC: `YYYY-MM-DDTHH:MM:SSZ`.
  - Example: `2025-03-15T06:30:00Z`

- **Latitude and longitude** must use the ISO 6709-style representation, with a maximum of three decimal places in minutes:
  - Latitude: signed `DDMM.MMM`
  - Longitude: signed `DDDMM.MMM`
  - Example latitude: `-1808.460`
  - Example longitude: `+17826.460`

- **Species codes** must use FAO ASFIS 3-character species codes.
  - Example: `YFT` – Yellowfin tuna
  - Example: `ALB` – Albacore tuna

- **Port codes** must use the applicable UN/LOCODE where a port is reported.
  - Example: `FJSUV` – Suva, Fiji

- **Boolean values** must be reported as `true` or `false`. Leave the CSV cell blank when the value is unknown or not applicable.

- **List-type values** must be stored as valid JSON array strings within the CSV cell.
  - Text-code example: `["NNT","RAO"]`
  - Number example: `[4,7]`

- **Numeric values** must use a decimal point (`.`) where a decimal value is required. Do not use thousands separators.

---

### Mandatory field indicator

The **Mandatory** column in the field-description tables identifies whether a field forms part of the **WCPFC Interim Electronic Monitoring Minimum Data Fields**.

- **Yes** – the field corresponds to a data field identified as **YES** in the WCPFC Interim Electronic Monitoring Minimum Data Fields.
- **No** – the field is not identified as a WCPFC minimum EM data field. It may nevertheless be included to support CSV relationships, data conversion, data quality, traceability, conditional WCPFC requirements, or national programme requirements.

A value of **No does not necessarily mean that the field can be omitted**. Some fields marked **No** are included in the WCPFC minimum CSV because they are required to maintain relationships between the CSV tables or to support information that becomes mandatory under particular conditions.

---

### CSV structure and relationships

The EM CSV specification is organised into five related tables:

1. **Trip** – metadata describing the fishing trip, vessel and EM analysis process.
2. **Set** – information about individual fishing sets, fishing effort, bait, gear configuration and mitigation measures.
3. **Set Log** – timestamped events recorded during setting and hauling operations.
4. **Catch** – information about individual catch events recorded during analysed sets.
5. **Compliance Events** – potential compliance events identified during EM analysis.

Each data level is represented as a separate CSV table to reduce repetition and provide a clear relational structure. Relationship identifiers are included where needed to associate records across the separate tables.

The primary relationships are:

- `em_trip_id` uniquely identifies an EM trip and links related records to their parent Trip.
- `em_set_id` uniquely identifies an EM set and links Set Log and Catch records to their parent Set.
- `em_catch_id` uniquely identifies an individual catch event.
- Compliance Events use the relevant identifiers to associate an event with the Trip, Set or Catch record to which it relates.

Relationship identifiers must match exactly between the CSV files submitted as part of the same dataset.

#### Identifier construction rules

Identifiers must be constructed consistently so that records can be linked reliably across tables and across resubmissions.

| Identifier | Construction rule |
|------------|-------------------|
| `em_trip_id` | Normalised vessel name + trip departure date in `YYYYMMDD` format |
| `em_set_id` | Parent `em_trip_id` + UTC set start datetime in `YYYYMMDDHHMMSS` format |
| `em_catch_id` | Parent `em_set_id` + `C` + four-digit sequential catch number within the set |
| `event_id` | Parent `em_trip_id` + `E` + four-digit sequential compliance-event number within the trip |

For identifier construction, the **normalised vessel name** must be converted to uppercase and all spaces and punctuation removed, retaining only letters and numbers.

Examples:

- `OCEAN VOYAGER` → `OCEANVOYAGER`
- `KOYO MARU NO. 55` → `KOYOMARUNO55`

Example identifier hierarchy:

```text
em_trip_id  = OCEANVOYAGER20250315
em_set_id   = OCEANVOYAGER2025031520250316194500
em_catch_id = OCEANVOYAGER2025031520250316194500C0001
event_id    = OCEANVOYAGER20250315E0001
```

The datetime component used in `em_set_id` must be derived from the UTC `set_start_datetime`.

Once assigned, `em_trip_id`, `em_set_id`, `em_catch_id`, and `event_id` must remain unchanged when a record is corrected or resubmitted.

The downloadable Trip, Set, Set Log, Catch and Compliance Event templates and their field descriptions are provided below.

---

### Trip Level Data

The trip-level table captures information about individual fishing trips monitored by EM systems.

Each row represents one EM trip and contains vessel identifiers, trip timing and locations, EM programme metadata, and analysis/review attributes.

**Download templates:** [WCPFC minimum CSV](./templates/em_trip_minimum_v1.0.csv) | [Comprehensive CSV](./templates/em_trip_v1.0.csv)

#### WCPFC minimum CSV example

| em_trip_id | vessel_name | ircs | wcpfc_vid | trip_start_datetime | depart_port | trip_start_lat | trip_start_lon | return_port | trip_end_lat | trip_end_lon | receiving_vessel_name | return_datetime | em_program_code | analyst_names | em_trip_analyst_codes | em_review_type | drc_em_software | trip_analysis_start_datetime | trip_analysis_end_datetime | total_number_sets | has_auto_bait_thrower | has_auto_branchline_attacher | is_observer_onboard |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OCEANVOYAGER20250315 | OCEAN VOYAGER | 3FIJ8 | 12345 | 2025-03-15T06:30:00Z | FJSUV | -1808.460 | +17826.460 | FJSUV | -1808.460 | +17826.460 |  | 2025-04-02T14:15:00Z | FJEM | ["Analyst One","Analyst Two"] | ["NNT"] | Secondary review | Satlink View Manager version 4.0 | 2025-04-03T08:00:00Z | 2025-04-04T16:30:00Z | 10 | false |  | false |

#### Field descriptions

| Field name | Type | Format | Description | Mandatory |
|------------|------|--------|-------------|-----------|
| em_trip_id | Text | Text | Unique identifier for the EM trip. The value must be unique within the submission and must be constructed using the normalised vessel name followed by the trip departure date in YYYYMMDD format. For identifier construction, convert the vessel name to uppercase and remove all spaces and punctuation, retaining only letters and numbers. | Yes |
| trip_analysis_method | Text | String | Describes how the EM data for the trip were generated, particularly where AI tools are used. For example: "This trip was analysed by humans only" or "This trip was analysed by humans and AI tools". | No |
| uvi | Number | Integer | The vessel's Unique Vessel Identifier (IMO number), where available. Refer to WCPFC [Conservation and Management Measure 2013-04](https://www.wcpfc.int/doc/conservation-and-management-measure-wcpfc-implementation-unique-vessel-identifier-uvi). | No |
| vessel_name | Text | Text | Name of the fishing vessel. | Yes |
| vessel_owner_company | Text | Text | Name of the company or vessel owner responsible for the fishing vessel. | No |
| vessel_registration_number | Text | Text | Flag State registration number of the fishing vessel. | No |
| flag | Text | Text | Flag or chartering nation of the fishing vessel. | No |
| ircs | Text | Text | International Radio Call Sign (IRCS) of the fishing vessel. | Yes |
| wcpfc_vid | Number | Integer | WCPFC vessel identification number. Refer to the [WCPFC Record of Fishing Vessels](https://vessels.wcpfc.int/). | Yes |
| trip_start_datetime | Text | ISO 8601 UTC: YYYY-MM-DDTHH:MM:SSZ | UTC date and time the vessel departs a port to start its fishing trip. If the vessel departs from a carrier vessel after an at-sea transhipment, use the UTC date and time of departure from the carrier vessel. | Yes |
| depart_port | Text | UN/LOCODE or AT SEA | Departure port code (UN/LOCODE). Use AT SEA when the trip begins at sea following a transhipment; departure coordinates must then be provided. Refer to the [Port codes reference table](/em/12_Port_codes/). | Yes |
| trip_start_lat | Text | ISO 6709: signed DDMM.MMM | Latitude of departure when the vessel starts the trip. | Yes |
| trip_start_lon | Text | ISO 6709: signed DDDMM.MMM | Longitude of departure when the vessel starts the trip. | Yes |
| return_port | Text | UN/LOCODE or AT SEA | Return port code (UN/LOCODE). Use AT SEA when the trip ends at sea for a full or partial unloading; the applicable receiving-vessel details and coordinates must then be provided. Refer to the [Port codes reference table](/em/12_Port_codes/). | Yes |
| trip_end_lat | Text | ISO 6709: signed DDMM.MMM | Latitude of return when the vessel ends the trip. | Yes |
| trip_end_lon | Text | ISO 6709: signed DDDMM.MMM | Longitude of return when the vessel ends the trip. | Yes |
| receiving_vessel_name | Text | Text; blank if not applicable | Name of the vessel receiving catch during an at-sea transhipment. This field is required when the start or end of the trip is AT SEA. | No |
| receiving_vessel_registration_number | Text | Text; blank if not applicable | Flag State registration number of the receiving vessel. | No |
| receiving_vessel_flag | Text | Text; blank if not applicable | Flag or chartering nation of the receiving vessel. | No |
| receiving_vessel_ircs | Text | Text; blank if not applicable | International Radio Call Sign (IRCS) of the receiving vessel. | No |
| receiving_vessel_wcpfc_vid | Number | Integer; blank if not applicable | WCPFC identification number of the receiving vessel. Refer to the [WCPFC Record of Fishing Vessels](https://vessels.wcpfc.int/). | No |
| return_datetime | Text | ISO 8601 UTC: YYYY-MM-DDTHH:MM:SSZ | UTC date and time the vessel ends the fishing trip. | Yes |
| em_program_code | Text | EM programme code | Code identifying the national or sub-regional EM programme, for example FJEM. Refer to the [EM programme codes reference table](/em/08_EM_program_codes/). | Yes |
| em_drc_code | Text | EM DRC code | Code identifying the EM Data Review Centre where the EM records were analysed. Refer to the [EM DRC codes reference table](/em/09_DRC_codes/). | No |
| analyst_names | List | Valid JSON array of analyst names | Name(s) of the EM analyst(s) who produced EM data at the trip level. Analyst codes are assigned by SPC/OFP and can be derived from the analyst names provided. | Yes |
| em_trip_analyst_codes | List | Valid JSON array of text codes | Code(s) for the EM analyst(s) who produced EM data at the trip level. SPC/OFP assigns these codes, and the analyst codes can be derived from the analyst names provided in analyst_names. | Yes |
| em_review_type | Text | Text | Type of EM review conducted for the trip. | Yes |
| em_trip_reviewer_codes | List | Valid JSON array of text codes | Code(s) for the EM Data Quality Reviewer(s) at the trip level. When one or more reviewer codes are provided, this indicates that a data quality review was conducted at the trip level. | No |
| drc_em_provider_code | Text | String | Code for the company providing the EM records analysis system used in the Data Review Centre. | No |
| drc_em_software | Text | String | Software name and version of the system used to analyse the EM records. | Yes |
| science_analysis_percentage | Number | Integer, 0-100 | Percentage of haul analysis undertaken for scientific monitoring. Programmes may vary analysis rates according to national procedures and rationale. 100 means entirely analysed, an intermediate value represents partial analysis, and 0 means compliance-only analysis. | No |
| compliance_analysis_percentage | Number | Integer, 0-100 | Percentage of haul analysis undertaken for compliance monitoring. Programmes may vary analysis rates according to national procedures and rationale. 100 means entirely analysed, an intermediate value represents partial analysis, and 0 means science-only analysis. | No |
| trip_analysis_start_datetime | Text | ISO 8601 UTC: YYYY-MM-DDTHH:MM:SSZ | UTC date and time when analysis of the trip started. | Yes |
| trip_analysis_end_datetime | Text | ISO 8601 UTC: YYYY-MM-DDTHH:MM:SSZ | UTC date and time when analysis of the trip ended. | Yes |
| total_number_sets | Number | Integer | Total number of sets conducted by the vessel during the trip. | Yes |
| set_numbers_planned_for_analysis | List | Valid JSON array of integers | List of set numbers planned for analysis. The EM programme should be able to demonstrate the protocol used to select sets, including the random-selection process. | No |
| digital_calibration | Boolean | true / false; blank if unknown or not applicable | Indicates whether the EM analyst performed a digital calibration of the measuring tool before analysis. This supports assessment of the accuracy of digital length measurements. | No |
| has_auto_bait_thrower | Boolean | true / false; blank if unknown or not applicable | Indicates whether the vessel has an automatic bait thrower. | Yes |
| has_auto_branchline_attacher | Boolean | true / false; blank if unknown or not applicable | Indicates whether the vessel has an automatic branchline attacher. | Yes |
| is_observer_onboard | Boolean | true / false; blank if unknown or not applicable | Indicates whether the EM records show an observer onboard the vessel. | Yes |
| comments | Text | String | General comments at the trip level about the analysis of EM records and production of EM data. | No |

> **Notes:**
> - `em_trip_id` must be unique within a submission. It must be constructed using the normalised vessel name followed by the trip departure date in `YYYYMMDD` format. For identifier construction, convert the vessel name to uppercase and remove all spaces and punctuation, retaining only letters and numbers.
> - Percentage fields are expressed as values from 0 to 100.
> - Vessel identification should be checked against the [WCPFC Record of Fishing Vessels](https://vessels.wcpfc.int/). If the UVI/IMO number or WCPFC VID is not available, vessel name, flag State registration number and IRCS should be provided to support unique vessel identification.
> - Port codes should use the [Port codes reference table](/em/12_Port_codes/) where applicable.
> - Refer to the [EM programme codes reference table](/em/08_EM_program_codes/) and [EM DRC codes reference table](/em/09_DRC_codes/) for standard programme and review-centre codes.

### Set Level Data

The set-level table captures information about individual fishing sets monitored by EM systems.

Each row represents one EM set and contains the parent trip identifier, set identifiers, analysis/review attributes, fishing effort information, bait information, and mitigation measures.

**Download templates:** [WCPFC minimum CSV](./templates/em_set_minimum_v1.0.csv) | [Comprehensive CSV](./templates/em_set_v1.0.csv)

#### WCPFC minimum CSV example

| em_trip_id | em_set_id | set_start_datetime | hooks_between_floats | baskets_deployed | baskets_monitored | total_hooks_deployed | bait_species_codes | tori_line_number | has_baits_dyed | has_deep_line_shooter | has_offal_management | has_side_setting_bird_curtain | has_weighted_branch_lines | shark_lines_observed | has_hook_shielding_device |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OCEANVOYAGER20250315 | OCEANVOYAGER2025031520250316194500 | 2025-03-16T19:45:00Z | 28 | 100 | 100 | 2800 | ["SAR","SQU"] | 0 | false | true | true |  | true | 0 |  |

#### Field descriptions

| Field name | Type | Format | Description | Mandatory |
|------------|------|--------|-------------|-----------|
| em_trip_id | Text | Text | Identifier of the parent EM trip. The value must exactly match an em_trip_id in the Trip CSV submitted in the same dataset. | No |
| em_set_id | Text | Text | Unique identifier for the EM set. The identifier must be constructed by appending the UTC set start datetime in YYYYMMDDHHMMSS format to the parent em_trip_id. | No |
| set_number | Number | Integer | Number of the set within the trip. | No |
| set_not_analysed_reason | Text | Reason-for-not-analysing code; blank if not applicable | Reason code explaining why a set planned or selected for analysis could not be analysed. Refer to the [Reason for not analysing codes reference table](/em/10_Reason_for_not_analysing_codes/). | No |
| set_analysis_method | Text | Text | Describes how the EM data for the set were generated, particularly where AI tools are used. For example: "This set was analysed by humans only" or "This set was analysed by humans and AI tools". | No |
| em_set_analyst_codes | List | Valid JSON array of text codes | Code(s) for the EM analyst(s) who produced EM data at the set level. | No |
| set_analysis_start_datetime | Text | ISO 8601 UTC: YYYY-MM-DDTHH:MM:SSZ | UTC date and time when analysis of the set started. | No |
| set_analysis_end_datetime | Text | ISO 8601 UTC: YYYY-MM-DDTHH:MM:SSZ | UTC date and time when analysis of the set ended. | No |
| em_set_reviewer_codes | List | Valid JSON array of text codes | Code(s) for the EM Data Quality Reviewer(s) at the set level. When one or more reviewer codes are provided, this indicates that a data quality review was conducted at the set level. | No |
| data_quality_control_process | Boolean | true / false; blank if unknown or not applicable | Indicates whether Data Quality Control procedures were conducted at the set level, including secondary review to verify or validate EM data. | No |
| set_start_datetime | Text | ISO 8601 UTC: YYYY-MM-DDTHH:MM:SSZ | UTC date and time when the first buoy enters the water to start setting the line. | Yes |
| hooks_between_floats | Number | Integer | Average number of hooks between floats. The protocol is to count hooks in three baskets towards the start, three baskets in the middle, and three baskets towards the end of the line, then divide the total by nine. | Yes |
| baskets_deployed | Number | Integer | Total number of baskets deployed. This is the number of floats deployed minus one. | Yes |
| baskets_monitored | Number | Integer | Total number of baskets monitored by the EM analyst during the haul. | Yes |
| total_hooks_deployed | Number | Integer | Total number of hooks deployed in the set, calculated from the number of baskets and hooks between floats. | Yes |
| bait_species_codes | List | Valid JSON array of text codes | FAO ASFIS species code(s) for bait used during the set. The protocol is to review bait used during analysis of three baskets towards the start, three baskets in the middle, and three baskets towards the end of the setting operation. Refer to the [FAO ASFIS species list](https://www.fao.org/fishery/en/collection/asfis/en) and the [Marine species identification manual for horizontal longline fishermen](https://coastfish.spc.int/en/index.php?option=com_content&Itemid=30&id=341). | Yes |
| bait_weight | Number | Number in kilograms | Total weight of bait used for the set, in kilograms. | No |
| tori_line_number | Number | Integer | Total number of tori lines attached to tori poles and used during setting. Use 0 when no tori line is used. | Yes |
| has_baits_dyed | Boolean | true / false; blank if unknown or not applicable | Indicates whether blue-dyed bait was used during setting. | Yes |
| has_deep_line_shooter | Boolean | true / false; blank if unknown or not applicable | Indicates whether a deep-setting line shooter was used. | Yes |
| has_offal_management | Boolean | true / false; blank if unknown or not applicable | Indicates whether strategic offal disposal was used. | Yes |
| has_side_setting_bird_curtain | Boolean | true / false; blank if unknown or not applicable | Indicates whether a bird curtain was used with side setting. | Yes |
| has_weighted_branch_lines | Boolean | true / false; blank if unknown or not applicable | Indicates whether weighted branch lines were used. | Yes |
| shark_lines_observed | Number | Integer | Number of shark lines (branch lines running from floats or drop lines) observed during the set. | Yes |
| has_hook_shielding_device | Boolean | true / false; blank if unknown or not applicable | Indicates whether hook-shielding devices were used during line setting. | Yes |
| comments | Text | String | Comments at the set level about analysis of the setting and hauling operations. | No |

> **Notes:**
> - `em_trip_id` must exactly match an `em_trip_id` in the Trip CSV submitted in the same dataset.
> - `em_set_id` must be unique within the submission. It must be constructed by appending the UTC set start datetime in `YYYYMMDDHHMMSS` format to the parent `em_trip_id`.
> - Refer to the [Reason for not analysing codes reference table](/em/10_Reason_for_not_analysing_codes/) where a planned or selected set could not be analysed.

### Set Log Data

The set-log table captures timestamped events recorded during the setting and hauling of a fishing set.

Each row represents one EM set-log event and contains the parent trip and set identifiers, event type, event timestamp, position, optional float identifier, and comments.

**Download templates:** [WCPFC minimum CSV](./templates/em_setlog_minimum_v1.0.csv) | [Comprehensive CSV](./templates/em_setlog_v1.0.csv)

#### WCPFC minimum CSV example

| em_trip_id | em_set_id | log_type | log_datetime | log_lat | log_lon |
|---|---|---|---|---|---|
| OCEANVOYAGER20250315 | OCEANVOYAGER2025031520250316194500 | SS | 2025-03-16T19:45:00Z | -1518.240 | +17632.520 |

#### Field descriptions

| Field name | Type | Format | Description | Mandatory |
|------------|------|--------|-------------|-----------|
| em_trip_id | Text | Text | Identifier of the parent EM trip. The value must exactly match an em_trip_id in the Trip CSV submitted in the same dataset. | No |
| em_set_id | Text | Text | Identifier of the parent EM set. The value must exactly match an em_set_id in the Set CSV submitted in the same dataset. | No |
| log_type | Text | SS \| FS \| SE \| HS \| FH \| HE | Code identifying the set-log event: SS = set start, FS = float deployed, SE = set end, HS = haul start, FH = float haul, and HE = haul end. | No |
| log_datetime | DateTime | ISO 8601 UTC: YYYY-MM-DDTHH:MM:SSZ | UTC date and time of the set-log event. | Yes |
| log_lat | Text | Signed DDMM.MMM | Latitude at the time of the set-log event. | Yes |
| log_lon | Text | Signed DDDMM.MMM | Longitude at the time of the set-log event. | Yes |
| float_id | Number | Integer | Incremental identifier assigned to a float during setting or hauling, where applicable. | No |
| comments | Text | Text | Comments or additional information about the set-log event. | No |

> **Notes:**
> - `em_trip_id` and `em_set_id` must exactly match the corresponding identifiers in the Trip and Set CSV files submitted in the same dataset.
> - `log_type` must use one of the standard EM set log event codes: `SS` (set start), `FS` (float deployed), `SE` (set end), `HS` (haul start), `FH` (float haul), or `HE` (haul end).
> - Set start, set end, haul start, and haul end information are mandatory WCPFC EM data fields. Therefore, each set must include `SS`, `SE`, `HS`, and `HE` set-log events. Float deployment and float haul information are not mandatory; however, where float information is captured, the corresponding `FS` and `FH` set-log events must be provided.

### Catch Level Data

The catch-level table captures information about individual catch events identified during EM analysis.

Each row represents one catch event and contains the parent trip and set identifiers, catch identifiers, analysis/review attributes, species and fate information, measurements, catch position, and Species of Special Interest interaction information.

**Download templates:** [WCPFC minimum CSV](./templates/em_catch_minimum_v1.0.csv) | [Comprehensive CSV](./templates/em_catch_v1.0.csv)

#### WCPFC minimum CSV example

| em_trip_id | em_set_id | em_catch_id | catch_datetime | hook_no | species_code | fate_code | condition_code | condition_release_code | length_code | length | sex_code | catch_lat | catch_lon | ssi_gear_interaction_code |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OCEANVOYAGER20250315 | OCEANVOYAGER2025031520250316194500 | OCEANVOYAGER2025031520250316194500C0001 | 2025-03-17T08:42:00Z | 12 | YFT | RGG | A1 |  | UF | 122.5 | U | -1708.460 | +17826.460 | IHI |

#### Field descriptions

| Field name | Type | Format | Description | Mandatory |
|------------|------|--------|-------------|-----------|
| em_trip_id | Text | Text | Identifier of the parent EM trip. The value must exactly match an em_trip_id in the Trip CSV submitted in the same dataset. | No |
| em_set_id | Text | Text | Identifier of the parent EM set. The value must exactly match an em_set_id in the Set CSV submitted in the same dataset. | No |
| em_catch_id | Text | Text | Unique identifier for the catch event. The identifier must be constructed using the parent em_set_id followed by C and a four-digit sequential catch number within the set. | No |
| catch_analysis_method | Text | Text | Describes how the EM data for the catch were generated, particularly where AI tools are used. For example: "This catch was analysed by humans only" or "This catch was analysed by humans and AI tools". | No |
| em_catch_analyst_codes | List | Valid JSON array of text codes | Code(s) for the EM analyst(s) who produced EM data at the catch level. | No |
| em_catch_reviewer_codes | List | Valid JSON array of text codes | Code(s) for the EM Data Quality Reviewer(s) at the catch level. When one or more reviewer codes are provided, this indicates that a data quality review was conducted at the catch level. | No |
| snap_datetime | Text | ISO 8601 UTC: YYYY-MM-DDTHH:MM:SSZ | UTC date and time, to the nearest second, when the branchline snap for the catch event is removed from the mainline. | No |
| catch_datetime | Text | ISO 8601 UTC: YYYY-MM-DDTHH:MM:SSZ | UTC date and time, to the nearest second, of the catch event as recorded by the EM equipment. | No |
| camera_id | Text | Text | Identifier of the EM camera that recorded the catch event. | No |
| hook_no | Number | Integer | Hook number between successive floats on which the catch was caught. | Yes |
| species_code | Text | FAO ASFIS 3-character species code | FAO ASFIS 3-character code for the species identified from the catch event. Refer to the [Species codes reference table](/em/01_Species_codes/) and the [FAO ASFIS species list](https://www.fao.org/fishery/en/collection/asfis/en). | Yes |
| fate_code | Text | Regional fate code | Regional fate code indicating whether and how the catch was retained, discarded, or escaped. Refer to the [Fate codes reference table](/em/02_Fate_codes/). | Yes |
| condition_code | Text | Regional condition code | Regional code describing the condition of the catch when caught. Refer to the [Condition codes reference table](/em/03_Condition_codes/). | Yes |
| condition_release_code | Text | Regional condition code; blank if not applicable | Regional code describing the condition of the catch when released or discarded. Leave blank when the catch is retained. Refer to the [Condition codes reference table](/em/03_Condition_codes/). | Yes |
| digital_measuring_method | Text | Digital measuring method code | Code for the digital measuring method used to produce the specimen length. Refer to the [Digital measuring method codes reference table](/em/11_Digital_measuring_method_codes/). | No |
| is_footage_quality_sufficient | Boolean | true / false; blank if unknown or not applicable | Indicates whether footage quality is sufficient for the specimen to be measured precisely and identified with confidence. | No |
| is_fish_in_calibration_area | Boolean | true / false; blank if unknown or not applicable | Indicates whether the measured specimen is positioned within the calibration area on deck. | No |
| is_length_accurate | Boolean | true / false; blank if unknown or not applicable | Indicates whether the digital length measurement is considered accurate. For a measurement to be accurate, digital calibration, sufficient footage quality, and placement within the calibration area must all be true. If digital_measuring_method is M2, this value must be false. | No |
| length_code | Text | Regional length code | Regional code identifying the type of length measurement. If digital_measuring_method is M1, length_code cannot be OW; if digital_measuring_method is M2, length_code must be OW. Refer to the [Length codes reference table](/em/04_Length_codes/). | Yes |
| length | Number | Decimal number (cm), max 1 decimal place | Digital length measurement of the specimen in centimetres, to a maximum of one decimal place. Refer to pages 77–79 of the [Longline Observer Guide](https://www.spc.int/DigitalLibrary/Doc/FAME/Manuals/Longline_Observer_Guide_2021.html) for regional length-measurement protocols. | Yes |
| sex_code | Text | Regional sex code | Regional code for the sex of the catch, where it can be determined. Refer to the [Sex codes reference table](/em/06_Sex_codes/). | Yes |
| catch_weight_vessel | Number | Decimal number (kg), max 1 decimal place | Weight of the specimen in kilograms, to the nearest decimal, as measured by the vessel crew. | No |
| catch_weight_code | Text | Regional weight code | Regional code describing the weight recorded for the specimen. Refer to the [Weight codes reference table](/em/13_Weight_codes/). | No |
| weighing_method | Text | Regional weighing method code | Code for the method used to produce catch_weight_vessel. Refer to the [Weighing method codes reference table](/em/14_Weighing_method_codes/). | No |
| catch_lat | Text | ISO 6709: signed DDMM.MMM | Latitude at the time of the catch event. | No |
| catch_lon | Text | ISO 6709: signed DDDMM.MMM | Longitude at the time of the catch event. | No |
| ssi_gear_interaction_code | Text | SSI gear interaction code; blank if not applicable | Regional gear-interaction code for Species of Special Interest (SSI). Refer to the [Gear interaction codes reference table](/em/05_Gear_interaction_codes/) and [SSI codes reference table](/em/15_SSIS_codes/). Additional guidance on SSI vessel interactions is provided on pages 97–98 of the [Longline Observer Guide](https://www.spc.int/DigitalLibrary/Doc/FAME/Manuals/Longline_Observer_Guide_2021.html). | Yes |
| tag_recovery_note | Text | Text | Text note recording tag recovery information for the catch event, where applicable. | No |
| ema_comments | Text | Text | Comments from the EM analyst about the catch event. | No |

> **Notes:**
> - `em_trip_id` and `em_set_id` must exactly match the corresponding identifiers in the Trip and Set CSV files submitted in the same dataset.
> - `em_catch_id` must be unique within the submission. It must be constructed using the parent `em_set_id`, followed by `C` and a four-digit sequential catch number within the set, for example `C0001`. The catch sequence restarts for each set.
> - `catch_datetime`, `catch_lat`, and `catch_lon` are not mandatory for all catch records. However, for Species of Special Interest (SSI) interactions, the interaction date and time, latitude, and longitude are mandatory WCPFC EM data fields and must be provided.

### Potential Compliance Event Data

The potential compliance event table captures events identified during EM analysis that may require compliance review.

Each row represents one potential compliance event and records when and where the event occurred, what part of the EM record it relates to, the applicable compliance category and event codes, and analyst comments.

**Download templates:** [WCPFC minimum CSV](./templates/em_compliance_minimum_v1.0.csv) | [Comprehensive CSV](./templates/em_compliance_v1.0.csv)

#### WCPFC minimum CSV example

| em_trip_id | event_id | event_datetime | event_relation | event_relation_id | event_lat | event_lon | event_category_code | event_type_code |
|---|---|---|---|---|---|---|---|---|
| OCEANVOYAGER20250315 | OCEANVOYAGER20250315E0001 | 2025-03-17T06:30:00Z | Set | OCEANVOYAGER2025031520250316194500 | -1529.100 | +17702.520 | P | P1 |

#### Field descriptions

| Field name | Type | Format | Description | Mandatory |
|------------|------|--------|-------------|-----------|
| em_trip_id | Text | Text | Identifier of the parent EM trip. The value must exactly match an em_trip_id in the Trip CSV submitted in the same dataset. | No |
| event_id | Text | Text | Unique identifier for the potential compliance event. The identifier must be constructed using the parent em_trip_id followed by E and a four-digit sequential compliance-event number within the trip. | No |
| event_datetime | DateTime | ISO 8601 UTC: YYYY-MM-DDTHH:MM:SSZ | UTC date and time of the potential compliance event. Compliance events may occur outside setting and hauling operations. | No |
| event_relation | Text | Trip \| Set \| Catch | Indicates the EM record level to which the event relates: Trip, Set, or Catch. | No |
| event_relation_id | Text | Text | Identifier of the related Trip, Set, or Catch record. Provide the applicable em_trip_id, em_set_id, or em_catch_id according to event_relation. | No |
| event_lat | Text | Signed DDMM.MMM | Latitude at the time of the potential compliance event. | No |
| event_lon | Text | Signed DDDMM.MMM | Longitude at the time of the potential compliance event. | No |
| event_category_code | Text | Regional compliance category code | Category code for the potential compliance issue identified by the EM analyst. Refer to the [Potential Compliance Categories and Events reference table](/em/07_Potential_Compliance_categories_and_Events_reference_codes/). | Yes |
| event_type_code | Text | Regional compliance event code | Specific compliance event code within the selected compliance category. Refer to the [Potential Compliance Categories and Events reference table](/em/07_Potential_Compliance_categories_and_Events_reference_codes/). | Yes |
| comments | Text | Text | Comments from the EM analyst describing the potential compliance event and relevant observable facts. | No |

> **Notes:**
> - `em_trip_id` must exactly match an `em_trip_id` in the Trip CSV submitted in the same dataset.
> - `event_id` must be unique within the submission. It must be constructed using the parent `em_trip_id`, followed by `E` and a four-digit sequential compliance-event number within the trip, for example `E0001`. The event sequence restarts for each trip.
> - `event_relation` identifies whether the event relates to a Trip, Set, or Catch record. The corresponding `event_relation_id` must contain the applicable `em_trip_id`, `em_set_id`, or `em_catch_id`.
> - `event_category_code` and `event_type_code` must use the standard codes in the [Potential Compliance Categories and Events reference table](/em/07_Potential_Compliance_categories_and_Events_reference_codes/).
> - Compliance issues are reported through the structured event records; separate Yes/No summary fields are not required where the corresponding result can be derived from these records.
