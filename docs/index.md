---
description: Spellstack API documentation, including getting started guide, endpoint reference, and configuration instructions for local development.
---

# Spellstack Documentation Site

Spellstack is a e-commerce platform featuring developer-focused spells designed for security, debugging, deployment, performance, and offensive operations. Spellstack API serves as the backend interface for the platform, providing RESTful endpoints for product catalog access, inventory management, purchase workflows, and account operations. This documentation site provides comprehensive guides for developers to get started with the API, understand endpoint contracts, and configure their local environment for development and testing.

![Spellstack logo](assets/images/TBlogo.png)

## Product Overview

Spellstack sells 12 unique tech-themed spells. Each spell has 3 purchasable variants that differ by format, potency, reusability, and price. The base catalog lists each spell with a base price and image, while individual purchasable variants are stored as inventory items linked to their parent spell.

**Product Catalog**  

Spellstack's catalog includes 12 core spells across five categories, with each spell offered in 3 purchasable variants.

- Protection: Firewall Spell, Encryption Hex, Patch Ward, Binary Barrier
- Debugging: Bug Banish
- Deployment: Deploy Surge, Cloud Summon
- Optimization: Cache Conjure, Quantum Compile
- Destruction: Recursive Loop, Null Pointer Curse, Merge Conflict Doom

Variant-level details such as format, potency, reusability, price, and stock are exposed through the API inventory endpoints and maintained in the backend inventory model.

## Documentation Map

Use this documentation set based on your task:

- API onboarding and endpoint contracts: [Getting Started with Spellstack API](API-User-Guides/Getting-Started-with-Spellstack-API.md)
- Local environment and runtime setup: [Configuring Spellstack API](API-User-Guides/Configuring-Spellstack-API.md)
- Release notes and version changes: [Release Notes v0.0.1](Release-Notes/Release-Notes-v-0.0.1.md)
- API endpoint reference: [Spellstack API endpoints](API-User-Guides/Spellstack-API-endpoints.md)
