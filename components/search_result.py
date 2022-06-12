import json

import pandas as pd
import streamlit as st
from page_sku import SKU, Attribute, Measurement, Price, Rating

from utility import stringfy


def search_result(result: list) -> None:
    hits_col, time_spent_col, view_col = st.columns(3)

    with view_col:
        view = st.radio("view mode", ["default", "json", "code"], horizontal=True)

    with hits_col:
        st.text(f"🔍 hits: {result['nbHits']}")

    with time_spent_col:
        st.text(f"⏱️ time spent: {result['processingTimeMs']}")

    for hit in result["hits"]:
        with st.expander(label=hit["name"], expanded=True):
            match view:
                case "default":
                    beautiful_hit(hit)
                case "json":
                    st.json(hit)
                case "code":
                    hit = json.dumps(hit, indent=2, ensure_ascii=False)
                    st.code(hit, language="json")


def beautiful_hit(hit: dict) -> None:
    sku = SKU(**hit)
    left_col, right_col = st.columns([2, 2])

    with right_col:
        display_basic(hit)

    with left_col:
        display_images(images=sku.images)
        display_segments(segments=sku.segments)
        display_rating(rating=sku.rating)
        display_measurement(measurement=sku.measurement, package=sku.package)
        display_weight(measurement=sku.measurement, package=sku.package)
        display_price(prices=sku.prices)

    display_attributes(attributes=sku.attributes, id_=str(sku.id))


def display_basic(hit: dict):
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
    if segments:
        dataframe = pd.DataFrame(data=segments, columns=["segments"])
        st.table(data=dataframe)


def display_rating(rating: Rating) -> None:
    if rating.curent:
        st.slider(
            label="rating",
            min_value=rating.min,
            max_value=rating.max,
            value=rating.curent,
            disabled=True,
        )


def display_measurement(measurement: Measurement, package: Measurement) -> None:
    dataframe = pd.DataFrame(
        data=[
            [
                stringfy(measurement.length),
                stringfy(measurement.width),
                stringfy(measurement.height),
                stringfy(measurement.unit),
            ],
            [
                stringfy(package.length),
                stringfy(package.width),
                stringfy(package.height),
                stringfy(package.unit),
            ],
        ],
        index=["⚽", "📦"],
        columns=["🇨", "🇱", "🇦", "📐"],
    )

    st.table(data=dataframe)


def display_weight(measurement: Measurement, package: Measurement) -> None:
    dataframe = pd.DataFrame(
        data=[
            [
                stringfy(measurement.weight),
                stringfy(measurement.weight_unit),
            ],
            [
                stringfy(package.weight),
                stringfy(package.weight_unit),
            ],
        ],
        index=["⚽", "📦"],
        columns=["🇵", "⚖️"],
    )

    st.table(data=dataframe)


def display_price(prices: list[Price]) -> None:
    dataframe = pd.DataFrame(
        data=[stringfy(p.amount) for p in prices],
        columns=["💲"],
        index=[p.currency for p in prices],
    )
    st.table(data=dataframe)


def display_attributes(attributes: list[Attribute], id_: str) -> None:
    if st.checkbox(label="👁️ attributes", key=f"{id_}_attributes"):
        dataframe = pd.DataFrame(
            data={
                "name": [a.name for a in attributes],
                "value": [a.value for a in attributes],
            }
        )
        st.table(data=dataframe)
