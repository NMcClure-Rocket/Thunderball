"""
Inventory service – business logic for inventory operations.

The hardcoded data here is a placeholder until the Db2 adapter is ready.
"""

# ── Placeholder BasePrice table data ─────────────────────────────────
_baseprice = [
    {"id": 1,  "name": "Firewall Spell",      "price": 14.99, "image": "/assets/base/firewall-spell.png"},
    {"id": 2,  "name": "Encryption Hex",       "price": 19.99, "image": "/assets/base/encryption-hex.png"},
    {"id": 3,  "name": "Bug Banish",           "price": 9.99,  "image": "/assets/base/bug-banish.png"},
    {"id": 4,  "name": "Deploy Surge",         "price": 24.99, "image": "/assets/base/deploy-surge.png"},
    {"id": 5,  "name": "Cache Conjure",        "price": 11.50, "image": "/assets/base/cache-conjure.png"},
    {"id": 6,  "name": "Recursive Loop",       "price": 16.75, "image": "/assets/base/recursive-loop.png"},
    {"id": 7,  "name": "Patch Ward",           "price": 12.00, "image": "/assets/base/patch-ward.png"},
    {"id": 8,  "name": "Quantum Compile",      "price": 29.99, "image": "/assets/base/quantum-compile.png"},
    {"id": 9,  "name": "Cloud Summon",         "price": 22.50, "image": "/assets/base/cloud-summon.png"},
    {"id": 10, "name": "Binary Barrier",       "price": 13.25, "image": "/assets/base/binary-barrier.png"},
    {"id": 11, "name": "Null Pointer Curse",   "price": 8.50,  "image": "/assets/base/null-pointer-curse.png"},
    {"id": 12, "name": "Merge Conflict Doom",  "price": 17.00, "image": "/assets/base/merge-conflict-doom.png"},
]

# ── Placeholder Inventory table data ─────────────────────────────────
_inventory = [
    # ── Firewall Spell (base_info=1) ──
    {"itemID": 1,  "name": "Firewall Spell",      "description": "Conjures an impenetrable network barrier that blocks unauthorized traffic and repels digital intruders.",                        "format": "Tome",   "potency": 8,  "reusable": "1", "category": "Protection",   "price": 189.99, "amount": 10, "base_info": 1},
    {"itemID": 2,  "name": "Firewall Spell",      "description": "A lightweight portable shield that filters packets and wards off brute-force attacks.",                                        "format": "PDF",    "potency": 5,  "reusable": "1", "category": "Protection",   "price": 124.50, "amount": 6,  "base_info": 1},
    {"itemID": 3,  "name": "Firewall Spell",      "description": "Single-use emergency firewall that instantly seals all open ports.",                                                            "format": "Scroll", "potency": 9,  "reusable": "0", "category": "Protection",   "price": 275.00, "amount": 3,  "base_info": 1},
    # ── Encryption Hex (base_info=2) ──
    {"itemID": 4,  "name": "Encryption Hex",       "description": "Wraps data in layers of AES-256 arcane ciphers, rendering it unreadable to adversaries.",                                      "format": "Tome",   "potency": 9,  "reusable": "1", "category": "Protection",   "price": 249.99, "amount": 5,  "base_info": 2},
    {"itemID": 5,  "name": "Encryption Hex",       "description": "Quick-cast encryption that scrambles payloads in transit with rotating keys.",                                                 "format": "PDF",    "potency": 6,  "reusable": "1", "category": "Protection",   "price": 159.75, "amount": 8,  "base_info": 2},
    {"itemID": 6,  "name": "Encryption Hex",       "description": "One-time pad hex that guarantees perfect secrecy for a single transmission.",                                                  "format": "Scroll", "potency": 10, "reusable": "0", "category": "Protection",   "price": 350.00, "amount": 2,  "base_info": 2},
    # ── Bug Banish (base_info=3) ──
    {"itemID": 7,  "name": "Bug Banish",           "description": "Summons a swarm of linting sprites that hunt down and eliminate code defects.",                                                 "format": "Tome",   "potency": 4,  "reusable": "1", "category": "Debugging",    "price": 99.99,  "amount": 15, "base_info": 3},
    {"itemID": 8,  "name": "Bug Banish",           "description": "Portable debugging guide that highlights stack traces and suggests fixes.",                                                    "format": "PDF",    "potency": 3,  "reusable": "0", "category": "Debugging",    "price": 69.50,  "amount": 12, "base_info": 3},
    # ── Deploy Surge (base_info=4) ──
    {"itemID": 9,  "name": "Deploy Surge",         "description": "Triggers a CI/CD pipeline blast that pushes code to production at lightning speed.",                                            "format": "Tome",   "potency": 7,  "reusable": "1", "category": "Deployment",   "price": 299.99, "amount": 4,  "base_info": 4},
    {"itemID": 10, "name": "Deploy Surge",         "description": "Compact deployment manual for zero-downtime rolling updates.",                                                                 "format": "PDF",    "potency": 5,  "reusable": "1", "category": "Deployment",   "price": 199.00, "amount": 7,  "base_info": 4},
    {"itemID": 11, "name": "Deploy Surge",         "description": "Emergency hotfix scroll that force-deploys a critical patch instantly.",                                                        "format": "Scroll", "potency": 8,  "reusable": "0", "category": "Deployment",   "price": 375.00, "amount": 2,  "base_info": 4},
    # ── Cache Conjure (base_info=5) ──
    {"itemID": 12, "name": "Cache Conjure",        "description": "Materializes a Redis-infused memory cache that accelerates data retrieval tenfold.",                                            "format": "Tome",   "potency": 6,  "reusable": "1", "category": "Optimization", "price": 149.99, "amount": 9,  "base_info": 5},
    {"itemID": 13, "name": "Cache Conjure",        "description": "Pocket reference for configuring distributed caches and TTL strategies.",                                                      "format": "PDF",    "potency": 4,  "reusable": "1", "category": "Optimization", "price": 109.25, "amount": 6,  "base_info": 5},
    # ── Recursive Loop (base_info=6) ──
    {"itemID": 14, "name": "Recursive Loop",       "description": "Traps enemies in an infinite callback spiral until their stack overflows.",                                                     "format": "Tome",   "potency": 7,  "reusable": "0", "category": "Destruction",  "price": 199.99, "amount": 5,  "base_info": 6},
    {"itemID": 15, "name": "Recursive Loop",       "description": "Compact incantation that spawns nested function calls to overwhelm targets.",                                                  "format": "PDF",    "potency": 5,  "reusable": "0", "category": "Destruction",  "price": 139.50, "amount": 8,  "base_info": 6},
    {"itemID": 16, "name": "Recursive Loop",       "description": "Single-use vortex that recursively dismantles an opponent's logic layer.",                                                     "format": "Scroll", "potency": 9,  "reusable": "0", "category": "Destruction",  "price": 310.00, "amount": 2,  "base_info": 6},
    # ── Patch Ward (base_info=7) ──
    {"itemID": 17, "name": "Patch Ward",           "description": "Continuously monitors dependencies and auto-applies security patches before exploits emerge.",                                  "format": "Tome",   "potency": 5,  "reusable": "1", "category": "Protection",   "price": 159.99, "amount": 7,  "base_info": 7},
    {"itemID": 18, "name": "Patch Ward",           "description": "Field guide for CVE detection and rapid vulnerability remediation.",                                                            "format": "PDF",    "potency": 3,  "reusable": "1", "category": "Protection",   "price": 99.00,  "amount": 11, "base_info": 7},
    # ── Quantum Compile (base_info=8) ──
    {"itemID": 19, "name": "Quantum Compile",      "description": "Harnesses qubit parallelism to compile massive codebases in milliseconds.",                                                     "format": "Tome",   "potency": 10, "reusable": "1", "category": "Optimization", "price": 399.99, "amount": 3,  "base_info": 8},
    {"itemID": 20, "name": "Quantum Compile",      "description": "Theoretical framework for superposition-based build optimization.",                                                             "format": "PDF",    "potency": 7,  "reusable": "1", "category": "Optimization", "price": 249.50, "amount": 5,  "base_info": 8},
    {"itemID": 21, "name": "Quantum Compile",      "description": "Experimental one-shot compiler burst that resolves all build errors simultaneously.",                                            "format": "Scroll", "potency": 10, "reusable": "0", "category": "Optimization", "price": 499.00, "amount": 1,  "base_info": 8},
    # ── Cloud Summon (base_info=9) ──
    {"itemID": 22, "name": "Cloud Summon",         "description": "Spins up auto-scaling infrastructure across multiple availability zones on command.",                                            "format": "Tome",   "potency": 8,  "reusable": "1", "category": "Deployment",   "price": 279.99, "amount": 4,  "base_info": 9},
    {"itemID": 23, "name": "Cloud Summon",         "description": "Quick-start guide for provisioning serverless functions and managed services.",                                                  "format": "PDF",    "potency": 5,  "reusable": "1", "category": "Deployment",   "price": 179.00, "amount": 9,  "base_info": 9},
    {"itemID": 24, "name": "Cloud Summon",         "description": "One-time terraform incantation that deploys an entire cloud environment.",                                                       "format": "Scroll", "potency": 9,  "reusable": "0", "category": "Deployment",   "price": 399.00, "amount": 2,  "base_info": 9},
    # ── Binary Barrier (base_info=10) ──
    {"itemID": 25, "name": "Binary Barrier",       "description": "Erects a low-level bitwise shield that corrupts malicious machine code on contact.",                                             "format": "Tome",   "potency": 6,  "reusable": "1", "category": "Protection",   "price": 169.99, "amount": 6,  "base_info": 10},
    {"itemID": 26, "name": "Binary Barrier",       "description": "Portable binary analysis toolkit for detecting buffer overflows and injection attacks.",                                          "format": "PDF",    "potency": 4,  "reusable": "0", "category": "Protection",   "price": 119.50, "amount": 10, "base_info": 10},
    # ── Null Pointer Curse (base_info=11) ──
    {"itemID": 27, "name": "Null Pointer Curse",   "description": "Corrupts an enemy's object references, causing catastrophic NullPointerExceptions at runtime.",                                  "format": "Tome",   "potency": 7,  "reusable": "0", "category": "Destruction",  "price": 129.99, "amount": 8,  "base_info": 11},
    {"itemID": 28, "name": "Null Pointer Curse",   "description": "Subtle hex that silently dereferences critical pointers in the target's codebase.",                                              "format": "PDF",    "potency": 5,  "reusable": "0", "category": "Destruction",  "price": 89.50,  "amount": 11, "base_info": 11},
    {"itemID": 29, "name": "Null Pointer Curse",   "description": "Devastating one-shot curse that nullifies every reference in memory.",                                                           "format": "Scroll", "potency": 9,  "reusable": "0", "category": "Destruction",  "price": 225.00, "amount": 3,  "base_info": 11},
    # ── Merge Conflict Doom (base_info=12) ──
    {"itemID": 30, "name": "Merge Conflict Doom",  "description": "Injects irreconcilable diffs across every branch, paralyzing the target's repository.",                                          "format": "Tome",   "potency": 8,  "reusable": "0", "category": "Destruction",  "price": 219.99, "amount": 4,  "base_info": 12},
    {"itemID": 31, "name": "Merge Conflict Doom",  "description": "Pocket chaos manual for seeding divergent commits into upstream branches.",                                                      "format": "PDF",    "potency": 6,  "reusable": "0", "category": "Destruction",  "price": 149.00, "amount": 7,  "base_info": 12},
    {"itemID": 32, "name": "Merge Conflict Doom",  "description": "Single-use rebase bomb that rewrites history across all open pull requests.",                                                    "format": "Scroll", "potency": 10, "reusable": "0", "category": "Destruction",  "price": 350.00, "amount": 2,  "base_info": 12},
]


def get_all_items() -> list[dict]:
    """Return every item in the catalogue."""
    return list(_baseprice)


def get_all_items_by_id(item_id: int) -> list[dict]:
    """Return ALL inventory items where base_info matches the given id."""
    return [item for item in _inventory if item["base_info"] == item_id]


def get_item_by_id(item_id: int) -> dict | None:
    """Look up a single item.  Returns None when not found."""
    return next((i for i in _inventory if i["base_info"] == item_id), None)
