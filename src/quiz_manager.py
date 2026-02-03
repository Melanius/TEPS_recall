import random

class VocabularyQuiz:
    def __init__(self, data):
        self.data = data
        self.questions = []
    
    def prepare_quiz(self, num_questions):
        """
        Selects questions and prepares options.
        """
        # Select random subset if requesting fewer than total
        if num_questions > len(self.data):
            num_questions = len(self.data)
        
        selected_items = random.sample(self.data, num_questions)
        
        self.questions = []
        for item in selected_items:
            correct_meaning = item['meaning']
            word = item['word']
            
            # Pick 3 distractors
            distractors = []
            while len(distractors) < 3:
                r = random.choice(self.data)
                if r['meaning'] != correct_meaning and r['meaning'] not in distractors:
                    distractors.append(r['meaning'])
            
            options = distractors + [correct_meaning]
            random.shuffle(options)
            
            correct_index = options.index(correct_meaning)
            
            self.questions.append({
                'text': word,
                'options': options,
                'correct_index': correct_index,
                'meaning': correct_meaning # Storing for review if needed
            })
            
    def get_question(self, index):
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None

class GrammarQuiz:
    def __init__(self, data):
        self.data = data
        self.questions = []
        # Fixed options for this specific grammar type (Gerund vs Infinitive)
        self.options = ["To-v (to 부정사)", "-ing (동명사)"]
        
    def prepare_quiz(self, num_questions):
        if num_questions > len(self.data):
            num_questions = len(self.data)
            
        selected_items = random.sample(self.data, num_questions)
        
        self.questions = []
        for item in selected_items:
            word = item['word']
            answer_type = item['answer'].lower() # 'to' or 'ing'
            meaning = item.get('meaning', '')
            
            correct_index = 0 if answer_type == 'to' else 1
            
            self.questions.append({
                'text': f"{word} [   ?   ]",
                'options': self.options,
                'correct_index': correct_index,
                'meaning': meaning,
                'word_only': word
            })

    def get_question(self, index):
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None

class ListeningQuiz:
    def __init__(self, data):
        self.data = data
        self.questions = []
    
    def prepare_quiz(self, num_questions):
        if num_questions > len(self.data):
            num_questions = len(self.data)
        
        # In listening mode, question IS the item itself (no distractors)
        selected_items = random.sample(self.data, num_questions)
        
        self.questions = []
        for item in selected_items:
            self.questions.append({
                'text': item['sentence'], # Map sentence to text for UI consistency
                'sentence': item['sentence'],
                'meaning': item['meaning'],
                'options': [], # No options in flashcard mode
                'correct_index': -1 
            })

    def get_question(self, index):
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None
