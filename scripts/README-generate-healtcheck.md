# Generate Healthcheck Script Documentation

This documentation explains the usage of the `generate-healthcheck.py` script. It provides command usage details, prerequisites, and examples for running each command.

---

## Table of Contents

- [Generate Healthcheck Script Documentation](#generate-healthcheck-script-documentation)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
  - [Click Command Categories](#click-command-categories)
    - [COMMANDS ARE LISTED WITH THIER DEFAULT --input-dir and --output-dir.  These can be changed, or omitted if default is to be used.](#commands-are-listed-with-thier-default---input-dir-and---output-dir--these-can-be-changed-or-omitted-if-default-is-to-be-used)
    - [Filtering Commands](#filtering-commands)
      - [**`filter`**](#filter)
      - [**`unfilter`**](#unfilter)
    - [Validation Commands](#validation-commands)
      - [**`validate_dir`**](#validate_dir)
      - [**`validate_item`**](#validate_item)
    - [Output Generation Commands](#output-generation-commands)
      - [**`asciidoc`**](#asciidoc)
      - [**`exportcsv`**](#exportcsv)
      - [**`check_procedures`**](#check_procedures)
    - [Miscellaneous Commands](#miscellaneous-commands)
      - [**`zap`**](#zap)
  - [Customizing Configuration](#customizing-configuration)
    - [Key Customization Options](#key-customization-options)
  - [Example Item File and Configuration](#example-item-file-and-configuration)
    - [Example Item File (`appdev-4090-monitoring-logging-application-logs.item`):](#example-item-file-appdev-4090-monitoring-logging-application-logsitem)

---

## Setup

Before using the script, ensure the following:

1. **Python Version**: Python 3.8 or higher is required.
2. **Install Dependencies**:
   - Navigate to the `scripts/` directory.
   - Run the following command to install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

---

## Click Command Categories

### COMMANDS ARE LISTED WITH THIER DEFAULT --input-dir and --output-dir.  These can be changed, or omitted if default is to be used. 

### Filtering Commands

#### **`filter`**

**Description**: Filters items based on tags defined in the `config.yaml` file.

**Usage**:

```bash
python3 generate-healthcheck.py filter \
    --input-dir ./content/healthcheck-items/ \
    --output-dir ./content/healthcheck-items/disabled/
```

#### **`unfilter`**

**Description**: Moves filtered items back to the main directory.

**Usage**:

```bash
python3 generate-healthcheck.py unfilter \
    --input-dir ./content/healthcheck-items/disabled/ \
    --output-dir ./content/healthcheck-items/
```

### Validation Commands

#### **`validate_dir`**

**Description**: Validates the YAML structure of all `.item` or `.item.yaml` files in a specified directory.

**Usage**:

```bash
python3 generate-healthcheck.py validate_dir <dirname>
```

#### **`validate_item`**

**Description**: Validates a single YAML item file.

**Usage**:

```bash
python3 generate-healthcheck.py validate_item <filename>
```

### Output Generation Commands

#### **`asciidoc`**

**Description**: Generates an AsciiDoc file containing health check data.

**Usage**:

```bash
python3 generate-healthcheck.py asciidoc \
    --input-dir ./content/healthcheck-items/ \
    --output-file ./content/healthcheck-body.adoc
```

#### **`exportcsv`**

**Description**: Exports health check data to a CSV file.

**Usage**:

```bash
python3 generate-healthcheck.py exportcsv \
    --input-dir ./content/healthcheck-items/ \
    --output-file ./content/healthcheck.csv
```

#### **`check_procedures`**

**Description**: Creates a list of all check procedures from health check items.

**Usage**:

```bash
python3 generate-healthcheck.py check_procedures \
    --input-dir ./content/healthcheck-items/ \
    --output-file ./content/check-procedures.txt
```

### Miscellaneous Commands

#### **`zap`**

**Description**: Resets customer environment findings in an item file to default values.

**Usage**:

```bash
python3 generate-healthcheck.py zap <filename>
```

---

## Customizing Configuration

The script relies on `config.yaml` for customization. This file defines categories, statuses, and tags for filtering and processing health check items. Below is an example configuration structure:

```yaml
categories:
  Infrastructure:
    text: "Infrastructure"
    short_text: "Infra"
  Platform:
    text: "Platform"
    short_text: "Platform"
  appdev:
    text: "Application Development"
    short_text: 'App Dev'
  security:
    text: "Security"
    short_text: "Security"
  Operation_ready:
    text: "Organizational Readiness"
    short_text: "Organizational Readiness"
skip_statuses:
- 'not_applicable'
- 'tbe'
- 'no_change'
statuses:
  changes_required:
    color: "#FF0000"
    text: "Changes Required"
    description: "Indicates critical changes are required."
  no_change:
    color: "#00FF00"
    text: "No Change"
    description: "No changes are needed."
  advisory:
    color: "#80E5FF"
    text: "Advisory"
    description: "Additional information provided without required changes."
tags:
  self_managed: True
  managed: False
  aws: False
  azure: False
  bare_metal: False
```

### Key Customization Options

- **Categories**: Define categories for health check items with `text` and `short_text`.
- **Statuses**: Configure statuses with `color`, `text`, and `description`.
- **Tags**: Enable or disable tags for filtering items.

---

## Example Item File and Configuration

Below is an example of an item file and its corresponding structure:

### Example Item File (`appdev-4090-monitoring-logging-application-logs.item`):

```yaml
version: "v2"
check_definition:
  category_key: "appdev"
  subcategory_key: "logging"
  severity_key: "medium"
  tags:
    - "self_managed"
    - "aws"
  description: "Monitor and log application logs."
  common_outcomes:
    - key: "log_collection_enabled"
      scenario_description_short_text: "Application logs are being collected."
      description_long_text: "Ensure application logs are consistently collected for monitoring and debugging purposes."
      impact_and_risk_text: "Logs are essential for identifying issues and auditing application behavior."
      remediation_text: "Configure logging in the application and ensure logs are forwarded to a centralized system."
  references:
    - url: "https://example.com/logging-best-practices"
      title: "Logging Best Practices"
customer_environment_findings:
  status: "changes_required"
  common_outcome_key: "log_collection_enabled"
  outcome_overrides:
    scenario_description_short_text: "Logging is partially configured."
    impact_and_risk_text: "Without comprehensive logging, issues may go undetected."
    remediation_text: "Complete the logging configuration to include all critical application components."
  additional_comments:
    additional_comments_text: "Ensure compliance with organizational logging standards."
    impact_risk_additional_text: "High impact on debugging and monitoring."
    remediation_additional_text: "Coordinate with the DevOps team for configuration completion."
```