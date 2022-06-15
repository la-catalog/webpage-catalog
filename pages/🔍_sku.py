import json
import os

import streamlit as st
from la_stopwatch import Stopwatch
from meilisearch.client import Client
from page_sku import SKU
from webpage_components import (
    display_attributes,
    display_basic,
    display_images,
    display_measurements,
    display_prices,
    display_rating,
    display_segments,
    display_weight,
    search_bar,
    search_info_bar,
)


def display_result(result: list, stopwatch: Stopwatch) -> None:
    view_mode = search_info_bar(
        results_quantity=result["nbHits"],
        time_spent=f"{stopwatch}",
    )

    for hit in result["hits"]:
        with st.expander(label=hit["name"], expanded=True):
            match view_mode:
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
        for field, value in hit.items():
            if not isinstance(value, (dict, list)):
                display_basic(field=field, value=value)

    with left_col:
        display_images(images=sku.images)
        display_segments(segments=sku.segments)
        display_rating(
            min_value=sku.rating.min,
            max_value=sku.rating.max,
            current_value=sku.rating.current,
        )
        display_measurements(
            main_length=sku.measurement.length,
            main_width=sku.measurement.width,
            main_height=sku.measurement.height,
            main_unit=sku.measurement.unit,
            package_length=sku.package.length,
            package_width=sku.package.width,
            package_height=sku.package.height,
            package_unit=sku.package.unit,
        )
        display_weight(
            main_weight=sku.measurement.weight,
            main_weight_unit=sku.measurement.weight_unit,
            package_weight=sku.package.weight,
            package_weight_unit=sku.package.weight_unit,
        )
        display_prices([(p.value, p.currency) for p in sku.prices])

    display_attributes(
        attributes=[(a.name, a.value) for a in sku.attributes],
        id_=str(sku.id),
    )


st.set_page_config(layout="wide", page_icon="📗")

query, marketplace = search_bar(
    marketplaces=[
        "google_shopping",
        "mercado_livre",
        "rihappy",
    ]
)

client = Client(os.environ["MEILISEARCH_URL"], api_key=os.environ["MEILISEARCH_KEY"])

stopwatch = Stopwatch()
result = client.index(uid=marketplace).search(query=query)

display_result(result, stopwatch.duration())
