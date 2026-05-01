# Voyagr — Architecture & Learning Plan

## Project Overview (High-Level)
**Voyagr** is a full-stack AI-powered personalized travel itinerary planner.  
Users provide destination, dates, budget, interests, group size, etc. → a LangGraph agent reasons step-by-step, calls real tools (weather, maps, flights, hotels, activities), and generates a complete multi-day trip plan with citations and reasoning.  
Built with FastAPI (backend) + Streamlit (frontend) using modern LangChain + LangGraph patterns.  
Primary learning focus: Deep mastery of LangGraph, tool/function calling, MCP/FastMCP, and production-grade agentic systems.

## Current Phase
Currently in: **Phase 0**

## Phase Progress Tracker
- [x] Phase 0: Project Setup & Architecture Mastery (10%)
- [x] Phase 1: Deep LangChain Foundations in Context of Agents (20%)
- [x] Phase 2: Tool & Function Calling Mastery (15%)
- [x] Phase 3: Model Context Protocol (MCP) & FastMCP (10%)
- [x] Phase 4: LangGraph State Machines & Workflow Orchestration (30%)
- [x] Phase 5: Streamlit Frontend + Full Integration (10%)
- [ ] Phase 6: Production Polish, Testing & Deployment (5%)

## Key Decisions & Why (Mid-Level — Update as we go)
(We will fill this section after each phase with architecture choices and rationale)

### Phase 0 Backend Foundation Decisions

- We chose a production-oriented FastAPI bootstrap instead of a minimal toy app so the backend starts with clean architecture boundaries.
- Configuration is centralized in a `Settings` class using `pydantic-settings`, so environment variables are validated in one place.
- API routes are separated from app assembly, so `main.py` owns application wiring while `api` owns endpoint definitions.
- Logging and exception handling are grouped under `app/core` as shared infrastructure concerns.
- API versioning is composed centrally at app assembly time using `app.include_router(..., prefix=...)` instead of hardcoding `/api/v1` in every route.
- Hatch packaging was explicitly configured with `packages = ["app"]` because the installable project name is `voyagr` while the Python package directory is `app`.

### Phase 1 LangChain Foundation Decisions

- Prompts are treated as a dedicated architectural layer (`app/prompt_library`) instead of being written inline inside routes or future agent logic.
- Prompt structure and few-shot example data are separated so each has a clear responsibility and can evolve independently.
- Reusable prompt definitions were upgraded from raw strings to LangChain prompt abstractions like `PromptTemplate` and `FewShotPromptTemplate`.
- LCEL-style runnable composition began with a prompt-formatting chain and then expanded into a full `prompt | model | parser` generation pipeline.
- Model construction was placed in a dedicated `app/models` layer so provider-specific setup does not leak into chains or future graph nodes.
- Package-level public interfaces (`__init__.py`) continue to be used consistently across subsystems, even though they require maintenance when new public objects are added.

### Phase 1 Completion Notes

- Prompts, examples, schemas, models, chains, memory, and tools were separated into dedicated layers instead of being mixed together.
- `PromptTemplate` and `FewShotPromptTemplate` were used to turn prompts into reusable components with explicit input contracts.
- LCEL composition was used to build both plain-text and structured-output itinerary pipelines.
- Structured output was introduced with Pydantic schemas so downstream systems can depend on predictable data instead of raw text.
- Memory was modeled as explicit structured state instead of vague hidden context.
- Custom tools were introduced first as local callable capabilities before moving to real external APIs.
- A key recurring lesson was that package-level public interfaces must stay aligned with internal implementation.

### Phase 2 Completion Notes

- Real external tools were introduced in layers: first weather, then discovery/places.
- Tool outputs were normalized behind app-level schemas instead of leaking raw provider payloads into chains.
- Tool failures were standardized with `ToolExecutionError` so workflows can handle provider issues consistently.
- The itinerary workflow was upgraded to use multi-tool enrichment before model invocation.
- Graceful degradation was introduced so useful planning can continue even when some external tools fail.
- Typed success contracts plus standardized failure contracts became the shared pattern for all tools.
- Deterministic multi-tool workflows were used as the bridge before future agentic tool selection and LangGraph orchestration.

### Phase 3 Completion Notes

- FastMCP was added as the framework for exposing MCP capabilities from Voyagr.
- The MCP server was kept separate from FastAPI because the two servers have different roles.
- Existing internal app capabilities were wrapped for MCP exposure instead of duplicating business logic.
- Voyagr now exposes all three major MCP capability types:
  - tools for actions
  - resources for readable context
  - prompts for reusable instruction templates
- `ARCHITECTURE.md` was exposed as an MCP resource to demonstrate readable project context.
- The itinerary prompt was exposed through MCP by reusing the internal prompt layer as the source of truth.
- STDIO-mode MCP behavior was learned as a process-waiting server pattern rather than a normal HTTP startup flow.

### Phase 4 Completion Notes

- LangGraph was introduced as the stateful orchestration layer above tools, chains, and schemas.
- Shared graph state was modeled explicitly with `VoyagrAgentState` instead of relying on implicit flow between steps.
- Workflow steps were split into focused nodes that read shared state and return partial state updates.
- Conditional routing was introduced through dedicated router functions instead of hardcoding every transition directly.
- The graph evolved from a linear flow into a state-driven branching workflow with fallback paths.
- A review stage was added after itinerary generation to demonstrate generate-then-evaluate workflow design.
- A guarded revision loop was introduced using `revision_count` and `max_revisions` to avoid infinite retries.
- Checkpointing was added with `InMemorySaver` so graph state can persist per thread during development.

### Phase 5 Completion Notes

- Streamlit was added as the frontend layer for collecting trip inputs and rendering workflow results.
- The frontend was integrated through FastAPI instead of calling LangGraph directly, preserving a clean backend boundary.
- A dedicated itinerary API endpoint was added so the UI can submit requests and receive full graph results in one response.
- The itinerary schema, prompt, and few-shot examples were upgraded together so the frontend could render a richer travel plan.
- The UI was designed to expose not just the final itinerary, but also weather, places, review status, and raw workflow state.
- Frontend and backend integration now reflects the real Voyagr architecture: Streamlit -> FastAPI -> LangGraph -> tools.


### Free-Tier-First External Service Stack

For Voyagr v1, we are intentionally choosing a free-tier-first stack because this is a personal project and we want to minimize cost while still learning production-style agent architecture.

**Planned service mapping:**
- Weather: **Open-Meteo**
- Maps / Geocoding / Places: **Ola Maps**
- Destination research / activity discovery: **Tavily**
- Flights search: **Amadeus Self-Service APIs**
- Hotels search: **Amadeus Hotel APIs**
- Booking: **No direct booking in v1** — only recommendations and external booking links

**Why this stack:**
- Open-Meteo is simple and free-tier-friendly for itinerary weather planning.
- Ola Maps is preferred over Google Places for v1 because it is more aligned with a free-tier-first personal project approach.
- Tavily is useful for web research, travel discovery, and gathering activity ideas.
- Amadeus gives us one ecosystem for both flights and hotels in a way that is suitable for learning and prototyping.
- Real booking is intentionally excluded from v1 because it adds unnecessary legal, operational, and integration complexity for an early personal project.

**Architectural implication:**
Voyagr should keep the tools layer provider-agnostic so we can swap providers later if pricing, limits, or product requirements change.


## Final Target Folder Structure
(We will build and document this live)
voyagr/
├── app/
│   ├── main.py
│   ├── config/
│   ├── core/
│   ├── agent/
│   ├── tools/
│   ├── prompt_library/
│   └── ...
├── streamlit_app.py
├── pyproject.toml
├── SYSTEM_PROMPT.md
├── ARCHITECTURE.md
└── ...

## Lessons Learned So Far
(You will add one bullet after every phase ends — this becomes your personal knowledge archive)
- A backend can look runnable as plain Python files but still fail at packaging/build time if project structure and build-tool expectations are not explicitly aligned.
- In LangChain-style architecture, prompts, models, and chains should be treated as separate reusable layers so workflows stay composable instead of turning into scattered glue code.
- A production-style LLM system is easier to scale when prompts, models, chains, schemas, memory, and tools are treated as separate reusable layers with stable public interfaces.
- A strong tools layer hides provider-specific mess behind clean typed outputs and standardized failures, which makes multi-tool workflows much easier to compose and debug.
- MCP becomes much more useful when internal tools, resources, and prompts are already cleanly separated, because the MCP layer can then expose them as wrappers instead of becoming a second logic layer.
- LangGraph becomes much easier to reason about when nodes do focused work, routers control transitions, and the shared state explicitly represents the full workflow lifecycle.
- Frontend quality depends heavily on backend contract quality, so richer schemas, stronger prompts, and clearer rendering often need to evolve together instead of being treated as separate layers.


## Edge Cases & Considerations We Will Address
- Long-running agent executions (background tasks)
- Tool error handling & retries
- Streaming responses in Streamlit
- Multi-tenancy / user-specific memory (future)
- Cost & latency optimization with Groq/Ollama