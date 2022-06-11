import json

import streamlit as st
from page_sku import SKU, Measurement, Rating


def search_result(result: list) -> None:
    hits_col, time_spent_col, view_col = st.columns(3)

    with view_col:
        view = st.radio("view mode", ["default", "json", "code"], horizontal=True)

    with hits_col:
        st.text(f"🔍 hits: {result['nbHits']}")

    with time_spent_col:
        st.text(f"⏱️ time spent: {result['processingTimeMs']}")

    for hit in result["hits"]:
        with st.expander(hit["name"], expanded=True):
            match view:
                case "default":
                    beautiful_hit(hit)
                case "json":
                    st.json(hit)
                case "code":
                    hit = json.dumps(hit, indent=2, ensure_ascii=False)
                    st.code(hit, language="json")


def beautiful_hit(hit: dict) -> None:
    left_col, right_col = st.columns([2, 2])

    with left_col:
        sku = SKU(**hit)
        display_images(sku.images)
        display_segments(sku.segments)
        display_rating(sku.rating)
        display_measurement(sku.measurement)

    with right_col:
        for field, value in hit.items():
            if not isinstance(value, (dict, list)):
                st.caption(body=field)
                st.code(body=value)


def display_images(images: list) -> None:
    if not images:
        return

    index = st.number_input(
        label="Image",
        min_value=0,
        max_value=len(images) - 1,
        step=1,
    )

    st.image(
        image=images[int(index)],
        width=250,
    )


def display_segments(segments: list) -> None:
    if not segments:
        return

    body = "| segments |\n| --- |"

    for s in segments:
        body += f"\n| {s} |"

    st.markdown(body=body)


def display_rating(rating: Rating) -> None:
    if not rating.curent:
        return

    st.slider(
        label="rating",
        min_value=rating.min,
        max_value=rating.max,
        value=rating.curent,
        disabled=True,
    )


def display_measurement(measurement: Measurement) -> None:
    body = ""

    if measurement.length and measurement.unit:
        body += f"🇨: {measurement.length} {measurement.unit}  \n"

    if measurement.width and measurement.unit:
        body += f"🇱: {measurement.width} {measurement.unit}  \n"

    if measurement.height and measurement.unit:
        body += f"🇦: {measurement.height} {measurement.unit}  \n"

    if measurement.weight and measurement.weight_unit:
        body += f"⚖️: {measurement.weight} {measurement.weight_unit}  \n"

    if body:
        st.text(body="")
        st.caption(body=body)
