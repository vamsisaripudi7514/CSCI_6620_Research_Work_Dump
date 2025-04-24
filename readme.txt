This GitHub repository has all the files related to the research being performed as part of the CSCI 6620 Course.

-> The baseline implementation folder has the baseline research codebase and their research paper.
-> The Literature Review folder has the PDFs of all the references studied as part of the research process.
-> Oral Presentation folder has all the images/graphical elements used, along with the final PPT and PDF generated.
-> The Poster Presentation folder has all the draw.io XML files for the created diagrams, logos used, and the final poster PPT and PDF files.

-> The Dynamic Feedback Implementation folder has the codebase developed for the current research using the baseline research code snippets.
	-> Inside the folder we have the following files and folders:
        ->	Step_4_static_correction.py performs iterative refinement using the static feedback approach.
        ->	Step_4_self_correction.py that performs iterative refinement using the dynamic feedback approach.
        ->	Step_3_5_dynamic_feedback.py that has a method implementation to get the dynamic feedback for the given inputs.
        ->	Inside the files folder, there are various files and folders;
            ->	Internal_configs: This subfolder holds configuration files such as: 
                ->	config.py: Contains API keys and LLM configuration used for experimentation.
                ->	extract.json: Used for extracting JSON values from LLM outputs. 
                ->	Instruction.py: Contains prompts for SQL generation, static feedback, dynamic feedback generation, and query refinement.
            ->	Evaluation_script.py: This file is used to calculate the execution accuracy of the generated queries.
            ->	Text files: They contain outputs for each model, for both static and dynamic feedback loops, along with the base queries.
            ->	ppl_dev.json: Contains records of the test split of the SPIDER dataset formatted as JSON objects. 
