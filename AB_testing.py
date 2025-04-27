import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

success_a = int(input("Enter number of conversions for Group A (Control): "))
n_a = int(input("Enter total number of users for Group A (Control): "))

success_b = int(input("Enter number of conversions for Group B (Treatment): "))
n_b = int(input("Enter total number of users for Group B (Treatment): "))

p1 = success_a / n_a
p2 = success_b / n_b
p_pool = (success_a + success_b) / (n_a + n_b)

z = (p1 - p2) / np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
p_value = stats.norm.sf(abs(z)) * 2

alpha = 0.05
decision = "Statistically Significant ✅" if p_value < alpha else "No Significant Difference ❌"

lift = (p2 - p1) / p1 * 100

conf_int_A = stats.norm.interval(0.95, loc=p1, scale=np.sqrt(p1*(1-p1)/n_a))
conf_int_B = stats.norm.interval(0.95, loc=p2, scale=np.sqrt(p2*(1-p2)/n_b))

results = pd.DataFrame({
    "Group": ["Control (A)", "Treatment (B)"],
    "Conversion Rate": [p1, p2],
    "95% CI Lower": [conf_int_A[0], conf_int_B[0]],
    "95% CI Upper": [conf_int_A[1], conf_int_B[1]],
})

print("\n--- A/B Testing Results ---")
print(results)
print(f"\nZ-Statistic: {z:.3f}")
print(f"P-Value: {p_value:.5f}")
print(f"Lift: {lift:.2f}%")
print(f"Result: {decision}")

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x="Group", y="Conversion Rate", data=results, palette="Set2", ci=None)
ax.errorbar(x=[0,1], y=results["Conversion Rate"], 
            yerr=[results["Conversion Rate"] - results["95% CI Lower"], results["95% CI Upper"] - results["Conversion Rate"]],
            fmt='none', c='black', capsize=5)
plt.title('A/B Test: Conversion Rates with 95% CI')
plt.ylim(0, max(results["Conversion Rate"]) + 0.05)
plt.grid(axis='y')
plt.show()
