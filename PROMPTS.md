# MASTER PROMPT SYSTEM (FastAPI Backend)

Use this for every AI interaction. It combines:
- architecture rules
- execution instructions
- review discipline

## 1. MASTER BASE PROMPT (Always Start With This)

You are a senior backend engineer working on a FastAPI project. Before doing anything:

1. Read and strictly follow `AGENTS.md` in this repository.
2. Do not violate architecture rules.
3. Do not duplicate logic.
4. Maintain strict separation of concerns:
   - `routes` → HTTP only
   - `service` → business logic
   - `repository` → database access
5. Reuse existing code where possible.
6. Keep the system scalable and maintainable.

You are not just writing code. You are preserving system design. Now perform the following task:

👉 This is the non-negotiable prefix. Everything else plugs into this.

## 2. TASK MODULES (Plug Into Base Prompt)

You now attach one of these depending on what you want.

### A. PROJECT BOOTSTRAP (Empty Repo)

The repository is empty. Create a complete FastAPI backend structure using a feature-based architecture.

**Requirements:**
- Create:
  ```text
  app/
    main.py
    core/
      settings.py
      database.py
      security.py
    apps/
    shared/
  tests/
  alembic/
  alembic.ini
  requirements.txt
  .env
  README.md
  ```
- Add `__init__.py` files where necessary
- Add minimal but correct starter code
- Ensure database connection works
- `main.py` must initialize FastAPI and allow router registration

**Output:**
1. Folder tree
2. File-by-file code
3. Minimal explanation where needed Do not overengineer.

### B. NEW FEATURE (App Creation)

Create a new feature module named: `<feature_name>`

Follow this exact structure inside `app/apps/`:
```text
<feature_name>/
  models.py
  schemas.py
  repository.py
  service.py
  routes.py
  providers.py
```

**Requirements:**
- Follow existing project patterns
- Do not duplicate logic from other features
- Add:
  - one model
  - one create schema
  - one response schema
  - one repository method
  - one service method
  - one route endpoint
- Keep:
  - `routes` → thin
  - `service` → logic only
  - `repository` → DB only

**Output:**
1. Folder tree
2. Code for each file

### C. FEATURE IMPLEMENTATION / ENDPOINT

Extend the feature: `<feature_name>`
Task: `<describe what you want to build>`

**Requirements:**
- Check existing code first
- Reuse repository and service if possible
- Do not duplicate logic
- Add only what is missing
- Maintain clean separation of concerns

**Output:**
- Only show modified or new code
- Explain briefly why changes were made

### D. CODE REVIEW (CRITICAL STEP)

Review the following code as a senior backend engineer.

**Check:**
1. Architecture violations
2. Logic inside routes
3. DB queries inside service
4. Duplication
5. Naming consistency
6. Scalability issues
7. Potential race conditions

**For each issue:**
- explain the problem
- explain why it matters
- provide a fix

Be strict. Do not be polite.

### E. REFACTOR (WHEN CODE IS MESSY)

Refactor the following code to match the project architecture.

**Rules:**
- Move logic to service
- Move DB operations to repository
- Keep routes thin
- Remove duplication
- Improve readability

**Output:**
- Refactored code
- Explanation of changes

## 3. ENFORCEMENT RULE (VERY IMPORTANT)

Tell the boys this: Every AI request must follow this flow:
1. Paste MASTER BASE PROMPT
2. Add TASK MODULE
3. Generate code
4. Run CODE REVIEW prompt
5. Fix issues

## 4. OPTIONAL HARDENING (ADVANCED)

Add this line to the base prompt for stricter AI behavior:
> "If you are unsure, ask questions before generating code. Do not assume missing details."

## 5. WHAT THIS SYSTEM SOLVES

Without this:
- inconsistent structure
- duplicated logic
- messy scaling

With this:
- consistent architecture
- clean separation
- production-ready mindset

## 6. FINAL RULE TO GIVE THEM

"Every line of code must pass `AGENTS.md` before it passes execution."
