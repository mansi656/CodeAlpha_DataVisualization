from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Allows saving charts even when no display is available.
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
LIVE_DATA = ROOT / "Task1_Web_Scraping" / "output" / "books_scraped.csv"
SAMPLE_DATA = ROOT / "shared_data" / "sample_books_dataset.csv"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

def main():
    source = LIVE_DATA if LIVE_DATA.exists() else SAMPLE_DATA
    print(f"Using dataset: {source}")
    df = pd.read_csv(source)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme()

    if "category" in df.columns and "price_gbp" in df.columns:
        data = df.dropna(subset=["category", "price_gbp"])
        grouped = data.groupby("category", as_index=False)["price_gbp"].mean().sort_values("price_gbp", ascending=False)
        plt.figure(figsize=(10, 6))
        sns.barplot(data=grouped, x="price_gbp", y="category")
        plt.title("Average Book Price by Category")
        plt.xlabel("Average price (£)")
        plt.ylabel("Category")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "average_price_by_category.png", dpi=160)
        plt.close()

    if "rating" in df.columns:
        rating_counts = df["rating"].dropna().astype(str).value_counts().sort_index()
        plt.figure(figsize=(8, 5))
        sns.barplot(x=rating_counts.index, y=rating_counts.values)
        plt.title("Number of Books by Rating")
        plt.xlabel("Rating (1–5)")
        plt.ylabel("Number of books")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "rating_distribution.png", dpi=160)
        plt.close()

    if "price_gbp" in df.columns:
        prices = pd.to_numeric(df["price_gbp"], errors="coerce").dropna()
        plt.figure(figsize=(8, 5))
        sns.histplot(prices, bins=12, kde=True)
        plt.title("Distribution of Book Prices")
        plt.xlabel("Price (£)")
        plt.ylabel("Number of books")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "price_distribution.png", dpi=160)
        plt.close()

    if "price_gbp" in df.columns and "rating" in df.columns:
        scatter = df.copy()
        scatter["price_gbp"] = pd.to_numeric(scatter["price_gbp"], errors="coerce")
        scatter["rating"] = pd.to_numeric(scatter["rating"], errors="coerce")
        scatter = scatter.dropna(subset=["price_gbp", "rating"])
        plt.figure(figsize=(8, 5))
        sns.scatterplot(data=scatter, x="rating", y="price_gbp", hue="category" if "category" in scatter.columns else None)
        plt.title("Book Price versus Rating")
        plt.xlabel("Rating (1–5)")
        plt.ylabel("Price (£)")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "price_vs_rating.png", dpi=160)
        plt.close()

    print("Charts saved in:", OUTPUT_DIR)
    for file in sorted(OUTPUT_DIR.glob("*.png")):
        print("-", file.name)

if __name__ == "__main__":
    main()
