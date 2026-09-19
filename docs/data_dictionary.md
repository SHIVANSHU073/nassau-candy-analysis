# Data Dictionary

| Field | Meaning |
|---|---|
| Row ID | Unique row identifier |
| Order ID | Order identifier |
| Order Date | Recorded order date |
| Ship Date | Recorded shipment date |
| Ship Mode | Shipping method |
| Customer ID | Customer identifier |
| Country/Region | Customer country |
| City | Customer city |
| State/Province | Customer state/province |
| Postal Code | Customer ZIP/postal code |
| Division | Product division |
| Region | Destination region |
| Product ID | Product identifier |
| Product Name | Product name |
| Sales | Order-line sales value |
| Units | Units in order line |
| Gross Profit | Sales minus Cost |
| Cost | Cost field |

## Derived
- `recorded_lead_time_days`
- `gross_margin_pct`
- order calendar features
- `factory` from product-factory reference mapping
