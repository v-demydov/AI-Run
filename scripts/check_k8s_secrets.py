#!/usr/bin/env python3
"""
CI preventive control for T-07 (STRIDE: Information Disclosure).

Rejects k8s manifests that inject credentials as plaintext env.value fields.
Every flagged name or pattern must be moved to a secretKeyRef before merge.
"""
import sys
import re
import glob
import yaml

FORBIDDEN_NAMES = {"DIAL_API_KEY", "DATABASE_URL", "DB_PASSWORD", "API_KEY", "SECRET_KEY"}

FORBIDDEN_VALUE_PATTERNS = [
    re.compile(r"sk-live-"),
    re.compile(r"postgres://[^:]+:[^@]+@"),
]


def scan_containers(containers, path, issues):
    for container in containers:
        for env_var in container.get("env", []):
            name = env_var.get("name", "")
            if "valueFrom" in env_var:
                continue
            value = str(env_var.get("value", ""))
            if name in FORBIDDEN_NAMES:
                issues.append(
                    f"{path}: env '{name}' uses plaintext value: — use secretKeyRef"
                )
            for pat in FORBIDDEN_VALUE_PATTERNS:
                if pat.search(value):
                    issues.append(
                        f"{path}: env '{name}' value matches forbidden pattern "
                        f"({pat.pattern})"
                    )


def check_file(path):
    issues = []
    with open(path) as fh:
        try:
            docs = list(yaml.safe_load_all(fh))
        except yaml.YAMLError as exc:
            return [f"{path}: YAML parse error: {exc}"]
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        containers = (
            doc.get("spec", {})
            .get("template", {})
            .get("spec", {})
            .get("containers", [])
        )
        scan_containers(containers, path, issues)
    return issues


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "k8s"
    files = sorted(
        glob.glob(f"{target}/**/*.yaml", recursive=True)
        + glob.glob(f"{target}/**/*.yml", recursive=True)
        + ([target] if target.endswith((".yaml", ".yml")) else [])
    )
    files = list(dict.fromkeys(files))

    all_issues = []
    for f in files:
        all_issues.extend(check_file(f))

    if all_issues:
        print("FAIL: plaintext credentials detected in k8s manifests")
        for issue in all_issues:
            print(f"  {issue}")
        print(
            "\nFix: use secretKeyRef "
            "(see Artefacts/800-wide/02-deploy-manifest.md)"
        )
        sys.exit(1)

    print(f"PASS: no plaintext credentials found in {len(files)} file(s)")


if __name__ == "__main__":
    main()
