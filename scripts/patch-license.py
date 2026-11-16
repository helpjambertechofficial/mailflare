#!/usr/bin/env python3
"""
License bypass patch for self-hosted Mailflare instance.
AGPL v3 compliant — source available at github.com/helpjambertechofficial/mailflare
"""
import pathlib
import re
import sys

LICENSE_FILE = pathlib.Path("src/lib/licenses/service.ts")

if not LICENSE_FILE.exists():
    print(f"ERROR: {LICENSE_FILE} not found")
    sys.exit(1)

content = LICENSE_FILE.read_text(encoding="utf-8")

ENTITLEMENTS_BYPASS = '''export async function getLicenseEntitlements(_env: CloudflareEnv): Promise<LicenseEntitlements> {
\t// Self-hosted: all features unlocked (AGPL v3 - source: github.com/helpjambertechofficial/mailflare)
\treturn {
\t\tplan: "team",
\t\tcanCustomizeBranding: true,
\t\tcanManageAccounts: true,
\t\tcanShareMailboxes: true,
\t\taccountSeatLimit: null,
\t\tcanForwardEmail: true,
\t};
}'''

STATUS_BYPASS = '''export async function getLicenseStatus(env: CloudflareEnv): Promise<LicenseStatus> {
\t// Self-hosted: all features unlocked (AGPL v3 - source: github.com/helpjambertechofficial/mailflare)
\tconst base = await getOrCreateLicenseSettings(env);
\treturn {
\t\tplan: "team",
\t\tstate: "active",
\t\tfeatures: ["branding", "accounts", "shared_mailboxes", "email_forwarding"],
\t\tseatLimit: null,
\t\tinstanceId: base.instanceId,
\t\tinstanceUrl: base.instanceUrl,
\t\tactive: true,
\t\tactivatedAt: base.activatedAt ?? new Date(),
\t\tvalidatedAt: base.validatedAt ?? new Date(),
\t};
}'''

patched = re.sub(
    r'export async function getLicenseEntitlements\(env.*?(?=\nexport |\Z)',
    ENTITLEMENTS_BYPASS + '\n\n',
    content, flags=re.DOTALL
)
patched = re.sub(
    r'export async function getLicenseStatus\(env.*?(?=\nexport |\Z)',
    STATUS_BYPASS + '\n\n',
    patched, flags=re.DOTALL
)

if patched != content:
    LICENSE_FILE.write_text(patched, encoding="utf-8")
    print("License patch applied successfully.")
else:
    print("Already patched or pattern not found — no changes made.")
