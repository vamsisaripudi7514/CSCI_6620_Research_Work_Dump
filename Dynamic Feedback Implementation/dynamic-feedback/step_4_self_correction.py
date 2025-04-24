from files.self_correction_gpt import GPT
import json
from tqdm import tqdm
from files.execute_sql import execute_sql
from files.internal_configs.Instruction import SELF_CORRECTION_PROMPT
from step_3_5_dynamic_feedback import get_dynamic_feedback
from files.internal_configs.extract_json import extract_json
# from utils.simplified_schema import simplified, explanation_collection
# import argparse
import time


def table_info_construct(ppl, simple_ddl, ddl_data, foreign_key):
    question = ppl['question'].strip()
    # evidence = ppl['evidence'].strip()
    example = ppl['example']

    table_info = '### Sqlite SQL tables, with their properties:\n'
    table_info += simple_ddl + '\n' + '### Here are some data information about database references.\n' + ddl_data + '\n### Foreign key information of Sqlite SQL tables, used for table joins:\n' + foreign_key + '\n### '

    table_info += f'\n### sql_keywords: {ppl["sql_keywords"]}'
    table_info += f'\n### conditions: {ppl["conditions"]}'

    # table_info = example.strip() + '\n\n' + "### Answer the question by sqlite SQL query only and with no explanation. You must minimize SQL execution time while ensuring correctness.\n" + table_info.strip() + '\n\n' + '### Hint: ' + evidence + "\n### Question: " + question + '\n\n' + 'The hint aims to direct your focus towards the specific elements of the database schema that are crucial for answering the question effectively.'
    table_info = '\n\n' + "### Answer the question by sqlite SQL query only and with no explanation. You must minimize SQL execution time while ensuring correctness.\n" + table_info.strip() + '\n\n' + "\n### Question: " + question + '\n\n'

    return table_info


def main(ppl_file, sql_file, output_file, x=0, y=0):
    gpt = GPT()

    # 1.加载prompt信息 从0开始
    with open(ppl_file, 'r') as f:
        ppls = json.load(f)

    with open(sql_file, 'r') as f:
        pre_sqls = f.readlines()

    sys_message = SELF_CORRECTION_PROMPT

    answers = []

    for i in tqdm(range(x, y+1)):
        prompt_message = ""
        message = []
        # message.append({'role': 'system', 'content': sys_message})
        ppl = ppls[i]
        db = ppl['db']

        # 简化ddl
        # simplified_ppl = []
        # with open(simplified_ppl_file, 'r') as simplified_f:
        #     simplified_ppl = json.load(simplified_f)
        simple_ddl, ddl_data, foreign_key = ppl['simplified_ddl'], ppl['ddl_data'], ppl['foreign_key']

        # 列描述
        # explanation = explanation_collection(ppl)

        table_info = table_info_construct(ppl, simple_ddl, ddl_data, foreign_key)

        pre_sql = pre_sqls[i].strip()

        num = 0
        while num < 5:

            row_count, column_count, result = execute_sql(pre_sql, db)
            print ("BLOCKER2")
            if num > 0:
                table_info = "### Buggy SQL: " + pre_sql.strip() + "\n" + f"### The result of the buggy SQL is [{result.strip()}]. Please fix the SQL to get the correct result."
            if row_count == 0 and column_count == 0:
                message.append({'role': 'user', 'content': table_info})
                dynamic_feedback = get_dynamic_feedback(table_info, result)
                # print(dynamic_feedback)
                prompt_message = SELF_CORRECTION_PROMPT + table_info + "### Dynamic feedback: " + dynamic_feedback
                answer = gpt(prompt_message,message)
                json_answer = extract_json(answer)
                # message, answer = gpt(message)
                num += 1
                try:
                    json_answer = json.loads(json_answer)
                except Exception as e:
                    json_answer = json_answer.replace('\\', '\\\\')
                    try:
                        json_answer = json.loads(json_answer)
                    except Exception as e:
                        break
                pre_sql = json_answer['sql'].strip()
                print(pre_sql,'This is printed')
                print("Updated SQL! ", i)
                # time.sleep(30)
            else:
                # print(pre_sql,'This is printed')
                print("ALL OK!", i)
                break
        # answers.append(pre_sql.replace('\n', ' '))
        with open(output_file, 'a') as f:
            # for answer1 in answers:
            f.write(pre_sql.replace('\n', ' ') + '\n')


if __name__ == '__main__':
    # 创建 ArgumentParser 对象
    # parser = argparse.ArgumentParser()

    # # 添加命令行选项

    # parser.add_argument("--start_index", type=int, default=0)
    # parser.add_argument("--ppl_file", type=str, default="src/information/ppl_dev.json")
    # parser.add_argument("--sql_4_output", type=str, default="src/sql_log/final_sql.txt")
    # parser.add_argument("--sql_refinement", type=str, default="src/sql_log/step_3_binary.txt")

    # 解析命令行参数
    # args = parser.parse_args()
    
    ppl_file = 'files/ppl_dev.json'
    # sql_refinement = 'files/step_3_sql.txt'
    # sql_refinement = 'files/gemini_2_flash_step_3.txt'
    sql_refinement = 'files/gemini_1.5_pro_step_3.txt'
    sql_4_output = 'files/gemini_1.5_pro_static_feedback.txt'
    start_index = 1583
    end_index = 2146
    
    for i in range(start_index,end_index+1):
        main(ppl_file,sql_refinement,sql_4_output,i,i)
        time.sleep(0.03)
