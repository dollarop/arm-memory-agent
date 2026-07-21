# Architecture

```mermaid
flowchart LR
  A["Learner notes, files, and section text"] --> B["Memory card normalizer"]
  B --> C["Deduplicated memory store"]
  C --> D["Tag/token retriever"]
  E["Current learner question"] --> D
  D --> F["Compact prompt pack"]
  F --> G["Agent answer: proof, practice, teach-back"]
  F --> H["SHA-256 audit hash"]
  C --> I["Naive full-context baseline"]
  I --> J["Benchmark comparison"]
  F --> J
```

The prototype keeps the agent CPU-friendly by replacing full-history prompting with deterministic memory retrieval. It can be validated on x86 and Arm64 because it uses only the Python standard library.
