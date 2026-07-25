from pathlib import Path

from loader import DataLoader
from validator import DataValidator
from cleaner import DataCleaner
from synthetic_features import SyntheticFeatureGenerator


def main():

    print("=" * 60)
    print("CUSTOMER SEGMENTATION DATA PIPELINE")
    print("=" * 60)

    # Initialize modules
    loader = DataLoader()
    validator = DataValidator()
    cleaner = DataCleaner()
    generator = SyntheticFeatureGenerator()

    # Step 1: Load dataset
    print("\n[1] Loading dataset...")
    df = loader.load_dataset()

    # Step 2: Validate dataset
    print("[2] Validating dataset...")
    validator.validate_columns(df)

    # Step 3: Clean dataset
    print("[3] Cleaning dataset...")
    df = cleaner.clean(df)

    # Step 4: Generate synthetic features
    print("[4] Generating synthetic banking features...")
    df = generator.generate(df)

    # Step 5: Dataset summary
    print("[5] Dataset Summary")
    cleaner.dataset_summary(df)

    numerical, categorical = cleaner.split_columns(df)

    print("\nNumerical Columns")
    print(numerical)

    print("\nCategorical Columns")
    print(categorical)

    # Step 6: Save processed dataset
    output_path = (
        Path(__file__)
        .resolve()
        .parents[2]
        / "data"
        / "processed"
        / "enhanced_bank_dataset.csv"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    print("\nEnhanced dataset saved successfully!")
    print(f"Location: {output_path}")

    print("\nPreview of Enhanced Dataset:")
    print(df.head())


    print("\n========== SYNTHETIC FEATURE SUMMARY ==========\n")

    print(df["annual_income"].describe())

    print("\n")

    print(df["credit_score"].describe())

    print("\n")

    print(df["account_balance"].describe())

    print("\n")

    print(df["digital_banking_score"].describe())

    print("\nProducts Distribution")

    print(df["number_of_products"].value_counts().sort_index())

    print("\nTransactions Distribution")

    print(df["monthly_transactions"].describe())

    print("\nPipeline completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
