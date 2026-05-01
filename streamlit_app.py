import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import streamlit as st


st.set_page_config(
    page_title="Voyagr",
    page_icon="V",
    layout="wide",
)


st.markdown(
    """
    <style>
    :root {
        --ink: #17212b;
        --muted: #5e6b76;
        --paper: #f6f1e8;
        --card: #fffdf8;
        --line: #ddd2bf;
        --accent: #d76b39;
        --accent-soft: #f4dfd4;
        --olive: #556b2f;
    }

    .stApp {
        background:
            radial-gradient(circle at top right, rgba(215,107,57,0.10), transparent 24%),
            linear-gradient(180deg, #f9f4ea 0%, #f3ecdf 100%);
    }

    .hero {
        padding: 1.4rem 1.6rem;
        border: 1px solid var(--line);
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(255,253,248,0.96), rgba(244,223,212,0.88));
        box-shadow: 0 16px 40px rgba(23, 33, 43, 0.07);
        margin-bottom: 1rem;
    }

    .hero h1 {
        margin: 0;
        color: var(--ink);
        font-size: 2.4rem;
        letter-spacing: -0.03em;
    }

    .hero p {
        margin: 0.55rem 0 0;
        color: var(--muted);
        font-size: 1rem;
    }

    .section-card {
        padding: 1rem 1.1rem;
        border: 1px solid var(--line);
        border-radius: 18px;
        background: rgba(255, 253, 248, 0.92);
        box-shadow: 0 10px 24px rgba(23, 33, 43, 0.05);
    }

    .day-card {
        padding: 0.9rem 1rem;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: var(--card);
        margin-bottom: 0.8rem;
    }

    .tiny-label {
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.72rem;
        margin-bottom: 0.3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def call_backend(api_base_url: str, payload: dict[str, Any]) -> dict[str, Any]:
    url = f"{api_base_url.rstrip('/')}/itinerary"
    request = Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Backend returned HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach backend: {exc}") from exc


def render_itinerary(itinerary: dict[str, Any]) -> None:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="tiny-label">Itinerary</div>', unsafe_allow_html=True)
    st.subheader(f"{itinerary['destination']} · {itinerary['trip_days']} days")
    st.write(itinerary["overview"])

    top_col1, top_col2 = st.columns(2)
    with top_col1:
        st.markdown("**Budget summary**")
        st.write(itinerary.get("budget_summary", "Not available."))
    with top_col2:
        st.markdown("**Pacing notes**")
        st.write(itinerary.get("pacing_notes", "Not available."))

    tips = itinerary.get("general_tips", [])
    if tips:
        st.markdown("**General tips**")
        for tip in tips:
            st.write(f"- {tip}")

    def render_activity_block(title: str, activities: list[dict[str, Any]]) -> None:
        st.markdown(f"**{title}**")
        if not activities:
            st.write("- No activities listed.")
            return

        for item in activities:
            st.markdown(
                f"- **{item['time_slot']} · {item['name']}**"
                f"  \n  {item['details']}"
                f"  \n  Cost: {item['estimated_cost']}"
                f"  \n  Weather fit: {item['weather_fit']}"
            )

    for day in itinerary.get("days", []):
        st.markdown('<div class="day-card">', unsafe_allow_html=True)
        st.markdown(f"### Day {day['day']}: {day['title']}")
        st.caption(f"Area focus: {day.get('area', 'Not specified')}")

        col1, col2, col3 = st.columns(3)
        with col1:
            render_activity_block("Morning", day.get("morning", []))
        with col2:
            render_activity_block("Afternoon", day.get("afternoon", []))
        with col3:
            render_activity_block("Evening", day.get("evening", []))

        meta_col1, meta_col2, meta_col3 = st.columns(3)
        with meta_col1:
            st.markdown("**Food recommendation**")
            st.write(day.get("food_recommendation", "Not available."))
        with meta_col2:
            st.markdown("**Transport tip**")
            st.write(day.get("transport_tip", "Not available."))
        with meta_col3:
            st.markdown("**Daily budget estimate**")
            st.write(day.get("daily_budget_estimate", "Not available."))

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_weather(weather: dict[str, Any] | None) -> None:
    if not weather:
        st.info("No weather data available.")
        return

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="tiny-label">Weather</div>', unsafe_allow_html=True)
    st.write(f"**{weather['destination']}, {weather.get('country') or 'Unknown'}**")
    rows = []
    for day in weather.get("forecast_days", []):
        rows.append(
            {
                "date": day["date"],
                "weather": day["weather"],
                "min_c": day["temperature_min_c"],
                "max_c": day["temperature_max_c"],
                "precip_mm": day["precipitation_mm"],
            }
        )
    st.dataframe(rows, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_places(places: dict[str, Any] | None) -> None:
    if not places:
        st.info("No place discovery data available.")
        return

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="tiny-label">Places</div>', unsafe_allow_html=True)
    if places.get("answer"):
        st.write(places["answer"])

    for item in places.get("results", []):
        st.markdown(f"**[{item['title']}]({item['url']})**")
        st.write(item["summary"])
        if item.get("score") is not None:
            st.caption(f"Score: {item['score']}")
        st.divider()

    st.markdown("</div>", unsafe_allow_html=True)


def render_review(result: dict[str, Any]) -> None:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="tiny-label">Review</div>', unsafe_allow_html=True)

    st.write(f"**Status:** {result.get('review_status') or 'unknown'}")
    st.write(f"**Revision count:** {result.get('revision_count', 0)}")

    for note in result.get("review_notes", []):
        st.write(f"- {note}")

    if result.get("errors"):
        st.warning("Workflow errors were recorded:")
        for error in result["errors"]:
            st.write(f"- {error}")

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    """
    <div class="hero">
        <h1>Voyagr</h1>
        <p>AI-powered trip planning with LangGraph orchestration, real weather, place discovery, review, and revision-aware workflows.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Connection")
    api_base_url = st.text_input(
        "FastAPI base URL",
        value="http://localhost:8000/api/v1",
        help="The Streamlit app posts trip requests to this backend.",
    )

st.subheader("Plan a trip")

with st.form("trip_form"):
    col1, col2 = st.columns(2)

    with col1:
        destination = st.text_input("Destination", value="Paris")
        trip_days = st.slider("Trip days", min_value=1, max_value=14, value=3)
        budget = st.selectbox("Budget", ["low", "medium", "high"], index=1)
        group_size = st.number_input("Group size", min_value=1, max_value=20, value=2)

    with col2:
        interests = st.text_input("Interests", value="museums, cafes, walking")
        max_revisions = st.slider("Max revisions", min_value=0, max_value=3, value=1)
        notes = st.text_area(
            "Notes",
            value="avoid rushing between places",
            height=120,
        )

    submitted = st.form_submit_button("Generate itinerary", use_container_width=True)

if submitted:
    payload = {
        "request": {
            "destination": destination,
            "trip_days": trip_days,
            "budget": budget,
            "interests": interests,
            "group_size": int(group_size),
            "notes": notes,
        },
        "max_revisions": max_revisions,
    }

    try:
        with st.spinner("Running the travel workflow..."):
            st.session_state["voyagr_response"] = call_backend(api_base_url, payload)
        st.success("Trip generated successfully.")
    except Exception as exc:
        st.error(str(exc))

response = st.session_state.get("voyagr_response")
if response:
    result = response["result"]

    st.caption(f"Thread ID: {response['thread_id']}")

    itinerary_tab, weather_tab, places_tab, review_tab, raw_tab = st.tabs(
        ["Itinerary", "Weather", "Places", "Review", "Raw state"]
    )

    with itinerary_tab:
        itinerary = result.get("itinerary")
        if itinerary:
            render_itinerary(itinerary)
        else:
            st.warning("No itinerary was returned.")

    with weather_tab:
        render_weather(result.get("weather"))

    with places_tab:
        render_places(result.get("places"))

    with review_tab:
        render_review(result)

    with raw_tab:
        st.json(response)
