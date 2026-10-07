"""
Step 2b: real data flowing into the same switchover pattern.

Same shape as switch_demo.py — one dropdown, one label — but now the
dropdown is populated from real Country values in exports_df, and the
callback computes a real number (total export value for that country)
instead of just echoing the selection back.

Run with:
    python switch_demo_real_data.py
"""

from nicegui import ui
import services.dgcis as dgcis

# Load once, at server startup — same pattern as the full dashboard will use
exports_df = dgcis.get_all_data("export")
countries = sorted(exports_df["Country"].unique().tolist())


def format_currency(value):
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    return f"${value:,.0f}"


@ui.page("/")
def demo_page():
    ui.label("Pick a country:")
    country_select = ui.select(options=countries, value=countries[0])

    result_label = ui.label()

    def on_country_change():
        selected = country_select.value
        # Real computation: total export value across all years for this country
        country_total = exports_df[exports_df["Country"] == selected]["ValueUSD"].sum()
        result_label.set_text(f"{selected} — total exports (all years): {format_currency(country_total)}")

    country_select.on_value_change(on_country_change)
    on_country_change()  # populate the label on first load, not just after a change


ui.run(title="Switch Test — Real Data", port=8083)
