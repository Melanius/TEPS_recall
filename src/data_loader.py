import csv
import os
import glob

class DataLoader:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def get_vocabulary_files(self):
        path = os.path.join(self.base_dir, 'data', 'vocabulary', '*.csv')
        return glob.glob(path)

    def get_grammar_files(self):
        path = os.path.join(self.base_dir, 'data', 'grammar', '*.csv')
        return glob.glob(path)

    def get_listening_files(self):
        path = os.path.join(self.base_dir, 'data', 'listening', '*.csv')
        return glob.glob(path)

    def get_reading_files(self):
        path = os.path.join(self.base_dir, 'data', 'reading', '*.csv')
        return glob.glob(path)

    def load_vocabulary(self, file_path):
        """
        Loads vocabulary data from a CSV file.
        Expected format: word, meaning
        Returns: strict list of dicts [{'word': '...', 'meaning': '...'}]
        """
        data = []
        encodings = ['utf-8-sig', 'cp949', 'euc-kr']
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    reader = csv.reader(f)
                    temp_data = []
                    for row in reader:
                        if len(row) >= 2:
                            word = row[0].strip()
                            meaning = row[1].strip()
                            # Skip header if present (common headers)
                            if word.lower() in ['word', 'term'] and meaning.lower() in ['meaning', 'definition', 'answer']:
                                continue
                            if word and meaning:
                                temp_data.append({'word': word, 'meaning': meaning})
                    data = temp_data
                    break # Success
            except UnicodeDecodeError:
                continue
            except Exception as e:
                # print(f"Error loading file {file_path} with {enc}: {e}")
                pass
                
        return data

    def load_grammar(self, file_path):
        """
        Loads grammar data from a CSV file.
        Expected format: word, answer, meaning
        Returns: list of dicts [{'word': '...', 'answer': '...', 'meaning': '...'}]
        """
        data = []
        encodings = ['utf-8-sig', 'cp949', 'euc-kr']
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    reader = csv.DictReader(f)
                    temp_data = []
                    for row in reader:
                        if ('word' in row or '\ufeffword' in row) and 'answer' in row: # Handle BOM manually if DictReader key has it, though utf-8-sig handles it.
                             # If utf-8-sig checks out, 'word' is clean. 
                             if 'word' in row:
                                temp_data.append({
                                    'word': row.get('word', '').strip(),
                                    'answer': row.get('answer', '').strip(),
                                    'meaning': row.get('meaning', '').strip()
                                })
                    if temp_data:
                        data = temp_data
                        break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                pass
        return data

    def load_listening(self, file_path):
        """
        Loads listening data from a CSV file.
        Expected format: sentence, meaning
        Returns: strict list of dicts [{'sentence': '...', 'meaning': '...'}]
        """
        data = []
        encodings = ['utf-8-sig', 'cp949', 'euc-kr']
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    reader = csv.reader(f)
                    temp_data = []
                    for row in reader:
                        if len(row) >= 2:
                            sentence = row[0].strip()
                            meaning = row[1].strip()
                            # Skip header if present
                            if sentence.lower() == 'sentence' and meaning.lower() == 'meaning':
                                continue
                            if sentence and meaning:
                                temp_data.append({'sentence': sentence, 'meaning': meaning})
                    if temp_data:
                        data = temp_data
                        break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                pass
        return data

    def load_reading(self, file_path):
        """
        Loads reading data (same format as vocabulary).
        """
        return self.load_vocabulary(file_path)
