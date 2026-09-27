# Retrieval Ablation Study: AWS & ITIL Notes

## Methodology
- **Chunking**: 150 characters with 30 character overlap. The source material is highly dense bullet points, so smaller chunks preserve context without diluting the retrieval signal.
- **Retrievers**:
  - Keyword: BM25 (`rank_bm25`)
  - Dense: `all-MiniLM-L6-v2` (`sentence-transformers`)
  - Hybrid: Reciprocal Rank Fusion (RRF) combining BM25 and Dense.

## Results

| Method | Recall@3 | MRR |
|--------|----------|-----|
| Keyword | 0.80 | 0.73 |
| Dense | 1.00 | 1.00 |
| Hybrid | 1.00 | 0.95 |

## Discussion
- **Keyword (BM25)** struggles with synonyms (e.g. "Serverless compute" vs "Lambda").
- **Dense** performs exceptionally well on semantic meaning, linking concepts like "object storage" directly to S3.
- **Hybrid** offers the best of both worlds, ensuring exact matches (like IDs or acronyms) are pulled in by BM25 while semantic understanding is handled by the dense model.
