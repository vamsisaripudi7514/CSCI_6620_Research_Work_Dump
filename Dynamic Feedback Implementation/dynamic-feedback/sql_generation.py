from files.self_correction_gpt import GPT as model
from files.internal_configs.Instruction import SQL_GENERATION_INSTRUCTION
import json
from tqdm import tqdm
import time
def sql_generation(prompt):
    gpt = model()

    # question = ppl['question'].strip()
    # evidence = ppl['evidence'].strip()
    # example = ppl['example']
    # table_info += f'\n### sql_keywords: {word_aug["sql_keywords"]}\n'
    # table_info += f'### tables: {table_aug["tables"]}\n'
    # table_info += f'### columns: {table_aug["columns"]}\n'
    # table_info += f'### conditions: {cond_aug["conditions"]}'

    # table_info = example.strip() + '\n\n' + "### Answer the question by sqlite SQL query only and with no explanation. You must minimize SQL execution time while ensuring correctness.\n" + table_info.strip() + '\n\n' + '### definition: ' + evidence + "\n### Question: " + question

    # 3.4. thought_gpt
    answer = gpt(prompt=prompt)
    try:
        answer = json.loads(answer)
    except Exception as e:
        print(e)
        answer = answer.replace("\\", "\\\\")
        answer = json.loads(answer)
    sql = answer['sql'].replace('\n', ' ')
    return sql

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


def main(ppl_file, output_file, x=0, y=0):

    # 1.加载prompt信息 从0开始
    with open(ppl_file, 'r') as f:
        ppls = json.load(f)

    answers = []

    for i in tqdm(range(x, y+1)):
        # if i == 984 or i== 1570:
        #     answers.append('---None--')
        #     break
        prompt_message = SQL_GENERATION_INSTRUCTION
        message = []
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

        prompt_message += table_info
        SQL_QUERY = sql_generation(prompt_message)
        answers.append(SQL_QUERY)
    with open(output_file, 'a') as f:
        for answer in answers:
            f.write(answer + '\n')

    
if __name__ == '__main__':
    
    ppl_file = 'files/ppl_dev.json'
    # sql_refinement = 'files/step_3_sql.txt'
    sql_4_output = 'files/gemini_1.5_pro_step_3.txt'
    start_index = 1042
    end_index = 2146
    
    for i in range(start_index,end_index+1):
        main(ppl_file,sql_4_output,i,i)
        time.sleep(0.03)