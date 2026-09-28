---
name: music-metadata-standards
description: DDEX and Believe compliant metadata structures for music catalogs.
version: 0.1.0
metadata.hermes.tags:
  - Architecture
  - DomainKnowledge
  - Music
  - Database
---

# Music Metadata Standards

Defines the strict separation of Release (Album) vs. Track metadata and the relational model for Contributors required by global music aggregators (e.g., DDEX, Believe). Prevents flat-schema anti-patterns where track-level details are improperly stored at the release level.

## When to Use
- "Design a music platform database."
- "Build a music upload wizard."
- "Fix ISRC, UPC, or contributor mapping logic."
- "Map music metadata to UI forms."

## Prerequisites
- PostgreSQL / Drizzle ORM (for schema implementation).

## How to Run
Apply these constraints when designing UI forms or database schemas using the `terminal` or `patch` tools.

## Quick Reference
- **Release (Album):** UPC, EAN, Cover Art, Global Price, Release Date.
- **Track:** ISRC, Track Type, Lyrics (Instrumental), Vocal Language.
- **Contributor:** Many-to-Many via Roles (Contributor -> Role -> Track).

## Procedure
1. **Separate Release vs. Track Data**
   Ensure database schemas and UI forms separate these fields completely:
   - **Release-Level (`product`):** UPC/EAN/SKU Barcodes, Main Release Title, Main Cover Art, Main Release Date.
   - **Track-Level (`productTrack`):** ISRC (International Standard Recording Code), Track Type (Original/Cover/Karaoke), Lyrics (Instrumental/Has Lyrics), Vocal Language, Explicit Rating.

2. **Implement Relational Contributor Model**
   Do NOT use flat columns like `primaryArtist` or `composer` on the Release or Track table. Instead, structure it relationally:
   - **`Contributor` Table:** Holds the individual or band (Name, Spotify URI, Apple Music URI).
   - **`TrackContributorRole` (Many-to-Many Pivot):** Maps a Contributor to a specific Track with a specific Role (e.g., "Main Artist", "Composer", "Producer", "Instrument: 12-String Guitar").

3. **Align UI Flow with Metadata Levels**
   - Step 1/2 (Release Info): Ask only for Release-level data (UPC, Album Title, Overall Cover).
   - Step 3 (Track Info / Modal): Open a dedicated sub-form per track to ask for Track-level data (ISRC, Instrumental toggle, Roles).

## Pitfalls
- **ISRC at Release Level:** A common mistake is placing an `isrc` column on the Album table. An album has a UPC; its individual tracks each have unique ISRCs.
- **Flat Contributor Fields:** Hardcoding `composer: text()` prevents assigning multiple composers or attributing an individual to multiple distinct roles across different tracks.

## Verification
Inspect the database schema (`cat src/db/schema.ts`) to ensure `isrc` is only on the track table and a pivot table exists for contributor roles.