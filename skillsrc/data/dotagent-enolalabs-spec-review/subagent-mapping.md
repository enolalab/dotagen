# Subagent Mapping: Tech Stack Detection

## How to Detect Tech Stack

### Phase 1: Scan Project Files

Check the project root (and one level deep) for these files:

| File | Language/Stack | Subagent |
|------|---------------|----------|
| `go.mod` | Go | `golang-pro` |
| `package.json` | JavaScript/TypeScript | `typescript-pro` or `javascript-pro` |
| `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile` | Python | `python-pro` |
| `Cargo.toml` | Rust | `rust-engineer` |
| `*.csproj`, `*.sln` | C# / .NET | `csharp-developer` |
| `pom.xml`, `build.gradle` | Java | `java-architect` |
| `Gemfile` | Ruby | `rails-expert` |
| `composer.json` | PHP | `php-pro` |
| `Pubspec.yaml` | Dart/Flutter | `flutter-expert` |
| `Package.swift` | Swift | `swift-expert` |
| `mix.exs` | Elixir | `elixir-expert` |

### Phase 2: Scan Spec Content for Keywords

Search the spec text for these patterns:

| Keyword Pattern | Maps To | Subagent |
|----------------|---------|----------|
| `React`, `JSX`, `Next.js`, `Remix` | React frontend | `react-specialist` or `nextjs-developer` |
| `Vue`, `Nuxt`, `Vite` | Vue frontend | `vue-expert` |
| `Angular`, `NgRx` | Angular frontend | `angular-architect` |
| `GraphQL`, `Apollo`, `Hasura` | GraphQL API | `graphql-architect` |
| `PostgreSQL`, `postgres` | PostgreSQL DB | `postgres-pro` |
| `MySQL`, `MariaDB` | MySQL DB | `database-administrator` |
| `MongoDB`, `mongoose` | MongoDB | `database-administrator` |
| `Redis`, `cache` | Redis/cache | `performance-engineer` |
| `Docker`, `container` | Containerization | `docker-expert` |
| `Kubernetes`, `K8s`, `helm` | Orchestration | `kubernetes-specialist` |
| `Terraform`, `IaC` | Infrastructure | `terraform-engineer` |
| `AWS`, `GCP`, `Azure` | Cloud platform | `cloud-architect` |
| `OAuth`, `JWT`, `authentication`, `auth` | Auth system | `penetration-tester` (additional) |
| `payment`, `Stripe`, `billing` | Payment system | `payment-integration` (additional) |
| `GDPR`, `CCPA`, `HIPAA`, `compliance` | Regulatory | `compliance-auditor` (additional) |

### Phase 3: Map to Review Groups

Based on detected tech stack, determine which subagents to dispatch per review group:

#### Technical & Code Quality
- **Always:** `backend-architect` (or `fullstack-developer` if full-stack)
- **Language-specific** (pick all that apply):
  - Go → `golang-pro`
  - Python → `python-pro`
  - TypeScript/JavaScript → `typescript-pro`
  - Java → `java-architect`
  - C# → `csharp-developer`
  - Rust → `rust-engineer`
  - PHP → `php-pro`
  - Ruby → `rails-expert`
- **Frontend-specific** (if frontend detected):
  - React → `react-specialist`
  - Vue → `vue-expert`
  - Next.js → `nextjs-developer`
  - Angular → `angular-architect`

#### Performance
- **Always:** `performance-engineer`
- **If database detected:** add `database-optimizer`
- **If cloud/infra detected:** add `cloud-architect`

#### Security
- **Always:** `security-auditor`
- **If auth/payment detected:** add `penetration-tester`
- **If compliance keywords detected:** add `compliance-auditor`

#### Process & Operations
- **Always:** `devops-engineer`
- **If K8s detected:** add `kubernetes-specialist`
- **If Docker detected:** add `docker-expert`
- **If Terraform detected:** add `terraform-engineer`

#### Product & People
- **Always:** `product-manager`
- **If UI/frontend detected:** add `ux-researcher`
- **If business logic heavy:** add `business-analyst`

### Fallback Rules

- If a specialized subagent is not available on the current platform, fall back to `general-purpose` with the reviewer prompt template
- If no tech stack is detected at all, use `general-purpose` for all review groups
- If the project is a library/CLI (no UI), skip the `ux-researcher` in Product review
