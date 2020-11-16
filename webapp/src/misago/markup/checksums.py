"""
Misago saves parsed strings in database.

Those strings are "trusted" and contain HTML that is rendered by templates
without additional sanitization step.

While this greatly improves speed, it also means that SQLInjections may
escalate to Code Injection vulnerabilities.

Because of this you should use this module to generate checksum for each model
that contains parsed strings. Each checksum should be generated from markup as
well as additional unique values that are specific for that model, like its PK,
post date, etc ect.

That way even if few items will contain the same content, they will have
different checksums, and as long as attacker has no access to filesystem,
he'll wont know SECRET_KEY and thus won't be able to generate valid checksums
for injected content

Because SHA256 is used for checksum generation, make sure you are storing them
in char fields with max_length=64
"""
from hashlib import sha256


def make_checksum(parsed, unique_values=None):
    unique_values = unique_values or []
    seeds = [parsed] + [str(v) for v in unique_values]

    return sha256("+".join(seeds).encode("utf-8")).hexdigest()


def is_checksum_valid(parsed, checksum, unique_values=None):
    return checksum == make_checksum(parsed, unique_values)
