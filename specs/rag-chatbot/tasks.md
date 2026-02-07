# Tasks: RAG Chatbot

**Input**: Design documents from `/specs/rag-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the feature specification, so test tasks are excluded per workflow rules.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/` (FastAPI application)
- **RAG utilities**: `rag/` (ingestion pipeline)
- **Frontend**: `website/src/components/` (React chat widget)

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize backend project structure and dependencies

- [X] T001 Create backend directory structure (backend/src/{api/routes,services,models,core})
- [X] T002 Create RAG utilities directory structure (rag/{ingest,scripts})
- [X] T003 Create Python virtual environment in backend/ directory
- [X] T004 [P] Create backend/requirements.txt with all dependencies (FastAPI, LangChain, sentence-transformers, qdrant-client, psycopg2, openai)
- [X] T005 [P] Create backend/.env.example with environment variable templates
- [X] T006 [P] Create backend/src/core/config.py for configuration management
- [X] T007 [P] Create backend/src/main.py with FastAPI application initialization
- [X] T008 [P] Create backend/.gitignore for Python project (venv/, __pycache__/, .env)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 Setup Qdrant Cloud account and create collection "textbook_chunks" with 384 dimensions (MANUAL - requires user account)
- [ ] T010 Setup Neon PostgreSQL database and obtain connection string (MANUAL - requires user account)
- [ ] T011 Create database schema in Neon (chat_sessions, chat_messages tables) per data-model.md (MANUAL - requires T010)
- [X] T012 [P] Create backend/src/core/database.py with SQLAlchemy engine and session management
- [X] T013 [P] Create backend/src/models/database.py with SQLAlchemy models (ChatSession, ChatMessage)
- [X] T014 [P] Create backend/src/models/chat.py with Pydantic models (QuestionRequest, AnswerResponse, Citation)
- [X] T015 [P] Configure CORS middleware in backend/src/main.py for frontend integration
- [X] T016 Create backend/src/api/routes/health.py with health check endpoint
- [ ] T017 Verify backend starts successfully with uvicorn (requires T009-T011 for full verification)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Question Answering (Priority: P1) 🎯 MVP

**Goal**: Enable learners to ask questions about textbook content and receive answers

**Independent Test**: POST to /api/chat/ask with a question, verify answer is returned with proper format

### Implementation for User Story 1

- [ ] T018 [P] [US1] Create backend/src/services/embeddings.py with MiniLM embedding generation
- [ ] T019 [P] [US1] Create backend/src/services/vector_store.py with Qdrant client and search operations
- [ ] T020 [P] [US1] Create backend/src/services/llm.py with OpenAI GPT-3.5-turbo integration
- [ ] T021 [US1] Create backend/src/services/rag.py with RAG pipeline (embed → search → generate)
- [ ] T022 [US1] Create backend/src/api/routes/chat.py with POST /api/chat/ask endpoint
- [ ] T023 [US1] Implement question embedding in RAG service
- [ ] T024 [US1] Implement vector search (top-k=5) in RAG service
- [ ] T025 [US1] Implement answer generation with LLM in RAG service
- [ ] T026 [US1] Store chat message in database after successful answer
- [ ] T027 [US1] Test question answering end-to-end with sample questions

**Checkpoint**: At this point, basic question answering should work (without citations yet)

---

## Phase 4: User Story 2 - Citations (Priority: P1) 🎯 MVP

**Goal**: Provide citations with answers so learners can verify information

**Independent Test**: Ask a question, verify response includes citations with chapter_id, section, and text_snippet

### Implementation for User Story 2

- [ ] T028 [P] [US2] Enhance backend/src/services/rag.py to extract citations from retrieved chunks
- [ ] T029 [P] [US2] Add citation formatting logic to include chapter_id, chapter_title, section, text_snippet
- [ ] T030 [US2] Update AnswerResponse model to include citations array
- [ ] T031 [US2] Store citations in chat_messages.citations JSONB field
- [ ] T032 [US2] Verify citations reference actual textbook chunks
- [ ] T033 [US2] Test citation accuracy with diverse questions

**Checkpoint**: Answers now include proper citations with source references

---

## Phase 5: User Story 3 - Answer Grounding (Priority: P2)

**Goal**: Ensure answers are accurate and don't hallucinate information

**Independent Test**: Ask questions outside textbook scope, verify chatbot responds "I don't know based on the textbook content"

### Implementation for User Story 3

- [ ] T034 [P] [US3] Create prompt template in backend/src/services/llm.py with grounding instructions
- [ ] T035 [P] [US3] Implement relevance scoring for retrieved chunks
- [ ] T036 [US3] Add logic to return "I don't know" if relevance scores are too low (<0.7)
- [ ] T037 [US3] Constrain LLM to only use provided context (temperature=0, strict prompt)
- [ ] T038 [US3] Test with out-of-scope questions (e.g., "What is quantum computing?")
- [ ] T039 [US3] Test with ambiguous questions to verify grounding

**Checkpoint**: Chatbot refuses to answer questions outside textbook scope

---

## Phase 6: User Story 4 - Document Ingestion (Priority: P3)

**Goal**: Enable admins to re-ingest textbook content when chapters are updated

**Independent Test**: POST to /api/ingest with admin API key, verify chunks are updated in Qdrant

### Implementation for User Story 4

- [ ] T040 [P] [US4] Create rag/ingest/loader.py to load Markdown files from website/docs/
- [ ] T041 [P] [US4] Create rag/ingest/chunker.py with RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
- [ ] T042 [P] [US4] Create rag/ingest/pipeline.py to orchestrate loading → chunking → embedding → storage
- [ ] T043 [US4] Implement frontmatter parsing to extract chapter metadata
- [ ] T044 [US4] Implement batch embedding generation (100 chunks at a time)
- [ ] T045 [US4] Implement batch upsert to Qdrant with metadata
- [ ] T046 [US4] Create rag/scripts/ingest_textbook.py CLI script for manual ingestion
- [ ] T047 [US4] Create backend/src/api/routes/ingest.py with POST /api/ingest endpoint (admin only)
- [ ] T048 [US4] Implement API key authentication for ingestion endpoint
- [ ] T049 [US4] Test ingestion with all 6 textbook chapters
- [ ] T050 [US4] Verify 10,000+ chunks are stored in Qdrant

**Checkpoint**: Document ingestion pipeline is fully functional

---

## Phase 7: Chat History (Priority: P2)

**Goal**: Enable conversation history retrieval

**Independent Test**: GET /api/chat/history with session_id, verify messages are returned in chronological order

### Implementation for Chat History

- [ ] T051 [P] Create backend/src/api/routes/chat.py GET /api/chat/history endpoint
- [ ] T052 [P] Implement session_id generation and tracking
- [ ] T053 Implement pagination for chat history (limit, offset parameters)
- [ ] T054 Query chat_messages table by session_id with proper ordering
- [ ] T055 Test history retrieval with multiple messages

**Checkpoint**: Chat history retrieval works correctly

---

## Phase 8: Frontend Integration (Priority: P1) 🎯 MVP

**Goal**: Embed chat widget in Docusaurus site for user interaction

**Independent Test**: Open textbook site, click chat button, ask question, verify answer displays with citations

### Implementation for Frontend

- [ ] T056 [P] Create website/src/components/ChatWidget/ChatWidget.tsx main component
- [ ] T057 [P] Create website/src/components/ChatWidget/ChatMessage.tsx message display component
- [ ] T058 [P] Create website/src/components/ChatWidget/ChatInput.tsx input field component
- [ ] T059 [P] Create website/src/components/ChatWidget/ChatWidget.css styling
- [ ] T060 [P] Create website/src/services/chatApi.ts API client for backend
- [ ] T061 Implement chat state management with React hooks
- [ ] T062 Implement question submission to backend API
- [ ] T063 Implement answer display with loading states
- [ ] T064 Implement citation display with clickable chapter links
- [ ] T065 Implement conversation history display
- [ ] T066 Add chat widget to Docusaurus via website/src/theme/Root.tsx
- [ ] T067 Test chat widget on desktop and mobile
- [ ] T068 Verify citations link to correct textbook chapters

**Checkpoint**: Chat widget is fully integrated and functional

---

## Phase 9: Deployment (Priority: P1) 🎯 MVP

**Purpose**: Deploy backend to Railway and verify production functionality

- [ ] T069 Create backend/Dockerfile for containerization
- [ ] T070 Create backend/railway.json with deployment configuration
- [ ] T071 Connect GitHub repository to Railway
- [ ] T072 Configure environment variables in Railway dashboard
- [ ] T073 Deploy backend to Railway
- [ ] T074 Verify health check endpoint is accessible
- [ ] T075 Test question answering on production API
- [ ] T076 Update frontend API URL to production Railway URL
- [ ] T077 Test end-to-end flow with production backend

**Checkpoint**: Backend is deployed and accessible from frontend

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and production readiness

- [ ] T078 [P] Add error handling for Qdrant connection failures
- [ ] T079 [P] Add error handling for OpenAI API failures
- [ ] T080 [P] Add error handling for database connection failures
- [ ] T081 [P] Implement request logging in backend
- [ ] T082 [P] Add rate limiting to prevent abuse (future: 100 requests/hour per session)
- [ ] T083 [P] Optimize embedding model loading (cache in memory)
- [ ] T084 [P] Add response time monitoring
- [ ] T085 Verify all acceptance criteria from spec.md
- [ ] T086 Create backend/README.md with setup instructions
- [ ] T087 Document API endpoints in backend/docs/
- [ ] T088 Run performance tests (verify <2s response time)
- [ ] T089 Verify Qdrant free tier usage is within limits

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (Question Answering): Can start after Foundational
  - US2 (Citations): Depends on US1 (need basic Q&A first)
  - US3 (Grounding): Can start after US1 (parallel with US2)
  - US4 (Ingestion): Can start after Foundational (parallel with US1)
- **Chat History (Phase 7)**: Depends on US1 completion
- **Frontend (Phase 8)**: Depends on US1 and US2 completion (need Q&A + citations)
- **Deployment (Phase 9)**: Depends on US1, US2, and Frontend completion (MVP ready)
- **Polish (Phase 10)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (Question Answering)**: Can start after Foundational - No dependencies on other stories
- **US2 (Citations)**: Depends on US1 (extends Q&A with citations)
- **US3 (Grounding)**: Can start after US1 (parallel with US2)
- **US4 (Ingestion)**: Independent - Can start after Foundational (parallel with US1)

### Within Each User Story

- US1: Services (embeddings, vector_store, llm) can be built in parallel, then RAG service integrates them
- US2: Citation logic extends US1, sequential dependency
- US3: Grounding logic extends US1, can be parallel with US2
- US4: Ingestion components (loader, chunker, pipeline) can be built in parallel

### Parallel Opportunities

- **Phase 1 (Setup)**: Tasks T004-T008 can run in parallel after T001-T003
- **Phase 2 (Foundational)**: Tasks T012-T016 can run in parallel after T009-T011
- **Phase 3 (US1)**: Tasks T018-T020 can run in parallel
- **Phase 4 (US2)**: Tasks T028-T029 can run in parallel
- **Phase 5 (US3)**: Tasks T034-T035 can run in parallel
- **Phase 6 (US4)**: Tasks T040-T042 can run in parallel
- **Phase 8 (Frontend)**: Tasks T056-T060 can run in parallel
- **Phase 10 (Polish)**: Tasks T078-T084 can run in parallel

---

## Parallel Example: User Story 1 (Question Answering)

```bash
# Launch all service implementations together:
Task: "Create backend/src/services/embeddings.py with MiniLM embedding generation"
Task: "Create backend/src/services/vector_store.py with Qdrant client and search operations"
Task: "Create backend/src/services/llm.py with OpenAI GPT-3.5-turbo integration"

# Then integrate them:
Task: "Create backend/src/services/rag.py with RAG pipeline (embed → search → generate)"
```

## Parallel Example: User Story 4 (Document Ingestion)

```bash
# Launch all ingestion components together:
Task: "Create rag/ingest/loader.py to load Markdown files from website/docs/"
Task: "Create rag/ingest/chunker.py with RecursiveCharacterTextSplitter"
Task: "Create rag/ingest/pipeline.py to orchestrate loading → chunking → embedding → storage"
```

---

## Implementation Strategy

### MVP First (US1 + US2 + Frontend + Deployment)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: US1 (Question Answering)
4. Complete Phase 4: US2 (Citations)
5. Complete Phase 8: Frontend Integration
6. Complete Phase 9: Deployment
7. **STOP and VALIDATE**: Test end-to-end Q&A with citations on production
8. Demo the MVP - functional chatbot with citations

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 (Question Answering) → Test independently → Basic Q&A works
3. Add US2 (Citations) → Test independently → Answers include sources
4. Add Frontend → Test independently → Chat widget functional (MVP!)
5. Deploy to Railway → Live chatbot available
6. Add US3 (Grounding) → Test independently → Improved accuracy
7. Add US4 (Ingestion) → Test independently → Admin can update content
8. Add Chat History → Test independently → Conversation tracking
9. Polish → Final production readiness

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: US1 (Question Answering)
   - Developer B: US4 (Document Ingestion) - parallel with US1
   - Developer C: Frontend components - can start structure
3. After US1 complete:
   - Developer A: US2 (Citations)
   - Developer B: Continue US4
   - Developer C: Frontend integration with US1
4. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 89 tasks
**MVP Tasks** (US1 + US2 + Frontend + Deployment): 51 tasks
**Enhancement Tasks** (US3 + US4 + History): 26 tasks
**Polish Tasks**: 12 tasks

**Tasks by User Story**:
- Setup: 8 tasks
- Foundational: 9 tasks
- US1 (Question Answering): 10 tasks
- US2 (Citations): 6 tasks
- US3 (Answer Grounding): 6 tasks
- US4 (Document Ingestion): 11 tasks
- Chat History: 5 tasks
- Frontend Integration: 13 tasks
- Deployment: 9 tasks
- Polish: 12 tasks

**Parallel Opportunities**: 35 tasks marked [P] can run in parallel within their phases

**Suggested MVP Scope**: Phases 1, 2, 3, 4, 8, 9 (51 tasks) deliver a fully functional chatbot with citations

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are NOT included per feature specification (no TDD requested)
- Focus on RAG accuracy and citation quality per constitution requirements
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
