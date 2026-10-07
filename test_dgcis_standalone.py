"""
Standalone test for the decoupled services/dgcis.py.

Run this alone, from the same folder level as `services/`:
    python test_dgcis_standalone.py

If this prints real data with no errors, the decoupling worked and you
can move to step 2 (a single NiceGUI filter wired to a label). If it
errors, we fix it here — no UI code involved yet, so any bug is purely
about the data layer.
"""

import services.dgcis as dgcis

print("Loading export data...")
exports_df = dgcis.get_all_data("export")
print(f"  Shape: {exports_df.shape}")
print(f"  Columns: {list(exports_df.columns)}")
print(exports_df.head(3))

print("\nLoading import data...")
imports_df = dgcis.get_all_data("import")
print(f"  Shape: {imports_df.shape}")

print("\nTesting derived functions...")
fy_totals = dgcis.get_fy_totals(exports_df)
print(fy_totals)

latest_fy = sorted(exports_df["financial_year"].unique())[-1]
hhi = dgcis.compute_hhi(exports_df, latest_fy)
yoy = dgcis.compute_yoy_growth(exports_df, latest_fy)
print(f"\nHHI for {latest_fy}: {hhi}")
print(f"YoY growth for {latest_fy}: {yoy}")

# Confirms caching actually works — this second call should be instant,
# since lru_cache holds the result from the first call above.
import time
start = time.time()
dgcis.get_all_data("export")
elapsed = time.time() - start
print(f"\nSecond call to get_all_data('export') took {elapsed:.4f}s (should be ~0 — confirms caching is working)")

print("\n✅ All good — dgcis.py works standalone, no Streamlit needed.")
