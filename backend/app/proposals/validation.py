from collections import Counter
from pathlib import Path

from app.core.config import AllowedRoot
from app.core.paths import PathEscapeError, resolve_asset_path
from app.db.models import Proposal


def validate_proposals(proposals: list[Proposal], root: AllowedRoot) -> None:
    target_counts = Counter(
        proposal.target_relative_path
        for proposal in proposals
        if proposal.operation == "move"
    )

    for proposal in proposals:
        validate_proposal(proposal, root, target_counts)


def validate_proposal(
    proposal: Proposal,
    root: AllowedRoot,
    target_counts: Counter[str],
) -> None:
    if proposal.operation != "move":
        proposal.validation_status = "skipped"
        proposal.validation_message = "Validation skipped for non-move proposal"
        return

    if target_counts[proposal.target_relative_path] > 1:
        block(proposal, "Multiple proposals target the same destination")
        return

    try:
        source_path = resolve_asset_path(root, proposal.source_relative_path)
        target_path = resolve_asset_path(root, proposal.target_relative_path)
    except PathEscapeError as error:
        block(proposal, str(error))
        return

    if target_path == source_path:
        block(proposal, "Target path is the same as the source path")
        return

    if target_path.exists():
        block(proposal, "Target path already exists")
        return

    if parent_conflicts_with_file(target_path, root.path):
        block(proposal, "Target parent path conflicts with an existing file")
        return

    proposal.validation_status = "valid"
    proposal.validation_message = "Target path is available"


def block(proposal: Proposal, message: str) -> None:
    proposal.status = "blocked"
    proposal.validation_status = "blocked"
    proposal.validation_message = message


def parent_conflicts_with_file(target_path: Path, root_path: Path) -> bool:
    root_path = root_path.resolve()
    for parent in target_path.parents:
        if parent == root_path:
            return False
        if parent.exists() and not parent.is_dir():
            return True
    return False
