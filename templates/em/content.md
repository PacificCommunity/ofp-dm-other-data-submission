## Electronic Monitoring (EM) Longline CSV Data Format

Electronic Monitoring (EM) data provide detailed records of fishing operations and catch events derived from onboard video cameras, sensors, and EM analysis systems. These data are produced through a structured review process conducted by trained EM analysts and, in some cases, supported by automated or artificial intelligence tools.

EM data capture information related to fishing activities, including trip metadata, gear deployment, catch events, species identification, and potential compliance observations. They support both **scientific monitoring** (for example, species composition, catch characterisation and fishing effort) and **compliance monitoring** (for example, mitigation measures, protected-species interactions and operational practices).

The EM Longline CSV templates provide a structured tabular format for submitting EM data to SPC/OFP. The templates incorporate the [WCPFC Interim Electronic Monitoring Minimum Data Fields](https://meetings.wcpfc.int/node/24512), together with additional fields required to support regional data management and submission processes. Field names, definitions, formats, codes and field order are aligned, where applicable, with the [EM Longline JSON standard](https://pacificcommunity.github.io/tufman2-json-standard/longline-em/). This alignment provides consistency between the CSV and JSON submission formats and supports future transition to direct JSON submission.

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

- **Yes** – a corresponding field is identified in the **DCC and/or WCPFC Field Name** column of the EM Longline specification.
- **No** – the field is supplementary to the WCPFC minimum data fields and has been included to support requirements such as data quality, traceability, national programme needs, or the CSV relational structure.

A value of **No does not necessarily mean that the field can be omitted**. Some non-minimum fields may still be needed to support relationships between the CSV tables, conversion of the CSV submission to the corresponding structured format, applicable DQC validation rules, or additional national EM programme requirements.

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

The downloadable Trip, Set, Set Log, Catch and Compliance Event templates and their field descriptions are provided below.
