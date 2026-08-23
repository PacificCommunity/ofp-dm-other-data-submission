#!/usr/bin/env python3
"""
Dynamic Template Generator for SciData Standards

This script generates CSV templates and Hugo markdown documentation from YAML definitions.
It provides a migration path from hardcoded markdown files to dynamically generated ones.

Usage:
    python generate_templates.py                    # Generate all dynamic templates
    python generate_templates.py --data-type em     # Generate only EM templates
    python generate_templates.py --dry-run          # Preview without writing files
    python generate_templates.py --verbose          # Show detailed output

Structure:
    templates/
        <data_type>/           # e.g., em/, operational-longline/
            content.md         # Custom introduction/description content
            <level>.yaml       # Data level definitions (e.g., trip.yaml, set.yaml)

Output:
    documents/<data_type>/
        _index.md              # Generated Hugo markdown
        templates/
            <data_type>_<level>_v<version>.csv
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


# Configuration for which data types use dynamic generation
# Add data types here as you migrate them from hardcoded to dynamic
DYNAMIC_DATA_TYPES = [
    "em",  # E-Monitoring - first to be migrated
    # Add more as needed:
    # "operational-longline",
    # "aggregated-purseseine",
]

# Preferred order for EM data levels in generated documentation and CSV processing.
EM_LEVEL_ORDER = ["trip", "set", "setlog", "catch", "compliance"]



class TemplateGenerator:
    """Generator class for building markdown and CSV from YAML definitions."""

    def __init__(self, workspace_root: Path | None = None, verbose: bool = False):
        self.verbose = verbose
        self.workspace_root = workspace_root or self._find_workspace_root()
        self.templates_dir = self.workspace_root / "templates"
        self.documents_dir = self.workspace_root / "documents"
        self.static_downloads_dir = self.workspace_root / "site-generator" / "static" / "downloads" / "templates"

    def _find_workspace_root(self) -> Path:
        """Find the workspace root by looking for known directories."""
        # Check common locations
        candidates = [
            Path.cwd(),
            Path.cwd().parent,
            Path(__file__).parent.parent,
        ]

        for candidate in candidates:
            if (candidate / "templates").exists() and (candidate / "documents").exists():
                return candidate
            if (candidate / "site-generator").exists():
                return candidate

        # Default to current directory
        return Path.cwd()

    def log(self, message: str, level: str = "info"):
        """Print log message if verbose mode is enabled."""
        symbols = {"info": "ℹ", "success": "✓", "warning": "⚠", "error": "✗"}
        symbol = symbols.get(level, "•")
        if self.verbose or level in ("success", "error", "warning"):
            print(f"  {symbol} {message}")

    def load_yaml_file(self, yaml_path: Path) -> dict[str, Any] | None:
        """Load and parse a YAML file."""
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.log(f"Error parsing YAML file {yaml_path}: {e}", "error")
            return None
        except FileNotFoundError:
            self.log(f"YAML file not found: {yaml_path}", "warning")
            return None

    def load_content_file(self, data_type: str) -> str | None:
        """Load custom content.md for a data type."""
        content_path = self.templates_dir / data_type / "content.md"
        if content_path.exists():
            with open(content_path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def load_data_type_templates(self, data_type: str) -> dict[str, dict]:
        """
        Load all YAML template definitions for a data type.
        
        Returns a dictionary with data levels as keys (trip, set, catch, etc.)
        and their parsed YAML content as values.
        """
        data_type_dir = self.templates_dir / data_type
        if not data_type_dir.exists():
            self.log(f"Data type directory not found: {data_type_dir}", "warning")
            return {}

        templates = {}
        
        # Load all YAML files in the data type directory
        for yaml_file in sorted(data_type_dir.glob("*.yaml")):
            data = self.load_yaml_file(yaml_file)
            if data:
                # Use the filename (without extension) as the level name
                level_name = yaml_file.stem
                templates[level_name] = data
                self.log(f"Loaded {level_name} template from {yaml_file.name}")

        return templates

    def _csv_columns(self, template_data: dict) -> dict[str, dict]:
        """Return fields that belong in the CSV representation.

        Fields explicitly marked ``json_only: true`` are documented in the
        JSON model but are not written as CSV columns. CSV-only relationship
        fields remain included.
        """
        columns = template_data.get("columns", {})
        return {
            name: spec
            for name, spec in columns.items()
            if not spec.get("json_only", False)
        }

    def _format_example_value(self, value: Any) -> str:
        """Format YAML example values consistently for CSV and markdown."""
        if value is None:
            return ""
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (list, dict)):
            return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        return str(value)

    def _escape_markdown_cell(self, value: Any) -> str:
        """Escape values so generated markdown tables remain valid."""
        text = self._format_example_value(value)
        return text.replace("|", "\\|").replace("\r", " ").replace("\n", "<br>")

    def generate_csv_template(
        self,
        data_type: str,
        level_name: str,
        template_data: dict,
        dry_run: bool = False,
    ) -> Path:
        """
        Generate a CSV template file with header and example row.
        
        Returns the path to the generated file.
        """
        # Determine output directory
        output_dir = self.documents_dir / data_type / "templates"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Also create in static downloads for Hugo
        self.static_downloads_dir.mkdir(parents=True, exist_ok=True)

        # Get version from metadata
        version = template_data.get("metadata", {}).get("version", "1.0")
        
        # Generate filename: em_trip_v1.0.csv
        csv_filename = f"{data_type}_{level_name}_v{version}.csv"
        csv_path = output_dir / csv_filename
        csv_static_path = self.static_downloads_dir / csv_filename

        if dry_run:
            self.log(f"Would generate CSV: {csv_path}", "info")
            return csv_path

        # Get columns and example data
        columns = self._csv_columns(template_data)
        col_names = list(columns.keys())

        # Use example values from column definitions. List/dict examples are
        # serialized as valid JSON so the sample row mirrors the documented
        # CSV convention for list-type fields.
        example_row = [
            self._format_example_value(columns[col].get("example", ""))
            for col in col_names
        ]

        # Write CSV to documents directory
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(col_names)
            writer.writerow(example_row)

        # Also write to static downloads
        with open(csv_static_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(col_names)
            writer.writerow(example_row)

        self.log(f"Generated CSV: {csv_filename}", "success")
        return csv_path

    def _format_type(self, col_type: str) -> str:
        """Convert YAML type to display type."""
        type_map = {
            "int": "Number",
            "float": "Number",
            "str": "Text",
            "string": "Text",
            "bool": "Boolean",
            "date": "Date",
            "datetime": "DateTime",
            "list": "List",
            "array": "List",
        }
        return type_map.get(col_type.lower(), col_type.capitalize())

    def _generate_level_section(
        self,
        level_name: str,
        template_data: dict,
        data_type: str,
    ) -> list[str]:
        """Generate markdown section for a single data level."""
        lines = []
        
        metadata = template_data.get("metadata", {})
        section = template_data.get("section", {})
        columns = self._csv_columns(template_data)
        version = metadata.get("version", "1.0")

        # Section title
        title = section.get("title", level_name.replace("_", " ").title() + " Data")
        lines.append(f"### {title}")
        lines.append("")

        # Introduction text
        intro = section.get("intro", "")
        if intro:
            lines.append(intro.strip())
            lines.append("")

        # Download link
        csv_filename = f"{data_type}_{level_name}_v{version}.csv"
        lines.append(f"**Download template:** [CSV Template](./templates/{csv_filename})")
        lines.append("")

        # Example row table
        lines.append("#### Example data")
        lines.append("")
        
        col_names = list(columns.keys())
        example_row = [
            self._escape_markdown_cell(columns[col].get("example", ""))
            for col in col_names
        ]

        lines.append("| " + " | ".join(col_names) + " |")
        lines.append("|" + "|".join(["---" for _ in col_names]) + "|")
        lines.append("| " + " | ".join(example_row) + " |")
        lines.append("")

        # Field descriptions table
        lines.append("#### Field descriptions")
        lines.append("")
        lines.append("| Field name | Type | Format | Description | Mandatory |")
        lines.append("|------------|------|--------|-------------|-----------|")

        for col_name, col_spec in columns.items():
            field_type = self._format_type(col_spec.get("type", "str"))
            format_val = self._escape_markdown_cell(col_spec.get("format", ""))
            description = self._escape_markdown_cell(col_spec.get("description", ""))
            mandatory = "Yes" if col_spec.get("mandatory", False) else "No"

            lines.append(
                f"| {col_name} | {field_type} | {format_val} | {description} | {mandatory} |"
            )

        lines.append("")

        # Notes section
        notes = section.get("notes", "")
        if notes:
            lines.append("> **Notes:**")
            for line in notes.strip().split("\n"):
                line = line.strip()
                if line.startswith("-"):
                    lines.append(f"> {line}")
                elif line:
                    lines.append(f"> - {line}")
            lines.append("")

        return lines

    # NEW: Generate reference tables section
    def _generate_reference_tables_section(
        self,
        templates: dict[str, dict],
    ) -> list[str]:
        """
        Generate a 'Reference tables' section aggregated from all level YAMLs.

        Expected YAML structure (in each level yaml):
        reference_tables:
            <table_id>:
            title: "Reference Table: ..."
            description: "..."
            columns: ["Code", "Description"]   # optional
            rows:
                - ["FULL", "Full review ..."]    # preferred simple row format
                - ["COMPLIANCE_ONLY", "..."]
            # OR rows as dicts:
            # rows:
            #   - code: FULL
            #     description: ...
        """
        lines: list[str] = []
        tables: list[tuple[str, dict]] = []

        # Collect tables from all levels, preserving level order
        for level_name, template_data in templates.items():
            ref_tables = template_data.get("reference_tables", {})
            if isinstance(ref_tables, dict):
                for table_id, table_spec in ref_tables.items():
                    tables.append((table_id, table_spec))
            elif isinstance(ref_tables, list):
                # If you ever choose list-style reference_tables later
                for table_spec in ref_tables:
                    if isinstance(table_spec, dict) and "id" in table_spec:
                        tables.append((table_spec["id"], table_spec))

        if not tables:
            return lines  # nothing to append

        lines.append("## Reference tables")
        lines.append("")

        # Render each table
        for idx, (table_id, table_spec) in enumerate(tables, start=1):
            title = table_spec.get("title") or f"Reference Table {idx}: {table_id}"
            description = table_spec.get("description", "").strip()

            # Heading (match your Operational LL style)
            anchor = table_spec.get("anchor")
            if anchor:
                lines.append(f'<a id="{anchor}"></a>')
            lines.append(f"### Reference Table {idx}: {title}")
            
            lines.append("")

            if description:
                lines.append(description)
                lines.append("")

            # Table columns
            header_cols = table_spec.get("columns")
            if not header_cols:
                # Sensible defaults
                header_cols = ["Code", "Description"]

            # Table rows
            rows = table_spec.get("rows", [])
            # Normalize rows to list[list[str]]
            norm_rows: list[list[str]] = []

            for r in rows:
                if isinstance(r, list):
                    norm_rows.append([str(x) for x in r])
                elif isinstance(r, dict):
                    # common keys: code/label/description
                    if len(header_cols) == 2:
                        # try code + description
                        code = r.get("code", r.get("value", ""))
                        desc = r.get("description", r.get("label", ""))
                        norm_rows.append([str(code), str(desc)])
                    else:
                        # fallback: match header keys if possible
                        norm_rows.append([str(r.get(h.lower(), "")) for h in header_cols])

            # Render markdown table
            lines.append("| " + " | ".join(header_cols) + " |")
            lines.append("|" + "|".join(["---" for _ in header_cols]) + "|")
            for r in norm_rows:
                # pad/truncate to header length
                r = (r + [""] * len(header_cols))[: len(header_cols)]
                lines.append("| " + " | ".join(r) + " |")
            lines.append("")

        return lines

    def generate_markdown(
        self,
        data_type: str,
        templates: dict[str, dict],
        dry_run: bool = False,
    ) -> Path:
        """
        Generate the Hugo markdown file for a data type.
        
        Combines content.md with dynamically generated template documentation.
        """
        output_dir = self.documents_dir / data_type
        output_dir.mkdir(parents=True, exist_ok=True)
        
        md_path = output_dir / "_index.md"

        if dry_run:
            self.log(f"Would generate markdown: {md_path}", "info")
            return md_path

        lines = []

        # Get description from first template's metadata
        first_template = next(iter(templates.values()), {})
        description = first_template.get("metadata", {}).get(
            "description", f"{data_type.upper()} data templates"
        )

        # Hugo front matter
        lines.append("---")
        lines.append(f'description: "{description}"')
        lines.append(f'# Auto-generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        lines.append("# Do not edit manually - regenerate with: python scripts/generate_templates.py")
        lines.append("---")
        lines.append("")

        # Load and insert custom content.md
        custom_content = self.load_content_file(data_type)
        if custom_content:
            lines.append(custom_content.strip())
            lines.append("")
            lines.append("---")
            lines.append("")

        '''
        # Templates overview section
        lines.append("## Data Templates")
        lines.append("")
        lines.append(
            "This section provides downloadable CSV templates for each data level. "
            "Note that decimal values should use a decimal point (`.`) to indicate "
            "the decimal value, and commas (`,`) should be omitted."
        )
        lines.append("")

        # Table of contents for data levels
        lines.append("### Data Levels")
        lines.append("")
        for level_name, template_data in templates.items():
            section_title = template_data.get("section", {}).get(
                "title", level_name.replace("_", " ").title()
            )
            # Create anchor link
            anchor = section_title.lower().replace(" ", "-")
            lines.append(f"- [{section_title}](#{anchor})")
        lines.append("")
    '''
        # Generate section for each data level in the preferred EM order.
        # Unknown/future levels are placed after the configured levels, alphabetically.
        order_index = {name: idx for idx, name in enumerate(EM_LEVEL_ORDER)}
        sorted_levels = sorted(
            templates.keys(),
            key=lambda x: (order_index.get(x, len(EM_LEVEL_ORDER)), x),
        )

        for level_name in sorted_levels:
            template_data = templates[level_name]
            level_lines = self._generate_level_section(
                level_name, template_data, data_type
            )
            lines.extend(level_lines)

        # NEW: Append reference tables (if any)
        ref_lines = self._generate_reference_tables_section(templates)
        if ref_lines:
            lines.extend(ref_lines)

        # Write markdown file
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        self.log(f"Generated markdown: {md_path}", "success")
        return md_path

    def process_data_type(self, data_type: str, dry_run: bool = False) -> bool:
        """
        Process a single data type: load templates, generate CSV and markdown.
        
        Returns True if successful, False otherwise.
        """
        print(f"\nProcessing {data_type.upper()}...")

        # Check if this data type should use dynamic generation
        if data_type not in DYNAMIC_DATA_TYPES:
            self.log(
                f"Skipping {data_type} - not in DYNAMIC_DATA_TYPES list. "
                "Add it to enable dynamic generation.",
                "warning",
            )
            return False

        # Load all templates for this data type
        templates = self.load_data_type_templates(data_type)
        
        if not templates:
            self.log(f"No template YAML files found for {data_type}", "warning")
            return False

        print(f"  Found {len(templates)} data level(s): {', '.join(templates.keys())}")

        # Generate CSV files in the same preferred level order used by the documentation.
        order_index = {name: idx for idx, name in enumerate(EM_LEVEL_ORDER)}
        sorted_level_names = sorted(
            templates.keys(),
            key=lambda x: (order_index.get(x, len(EM_LEVEL_ORDER)), x),
        )
        for level_name in sorted_level_names:
            self.generate_csv_template(data_type, level_name, templates[level_name], dry_run)

        # Generate combined markdown
        self.generate_markdown(data_type, templates, dry_run)

        return True

    def process_all(self, dry_run: bool = False) -> dict[str, bool]:
        """
        Process all dynamic data types.
        
        Returns a dict mapping data type to success status.
        """
        results = {}
        
        for data_type in DYNAMIC_DATA_TYPES:
            results[data_type] = self.process_data_type(data_type, dry_run)

        return results


def main():
    """Main entry point for the template generator."""
    parser = argparse.ArgumentParser(
        description="Generate CSV templates and Hugo markdown from YAML definitions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_templates.py                    # Generate all dynamic templates
  python generate_templates.py --data-type em    # Generate only EM templates  
  python generate_templates.py --dry-run         # Preview without writing files
  python generate_templates.py --list            # List available data types
        """,
    )
    
    parser.add_argument(
        "--data-type", "-t",
        type=str,
        help="Process only this specific data type (e.g., 'em', 'operational-longline')",
    )
    
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Preview what would be generated without writing files",
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output",
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List data types enabled for dynamic generation",
    )
    
    parser.add_argument(
        "--workspace", "-w",
        type=str,
        help="Path to workspace root (auto-detected if not specified)",
    )

    args = parser.parse_args()

    # Show list of dynamic data types
    if args.list:
        print("Data types enabled for dynamic generation:")
        for dt in DYNAMIC_DATA_TYPES:
            print(f"  - {dt}")
        print("\nTo add more, edit DYNAMIC_DATA_TYPES in generate_templates.py")
        return 0

    # Initialize generator
    workspace_root = Path(args.workspace) if args.workspace else None
    generator = TemplateGenerator(workspace_root=workspace_root, verbose=args.verbose)

    print("=" * 60)
    print("SciData Template Generator")
    print("=" * 60)
    print(f"Workspace: {generator.workspace_root}")
    print(f"Templates: {generator.templates_dir}")
    print(f"Documents: {generator.documents_dir}")
    
    if args.dry_run:
        print("\n*** DRY RUN - No files will be written ***")

    # Process templates
    if args.data_type:
        success = generator.process_data_type(args.data_type, args.dry_run)
        results = {args.data_type: success}
    else:
        results = generator.process_all(args.dry_run)

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for data_type, success in results.items():
        status = "✓" if success else "✗"
        print(f"  {status} {data_type}")

    print(f"\n{success_count}/{total_count} data type(s) processed successfully")

    if args.dry_run:
        print("\n*** DRY RUN complete - no files were written ***")
    else:
        print("\n✅ Generation complete!")
        print("\nNext steps:")
        print("  1. Review generated files in documents/<data_type>/")
        print("  2. Run 'hugo server' in site-generator/ to preview")
        print("  3. Commit changes to git")

    return 0 if success_count == total_count else 1


if __name__ == "__main__":
    sys.exit(main())