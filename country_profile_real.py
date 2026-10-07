"""
Country profile page — real trade data, styled like the Kenya mockup.

Note: the GDP/population/membership fields from the original mockup
came from World Bank/Wikidata, which aren't wired in yet — that's the
separate Module 1 data layer. This version shows real trade stats
(from your actual dgcis data) in the same card style, with the
not-yet-built fields clearly marked as placeholders, not faked.

Run with:
    python country_profile_real.py
"""

from nicegui import ui
import services.dgcis as dgcis
from components.charts import dgcis_trend_chart
from utils.theme import NAVY, ICE, GOLD

exports_df = dgcis.get_all_data("export")
imports_df = dgcis.get_all_data("import")
countries = sorted(exports_df["Country"].unique().tolist())


def format_currency(value):
    if value is None:
        return "N/A"
    abs_value = abs(value)
    sign = "-" if value < 0 else ""
    if abs_value >= 1_000_000_000:
        return f"{sign}${abs_value / 1_000_000_000:.2f}B"
    if abs_value >= 1_000_000:
        return f"{sign}${abs_value / 1_000_000:.2f}M"
    return f"{sign}${abs_value:,.0f}"


@ui.page("/")
def profile_page():
    ui.colors(primary=NAVY, secondary=ICE, accent=GOLD)
    ui.query("body").classes("bg-gray-50")

    with ui.column().classes("w-full max-w-4xl mx-auto p-6 gap-4"):
        with ui.row().classes("items-center gap-4"):
            ui.label("Country Profile").classes("text-2xl font-bold")
            country_select = ui.select(options=countries, value=countries[0]).classes("min-w-[220px]")

        results_area = ui.column().classes("w-full gap-4")

        def refresh():
            results_area.clear()
            selected = country_select.value

            country_exports = exports_df[exports_df["Country"] == selected]
            country_imports = imports_df[imports_df["Country"] == selected]

            total_exports = country_exports["ValueUSD"].sum()
            total_imports = country_imports["ValueUSD"].sum()
            trade_balance = total_exports - total_imports

            top_commodity_row = (
                country_exports.groupby("Commodity")["ValueUSD"].sum().sort_values(ascending=False)
            )
            top_commodity = top_commodity_row.index[0] if len(top_commodity_row) else "N/A"

            with results_area:
                # --- Header ---
                with ui.row().classes("items-center gap-4"):
                    with ui.element("div").classes(
                        "w-14 h-14 rounded-lg flex items-center justify-center text-2xl font-bold"
                    ).style(f"background-color: {ICE}; color: {NAVY}"):
                        ui.label(selected[:2].upper())
                    with ui.column().classes("gap-0 flex-1"):
                        ui.label(selected).classes("text-2xl font-bold")
                        ui.label("India trade profile (all years in dataset)").classes(
                            "text-sm text-gray-500"
                        )

                # --- Stat cards: real trade data ---
                with ui.row().classes("w-full gap-3"):
                    def stat_card(label, value, accent=False):
                        with ui.card().classes("flex-1 min-w-[160px] shadow-sm"):
                            ui.label(label).classes("text-xs text-gray-500")
                            ui.label(value).classes(
                                f"text-2xl font-semibold {'text-green-600' if accent and trade_balance >= 0 else 'text-red-600' if accent else ''}"
                            )

                    stat_card("Total Exports", format_currency(total_exports))
                    stat_card("Total Imports", format_currency(total_imports))
                    stat_card("Trade Balance", format_currency(trade_balance), accent=True)
                    stat_card("Top Export Commodity", top_commodity)

                # --- Trend chart: real data, existing chart function reused as-is ---
                with ui.card().classes("w-full shadow-sm"):
                    ui.label(f"Export Trend by Financial Year — {selected}").classes(
                        "text-sm font-medium mb-2"
                    )
                    fy_totals = dgcis.get_fy_totals(country_exports)
                    ui.plotly(dgcis_trend_chart(fy_totals, "Export")).classes("w-full")

                # --- Not-yet-built fields — honestly marked, not faked ---
                with ui.card().classes(
                    "w-full shadow-sm border-2 border-dashed"
                ).style(f"border-color: {ICE}"):
                    ui.label("Country Profile (Module 1) — coming soon").classes(
                        "text-xs text-gray-500 mb-1"
                    )
                    ui.label(
                        "GDP, population, income classification, multilateral memberships, "
                        "and diplomatic relations will appear here once the World Bank / "
                        "Wikidata data layer is wired in."
                    ).classes("text-sm text-gray-400 italic")

        country_select.on_value_change(refresh)
        refresh()


ui.run(title="Country Profile", port=8084)
