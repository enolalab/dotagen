---
name: "dotagent:apollographql:apollo-kotlin"
description: "A GraphQL client for Android, JVM, and Kotlin Multiplatform projects"
category: "Backend & APIs"
vendor: "apollographql"
license: MIT
compatibility: JVM 8+, Kotlin 1.9+, Gradle 8+, Android/JVM/Kotlin Multiplatform projects.
allowed-tools: Bash(./gradlew:*) Bash(gradle:*) Bash(curl:*) Read Write Edit Glob Grep WebFetch
---

# Apollo Kotlin Guide

Apollo Kotlin is a strongly typed GraphQL client that generates Kotlin models from your GraphQL operations and schema, that can be used in Android, JVM, and Kotlin Multiplatform projects.

## Process

Follow this process when adding or working with Apollo Kotlin:

- [ ] Confirm target platforms (Android, JVM, KMP), GraphQL endpoint(s), and how schemas are sourced.
- [ ] Configure Gradle and code generation, including custom scalars
- [ ] Create a shared `ApolloClient` with auth, logging, and caching.
- [ ] Implement operations.
- [ ] Validate behavior with tests and error handling.


## Reference Files

- [Setup](references/setup.md) - Gradle plugin, schema download, codegen config (including scalars), client configuration (auth, logging, interceptors)
- [Operations](references/operations.md) - Queries, mutations, subscriptions, and how to execute them
- [Caching](references/caching.md) - Setup and use the normalized cache
- [Migration Guide](references/migrating-from-4.md) - Migrate from Apollo Kotlin 4

## Scripts

- [list-apollo-kotlin-versions.sh](scripts/list-apollo-kotlin-versions.sh) - List versions of Apollo Kotlin
- [list-apollo-kotlin-normalized-cache-versions.sh](scripts/list-apollo-kotlin-normalized-cache-versions.sh) - List versions of the Apollo Kotlin Normalized Cache library

## Key Rules

- Prefer Apollo Kotlin v5+. Do not use v3 or older versions.
- Keep schema and operations in source control to make builds reproducible.
