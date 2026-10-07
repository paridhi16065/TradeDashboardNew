from nicegui import ui

countries = ["Kenya", "USA", "UAE", "Brazil"]

@ui.page("/")
def demo_page():
    ui.label("Pick a country:")
    country_select = ui.select(options=countries, value=countries[0])

    result_label = ui.label(f"Selected: {country_select.value}")

    def on_country_change():
        result_label.set_text(f"Selected: {country_select.value}")

    country_select.on_value_change(on_country_change)


ui.run(title="Switch Test", port=8082)