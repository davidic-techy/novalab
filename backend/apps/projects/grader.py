import re

class ProjectAutoGrader:
    """
    Analyzes project artifacts against the grading rubric.
    """
    
    @staticmethod
    def grade(project):
        """
        Returns (score, feedback_string)
        """
        rubric = project.template.grading_config
        files = project.artifact_data
        
        score = 0
        total_possible = 100
        feedback = []

        # 1. Check for Required Files
        required_files = rubric.get('required_files', [])
        for filename in required_files:
            if filename in files:
                score += 10
                feedback.append(f"✅ Found {filename}")
            else:
                feedback.append(f"❌ Missing {filename}")

        # 2. Check for Keywords (Simple Static Analysis)
        # e.g. rubric: {"keywords": ["def ", "class ", "import pandas"]}
        code_content = "\n".join(files.values())
        keywords = rubric.get('required_keywords', [])
        
        for keyword in keywords:
            if keyword in code_content:
                score += 5
                feedback.append(f"✅ Used concept: {keyword}")
            else:
                feedback.append(f"⚠️ Missing concept: {keyword}")

        # Cap score at 100
        final_score = min(score, total_possible)
        
        return final_score, "\n".join(feedback)