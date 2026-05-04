# AGENTS.md

## Backend Engineering Guidelines For FastAPI

### Purpose

This document defines the engineering standards that every AI agent must follow
before generating or modifying code in this FastAPI backend.

The goal is not simply to produce working code. The goal is to protect the
architecture, keep the codebase maintainable, and ensure that every change fits
cleanly into the existing system.

Poorly structured code creates long-term problems:

- Duplicated business logic.
- Inconsistent feature organization.
- Database access scattered across the project.
- Route handlers that become difficult to test.
- Features that are hard to extend without rewriting.

Every agent working on this project is expected to write code with the discipline
of a senior backend engineer.

## Required Understanding Before Coding

Before making any code changes, first understand the structure and behavior of
the project.

### 1. Review The Project Structure

Understand where each responsibility belongs:

```text
app/
main.py
core/
apps/
shared/
```

Do not create new folders or patterns without confirming that they are needed
and consistent with the existing architecture.

### 2. Identify The Feature Being Modified

Before writing new code:

- Check whether the feature already exists.
- Extend existing functionality where appropriate.
- Avoid creating duplicate modules for the same responsibility.
- Keep feature boundaries clear.

If a feature already exists, improve or extend it instead of recreating it.

### 3. Follow The Architecture Flow

The expected backend flow is:

```text
Route -> Service -> Repository -> Database
```

Each layer has a specific responsibility:

- `Route`: Handles HTTP requests and responses.
- `Service`: Owns business logic and workflows.
- `Repository`: Owns database queries.
- `Database`: Persists and retrieves data.

The layers must remain separate. This keeps the application easier to test,
debug, and scale.

### 4. Search Before Writing

Before creating any of the following, search the codebase first:

- Models.
- Schemas.
- Services.
- Repositories.
- Utility functions.
- Authentication or validation logic.

Reuse existing code where possible. Do not duplicate logic that already exists
in the project.

## Architecture Rules

These rules are non-negotiable.

### Routes

Route files should only:

- Receive requests.
- Validate request input through schemas or dependencies.
- Call the appropriate service.
- Return the response.

Routes must not contain:

- Business logic.
- Database queries.
- Complex workflows.

### Services

Service files should contain:

- Business rules.
- Application workflows.
- Validation that goes beyond basic schema validation.
- Coordination between repositories or domain operations.

Services must not contain:

- Raw HTTP response handling.
- FastAPI-specific exception formatting.
- Unstructured database access when a repository layer exists.

### Repositories

Repository files should contain database access only.

Repositories may:

- Query records.
- Create records.
- Update records.
- Delete records.
- Encapsulate SQLAlchemy query logic.

Repositories must not contain:

- Business rules.
- HTTP concerns.
- Request validation logic.

### Schemas

Schema files are responsible for:

- Request validation.
- Response formatting.
- API-facing data contracts.

Schemas should not contain business workflows or database behavior.

### Models

Model files define the database structure only.

Models should remain simple and should not contain business rules that belong in
the service layer.

### Providers

Provider files are used to create services and inject dependencies.

They should make dependency wiring explicit and keep construction logic out of
routes.

## Code Generation Rules

### Keep Features Organized

Do not place all logic in one file. A feature should follow this structure when
the project uses a full layered layout:

```text
models.py
schemas.py
repository.py
service.py
routes.py
providers.py
```

Use the existing project pattern first. Add missing layers only when they improve
clarity and match the direction of the codebase.

### Maintain Feature Isolation

Feature-specific code should stay inside its feature boundary.

For example:

- Code inside `users/` should not leak into `payments/`.
- Cross-feature interactions should be explicit.
- Shared logic should live in an agreed shared module, not copied between
  features.

### Use Consistent Naming

Names should be clear, predictable, and aligned with the rest of the project.

Examples:

- `UserService`
- `UserRepository`
- `UserCreateSchema`
- `ApplicationService`
- `ApplicationRepository`

Avoid vague names such as `Manager`, `Handler`, or `Helper` unless the project
already uses them consistently.

### Keep Functions Small

Each function should do one thing well.

A good function is:

- Easy to read.
- Easy to test.
- Easy to reuse.
- Clear about what it accepts and returns.

If a function is doing too much, split it into smaller named operations.

## Safety And Reliability Rules

### Prevent Race Conditions

When writing logic that updates data or depends on existing state, assume that
multiple requests can happen at the same time.

Avoid unsafe patterns such as:

```text
read -> modify -> write
```

Prefer:

- Atomic database operations.
- Unique constraints.
- Transactions.
- Row-level locking when required.
- Database-enforced integrity instead of application-only assumptions.

### Avoid Duplication

Before implementing new logic:

- Search for an existing implementation.
- Reuse shared helpers where appropriate.
- Extend current behavior instead of creating parallel behavior.

Duplicate code makes bugs harder to fix and makes the system harder to reason
about.

### Handle Errors Deliberately

Errors should be clear, controlled, and useful.

Do not expose raw exceptions to API clients. Convert internal failures into
meaningful application or HTTP errors at the correct layer.

### Avoid Silent Failures

Every failure should be explicit.

The code should not ignore important errors, swallow exceptions without action,
or return misleading success responses.

## Database Rules

### Use Migrations

Schema changes must be tracked through Alembic migrations.

Do not rely on automatic table creation for production behavior. Every database
change should be versioned, reviewed, and applied intentionally.

### Keep Models Focused

Database models should define structure and relationships.

Do not place business workflows, HTTP behavior, or request validation in model
classes.

## Adding A New Feature

When adding a feature, follow this order:

1. Check whether the feature already exists.
2. Review the current project structure and naming conventions.
3. Add or update the required files:
   - `models.py`
   - `schemas.py`
   - `repository.py`
   - `service.py`
   - `routes.py`
   - `providers.py`
4. Register routes in `main.py` where appropriate.
5. Reuse existing logic wherever possible.
6. Confirm the layer separation is still clean.
7. Add or update migrations for database changes.
8. Add tests when behavior changes.

## Output Requirements For AI Agents

When generating code, every agent must:

- Follow the existing project structure.
- Keep code readable and minimal.
- Add comments only where they clarify non-obvious behavior.
- Avoid overengineering.
- Use clear names.
- Preserve feature boundaries.
- Avoid duplicating existing logic.
- Respect the route-service-repository separation.

## Red Flags

Do not introduce any of the following:

- Business logic inside route handlers.
- Database queries inside route handlers.
- Duplicate models or schemas.
- New feature folders when an existing feature should be extended.
- Large unstructured functions.
- Silent exception handling.
- Hardcoded production secrets.
- Schema changes without migrations.
- Code that ignores existing project patterns.

## Final Engineering Principle

The responsibility of an AI agent is not to generate code quickly. The
responsibility is to generate code that can be maintained, tested, extended, and
scaled without forcing a future rewrite.

Every change should leave the backend easier to understand than it was before.
