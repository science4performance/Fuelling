# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "plotly==6.9.0",
# ]
# ///

import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    pass


@app.cell
def _(mo):
    mo.md(r"""
    # How many carbs?
    This project explores the impact of fuelling strategies for professional and competitive cyclists. We begin by exploring the Basal Metabolic Rate (BMR), which is minimum number of calories your body burns at rest for basic functions like breathing, circulation and cell production. This sets a reference for considering the energy demands of high level endurance performance and the amount of energy consumed in the form of carbohydrates during the activity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Basal Metabolic Rate (BRM)
    Even at rest, the body burns a certain amount of energy to maintain basic metabolism in order to stay alive. This is principally determined by the cells that make up Fat Free Mass, defined as Total Body Mass minus Total Body Fat. The term Lean Body Mass is often used interchangeably with Fat Free Mass, though the strict definition of Lean Body Mass excludes the skeleton, which is metabolically active, as bone is continually formed and resorbed.<br>
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
    return age, body_fat, controls, go, height, sex, weight


@app.cell
def _(age, body_fat, go, height, mo, sex, weight):
    def calculate_bmr(weight_kg, height_cm, age_years, sex_value, body_fat_pct):
        if sex_value == "Male":
            mifflin_st_jeor = 10 * weight_kg + 6.25 * height_cm - 5 * age_years + 5
        else:
            mifflin_st_jeor = 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 161

        lbm = weight_kg * (1 - body_fat_pct / 100)
        katch_mcardle = 370 + 21.6 * lbm
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
                text=[f"{katch_mcardle:.0f}", f"{mifflin_st_jeor:.0f}"],
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


    return


@app.cell
def _(controls):
    controls
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
