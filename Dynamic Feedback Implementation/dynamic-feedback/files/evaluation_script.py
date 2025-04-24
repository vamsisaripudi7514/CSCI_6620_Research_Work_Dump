import json
from tqdm import tqdm
from execute_sql import execute_sql 
from execute_sql import get_all_schema, extract_tables_and_columns


def load_data(final_sql_path, ppl_dev_path, schema_json_path):
    with open(final_sql_path, 'r', encoding='utf-8') as f:
        predicted_sqls = [line.strip() for line in f.readlines()]

    with open(ppl_dev_path, 'r', encoding='utf-8') as f:
        gold_data = json.load(f)

    with open(schema_json_path, 'r', encoding='utf-8') as f:
        predicted_schema = json.load(f)

    return predicted_sqls, gold_data, predicted_schema




def evaluate_sql_accuracy(predicted_sqls, gold_data):
    exec_correct = 0
    exact_correct = 0
    total = len(predicted_sqls)

    for idx in tqdm(range(total), desc="Evaluating SQL"):
        pred_sql = predicted_sqls[idx]
        gold_sql = gold_data[idx]['gold_sql']
        db_name = gold_data[idx]['db']

        try:
            pred_rows, _, _ = execute_sql(pred_sql, db_name)
            gold_rows, _, _ = execute_sql(gold_sql, db_name)

            if pred_rows == gold_rows:
                exec_correct += 1
            else:
                print("failed at index", idx+1)
                print("predicted:", pred_sql)
        except Exception as e:
            print(f"[Execution Error] index={idx}: {e}")



    exec_acc = (exec_correct / total) * 100
    return exec_acc, exec_correct, total



def main():
    # Update file paths as needed
    # final_sql_path = 'step_4_sql.txt'
    # final_sql_path = 'gemini_step_3.txt'
    # final_sql_path = 'gemini_pro_2_flash_lite_static_feedback.txt'
    # final_sql_path = 'gemini_pro_2_flash_lite_dynamic_feedback.txt'
    # final_sql_path = 'gemini_2_flash_step_3.txt'
    # final_sql_path = 'gemini_pro_2_flash_static_feedback.txt'
    # final_sql_path = 'gemini_pro_2_flash_dynamic_feedback.txt'
    # final_sql_path = 'gemini_1.5_pro_step_3.txt'
    # final_sql_path = 'gemini_1.5_pro_static_feedback.txt'
    final_sql_path = 'gemini_1.5_pro_dynamic_feedback.txt'
    ppl_dev_path = 'ppl_dev.json'
    schema_json_path = 'ppl_dev.json'

    print("Loading data...")
    predicted_sqls, gold_data, predicted_schema = load_data(final_sql_path, ppl_dev_path, schema_json_path)

    print("\n[1] Evaluating SQL accuracy...")
    exec_acc, exec_correct, total = evaluate_sql_accuracy(predicted_sqls, gold_data)


    print("\n========== Evaluation Report ==========")
    print(f"Total Queries Evaluated:      {total}")
    print(f"Execution Accuracy:         {exec_acc:.2f}%  ({exec_correct}/{total})")
    print("========================================")


if __name__ == "__main__":
    main()
