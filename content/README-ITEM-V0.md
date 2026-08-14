This file describes the older V0 style item files.  It's recommended
to not use this format for new item files.

Item files are individual YAML files with a specific format.

An example:

```
---
version: v0 
metadata:
  category_key: "ocp_config"
  item_evaluated: "Master Nodes are Set"
  product_version: "3+"
  references:  
    - title: "OpenShift Docs"
      url: "https://docs.openshift.com"
    - title: "Red Hat Docs"
      url: "https://docs.redhat.com"
  acceptance_criteria:
    no_change:
      - "Master node number >= 3 and colocated etcd"
      - "Master node number >= 2 and external etcd"
    required:
      - "Master node number < 3 and colocated etcd"
    recommended:
      - "Master node number < 2 and external etcd"
results:
  result_text: "1 master node and colocated etcd"
  recommendation: required
  impact_risk_text: "No High Availability"
  remediation_text: "Redeploy cluster with more nodes"
  additional_comments_text: |-
    BLAH BLAH BLAH
```

This file has major sections:  `metadata` and `results`.

`metadata` contains keys that define the item to be evaluated.  These
will stay consistent between different engagements, and should not be
modified per client.

* `category_key` - The category the item is under.  This key must exist in `categories.yaml`
* `item_evaluated` - A brief description of the item being evaluated.  
* `product_version` - A text description of what version of the product this item applies do.
* `references` - An array of  reference URL/titles for this item.  Generally, a URL to an
  official documentation source describing why this item is important
  and what the proper values should be.
* `acceptance_criteria` - a dictionary of recommendation status keys
  and what a customer environment should look like to meet that
  status.

`results` contains keys with information discovered in the client's
environment.  These will be specific to a specific customer and should
be changed.

* `result_text` - A brief description of what is found by the consultant in the Customer's environment
* `recommendation` - a recommendation status key informing the customer what they should do in response to the `result`.  See "What are the default recommendation status keys?" for more information.
* `impact_risk_text` - What is the impact of this risk, specific to the customer.
* `remediation_text` - What should be done by the customer to remediate this
* `additional_comments_text` - Any additional comments that the consultant wishes to include.

`result_text` is used in tables in the generated Asciidoc.  Thus, should be kept as short as possible.

`impact_risk_text`, `remediation_text`, and `additional_comments_text`
are presented in a detail section below the tables.  Consultants
should be as descriptive as necessary here and can include Asciidoc
syntax.  For long values, consultants should consider using
[https://yaml-multiline.info/](YAML Multiline) syntax.

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
