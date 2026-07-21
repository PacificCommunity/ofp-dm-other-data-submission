## FAD Buoy Data Format

Fish Aggregating Device (FAD) buoy data encompasses two categories of information collected by electronic buoys deployed at sea by purse seine fishing vessels: **positional data** (GPS fixes transmitted at regular intervals) and **echosounding data** (acoustic biomass estimates of fish aggregations beneath the buoy).

FAD buoy data are submitted by **buoy technology providers** on behalf of fishing companies, in compliance with ISSF Conservation Measure 3.7 and the reporting obligations of tuna Regional Fisheries Management Organisations (RFMOs). Data are used by SPC–OFP for FAD monitoring, stock assessment inputs, and ecosystem studies.

Each record in a position file represents a single GPS transmission from a buoy. Each record in an echosounding file represents a single acoustic reading, linked to a position record via a unique transmission identifier. The **combined format** — where position and echosounding data are provided in a single file — is the **preferred submission format**, as it directly associates each acoustic reading with its corresponding GPS fix.

Submissions must cover data from within the **WCPFC Convention Area**. Where FADs drift across the WCPFC–IATTC overlap zone, data may be shared with IATTC in accordance with inter-RFMO agreements.

---

## ISSF Guidelines Reminder

Submission of FAD buoy data is governed by **ISSF Conservation Measure 3.7** (Transactions with Vessels or Companies with Vessel-Based FAD Management Policies). The relevant requirements are:

- Purse seine vessels and supply vessels covered by a FAD Management Policy must report **FAD position data** to the relevant RFMO science bodies and/or national scientific institutions and/or their flag State.
- Reporting must occur with a **maximum time lag of 90 days**.
- Where data are reported to national institutions, those institutions must make the data available to the relevant RFMO for scientific purposes.

**ISSF minimum required data fields:**

- Buoy ID
- Fishing Company
- Vessel Name / Vessel IMO Number
- Date
- Time
- Latitude
- Longitude

The SPC–OFP standard described in this document is fully consistent with and extends these minimum requirements.

**Submission schedule (recommended):**

| FAD buoy data for month of… | Submission deadline |
| --------------------------- | ------------------- |
| January 2026                | 31 March 2026       |
| February 2026               | 30 April 2026       |
| March 2026                  | 30 May 2026         |
| …                           | …                   |

Data for each calendar month should be submitted as a complete file before the 90-day deadline.

---

## Field Formatting Details

- All **datetime fields** must be in ISO 8601 format: `YYYY-MM-DD HH:MM:SS`, expressed in **UTC**. Local times are not accepted.
- **Coordinates** must be in **signed decimal degrees**: negative values for South latitudes and West longitudes (e.g. `-10.2345` for 10.2345°S). A minimum of **2 decimal places** is required; **4 decimal places** is strongly recommended for scientific usability.
- **Coordinates are mandatory** and must never be blank. Records without a valid GPS fix should not be submitted.
- The **`transmission_id`** field must be unique within a submission file. It serves as the primary key linking position records to echosounding records when data are submitted in two separate files. If no natural unique identifier exists in the source system, providers should generate a synthetic key (e.g. `{buoy_id}_{transmission_datetime}` with special characters removed).
- **Echosounding values** (`sounder_values`) must be provided as a **dash-separated string** of numeric values, one per depth layer (e.g. `0-0-3-5-12-8-0-0`). The depth covered by each layer is defined by `start_depth_m` and `sounder_depth_interval_m`. The total depth range is implicit from the number of values in the string.
- **`buoy_provider`** must use the two-letter codes defined in Reference Table 1. For providers not yet listed, contact SPC–OFP to request addition to the reference table before submission.
- **`sounder_unit`** must use the codes defined in Reference Table 2.
- **File format**: CSV (`.csv`) or Excel (`.xlsx`) are accepted. UTF-8 encoding is required for CSV files.
- **File naming convention**: `FAD_{buoy_provider}_{vessel_imo}_{YYYYMM}.csv` (or `.xlsx`). Example: `FAD_SL_1024172_202508.csv`.
- **Submission channel**: files must be sent to **ofp.fad.data@spc.int**.
- **Submission frequency**: monthly, one file per vessel per month, covering the complete calendar month.

---

## Document Structure and Data Fields Format

FAD buoy data may be submitted in one of three formats:

- **Combined format** *(preferred)*: positions and echosounding data in a single file. Each row contains a position fix and, where available, an associated echosounding reading. Rows with no echosounding data leave the sounder fields blank.
- **Positions-only format**: a file containing only GPS position records. Must be paired with a separate echosounding file using `transmission_id` as the linking key.
- **Echosounding-only format**: a file containing only acoustic readings, each referencing a position record via `transmission_id`.

### CSV Data Templates

- [Combined Template — Positions + Echosounding](./templates/FAD_combined_template.csv)
- [Positions-only Template](./templates/FAD_positions_template.csv)
- [Echosounding-only Template](./templates/FAD_echosounding_template.csv)

---

### Combined Format (Preferred)

This is the recommended submission format. Each row represents one position transmission. Echosounding fields are populated where an acoustic reading is associated with that transmission; they are left blank where no echosounding data exists for that position fix.

#### Example — Combined format

| transmission_id | buoy_id    | buoy_provider | vessel_name | vessel_imo | transmission_datetime | latitude  | longitude  | speed_knots | water_temp_c | heading_degrees | battery_voltage | deployment_date     | buoy_model | buoy_type | sounder_datetime    | start_depth_m | sounder_depth_interval_m | sounder_unit | sounder_values              |
| --------------- | ---------- | ------------- | ----------- | ---------- | --------------------- | --------- | ---------- | ----------- | ------------ | --------------- | --------------- | ------------------- | ---------- | --------- | ------------------- | ------------- | ------------------------ | ------------ | --------------------------- |
| TXN-001         | SLX+485094 | SL            | Vessel A    | 1024172    | 2025-08-01 20:07:00   | -10.2345  | 123.2346   | 0.06        | 29.0         |                 |                 | 2025-03-13 00:00:00 |            | echo      | 2025-08-01 18:34:00 | 0             | 10                       | index        | 0-0-0-0-0-0-0-0-0-1        |
| TXN-002         | SLX+485094 | SL            | Vessel A    | 1024172    | 2025-08-02 20:07:00   | -10.1982  | 123.2501   | 0.19        | 28.0         |                 |                 | 2025-03-13 00:00:00 |            | echo      |                     |               |                          |              |                             |
| TXN-003         | T8X-374142 | ZB            | Vessel B    | 9587548    | 2025-12-01 00:30:00   | -3.4521   | 156.7823   | 0.4         | 30.5         | 217             |                 | 2025-11-14 07:36:00 |            | echo      | 2025-12-01 00:28:00 | 0             | 10                       | t            | 0-0-2.5-3.2-8.6-5.6-0-0-0-0-0-0-0 |

#### Field descriptions — Combined format

| Field name                 | Type     | Format / Allowed values                          | Description                                                                                                                                   | Mandatory                              |
| -------------------------- | -------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| transmission_id            | String   | Free text, unique within file                    | Unique identifier for this position transmission. Used as the primary key to link echosounding records when submitted in a separate file.     | No                                    |
| buoy_id                    | String   | Free text                                        | Buoy identifier as assigned by the buoy technology provider.                                                                                  | Yes                                    |
| buoy_provider              | String   | 2-letter code — see Reference Table 1            | Code identifying the buoy technology provider. Determines how to interpret provider-specific fields.                                          | Yes                                    |
| vessel_name                | String   | Free text                                        | Name of the fishing vessel operating the buoy.                                                                                                | Yes                                    |
| vessel_imo                 | Number   | 7-digit IMO number                               | IMO number of the fishing vessel. Used as the primary vessel identifier.                                                                      | Yes                                    |
| transmission_datetime      | Datetime | YYYY-MM-DD HH:MM:SS (UTC)                        | Date and time of the GPS position transmission, in UTC.                                                                                       | Yes                                    |
| latitude                   | Number   | Signed decimal degrees, min. 2 decimal places    | Latitude of the buoy at time of transmission. Negative values indicate South.                                                                 | Yes                                    |
| longitude                  | Number   | Signed decimal degrees, min. 2 decimal places    | Longitude of the buoy at time of transmission. Negative values indicate West.                                                                 | Yes                                    |
| speed_knots                | Number   | Decimal, knots                                   | Speed of the buoy (drift speed) at time of transmission, in knots.                                                                            | No                                     |
| water_temp_c               | Number   | Decimal, degrees Celsius                         | Sea surface temperature recorded by the buoy sensor, in degrees Celsius.                                                                      | No                                     |
| heading_degrees            | Number   | 0–360, degrees                                   | Heading or drift direction of the buoy, in degrees from North.                                                                                | No                                     |
| battery_voltage            | Number   | Decimal, volts                                   | Battery voltage of the buoy at time of transmission.                                                                                          | No                                     |
| deployment_date            | Datetime | YYYY-MM-DD HH:MM:SS (UTC)                        | Date and time the buoy was deployed or last activated in the water, in UTC.                                                                   | No                                     |
| buoy_model                 | String   | Free text                                        | Model name or identifier of the buoy hardware (e.g. `KTI-21SF`).                                                                             | No                                     |
| buoy_type                  | String   | Free text                                        | Category or type of the buoy (e.g. `echo`, `tracking`).                                                                                      | No                                     |
| sounder_datetime           | Datetime | YYYY-MM-DD HH:MM:SS (UTC)                        | Date and time the echosounding reading was taken, in UTC. May differ from `transmission_datetime`.                                            | Yes, if echosounding data is present   |
| start_depth_m              | Number   | Integer, metres                                  | Depth of the first echosounding layer, in metres (typically 0 for surface).                                                                   | Yes, if echosounding data is present   |
| sounder_depth_interval_m   | Number   | Integer, metres                                  | Depth interval represented by each layer in `sounder_values`, in metres (e.g. `10` means each value covers a 10 m depth band).               | Yes, if echosounding data is present   |
| sounder_unit               | String   | 2-letter code — see Reference Table 2            | Unit of the values in `sounder_values`.                                                                                                       | Yes, if echosounding data is present   |
| sounder_values             | String   | Dash-separated numeric string (e.g. `0-0-3-5-2`) | Echosounding values, one per depth layer, from shallowest to deepest. The depth range of layer N is `start_depth_m + (N-1) * sounder_depth_interval_m` to `start_depth_m + N * sounder_depth_interval_m`. | Yes, if echosounding data is present   |

---

### Positions-only Format

Used when positions and echosounding data are submitted in two separate files. Each row represents one GPS transmission. The `transmission_id` field is mandatory and must match corresponding records in the echosounding file.

#### Example — Positions-only

| transmission_id | buoy_id    | buoy_provider | vessel_name | vessel_imo | transmission_datetime | latitude | longitude | speed_knots | water_temp_c | heading_degrees | battery_voltage | deployment_date     | buoy_model | buoy_type |
| --------------- | ---------- | ------------- | ----------- | ---------- | --------------------- | -------- | --------- | ----------- | ------------ | --------------- | --------------- | ------------------- | ---------- | --------- |
| TXN-001         | SLX+485094 | SL            | Vessel A    | 1024172    | 2025-08-01 20:07:00   | -10.2345 | 123.2346  | 0.06        | 29.0         |                 |                 | 2025-03-13 00:00:00 |            | echo      |
| TXN-002         | SLX+485094 | SL            | Vessel A    | 1024172    | 2025-08-02 20:07:00   | -10.1982 | 123.2501  | 0.19        | 28.0         |                 |                 | 2025-03-13 00:00:00 |            | echo      |

Field descriptions for the positions-only format are identical to the position-related fields in the combined format table above.

---

### Echosounding-only Format

Used when submitted separately from position data. Each row represents one acoustic reading. The `transmission_id` must match a record in the corresponding positions file. Where an exact `transmission_id` match is not possible (e.g. because the sounder fires on a different schedule than the GPS), provide `buoy_id` and `sounder_datetime` — SPC will perform a nearest-position match at ingestion.

#### Example — Echosounding-only

| transmission_id | buoy_id    | buoy_provider | sounder_datetime    | start_depth_m | sounder_depth_interval_m | sounder_unit | sounder_values              |
| --------------- | ---------- | ------------- | ------------------- | ------------- | ------------------------ | ------------ | --------------------------- |
| TXN-001         | SLX+485094 | SL            | 2025-08-01 18:34:00 | 0             | 10                       | index        | 0-0-0-0-0-0-0-0-0-1        |
| TXN-003         | T8X-374142 | ZB            | 2025-12-01 00:28:00 | 0             | 10                       | t            | 0-0-2.5-3.2-8.6-5.6-0-0-0-0-0-0-0 |

#### Field descriptions — Echosounding-only

| Field name               | Type     | Format / Allowed values                          | Description                                                                                                                                   | Mandatory |
| ------------------------ | -------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| transmission_id          | String   | Free text, matches position file                 | Identifier linking this echosounding record to a position record in the positions file. Should match `transmission_id` in the positions file. | Yes       |
| buoy_id                  | String   | Free text                                        | Buoy identifier as assigned by the buoy technology provider.                                                                                  | Yes       |
| buoy_provider            | String   | 2-letter code — see Reference Table 1            | Code identifying the buoy technology provider.                                                                                                | Yes       |
| sounder_datetime         | Datetime | YYYY-MM-DD HH:MM:SS (UTC)                        | Date and time the echosounding reading was taken, in UTC.                                                                                     | Yes       |
| start_depth_m            | Number   | Integer, metres                                  | Depth of the first echosounding layer, in metres.                                                                                             | Yes       |
| sounder_depth_interval_m | Number   | Integer, metres                                  | Depth interval represented by each layer in `sounder_values`, in metres.                                                                      | Yes       |
| sounder_unit             | String   | 2-letter code — see Reference Table 2            | Unit of the values in `sounder_values`.                                                                                                       | Yes       |
| sounder_values           | String   | Dash-separated numeric string                    | Echosounding values, one per depth layer, from shallowest to deepest.                                                                         | Yes       |

---

## References

### Reference Table 1 — Buoy Provider Codes

This list is maintained by SPC–OFP. Providers not listed should contact [ofp.fad.data@spc.int](mailto:ofp.fad.data@spc.int) to request addition before submitting data.

| Code | Provider name        | Website / Contact                        |
| ---- | -------------------- | ---------------------------------------- |
| SL   | SatLink              | https://www.satlink.es                   |
| ZB   | Zunibal              | https://www.zunibal.com                  |
| KT   | Kato Denki           | https://www.kato-denki.com               |
| MI   | Marine Instruments   | https://www.marine-instruments.es        |

### Reference Table 2 — Sounder Unit Codes

| Code    | Unit                        | Description                                                                                                                                          |
| ------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| t       | Metric tonnes               | Estimated biomass beneath the buoy, expressed in metric tonnes. Typically derived from the provider's proprietary acoustic-to-biomass conversion model. |
| index   | Dimensionless relative index | A relative biomass index on a provider-specific scale. Values are not directly comparable across providers without calibration metadata.              |
| dB      | Decibels                    | Raw acoustic backscatter expressed in decibels. Requires additional processing to derive biomass estimates.                                           |
