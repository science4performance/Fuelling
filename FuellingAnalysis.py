# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "matplotlib==3.11.1",
#     "openai==2.50.0",
#     "pandas==3.0.5",
#     "plotly==6.9.0",
# ]
# ///

import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    pass


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $Power=WorkDone/Time=Energy/Time=Joules/second=Watts=kcals/day=carbs/hour$
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # How many carbs?
    A fascinating recent item on <a href="https://escapecollective.com/the-number-that-may-define-the-limits-of-human-endurance/?gift-token=YhDxW3xX&ref=Gift">Escape Collective</a> explores the limits of human endurance in terms of energy expenditure expressed as multiples of Basal Metabolic Rate (BMR). This article explores the significance of fuelling strategies relative to energy expenditure for professional and competitive cyclists. We begin by defining BMR, which is minimum number of calories your body burns at rest for basic functions like breathing, circulation and cell production. This sets a reference for considering the magnitude of energy required for high level endurance performance. How much benefit is provided by the modern trend of consuming up to 100 g or 120 g per hour of carbohydrates during the activity?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Staying Alive - Basal Metabolic Rate (BRM)
    Even at rest, the body burns a certain amount of energy to maintain basic metabolism in order to stay alive. This is principally determined by the cells that make up Fat Free Mass, defined as Total Body Mass minus Total Body Fat. A DEXA scan is the gold standard for measuring % body fat, though other methods such as impedence scales give an estimate. The term Lean Body Mass is often used interchangeably with Fat Free Mass, though the strict definition of Lean Body Mass excludes the skeleton, which is metabolically active, as bone is continually formed and resorbed.<br>
    Since the accurate measurement of BMR requires laboratory conditions, a number of formulae have been devised to estimate it. If you know your % body fat, you can use the <a href="https://books.google.co.uk/books/about/Exercise_Physiology.html?id=mwLsEAAAQBAJ&redir_esc=y">Katch-McArdle Formula (1996)</a>, otherwise the <a href="https://www.sciencedirect.com/science/article/abs/pii/S0002916523166986?via%3Dihub">Mifflin-St Jeor Equation (1990)</a> effectively estimates lean body mass from height, weight, age and sex.<br>
    ### Mifflin-St Jeor Equation
    Men:<br>
    $BMR = (10 \times \text{weight in kg}) + (6.25 \times \text{height in cm}) - (5 \times \text{age in years}) + 5$<br>
    Women:<br>
    $BMR = (10 \times \text{weight in kg}) + (6.25 \times \text{height in cm}) - (5 \times \text{age in years}) - 161$
    ### Katch-McArdle Formula (only based on lean body mass)
    Men and Women:<br>
    $BMR = 370 + (21.6 \times \text{LBM})$<br>
    $\text{LBM} = \text{Weight in kg} \times \left(1 - \frac{\text{Body Fat \%}}{100}\right)$
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    import plotly.graph_objects as go
    import pandas as pd
    from plotly.subplots import make_subplots
    JOULES_TO_KCALS = 0.0002390057
    EFFICIENCY = 0.22


    weight = mo.ui.slider(40, 120, value=70, step=1, label="Weight (kg)")
    height = mo.ui.slider(140, 220, value=175, step=1, label="Height (cm)")
    age = mo.ui.slider(10, 90, value=30, step=1, label="Age (years)",)
    sex = mo.ui.dropdown(["Male", "Female"], value="Male", label="Sex")
    body_fat = mo.ui.slider(0, 40, value=15, step=1, label="Body fat (%)")

    controls = mo.vstack(
        [sex, height, weight, age, body_fat],
        justify="space-between",
        align="center",
    )
    return (
        EFFICIENCY,
        JOULES_TO_KCALS,
        age,
        body_fat,
        controls,
        go,
        height,
        make_subplots,
        pd,
        sex,
        weight,
    )


@app.cell
def _(JOULES_TO_KCALS, age, body_fat, go, height, mo, sex, weight):
    def BMR2Wattsperkg(BMR, weight_kg):
        return BMR/24/60/60/JOULES_TO_KCALS/weight_kg

    def calculate_katch_mcardle(weight_kg,body_fat_pct):
        lbm = weight_kg * (1 - body_fat_pct / 100)
        return 370 + 21.6 * lbm, lbm

    def calculate_mifflin_st_jeor(weight_kg, height_cm, age_years, sex_value):
        if sex_value == "Male":
            return 10 * weight_kg + 6.25 * height_cm - 5 * age_years + 5
        else:
            return 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 161


    def calculate_bmr(weight_kg, height_cm, age_years, sex_value, body_fat_pct):
        mifflin_st_jeor = calculate_mifflin_st_jeor(weight_kg, height_cm, age_years, sex_value)
        katch_mcardle, lbm = calculate_katch_mcardle(weight_kg,body_fat_pct)
        return mifflin_st_jeor, katch_mcardle, lbm

    mifflin_st_jeor, katch_mcardle, lbm = calculate_bmr(
        weight.value,
        height.value,
        age.value,
        sex.value,
        body_fat.value,
    )

    summary = mo.md(
        f"""
        **Estimated BMR**
        - Mifflin-St Jeor: {mifflin_st_jeor:.0f} kcal/day
        - Katch-McArdle: {katch_mcardle:.0f} kcal/day
        - Lean body mass: {lbm:.1f} kg
        """
    )

    fig = go.Figure(
        data=[
            go.Bar(
                y=["Katch-McArdle<br>Lean body mass only", "Mifflin-St Jeor<br>Sex,height,weight,age"],
                x=[katch_mcardle, mifflin_st_jeor],
                orientation="h",
                marker_color=["#f58518", "#4c78a8"],
                text=[f"{katch_mcardle:.0f}kcals/day or {BMR2Wattsperkg(katch_mcardle,weight.value)*weight.value:.0f} Watts or {BMR2Wattsperkg(katch_mcardle,weight.value):.1f} Watts/kg", 
                      f"{mifflin_st_jeor:.0f}kcals/day or {BMR2Wattsperkg(mifflin_st_jeor,weight.value)*weight.value:.0f} Watts or {BMR2Wattsperkg(mifflin_st_jeor,weight.value):.1f} Watts/kg"],
                textposition="outside",
            )
        ]
    )
    fig.update_layout(
        title="BMR estimate comparison",
        xaxis_title="Estimated BMR (kcal/day)",
        xaxis=dict(range=[0, 3000]),
        template="plotly_white",
        margin=dict(t=40, b=20, l=20, r=20),
        height=360,
    )
    return (calculate_katch_mcardle,)


@app.cell
def _(controls):
    controls
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can estimate your Basal Metabolic Rate using the sliders. If you don't know your % body fat, you can obtain an estimate by entering the other inputs and then adjusting the Body Fat slider until the two bars match. Some researchers prefer to use an equation devised by  <a href="https://www.sciencedirect.com/science/article/pii/S0002822396000107#BIB2">Cunningham (1980)</a> for endurance athletes. This model is very similar to Katch McArdle, but systematically predicts BMR about 130 kcal (5%-10%) higher. After accounting for their lower percentage body fat, highly trained individuals tend to have a greater concentration of miochondria in the muscles and enlarged metabolically active organs, such as the heart, explaining a more elevated BMR.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    At 1,800 <span title="1 kcal is 1000 calories or a Calorie with capital C" style="border-bottom: 1px dashed #666; cursor: help;">kcal</span> per day (75 kcal per hour), the BMR of an average male equates to 87 Watts (a little over 1 Watt/kg of total body mass). This power is similar to an incandescent lightbulb or about the same as charging a laptop. The brain uses about 20% of BMR, somewhat less than 20 Watts. The fact that AI companies are hooking up with power stations to provide the gigaWatts required to run massive data centres shows that AI researchers have a long, long way to go before they come anywhere close to matching the efficiency of natural intelligence.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Watts occurring?
    The mention of Watts usually catches the attention of any serious cyclists in the room. The speed at which a rider completes any route, from a lap of the local park to the Tour de France, comes down to the power that can be sustained from start to completion. This is often expressed in terms of a <a href="https://science4performance.com/2018/05/11/strava-power-curve/">Power Curve</a>, which plots the maximum power against time. A 2022 <a href="https://velo2max.com/wp-content/uploads/2024/08/ijspp-article-p701.pdf">study by Valenzuela</a> analysed the power files of 98 world tour and 46 professional tour male cyclists, analysing efforts up to 4 hours. The following charts show the results expressed in terms of absolute Watts and as Watts/kg versus time, using a log-log scale.
    """)
    return


@app.cell
def _(EFFICIENCY, JOULES_TO_KCALS, go, make_subplots, pd):

    # 1. Dataset from Table 1
    data = [
        [1111, 17.29, 1218, 18.22, 1393, 21.08, 1623, 23.26, 1797, 24.65],  # 1 s
        [995, 15.71, 1091, 16.59, 1202, 17.99, 1344, 19.78, 1529, 20.83],  # 5 s
        [913, 14.28, 991, 15.24, 1113, 16.59, 1240, 17.92, 1385, 18.90],  # 10 s
        [707, 10.88, 766, 11.71, 831, 12.62, 947, 13.36, 1040, 14.15],  # 30 s
        [580, 8.87, 617, 9.51, 677, 10.10, 744, 10.74, 820, 11.33],  # 60 s
        [432, 6.52, 450, 6.75, 472, 7.06, 503, 7.34, 531, 7.65],  # 300 s
        [399, 5.92, 414, 6.19, 435, 6.45, 455, 6.77, 481, 7.00],  # 600 s
        [369, 5.47, 387, 5.79, 403, 6.03, 426, 6.29, 453, 6.59],  # 1200 s
        [347, 5.10, 361, 5.36, 384, 5.71, 406, 6.02, 427, 6.24],  # 1800 s
        [310, 4.71, 329, 4.91, 350, 5.15, 368, 5.47, 398, 5.76],  # 3600 s
        [282, 4.23, 296, 4.47, 312, 4.70, 330, 4.91, 355, 5.12],  # 7200 s
        [266, 4.00, 281, 4.27, 297, 4.45, 315, 4.64, 338, 4.84],  # 10800 s
        [252, 3.83, 268, 4.03, 284, 4.24, 298, 4.42, 325, 4.63],  # 14400 s
    ]

    time_seconds = [
        1,
        5,
        10,
        30,
        60,
        300,
        600,
        1200,
        1800,
        3600,
        7200,
        10800,
        14400,
    ]
    time_labels = [
        "1s",
        "5s",
        "10s",
        "30s",
        "1m",
        "5m",
        "10m",
        "20m",
        "30m",
        "1h",
        "2h",
        "3h",
        "4h",
    ]
    percentiles = ["P10", "P25", "P50", "P75", "P90"]

    columns = pd.MultiIndex.from_product(
        [percentiles, ["W", "W_kg"]],
        names=["percentile", "unit"],
    )

    df = pd.DataFrame(data, index=time_seconds, columns=columns)
    df.index.name = "time_seconds"



    # Loop through each percentile and assign the new tuple key (percentile, 'kcals')
    for p in percentiles:
        df[(p, "kcals")] = (df[(p, "W")] * df.index * JOULES_TO_KCALS) / EFFICIENCY


    # 2. Setup Plotly Subplots
    fig1 = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Absolute Power (W) vs Duration",
            "Relative Power (W/kg) vs Duration",
        ),
        horizontal_spacing=0.08,
    )

    colors = {
        "P10": "#1f77b4",
        "P25": "#ff7f0e",
        "P50": "#2ca02c",
        "P75": "#d62728",
        "P90": "#9467bd",
    }

    for p in percentiles:
        # Subplot 1: Absolute Power (Watts)
        fig1.add_trace(
            go.Scatter(
                x=df.index,
                y=df[(p, "W")],
                mode="lines+markers",
                name=p,
                legendgroup=p,
                line=dict(color=colors[p], width=2),
                marker=dict(size=6),
                hovertemplate=f"<b>{p}</b><br>Duration: %{{x}}s<br>Power: %{{y}} W<extra></extra>",
            ),
            row=1,
            col=1,
        )

        # Subplot 2: Relative Power Output (W/kg)
        fig1.add_trace(
            go.Scatter(
                x=df.index,
                y=df[(p, "W_kg")],
                mode="lines+markers",
                name=p,
                legendgroup=p,
                showlegend=False,  # Legend linked via legendgroup
                line=dict(color=colors[p], width=2),
                marker=dict(size=6),
                hovertemplate=f"<b>{p}</b><br>Duration: %{{x}}s<br>Relative Power: %{{y}} W/kg<extra></extra>",
            ),
            row=1,
            col=2,
        )

    # 3. Configure Logarithmic Axes & Custom Ticks
    fig1.update_xaxes(
        type="log",
        tickvals=time_seconds,
        ticktext=time_labels,
        title_text="Duration (log scale)",
        gridcolor="rgba(200, 200, 200, 0.3)",
    )

    fig1.update_yaxes(
        type="log",
        title_text="Absolute Power (Watts, log scale)",
        row=1,
        col=1,
        gridcolor="rgba(200, 200, 200, 0.3)",
    )

    fig1.update_yaxes(
        type="log",
        title_text="Relative Power (W/kg, log scale)",
        row=1,
        col=2,
        gridcolor="rgba(200, 200, 200, 0.3)",
    )

    fig1.update_layout(
        title=dict(
            text="<b>Male Professional Cyclists Power Profile (Log-Log Scale)<br>with percentile breakdown</b>",
            x=0.5,
        ),
        template="plotly_white",
        height=550,
        width=1100,
        legend_title_text="Percentile",
    )

    # Display interactively or export as HTML file
    fig1
    # fig.write_html("power_profiles_loglog.html")
    return (time_labels,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The mean height, weight and age of the participants were 180 cm, 68 kg and 29 years. The Miffin estimate of BMR would be 1665 kcals, while assuming very low body fat of 5% gives 1765 kcals and boosting this by 5% to account for a highly trained musculature gives a BMR of 1850 kcal per day for the average participant in the study. This can also be expressed as 90 Watts or 1.3 Watts/kg. The purpose of converting BMR into Watt/kg is to set into context the results cyclists are used to seeing in their power files.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Consider the 50th percentile cyclist, who maintained 4.2 Watts/kg for 4 hours. He probably felt pretty hot, because muscles are only about 20% to 25% efficient at converting chemical energy into mechanical energy, with the rest wasted as heat. So he would have to burn about 19.1 Watts/kg to maintain the power displayed on his head unit, in addition to the 1.3 Watts/kg BMR. This is almost 16 times BMR. And that takes a lot of energy: 4,777 kcals. The tool below calcuates the energy required to sustain a certain number of Watts/kg for rides of different durations. Note that total energy demand includes both mechanical energy and Basal Metabolic Rate (because the cyclist has to stay alive while cycling!). We can also explore the effect of consuming carbohydrates while riding.
    """)
    return


@app.cell
def _(mo, time_labels):

    weight2 = mo.ui.slider(40, 120, value=68, step=1, label="Weight (kg)")
    w_kg = mo.ui.slider(1, 10, value=4.2, step=0.1, label="Watts per kg")
    duration = mo.ui.dropdown(time_labels[7:], value="4h", label="Duration")
    fuelling = mo.ui.slider(0, 150, value=0, step=10, label="Carbs (g per hour)")

    controls2 = mo.vstack(
        [weight2, w_kg, fuelling, duration],
        justify="space-between",
        align="center",
    )
    return controls2, duration, fuelling, w_kg, weight2


@app.cell
def _(
    EFFICIENCY,
    JOULES_TO_KCALS,
    calculate_katch_mcardle,
    duration,
    fuelling,
    go,
    w_kg,
    weight2,
):

    duration_seconds = {
        "20m": 1200,
        "30m": 1800,
        "1h": 3600,
        "2h": 7200,
        "3h": 10800,
        "4h": 14400,
    }
    bod_fat = 5
    k_m, _ = calculate_katch_mcardle(weight2.value,bod_fat)
    bmrWatts = k_m*1.05/JOULES_TO_KCALS/24/60/60
    seconds = duration_seconds.get(duration.value, 14400)
    time = list(range(0, seconds + 1, max(1, seconds // 200)))
    bmr_demand = [ bmrWatts * t * JOULES_TO_KCALS for t in time]
    energy_demand = [(w_kg.value * weight2.value / EFFICIENCY + bmrWatts) * t * JOULES_TO_KCALS for t in time]
    with_fuelling = [energy_demand[i] - (fuelling.value * 4 / 3600 * t) for i, t in enumerate(time)]

    fig3 = go.Figure()
    fig3.add_trace(
        go.Scatter(
            x=time,
            y=bmr_demand,
            mode="lines",
            name="BMR demand",
            line=dict(color="#7fff00", width=3),
        )
    )
    fig3.add_trace(
        go.Scatter(
            x=time,
            y=with_fuelling,
            mode="lines",
            name="With fuelling",
            line=dict(color="#f58518", width=3),
        )
    )
    fig3.add_trace(
        go.Scatter(
            x=time,
            y=energy_demand,
            mode="lines",
            name="Total energy expended",
            line=dict(color="#4c78a8", width=3),
        )
    )
    fig3.update_layout(
        title=f"Analysis for {weight2.value} kg rider at {w_kg.value} Watts/kg ({weight2.value*w_kg.value:.0f} Watts) for {duration.value}, fuelling at {fuelling.value} g of carbs per hour<br>Total energy demand (incl BMR): {energy_demand[-1]:.0f} kcals. Net energy demand with fuelling {with_fuelling[-1]:.0f} kcals",
        xaxis_title="Time",
        yaxis_title="Energy expended kcals",
        xaxis=dict(
            range=[0, seconds],
            tickmode="array",
            tickvals=list(duration_seconds.values()),
            ticktext=list(duration_seconds.keys()),
        ),
        yaxis=dict(autorange="reversed"),
        template="plotly_white",
        margin=dict(t=40, b=20, l=20, r=20),
        height=400,
        legend=dict(title="Series"),
    )
    return


@app.cell
def _(controls2):
    controls2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Burning over 4777 kcals without fuelling leaves the body in a significant energy deficit compared with the start of the day. The rider would need to eat a large meal, ideally within 20 minutes, while the body is still primed for <a href="https://journals.physiology.org/doi/abs/10.1152/jappl.1988.64.4.1480">rapid glycogen resynthesis</a>. Recent years have seen elite athletes increase their consumption of carbohydrates during exercise, with professional cyclists taking on 90 g to 120+ g per hour of a glucose/fructose mix. Above these levels, specialised transport proteins become saturated.<br>If you shift the Carbs slider over to 100 g, the energy deficit is reduced to 3177 kcals at the end of a four hour ride. This is because 100 g of carbs are converted to roughly 400 kcals, so after four hours the rider has an extra 1600 kcals. This has the advantages of
    - preserving muscle and liver glycogen stores and
    - accelerating recovery due to a lower energy deficit.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It is also possible to convert carbs per hour into Watts. Every 100 g of carbohydrate produces 400 kcals, which is just over 1600 kJoules per hour or 464 joules per second. Given an efficiency of 22%, this converts to 102 Watts of mechanical power. Unfortunately this does not mean that a 200 Watts rider can suddenly match his friend who is riding at 300 Watts, but it does mean that, by fuelling with 100 g of carbs per hour the 300 Watts rider is depleting glycogen stores at the same rate as a non-fuelling 200 Watts rider.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Back to basics
    Bringing this back to Basal Metabolic Rate, average males tick over at about 1.1 Watts/kg and females about 1.0 Watts/kg. Due to energy lost in generating mechanical energy in muscles, riding a bike relatively slowly at 1.0 Watt/kg has a power demand of about 4.5 Watts/kg. <br>Although professional riders have a slightly more elevated BMR, they are able to sustain phenomenal power to weight ratios for long periods, burning energy are rates approaching 20 times BMR. A 68 kg rider consuming 100 g of carbs per hour is conusming about 4.5 times BMR. This allows the cyclist to conserve a significant amount of glycogen stores, reduces energy deficits and accelerates recover.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Since power is work done per unit time, we can obtain the amount of energy expended over each duration.
    """)
    return


if __name__ == "__main__":
    app.run()
