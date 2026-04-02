# Voyagr — Architecture & Learning Plan

## Project Overview (High-Level)
**Voyagr** is a full-stack AI-powered personalized travel itinerary planner.  
Users provide destination, dates, budget, interests, group size, etc. → a LangGraph agent reasons step-by-step, calls real tools (weather, maps, flights, hotels, activities), and generates a complete multi-day trip plan with citations and reasoning.  
Built with FastAPI (backend) + Streamlit (frontend) using modern LangChain + LangGraph patterns.  
Primary learning focus: Deep mastery of LangGraph, tool/function calling, MCP/FastMCP, and production-grade agentic systems.

## Current Phase
Currently in: **Phase 0**

## Phase Progress Tracker
- [x] Phase 0: Project Setup & Architecture Mastery
- [ ] Phase 1: Deep LangChain Foundations in Context of Agents  
- [ ] Phase 2: Tool & Function Calling Mastery  
- [ ] Phase 3: Model Context Protocol (MCP) & FastMCP  
- [ ] Phase 4: LangGraph — The Heart of the Project  
- [ ] Phase 5: Streamlit Frontend + Full Integration  
- [ ] Phase 6: Production Polish, Testing & Deployment  

## Key Decisions & Why (Mid-Level — Update as we go)
(We will fill this section after each phase with architecture choices and rationale)

### Phase 0 Backend Foundation Decisions

- We chose a production-oriented FastAPI bootstrap instead of a minimal toy app so the backend starts with clean architecture boundaries.
- Configuration is centralized in a `Settings` class using `pydantic-settings`, so environment variables are validated in one place.
- API routes are separated from app assembly, so `main.py` owns application wiring while `api` owns endpoint definitions.
- Logging and exception handling are grouped under `app/core` as shared infrastructure concerns.
- API versioning is composed centrally at app assembly time using `app.include_router(..., prefix=...)` instead of hardcoding `/api/v1` in every route.
- Hatch packaging was explicitly configured with `packages = ["app"]` because the installable project name is `voyagr` while the Python package directory is `app`.


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


## Edge Cases & Considerations We Will Address
- Long-running agent executions (background tasks)
- Tool error handling & retries
- Streaming responses in Streamlit
- Multi-tenancy / user-specific memory (future)
- Cost & latency optimization with Groq/Ollama