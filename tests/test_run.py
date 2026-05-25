# -------------------------------------------------------------------------------
# filename: app/tests/test_run.py
# Author: Joseph Egan
# 2026-05-04
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: unittest runner for project tests

import unittest


def build_suite() -> unittest.TestSuite:
    loader = unittest.defaultTestLoader
    return loader.loadTestsFromNames([
        "tests.test_validation",
        "tests.test_database",
    ])


def main() -> int:
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(build_suite())
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
