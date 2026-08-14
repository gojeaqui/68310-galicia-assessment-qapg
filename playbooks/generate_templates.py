import os
import yaml
import shutil

SOURCE_DIR = "../content/healthcheck-items"
DEST_DIR = "healthcheck-item-templates"
APPEND_BLOCK = """  outcome_evidence: |
    {% filter indent(width=4) %}{{ merged_output }}{% endfilter %}
"""

os.makedirs(DEST_DIR, exist_ok=True)

bad_files = []
created_files = []
fallback_files = []

for filename in os.listdir(SOURCE_DIR):
    if not filename.endswith(".item"):
        continue

    filepath = os.path.join(SOURCE_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Try to parse YAML
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError:
        bad_files.append(filename)
        data = None

    has_command = False

    if data:
        # Safely check check_procedures in structured YAML
        check_def = data.get("check_definition", {})
        procedures = check_def.get("check_procedures", [])
        for p in procedures:
            if isinstance(p, dict):
                p_type = str(p.get("type", "")).strip().lower()
                if p_type == "command":
                    has_command = True
                    break
    else:
        # Fallback: raw text match for type: command
        if "type: command" in content or 'type: "command"' in content:
            has_command = True
            fallback_files.append(filename)

    # If command-type check found, create the .j2 template
    if has_command:
        dest_path = os.path.join(DEST_DIR, os.path.splitext(filename)[0] + ".j2")

        shutil.copy(filepath, dest_path)
        with open(dest_path, "a", encoding="utf-8") as f:
            f.write("\n" + APPEND_BLOCK)

        created_files.append(filename)
        print(f"✅ Created template: {dest_path}")
    else:
        print(f"➡️  No command-type check found in: {filename}")

# Summary
print("\n===== SUMMARY =====")
print(f"✅ Templates created: {len(created_files)}")
if fallback_files:
    print(f"⚠️  Used fallback detection for: {len(fallback_files)} files")
    for f in fallback_files:
        print(f"   - {f}")
if bad_files:
    print(f"❌ Could not parse YAML in: {len(bad_files)} files")
    for f in bad_files:
        print(f"   - {f}")
print("===================")
