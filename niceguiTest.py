# 
"""
Country Profile page — NiceGUI prototype, placeholder data.

Run with:
    pip install nicegui
    python country_profile_prototype.py

Opens in your browser automatically. This is a look-and-feel test, not
wired to real data yet — swap the placeholder values for calls into
services/dgcis.py / services/country_profile.py once the layout feels right.
"""

from nicegui import ui

# Theme — same navy/ice/gold used across the presentation decks
NAVY = "#1E2761"
ICE = "#CADCFC"
GOLD = "#D4A94C"
SLATE = "#5A6B8C"

ui.colors(primary=NAVY, secondary=ICE, accent=GOLD)

# --- Placeholder data (stand-in for Kenya, swap for real fetch later) ---
country = {
    "name": "Kenya",
    "flag": "🇰🇪",
    "capital": "Nairobi",
    "region": "Eastern Africa",
    "iso": "KE",
    "gdp": "$118B",
    "population": "55.1M",
    "income_group": "Lower-middle",
    "trade_balance": "+$0.4B",
    "ldc_status": "LDC status",
    "memberships": ["WTO", "UN", "AU", "COMESA", "IORA", "+6 more"],
    "diplomatic_since": "1963",
    "borders": ["Tanzania", "Uganda", "Ethiopia", "+3"],
}

trend_years = ["FY21-22", "FY22-23", "FY23-24", "FY24-25", "FY25-26"]
trend_values = [0.8, 1.0, 0.9, 1.2, 1.4]  # placeholder trade values, $B


def stat_card(label: str, value: str, accent: bool = False):
    with ui.card().classes("flex-1 min-w-[140px] shadow-sm"):
        ui.label(label).classes("text-xs text-gray-500")
        ui.label(value).classes(
            f"text-2xl font-semibold {'text-green-600' if accent else ''}"
        )


def badge_row(items: list[str]):
    with ui.row().classes("gap-2 flex-wrap"):
        for i, item in enumerate(items):
            (ui.badge(item, color="primary") if i == 0 else ui.badge(item, color="grey-3").props("text-color=grey-8"))


@ui.page("/")
def country_profile_page():
    ui.query("body").classes("bg-gray-50")

    with ui.column().classes("w-full max-w-5xl mx-auto p-6 gap-4"):

        # --- Header ---
        with ui.row().classes("items-center gap-4"):
            with ui.element("div").classes(
                "w-14 h-14 rounded-lg flex items-center justify-center text-3xl"
            ).style(f"background-color: {ICE}"):
                ui.label(country["flag"])
            with ui.column().classes("gap-0 flex-1"):
                ui.label(country["name"]).classes("text-2xl font-bold")
                ui.label(f"{country['capital']} · {country['region']} · ISO {country['iso']}").classes(
                    "text-sm text-gray-500"
                )
            ui.badge(country["ldc_status"], color="amber-3").props("text-color=amber-9").classes("px-3 py-1")

        # --- Stat cards row ---
        with ui.row().classes("w-full gap-3"):
            stat_card("GDP", country["gdp"])
            stat_card("Population", country["population"])
            stat_card("Income Group", country["income_group"])
            stat_card("India Trade Balance", country["trade_balance"], accent=True)

        # --- Membership panel ---
        with ui.card().classes("w-full shadow-sm"):
            ui.label("Multilateral Memberships").classes("text-xs text-gray-500 mb-2")
            badge_row(country["memberships"])

        # --- Trend chart ---
        with ui.card().classes("w-full shadow-sm"):
            ui.label("Bilateral Trade Trend").classes("text-xs text-gray-500 mb-2")
            ui.echart(
                {
                    "xAxis": {"type": "category", "data": trend_years},
                    "yAxis": {"type": "value", "axisLabel": {"formatter": "${value}B"}},
                    "series": [
                        {
                            "data": trend_values,
                            "type": "line",
                            "smooth": True,
                            "areaStyle": {
                                "color": {
                                    "type": "linear",
                                    "x": 0, "y": 0, "x2": 0, "y2": 1,
                                    "colorStops": [
                                        {"offset": 0, "color": "rgba(30,39,97,0.45)"},
                                        {"offset": 1, "color": "rgba(30,39,97,0.02)"},
                                    ],
                                }
                            },
                            "lineStyle": {"color": NAVY, "width": 3},
                            "itemStyle": {"color": NAVY},
                        }
                    ],
                    "grid": {"left": 50, "right": 20, "top": 20, "bottom": 30},
                }
            ).classes("w-full h-64")

        # --- Two-column info panels ---
        with ui.row().classes("w-full gap-3"):
            with ui.card().classes("flex-1 shadow-sm"):
                ui.label("India Relations").classes("text-xs text-gray-500 mb-1")
                ui.label(f"Diplomatic ties since {country['diplomatic_since']}").classes(
                    "text-base font-medium"
                )
            with ui.card().classes("flex-1 shadow-sm"):
                ui.label("Borders").classes("text-xs text-gray-500 mb-1")
                ui.label(", ".join(country["borders"])).classes("text-base font-medium")


ui.run(title="Country Profile — Prototype", port=8081)