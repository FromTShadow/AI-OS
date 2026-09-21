"""
Debugging-oriented executable evaluation for AI-OS Benchmark V3.

Extends the base CodeEvaluatorV3 with hidden tests for a more
challenging normalize_scores repair task.
"""

import subprocess

from brain.benchmarks.code_evaluator_v3 import CodeEvaluatorV3


class DebugCodeEvaluatorV3(CodeEvaluatorV3):
    FUNCTION_NAME = "normalize_scores"

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
            [10.0, 20.0, 30.0],
            [0.0, 0.5, 1.0],
        ),
        (
            [30.0, 10.0, 20.0],
            [1.0, 0.0, 0.5],
        ),
        (
            [-10.0, 0.0, 10.0],
            [0.0, 0.5, 1.0],
        ),
        (
            [5.0],
            [0.0],
        ),
        (
            [5.0, 5.0, 5.0],
            [0.0, 0.0, 0.0],
        ),
        (
            [],
            [],
        ),
    ]

    for original, expected in tests:
        source = list(original)

        result = normalize_scores(source)

        assert len(result) == len(expected)

        for actual, target in zip(result, expected):
            assert abs(actual - target) < 1e-9, (
                f"expected {expected!r}, got {result!r}"
            )

        assert source == original, (
            "function mutated its input"
        )


__ai_os_run_tests()
"""
        )

        return self._execute_test_program(
            test_program
        )

    def _execute_test_program(
        self,
        test_program: str,
    ) -> tuple[bool, str | None]:
        import sys
        import tempfile
        from pathlib import Path

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
                or "Generated code failed debugging tests."
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