import os

def is_valid_path(path_str):
    """
    Checks if a given path string is a valid path (file or directory).

    Args:
        path_str: The path string to check.

    Returns:
        True if the path is valid, False otherwise.
    """
    if not isinstance(path_str, str):
        return False  # Path must be a string
    return os.path.exists(path_str)

path1 = "C:\\Users\\vamsi\\Documents\\1MTSU\\SEM 2\\Research Methods in Computer Science\\Research Project\\codebase\\RSL-SQL\\dynamic-feedback-test\\files\\test_database\\soccer_3\\soccer_3.sqlite"
path2= r"C:/Users/vamsi/Documents/1MTSU/SEM 2/Research Methods in Computer Science/Research Project/codebase/RSL-SQL/dynamic-feedback-test/files/test_database/soccer_3/soccer_3.sqlite"
db_name="soccer_3"
db_path=f"C:\\Users\\vamsi\\Documents\\1MTSU\\SEM 2\\Research Methods in Computer Science\\Research Project\\codebase\\RSL-SQL\\dynamic-feedback-test\\files\\test_database\\{db_name}\\{db_name}.sqlite"

print(f"'{db_path}' is valid: {is_valid_path(db_path)}")

