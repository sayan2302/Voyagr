# Voyagr — Architecture & Learning Plan

## Project Overview (High-Level)
**Voyagr** is a full-stack AI-powered personalized travel itinerary planner.  
Users provide destination, dates, budget, interests, group size, etc. → a LangGraph agent reasons step-by-step, calls real tools (weather, maps, flights, hotels, activities), and generates a complete multi-day trip plan with citations and reasoning.  
Built with FastAPI (backend) + Streamlit (frontend) using modern LangChain + LangGraph patterns.  
Primary learning focus: Deep mastery of LangGraph, tool/function calling, MCP/FastMCP, and production-grade agentic systems.

## Current Phase
Currently in: **Phase 0**

## Phase Progress Tracker
- [ ] Phase 0: Project Setup & Architecture Mastery  
- [ ] Phase 1: Deep LangChain Foundations in Context of Agents  
- [ ] Phase 2: Tool & Function Calling Mastery  
- [ ] Phase 3: Model Context Protocol (MCP) & FastMCP  
- [ ] Phase 4: LangGraph — The Heart of the Project  
- [ ] Phase 5: Streamlit Frontend + Full Integration  
- [ ] Phase 6: Production Polish, Testing & Deployment  

## Key Decisions & Why (Mid-Level — Update as we go)
(We will fill this section after each phase with architecture choices and rationale)

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

## Edge Cases & Considerations We Will Address
- Long-running agent executions (background tasks)
- Tool error handling & retries
- Streaming responses in Streamlit
- Multi-tenancy / user-specific memory (future)
- Cost & latency optimization with Groq/Ollama