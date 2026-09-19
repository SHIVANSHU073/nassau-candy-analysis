# Executive Summary

The project establishes reusable decision-support infrastructure for Nassau Candy Distributor.

The dataset has no missing cells or duplicate rows and its financial fields are internally consistent. However, recorded order-to-ship intervals are 904–1,642 days, creating a major data-quality limitation.

Gradient Boosting produced the lowest tested RMSE, but R² was only about 0.04. It should not be presented as a highly reliable shipping predictor.

Each product is associated with one historical factory, so alternative-factory effects are not empirically identified. The Streamlit simulator therefore labels those results as model-based simulations.

Capacity, transportation cost, production constraints and reassignment costs are also unavailable, so operational feasibility and true incremental profit cannot be established.
