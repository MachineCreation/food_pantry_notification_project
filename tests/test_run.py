# -------------------------------------------------------------------------------
# filename: app/tests/test_run.py
# Author: Joseph Egan
# 2026-05-04
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description:

# Local imports
from tests import test_database, test_validation
from app.database.models.Database import Database
from app.logic.utilities.validation import (
    input_string,
    is_email_or_username,
    non_empty_string,
    is_valid_password,
    validate_passwords_match
)

# python imports
from typing import Callable


def main():
    '''
    runs automated basic tests on the app
    '''
# --------------------------------- test database ----------------------------
    try:
        database = Database()
        print("Database object: PASSED")
    except Exception as e:
        print(f"Database object: FAILED — {e}")
        return

    try:
        test_database.setup_database_tests(database)

        run_function_test(
            database,
            database.ensure_connection,
            test_database.test_ensure_connection()
            )
        run_function_test(
            database,
            database.execute_query,
            test_database.test_execute_query()
            )
        run_function_test(
            database,
            database.authenticate_user,
            test_database.test_authenticate_user()
            )
        run_function_test(
            database,
            database.sign_up_user,
            test_database.test_sign_up_user()
            )

    finally:
        test_database.cleanup_database_tests(database)
        database.disconnect()

    run_function_test(
        database,
        input_string,
        test_validation.test_input_string()
    )

    run_function_test(
        database,
        non_empty_string,
        test_validation.test_non_empty_string()
    )

    run_function_test(
        database,
        is_email_or_username,
        test_validation.test_is_email_or_username()
    )

    run_function_test(
        database,
        is_valid_password,
        test_validation.test_is_valid_password()
    )

    run_function_test(
        database,
        validate_passwords_match,
        test_validation.test_validate_passwords_match()
    )


def run_function_test(
    database: Database,
    tested_function: Callable,
    params_results: dict,
):
    for instance_name, parameters in params_results.items():
        try:
            if "before" in parameters:
                parameters["before"](database)

            results = tested_function(**parameters.get("params", {}))

            if "expected exception" in parameters:
                print(
                    f"{instance_name}: FAILED "
                    f"expected exception {parameters['expected exception']}, \
                    got result {results}"
                )

            elif "expected type" in parameters:
                if isinstance(results, parameters["expected type"]):
                    print(f"{instance_name}: PASSED")
                else:
                    print(
                        f"{instance_name}: FAILED "
                        f"expected type {parameters['expected type']}, got \
                            {type(results)}"
                    )

            elif "validate" in parameters:
                if parameters["validate"](results):
                    print(f"{instance_name}: PASSED")
                else:
                    print(f"{instance_name}: FAILED validation, got {results}")

            elif results == parameters["expected results"]:
                print(f"{instance_name}: PASSED")

            else:
                print(
                    f"{instance_name}: FAILED "
                    f"expected {parameters['expected results']}, got {results}"
                )

        except Exception as e:
            if "expected exception" in parameters and isinstance(
                e,
                parameters["expected exception"]
            ):
                print(f"{instance_name}: PASSED")
            else:
                print(f"{instance_name}: FAILED FOR EXCEPTION — {e}")


if __name__ == "__main__":
    main()
