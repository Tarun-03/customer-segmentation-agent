from pathlib import Path

import pandas as pd

from trainer import ClusterTrainer
from preprocessor import DataPreprocessor
from evaluator import ClusterEvaluator
from profiler import ClusterProfiler
from personas import PersonaGenerator
from recommendation import RecommendationEngine

def main():

    print("=" * 60)
    print("CUSTOMER SEGMENTATION PIPELINE")
    print("=" * 60)

    project_root = Path(__file__).resolve().parents[2]

    dataset_path = (
        project_root
        / "data"
        / "processed"
        / "enhanced_bank_dataset.csv"
    )

    print("\n[1] Loading dataset...")

    df = pd.read_csv(dataset_path)

    print(f"Dataset Shape : {df.shape}")

    print("\n[2] Preprocessing dataset...")

    preprocessor = DataPreprocessor(df)

    X_processed, transformer = preprocessor.preprocess()

    print("Preprocessing completed successfully.")

    print(f"Processed Shape : {X_processed.shape}")

    print("\n[3] Evaluating optimal number of clusters...")

    evaluator = ClusterEvaluator()

    recommended_k = evaluator.evaluate(X_processed)

    # Business decision for better customer segmentation
    final_k = 4

    print("\n" + "=" * 60)
    print(f"Recommended K (Silhouette): {recommended_k}")
    print(f"Final K Used: {final_k}")
    print("=" * 60)

    print(
        project_root
        / "data"
        / "outputs"
        / "plots"
    )

    trainer = ClusterTrainer(n_clusters=4)

    trainer.save_preprocessor(transformer)

    model, labels = trainer.train(X_processed)

    df["cluster"] = labels

    output_path = (
        project_root
        / "data"
        / "processed"
        / "clustered_customers.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(f"\nClustered dataset saved to:\n{output_path}")

    print("\n[4] Profiling customer clusters...")

    profiler = ClusterProfiler()

    summary = profiler.profile(df)

    print("\n[5] Generating customer personas...")

    persona_generator = PersonaGenerator()

    persona_df = persona_generator.generate(summary)

    print("\n[6] Generating recommendations...")

    recommendation_engine = RecommendationEngine()

    recommendation_df = recommendation_engine.generate(persona_df)


if __name__ == "__main__":
    main()