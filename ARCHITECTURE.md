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
- [ ] Phase 2: Tool & Function Calling Mastery (15%)
- [ ] Phase 3: Model Context Protocol (MCP) & FastMCP (10%)
- [ ] Phase 4: LangGraph — The Heart of the Project (30%)
- [ ] Phase 5: Streamlit Frontend + Full Integration (10%)
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


## Edge Cases & Considerations We Will Address
- Long-running agent executions (background tasks)
- Tool error handling & retries
- Streaming responses in Streamlit
- Multi-tenancy / user-specific memory (future)
- Cost & latency optimization with Groq/Ollama