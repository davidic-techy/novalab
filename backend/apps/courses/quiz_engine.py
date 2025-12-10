class QuizEngine:
    """
    Service to calculate scores for student submissions.
    """
    
    @staticmethod
    def grade_submission(lesson, student_answers):
        """
        lesson: The Lesson model instance (must be type QUIZ).
        student_answers: Dict of {question_id: selected_option_key}
        
        Returns: (score_percentage, results_details)
        """
        questions = lesson.questions.all()
        total_questions = questions.count()
        
        if total_questions == 0:
            return 0, []

        correct_count = 0
        results = []

        for question in questions:
            # Get the student's answer for this question ID (converted to string)
            student_selection = student_answers.get(str(question.id))
            is_correct = (student_selection == question.correct_answer)
            
            if is_correct:
                correct_count += 1
            
            results.append({
                "question_id": question.id,
                "is_correct": is_correct,
                "correct_answer": question.correct_answer 
                # Don't send correct answer back if you want them to retry blindly!
            })

        score = (correct_count / total_questions) * 100
        return round(score, 2), results