import os
import pandas as pd

def search_csv_files(directory, column_name, search_string, result_directory, result_columns):
    results = []
    all_matches = []

    if not os.path.exists(directory):
        return results

    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            try:
                df = pd.read_csv(file_path, encoding='utf-8')

                if column_name not in df.columns:
                    continue

                matching_rows = df[df[column_name].astype(str).str.contains(search_string, case=False, na=False)]

                if not matching_rows.empty:
                    results.append((file, matching_rows))

                    if all(col in df.columns for col in result_columns):
                        all_matches.append(matching_rows[result_columns])

            except:
                continue

    if all_matches:
        combined_results = pd.concat(all_matches, ignore_index=True)

        if not combined_results.empty:
            result_file_path = os.path.join(result_directory, "result.csv")
            combined_results.to_csv(result_file_path, index=False, encoding='utf-8')
            print("File written to CSV")

    return results

def main():
    directory = input("Enter the CSV Directory: ").strip()
    if not os.path.exists(directory):
        return

    column_name = input("Enter coloumn name: ").strip()
    search_string = input("Enter the Search String: ").strip()
    result_columns = input("Enter the Result coulmns to be exported: ").strip().split(",")
    result_directory = input("Enter the result Directory: ").strip()

    if not column_name or not search_string or not result_columns or not result_directory:
        return

    result_columns = [col.strip() for col in result_columns]

    search_csv_files(directory, column_name, search_string, result_directory, result_columns)

if __name__ == "__main__":
    main()

