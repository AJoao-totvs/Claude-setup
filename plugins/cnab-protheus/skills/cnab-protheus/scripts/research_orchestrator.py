"""Research orchestrator — dispatches subagents to fetch and cache bank CNAB specs.

v1.0-a: stub. Full implementation in v1.0-b when we extend to banks beyond BB pagamento.

For BB pagamento, the spec at references/specs/bb/pagamento.yaml was hand-curated
from the 001PG.2PE fixture; no online research was needed.
"""

from pathlib import Path


def research_spec(banco: str, operacao: str, output_path: Path) -> None:
    """Stub. In v1.0-a, only BB pagamento is supported, and its spec is already cached."""
    raise NotImplementedError(
        f"research_orchestrator stub: dispatching research subagents for "
        f"({banco!r}, {operacao!r}) is implemented in v1.0-b. "
        f"For v1.0-a, only BB pagamento is supported, and its spec is at "
        f"references/specs/bb/pagamento.yaml."
    )
