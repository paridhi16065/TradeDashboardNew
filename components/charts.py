import plotly.express as px

from utils.theme import CHART_SEQUENCE, NAVY, FONT_BODY, FONT_HEAD, TEXT, GRIDLINE


def apply_chart_style(fig, value_axis="y", currency=True, show_legend=None, smooth_line=False):
    """Shared polish pass — call at the end of every chart function so
    every chart in the app stays visually consistent. One place to
    change fonts/colors/spacing instead of fixing each chart separately.

    value_axis: "y" for vertical bars/lines (value on y-axis), "x" for
    horizontal bars (value on x-axis) — controls which axis gets the
    gridline + currency formatting.

    smooth_line: for single-series line charts — applies the smooth
    curve + gradient area-fill look (matching the mockup), and forces
    the navy brand color directly onto the trace. Plotly Express
    assigns its own default trace color at creation time, and setting
    `colorway` on the layout afterward does NOT retroactively override
    an already-colored trace — that's why charts were showing Plotly's
    default blue-purple instead of navy. Setting line_color/marker_color
    directly on the trace, as done below, is what actually fixes it.
    """
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",  # transparent — blends into the dark app background
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_BODY, size=13, color=TEXT),
        title_font=dict(family=FONT_HEAD, size=18, color=TEXT),
        margin=dict(l=10, r=20, t=60, b=40),
        height=420,
        colorway=CHART_SEQUENCE,
    )
    if show_legend is not None:
        fig.update_layout(showlegend=show_legend)

    fig.update_xaxes(
        showgrid=(value_axis == "x"), gridcolor=GRIDLINE, color=TEXT,  zeroline = False
    )
    fig.update_yaxes(
        showgrid=(value_axis == "y"), gridcolor=GRIDLINE, color=TEXT, zeroline=False
    )
    if currency:
        if value_axis == "x":
            fig.update_xaxes(tickprefix="$", tickformat="~s")
        else:
            fig.update_yaxes(tickprefix="$", tickformat="~s")

    fig.update_traces(marker=dict(cornerradius=8), selector=dict(type="bar"))

    if smooth_line:
        fig.update_traces(
            selector=dict(type="scatter"),
            mode="lines+markers",
            line=dict(color=NAVY, width=3, shape="spline", smoothing=0.6),
            marker=dict(color="white", size=7, line=dict(color=NAVY, width=2)),
            fill="tozeroy",
            fillgradient=dict(
                type="vertical",
                colorscale=[
                    (0.0, "rgba(30,39,97,0.02)"),
                    (1.0, "rgba(30,39,97,0.30)"),
                ],
            ),
        )

    return fig


def commodity_bar_chart(df):
    commodities = (
        df.groupby("cmdDesc")["primaryValue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig = px.bar(
        commodities,
        x="primaryValue",
        y="cmdDesc",
        orientation="h",
        title="Top 10 Traded Commodities",
        text_auto=".2s",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    fig.update_traces(textposition="outside")
    return apply_chart_style(fig, value_axis="x")


def partner_bar_chart(df):
    fig = px.bar(
        df,
        x="TradeValue",
        y="Partner",
        orientation="h",
        title="Top Trade Partners",
        text_auto=".2s",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    fig.update_traces(textposition="outside")
    return apply_chart_style(fig, value_axis="x")


def trade_trend_chart(df):
    yearly = df.groupby("period")["primaryValue"].sum().reset_index()
    fig = px.line(yearly, x="period", y="primaryValue", markers=True, title="Trade Trend Over Time")
    return apply_chart_style(fig, value_axis="y", show_legend=False, smooth_line=True)


def dgcis_commodity_chart(df):
    fig = px.bar(
        df, x="ValueUSD", y="Commodity", orientation="h", title="Top 10 Commodities",
        text_auto=".2s",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    fig.update_traces(textposition="outside")
    return apply_chart_style(fig, value_axis="x")


def dgcis_country_chart(df):
    fig = px.bar(
        df, x="ValueUSD", y="Country", orientation="h", title="Top 10 Countries",
        text_auto=".2s",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    fig.update_traces(textposition="outside")
    return apply_chart_style(fig, value_axis="x")


def dgcis_trend_chart(fy_totals_df, flow_label):
    fig = px.line(
        fy_totals_df, x="financial_year", y="ValueUSD", markers=True,
        title=f"{flow_label} by Financial Year",
    )
    # Single series — legend is pure clutter here. No reference line —
    # it visually clashed with the new gradient fill; can add back as
    # a thin dashed line later if you still want the multi-year average.
    return apply_chart_style(fig, value_axis="y", show_legend=False, smooth_line=True)