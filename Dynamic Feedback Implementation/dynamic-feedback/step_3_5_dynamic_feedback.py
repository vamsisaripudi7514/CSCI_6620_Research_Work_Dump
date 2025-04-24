from files.self_correction_gpt import GPT as model
from files.internal_configs.Instruction import DYNAMIC_FEEDBACK_PROMPT
def get_dynamic_feedback(table_info, result):
    gpt = model()
    prompt = DYNAMIC_FEEDBACK_PROMPT+table_info + result
    feedback = gpt(prompt=prompt)
    print(feedback)
    return feedback
    