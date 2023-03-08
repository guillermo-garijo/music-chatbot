class User:
    def __init__(self):
        self.question_answers={}
    def setQuestionAnswer(self, question, n_response):
        self.question_answers[question]=n_response
    def printUser(self):
        print(self.question_answers)