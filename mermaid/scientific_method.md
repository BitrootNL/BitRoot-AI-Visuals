   ```mermaid
graph TD
    A[Initial question/observation]:::start --> B[Background research]:::process
    B --> C[Form a hypothesis]:::decision
    C --> D[Empiric testing]:::process
    D --> E{Analyze results and evaluate hypothesis}:::decision
    E --> F[Communicate results]:::endnode
    E -- Hypothesis false? --> C
```