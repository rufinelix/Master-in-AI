import argparse
from rouge_score import rouge_scorer

def calculate_rouge(reference: str, candidate: str):
    """
    Calculates ROUGE-1, ROUGE-2, and ROUGE-L scores (fmeasure).
    Adapted from the Nguyen et al. METAGENTE repository.
    """
    # use_stemmer=True matches the original implementation
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    scores = scorer.score(reference, candidate)
    
    return {
        "rouge1": scores["rouge1"].fmeasure,
        "rouge2": scores["rouge2"].fmeasure,
        "rougeL": scores["rougeL"].fmeasure
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a candidate summary against a reference summary using ROUGE.")
    parser.add_argument("--reference", type=str, required=True, help="The ground truth reference text")
    parser.add_argument("--candidate", type=str, required=True, help="The generated candidate text")
    args = parser.parse_args()
    
    results = calculate_rouge(args.reference, args.candidate)
    print(f"ROUGE-1: {results['rouge1']:.4f}")
    print(f"ROUGE-2: {results['rouge2']:.4f}")
    print(f"ROUGE-L: {results['rougeL']:.4f}")
