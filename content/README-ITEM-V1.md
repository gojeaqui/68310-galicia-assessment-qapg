# Introduction

v1 item files are the current standard for item files, and offer
improvements over the old version.  It's recommended to use this
format for new item files.

Item files are individual YAML files with a specific format.

# v1 Sample

An example:

```
---
version: v1
metadata:
  category_key: "infra"
  item_evaluated: "Infrastructure Provider(s)"
  references:  # List of Reference
    - title: "Display text for link"
      url: "URL of reference"
  check_procedures:
    - type: survey
      question: "What infrastructure providers (e.g. AWS, Bare Metal, VMware) are your clusters installed on?"
  acceptance_criteria:
    no_change:
      - id: 'nochange_01'
        condition_description: 'Infrastructure provider is a Red Hat tested infrastructure provider. Bare-metal, vSphere, RHOSP, AWS, GCP, Azure, IBM Z or LinuxONE, IBM Power Systems, RHV.'
    changes_recommended:
      - id: 'recommend01'
        condition_description: "Infrastructure provider is a non tested infrastructure provider. Moving to a Red Hat tested infrastructure provider is recommended."
        impact_risk_text: "Non supported infrastructure providers limit Red Hat Support's ability to assist in cases.  Unsupported infrastructure may behave in unusual ways or lack capabilities for essential OpenShift features."
        remediation_text: "Re-install clusters on supported infrastructure type."
results:
  result_short_text: "short text"  # Short description of results
  result_long_text:  "this is a longer text" # Optional longer result description
  recommendation: changes_recommended
  acceptance_criteria_id:  'recommend01'
  impact_risk_additional_text: "Additional impact risk from consultant"
  remediation_additional_text: "Additional remediation text from consultant"
  additional_comments_text: "Additional comments from consultant"
```

This file has major sections:  `metadata` and `results`.

# metadata section

`metadata` contains keys that define the item to be evaluated.  These
will stay consistent between different engagements, and should not be
modified per client.

* `category_key` - The category the item is under.  This key must exist in `categories.yaml`
* `item_evaluated` - A brief description of the item being evaluated.  
* `references` - An array of  reference URL/titles for this item.  Generally, a URL to an
  official documentation source describing why this item is important
  and what the proper values should be.
* `check_procedures` - an array of objects defining how to check the item
* `acceptance_criteria` - a dictionary of statuses, whis pre-filled acceptance criteria and associated text.

## reference

The `reference` key is an array.  Every element represents a URL and
should have two keys:

* 'title' - display text for the URL
* 'url' - the URL for the reference

## check_procedures

The `check_procedures` key is an array.  Every element represents a
check that the consultant could or should do to validate the item's
result.

There are three types of procedures:

* Survey - for a question that needs to be asked to the customer

```
    - type: survey
      question: "Example question?"
```

* command - for a command that needs to be run against OpenShift cluster(s)
```
    - type: command
      command: |
        oc get nodes
```

* gui_action - for an action that needs to be taken in the OpenShift
  console or console of related product.
```
    - type: gui_action
      description: |
        explaination of GUI action
```

## acceptance_criteria

`acceptance_criteria` is the most complicated section.  It's meant to
provide pre-populated guidance and verbiage for a variety of
situations that the consultant may encounter for the issue.

`acceptance_criteria` is a dictionary of statuses, with the value of
each dictionary key being an array.

```
  acceptance_criteria:
    no_change:
      - <ITEM 1>
      - <ITEM 2>
    changes_recommended:
      - <ITEM 1>
      - <ITEM 2>
    changes_required:
      - <ITEM 1>
      - <ITEM 2>
```

The keys for the dictionary are sourced from `config.yaml` and map to
the statuses.  It is not required to have a key for every possible
status!

In the array for each status, there can be one or more complex objects
following this format:

```
      - id: "unique_condition_id"
        condition_description: "The excample condition the consultant may observe."
        impact_risk_text: "What is the impact and risk of this condition"
        remediation_text: "How should the customer remediate this condition"
```

The `id` key should have a unique value in the array.  This will later
be used in the results section.


# results section

`results` contains keys with information discovered in the client's
environment.  These will be specific to a specific customer and should
be changed.

* `result_short_text` - A very brief description of what is found by the consultant in the Customer's environment.  This should be kept as short as possible, since it will be included in all tables in the document.
* ` result_long_text` - if more extensive description of the result is required, place it in this comment.  This will be placed in the detail section.
* `recommendation` - a recommendation status key informing the customer what they should do in response to the `result`.  See "What are the default recommendation status keys?" for more information.
* `acceptance_criteria_id` - matches the id field in an acceptance_criteria object.  This will cause verbiage from the acceptance criteria object to be written to the detail section.  If left blank, then this is ignored.
* `impact_risk_additional_text` - Additional comments from the consultant on impact/risk.  Set to "" if unneeded.
* `remediation_additional_text` - Additional comments from the consultant on remediation.  Set to "" if unneeded.
* `additional_comments_text` - Any additional comments that the consultant wishes to include.  Set to "" if unneeded.

`impact_risk__additional_text`, `remediation_additional_text`, and
`additional_comments_text` are presented in a detail section below the
tables.  Consultants should be as descriptive as necessary here and
can include Asciidoc syntax.  For long values, consultants should
consider using [https://yaml-multiline.info/](YAML Multiline) syntax.

# What if there are no acceptance criteria matching the situation in my customer?

There are two options:

1.  You can add a `acceptance_criteria` object that matches what
you're seeing at the customer.  Please make this as generic as
possible, and contribute it back to the main CER template.

2.  Leave `acceptance_criteria` blank, and use the
`impact_risk_additional_text` and `remediation_additional_text` fields
in results to provide customer specific answers.

# What are the default recommendation status keys?

|Key                 |  Description
|----                |---- 
|changes_required    |Indicates Changes Required for system stability, subscription compliance, or other reason.
|changes_recommended |Indicates Changes Recommended to align with recommended practices
|advisory            |No change required or recommended, but additional information provided.
|not_applicable      |Not applicable to customer's environment
|no_change           |No Change Required.  Environment is in-line with required and recommended practices
|tbe                 |To Be Evaluated.  Used when delivering draft versions, before the engagement is complete

Each key has built in text and coloring that the script takes care of
automatically.

# What are the rules for an item being printed in the detail section?

If an item has a status of `not_applicable`, `tbe` or `no_change` it will not get
printed in the detail section, since there is generally nothing to
say.

If an item with one of these result statuses has the
`additional_comments_text` completed (i.e. is not an empty string),
then a detail section WILL be created, but will exclude the
`impact_risk_text` and `remediation_text` section, REGARDLESS of
whether or not those keys have values in the item's yaml file.
