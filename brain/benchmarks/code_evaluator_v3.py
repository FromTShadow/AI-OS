"""
Executable coding evaluation for AI-OS Benchmark V3.

Evaluates generated Python by executing it in a separate subprocess
with a timeout and deterministic behavioral tests.
"""

import ast
import subprocess
import sys
import tempfile

from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class CodeQualityResultV3:
    score: float
    passed_checks: List[str] = field(default_factory=list)
    failed_checks: List[str] = field(default_factory=list)
    error: str | None = None


class CodeEvaluatorV3:
    FUNCTION_NAME = "remove_duplicates"

    def evaluate(
        self,
        code: str,
    ) -> CodeQualityResultV3:
        passed = []
        failed = []

        # 1. Syntax
        try:
            tree = ast.parse(code)
            passed.append("valid_python")
        except SyntaxError as exc:
            return CodeQualityResultV3(
                score=0.0,
                failed_checks=[
                    "valid_python",
                    "function_exists",
                    "type_annotations",
                    "behavior",
                ],
                error=str(exc),
            )

        # 2. Required function
        function = next(
            (
                node
                for node in tree.body
                if isinstance(
                    node,
                    (ast.FunctionDef, ast.AsyncFunctionDef),
                )
                and node.name == self.FUNCTION_NAME
            ),
            None,
        )

        if function is None:
            failed.append("function_exists")
        else:
            passed.append("function_exists")

        # 3. Type annotations
        has_annotations = (
            function is not None
            and bool(function.args.args)
            and all(
                argument.annotation is not None
                for argument in function.args.args
            )
            and function.returns is not None
        )

        if has_annotations:
            passed.append("type_annotations")
        else:
            failed.append("type_annotations")

        # 4. Real execution tests
        behavior_passed, error = self._run_behavior_tests(
            code
        )

        if behavior_passed:
            passed.append("behavior")
        else:
            failed.append("behavior")

        weights = {
            "valid_python": 10.0,
            "function_exists": 10.0,
            "type_annotations": 10.0,
            "behavior": 70.0,
}

        score = sum(
            weights[check]
            for check in passed
)

        return CodeQualityResultV3(
            score=round(score, 1),
            passed_checks=passed,
            failed_checks=failed,
            error=error,
        )

    def _run_behavior_tests(
        self,
        code: str,
    ) -> tuple[bool, str | None]:
        test_program = (
            code
            + """

def __ai_os_run_tests():
    tests = [
        (
            ["a", "b", "a", "c"],
            ["a", "b", "c"],
        ),
        (
            [],
            [],
        ),
        (
            ["x"],
            ["x"],
        ),
        (
            ["a", "a", "a"],
            ["a"],
        ),
        (
            ["b", "a", "b", "c", "a"],
            ["b", "a", "c"],
        ),
    ]

    for original, expected in tests:
        source = list(original)

        result = remove_duplicates(source)

        assert result == expected, (
            f"expected {expected!r}, got {result!r}"
        )

        assert source == original, (
            "function mutated its input"
        )


__ai_os_run_tests()
"""
        )

        temporary_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                encoding="utf-8",
                delete=False,
            ) as temporary_file:
                temporary_file.write(test_program)
                temporary_path = Path(
                    temporary_file.name
                )

            completed = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    str(temporary_path),
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if completed.returncode == 0:
                return True, None

            error = (
                completed.stderr.strip()
                or completed.stdout.strip()
                or "Generated code failed execution tests."
            )

            return False, error

        except subprocess.TimeoutExpired:
            return (
                False,
                "Generated code exceeded the 5-second timeout.",
            )

        finally:
            if temporary_path is not None:
                temporary_path.unlink(
                    missing_ok=True
                )