## Electronic Monitoring (EM) Longline CSV Data Format

Electronic Monitoring (EM) data provide detailed records of fishing operations and catch events derived from onboard video cameras, sensors, and EM analysis systems. These data are produced through a structured review process conducted by trained EM analysts and, in some cases, supported by automated or artificial intelligence tools.

EM data capture information related to fishing activities, including trip metadata, gear deployment, catch events, species identification, and potential compliance observations. They support both **scientific monitoring** (for example, species composition, catch characterisation and fishing effort) and **compliance monitoring** (for example, mitigation measures, protected-species interactions and operational practices).

The EM Longline CSV templates are aligned, wherever applicable, with the field names, definitions, formats, codes and field order used in the **EM Longline JSON standard**, which is itself aligned with the WCPFC Interim Electronic Monitoring Minimum Standards. The CSV format provides a practical tabular submission option for national EM programmes and data providers that are not yet producing the regional JSON structure directly.

### CSV as a transition to JSON submission

The CSV templates are intended to support a gradual transition toward direct JSON submission. Data providers should therefore use the JSON-aligned field names, formats and reference codes defined in this specification when producing CSV data.

The current data flow is:

1. A Distant Water Fishing Nation (DWFN) or EM data provider submits EM data using the CSV templates.
2. The CSV tables are converted into the corresponding EM Longline JSON structure.
3. The generated JSON is submitted to the **EM Data Quality Control (DQC) API** for validation.
4. Validation errors are corrected before resubmission.
5. JSON data that pass the applicable DQC checks can then be submitted to the **TUFMAN2 API**.

The longer-term direction is for countries and EM service providers to produce and submit the EM Longline JSON format directly. New or upgraded national EM systems are therefore encouraged to design their outputs around the JSON standard so that future transition from CSV to JSON requires minimal system changes.

---

### Field formatting details

To minimise transformation during CSV-to-JSON conversion, CSV values should use the same representation as the JSON standard wherever possible.

- **Datetime values** must use ISO 8601 format in UTC: `YYYY-MM-DDTHH:MM:SSZ`.
  - Example: `2025-03-15T06:30:00Z`

- **Latitude and longitude** must use the ISO 6709-style representation used by the EM Longline JSON standard, with a maximum of three decimal places in minutes:
  - Latitude: signed `DDMM.MMM`
  - Longitude: signed `DDDMM.MMM`
  - Example latitude: `-1808.460`
  - Example longitude: `+17826.460`

- **Species codes** must use FAO ASFIS 3-character species codes.
  - Example: `YFT` – Yellowfin tuna
  - Example: `ALB` – Albacore tuna

- **Port codes** must use the applicable UN/LOCODE where a port is reported.
  - Example: `FJSUV` – Suva, Fiji

- **Boolean values** must be reported as `true` or `false`. Leave the CSV cell blank when the value is unknown or not applicable. During CSV-to-JSON conversion, an applicable blank nullable value may be represented as JSON `null`.

- **List-type values** must be stored as valid JSON array strings within the CSV cell.
  - Text-code example: `["NNT","RAO"]`
  - Number example: `[4,7]`

- **Numeric values** must use a decimal point (`.`) where a decimal value is required. Do not use thousands separators.

---

### Mandatory field indicator

The **Mandatory** column in the field-description tables identifies whether a field forms part of the **WCPFC Interim Electronic Monitoring Minimum Data Fields**.

- **Yes** – a corresponding field is identified in the **DCC and/or WCPFC Field Name** column of the EM Longline JSON standard.
- **No** – the field is supplementary to the WCPFC minimum data fields and has been included to support requirements such as data quality, traceability, national programme needs, system integration, or the CSV relational structure.

A value of **No does not mean that the field should be omitted**. Some non-minimum fields may still be required by the CSV submission specification, CSV-to-JSON conversion, DQC validation rules, or national programme requirements.

---

### CSV structure and relationships

The current EM CSV specification is structured into three primary data levels:

1. **Trip level** – metadata describing the fishing trip, vessel and EM analysis process.
2. **Set level** – information about individual fishing sets and mitigation measures.
3. **Catch level** – information about individual catch events recorded during analysed sets.

Each level is represented as a separate CSV table to reduce repetition and provide a clear relational structure. The JSON standard is hierarchical, so additional relationship fields are included in the CSV representation where needed to reconstruct the nested JSON objects.

The primary relationships are:

- `em_trip_id` uniquely identifies an EM trip.
- Each Set row contains `em_trip_id` to link the set to its parent Trip row.
- `em_set_id` uniquely identifies an EM set.
- Each Catch row contains both `em_trip_id` and `em_set_id` to link the catch to its parent Trip and Set rows.
- `em_catch_id` uniquely identifies an individual catch event.

Relationship identifiers must match exactly between the CSV files submitted as part of the same dataset. Identifier fields marked as CSV-only relationship fields are used during CSV-to-JSON conversion and do not create additional properties in the nested JSON object where the relationship is already represented by the JSON hierarchy.

The full EM Longline JSON standard also contains **Set Log (EmSetLog)** and **Potential Compliance Event (ComplianceEvent)** structures. These are not yet represented as separate CSV templates in the current three-table release and may be added as the CSV specification is extended toward full JSON coverage.

The downloadable Trip, Set and Catch templates and their field descriptions are provided below.
