---
id: 001
title: Project Constitution Initial Setup
stage: constitution
date: 2026-01-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: DELL
command: /sp.constitution
labels: ["constitution", "project-setup", "architecture", "ai-textbook"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

/sp.constitution # Project Constitution: AI-Native Textbook for physical AI and Humanoid Robotics

## 1. Mission
Build a fully AI-native, interactive, intelligent textbook that teaches the Physical AI & Humanoid Robotics course. The product must be fast, simple, beautiful and feel like a REAL AI-powered education platform -- not just a book.

## 2. Core-Deliverables
1. A Docusaurus-based interactive textbook with 6-8 short, clean, modern chapters.
2. A fully functional RAG  chatbot answering questions ONLY from the book.
3. User authentication (signup/login) using Better-Auth.
4. Personalized chapter content based on user-background.
5. One-click Urdu translation for every chapter.
6. Auto-generated summaries, quizzes, and learning boosters.

## 3. Success criteria
- Clean UI, fast loading, mobile friendly.
- Book readable in < 45 minutes total.
- RAG answers accurate, cited and grounded.
- Personalization visibly improves text.
- Urdu translation high-quality and fast.
- Fully deployed:
  - Frontend -> Vercel
  - Backend -> Railway
  - Vectors -> Qdrant
  - Database -> Neon

## 4. Non-Goals
- No extra animation beyond minimal useful motion.
- No overly long chapters (short + clear only).
- No complex robotics code -- only education content.

## 5. Architecture Principles
- Keep frontend extremely simple, readable.
- Keep backend modular (FastAPI + services + routes).
- All data must be stored cleanly in Neon + Qdrant.
- Use clean folder structure:
  - `/backend`
  - `/website`
  - `/rag`
  - `/agents`
- Use reusable agent skill for bonus scoring.

## 6. User Stories (Prioritized)
1. As a learner, I want to read the textbook smoothly.
1. As a learner, I want to ask the chatbot questions.
1. As a learner, I want personalized content based on my background.
1. As a learner, I want Urdu translation.
1. As a learner, I want summaries + quizzes.
1. As an admin, I want clean architecture and deployment.

## 7. Constraints
- Must work on free tiers (Qdrant + Neon).
- Must deploy within 90 seconds demo recording.
- Must support low-end devices (users reading on phones).
- Must avoid complexity and heavy dependencies.

## 8. Risks and Mitigations
- **RAG low accuracy** -> use chunking + MiniLM embeddings.
- **Token usage high** -> implement in phases.
- **User confusion** -> keep UI minimal and clean.
- **Backend errors** -> add health checks + logging.

## 9. Definition of Done
- All chapters visible and readable.
- Chatbot fully functional with grounded answers.
- Auth + personalization + translation working.
- Quizzes + summaries per chapter generated.
- Fully developed URLs live and stable.
- 90-second demo recorded.

## Response snapshot

Constitution successfully created and stored at `.specify/memory/constitution.md`. The constitution establishes:

**Mission**: Build a fully AI-native, interactive, intelligent textbook for Physical AI & Humanoid Robotics that is fast, simple, and beautiful.

**Core Deliverables**:
1. Docusaurus-based textbook (6-8 chapters)
2. RAG chatbot (book-grounded answers only)
3. Better-Auth authentication
4. Personalized content based on user background
5. One-click Urdu translation
6. Auto-generated summaries, quizzes, and learning boosters

**Tech Stack**:
- Frontend: Docusaurus → Vercel
- Backend: FastAPI → Railway
- Vectors: Qdrant (free tier)
- Database: Neon (free tier)

**Architecture**: Clean folder structure (`/backend`, `/website`, `/rag`, `/agents`) with modular FastAPI backend and simple, readable frontend.

**Key Constraints**: Free tier compatibility, 90-second demo requirement, mobile-friendly, minimal complexity.

## Outcome

- ✅ Impact: Project constitution established as authoritative source for all development decisions
- 🧪 Tests: No tests required for documentation
- 📁 Files: Created/updated `.specify/memory/constitution.md`
- 🔁 Next prompts: Create feature specs, implement folder structure, set up development environment
- 🧠 Reflection: Constitution provides clear mission, deliverables, constraints, and success criteria. Ready to guide all subsequent development work.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - constitution establishment
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin with folder structure setup and initial Docusaurus configuration
