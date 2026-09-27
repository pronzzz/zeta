import re

class Grader:
    def __init__(self, model_manager):
        self.model_manager = model_manager

    def grade(self, task, response, metadata):
        """
        Rule-based grading first (did it call the right skill, is a regex/field present);
        fall back to LLM-as-judge only for open-ended tasks.
        """
        expected_skill = task.get("expected_skill")
        pass_criteria = task.get("pass_criteria")
        
        # 1. Check if the expected skill was invoked
        used_skill = metadata.get("tool_used") or metadata.get("tool_denied")
        if expected_skill and used_skill != expected_skill:
            return False, f"Expected skill {expected_skill}, but used {used_skill}"

        # 2. Rule-based regex fallback (simple checks)
        if "numeric price" in pass_criteria:
            if re.search(r'\d+', response):
                return True, "Passed rule-based check: found numeric value"
        
        if "note" in pass_criteria and "created" in pass_criteria:
            if "created" in response.lower() or "saved" in response.lower():
                return True, "Passed rule-based check: note creation confirmed"
                
        # 3. LLM-as-judge fallback
        prompt = f"""
You are an expert judge grading an AI agent's response.
Task Input: {task['input']}
Pass Criteria: {pass_criteria}
Agent Response: {response}

Does the agent response meet the pass criteria? 
Answer with a single word: YES or NO.
"""
        try:
            judge_response = self.model_manager.generate(prompt, stream=False)
            if "YES" in judge_response.upper():
                return True, "Passed LLM judge"
            else:
                return False, f"Failed LLM judge: {judge_response}"
        except Exception as e:
            return False, f"Error in LLM judge: {e}"
