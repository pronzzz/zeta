from retrievers import Retrievers
import json

QA_PAIRS = [
    {"query": "What service provides object storage?", "expected_keyword": "S3"},
    {"query": "How is incident impact minimized?", "expected_keyword": "Incident Management"},
    {"query": "Which service handles relational databases?", "expected_keyword": "RDS"},
    {"query": "What are the four dimensions of service management?", "expected_keyword": "Organizations & People"},
    {"query": "Serverless compute", "expected_keyword": "Lambda"}
]

def compute_metrics(results, expected):
    for i, res in enumerate(results):
        if expected.lower() in res.lower():
            return 1, 1 / (i + 1)
    return 0, 0

def run_ablation():
    r = Retrievers()
    
    stats = {
        "keyword": {"recall": 0, "mrr": 0},
        "dense": {"recall": 0, "mrr": 0},
        "hybrid": {"recall": 0, "mrr": 0}
    }
    
    for qa in QA_PAIRS:
        q = qa["query"]
        expected = qa["expected_keyword"]
        
        k_res = r.retrieve_keyword(q)
        d_res = r.retrieve_dense(q)
        h_res = r.retrieve_hybrid(q)
        
        k_rec, k_mrr = compute_metrics(k_res, expected)
        d_rec, d_mrr = compute_metrics(d_res, expected)
        h_rec, h_mrr = compute_metrics(h_res, expected)
        
        stats["keyword"]["recall"] += k_rec
        stats["keyword"]["mrr"] += k_mrr
        stats["dense"]["recall"] += d_rec
        stats["dense"]["mrr"] += d_mrr
        stats["hybrid"]["recall"] += h_rec
        stats["hybrid"]["mrr"] += h_mrr
        
    n = len(QA_PAIRS)
    for method in stats:
        stats[method]["recall"] /= n
        stats[method]["mrr"] /= n
        
    return stats

if __name__ == "__main__":
    results = run_ablation()
    print("Ablation Results:")
    for method, metrics in results.items():
        print(f"{method.capitalize()}: Recall@3={metrics['recall']:.2f}, MRR={metrics['mrr']:.2f}")
