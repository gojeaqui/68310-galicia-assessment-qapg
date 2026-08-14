# What are the healthcheck scripts?

The healthcheck scripts are designed for engagements where a list of
"check items" are evaluated and given a recommendation and a
remediation.

These scripts should be generic enough to use with any technology.
The first usage of these is for an OpenShift 4 Architecture
Review/Healthcheck.

# What is required to run these scripts?

- Python 3

And the following Python packages:
`pyyaml`, 
`click`, 
`typing_extensions`

These can be installed on RHEL/Fedora using the yum package manager:
```
# yum install python3-pyyaml python3-click python3-typing-extensions python3-cerberus
```
or the Python pip package manager:
```
$ python -m venv . && . bin/activate
$ pip install pyyaml click typing_extensions cerberus
```

# How do I use these scripts?

Usage is:

```
$ ./scripts/generate-healthcheck.py
Usage: generate-healthcheck.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  asciidoc          Generate Healthcheck AsciiDoc
  check-procedures  Create a list of all check procedures in a directory...
  exportcsv         Generate healthcheck csv
  validate-dir      Validate yaml of all item files in a directory
  validate-item     Validate a single item file
  zap               Reset customer environment findings to default values
```

To generate a list of all check procedures based on item files a directory:

```
$ ./scripts/generate-healthcheck.py check-procedures
Check Procedures written to ./content/check-procedures.txt
```

To generate a the health check ascii doc, use the asciidoc subcommand:

```
$ ./scripts/generate-healthcheck.py asciidoc --help
Usage: generate-healthcheck.py asciidoc [OPTIONS]

  Generate Healthcheck  AsciiDoc

Options:
  --input-dir DIRECTORY  [default: ./content/healthcheck-items/]
  --output-file FILE     [default: ./content/healthcheck-body.adoc]
  --help                 Show this message and exit.
```

If run from <CER_ROOT>, then no parameters are needed, although input
and ouput locations can be overridden if desired.

Sample run:

```
$ cd <CER_ROOT>
$ ./scripts/generate-healthcheck.py asciidoc
Generating AsciiDoc ./content/healthcheck-body.adoc
Loading './content/healthcheck-items/1010_compute-provider.item'
Loading './content/healthcheck-items/1020_installation-type.item'
Loading './content/healthcheck-items/1030_if-upi-is-customer-using-additional-machinesets.item'
Loading './content/healthcheck-items/1040_vmware-version.item'
< OUTPUT TRUNCATED >
Loading './content/healthcheck-items/6510_token_auth_file.item'
Loading './content/healthcheck-items/6520_kubelt_cert.item'
Loading './content/healthcheck-items/6530_kubelet_key.item'
Completed
$ git commit -m "Updated healtcheck" ./content/healthcheck-body.adoc 
$ ./generate_pdf
Generating pdf using podman... 
Generated: cer-test-2022-01-17-10-13-14.pdf
```

The two optional parameters can be used to override the default input
and ouput locations, if needed.

`--input-dir` specifies a directory which contains an assortment of
item and config files.  By default, this is in
`<CER_ROOT>/content/healthcheck-items/`.

`--output-file` specifies a file for the generated Asciidoc output.
The script will overwrite any existing contents of that file!  By
default, this file is `<CER_ROOT>/content/healthcheck-body.adoc`.

# Are these scripts integrated into the CER CI/CD?

At the moment, no.  The scripts should be run, and then, the output CHECKED INTO GIT.

Since the output of this script is just ASCIIDOC, the CI/CD will pick it up automatically

# What is contained in the input directory?

The input directory contains the following files:

1.  `config.yaml` - (Optional) a file which overrides the default
    configuration for result names, coloring, et cetera.

2.  `categories.yaml` - (Required) a file contains the defined
    categories for the items

3.  `*.item` - (Required) item files contain line items for the health
    check.  There may be many items.

# How to use the *.item files?

During a health check, fill out the "results" section in each item
file and check them into git!

If a particular item file is not needed for your healthcheck, delete
or rename them from your repository using `git rm` or `git mv`
commands.

At time of writing, there are two formats for the item files: an older
v0 and a newer v1.  We are slowly converting all item files to v1, but
the script will handle both versions.

For more information, see [README-ITEM-V0.md](./README-ITEM-V0.md) or [README-ITEM-V1.md](./README-ITEM-V1.md)

