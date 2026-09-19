# Assumptions and Data-Quality Decisions

1. Dates are parsed using `DD-MM-YYYY`.
2. Raw date relationships are preserved; no dates are silently corrected.
3. Recorded lead time is a dataset target only, not verified physical transit time.
4. Product-to-factory mapping is reference configuration, not learned assignment data.
5. Product and factory are strongly confounded because each product maps to one factory.
6. No factory capacity, transportation cost, reassignment cost, inventory constraint, or production constraint is assumed.
7. Outliers are investigated rather than mechanically removed.
8. Counterfactual factory predictions are labelled simulations/model proxies.
9. Incremental profit cannot be calculated without incremental logistics/production costs.
