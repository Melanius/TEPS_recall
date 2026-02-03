import streamlit as st
import os
import sys
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import DataLoader
from data_loader import DataLoader
from quiz_manager import VocabularyQuiz, GrammarQuiz, ListeningQuiz

# --- Page Config ---
st.set_page_config(
    page_title="TEPS Remember",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Mobile & Aesthetics ---
st.markdown("""
<style>
    /* Global Font & Background */
    .stApp {
        background-color: #f0f2f6; 
    }
    
    /* Card Style */
    .css-1r6slb0, .css-12oz5g7 { 
        padding: 1rem;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        font-size: 18px;
        border: 1px solid #d1d5db;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
        background-color: white;
        color: #333;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-color: #4CAF50;
        color: #4CAF50;
    }
    
    .stButton > button:active {
        background-color: #e5e7eb;
        transform: translateY(1px);
    }

    /* Question Card */
    .question-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
        border-left: 5px solid #6C63FF;
    }
    
    .question-text {
        font-size: 28px;
        font-weight: bold;
        color: #1f2937;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    
    .meaning-text {
        font-size: 16px;
        color: #6b7280;
    }

    /* Progress Bar Color */
    .stProgress > div > div > div > div {
        background-color: #6C63FF;
    }
    
    /* Result Cards */
    .result-card-correct {
        background-color: #ecfdf5;
        border: 1px solid #10b981;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 5px;
    }
    
    .result-card-wrong {
        background-color: #fef2f2;
        border: 1px solid #ef4444;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- State Management ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'quiz_instance' not in st.session_state:
    st.session_state.quiz_instance = None
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'wrong_answers' not in st.session_state:
    st.session_state.wrong_answers = [] # Stores dicts of wrong questions
if 'mode' not in st.session_state:
    st.session_state.mode = None
if 'user_answered' not in st.session_state:
    st.session_state.user_answered = False
if 'last_feedback' not in st.session_state:
    st.session_state.last_feedback = None

# --- Helper Functions ---
def reset_quiz():
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.wrong_answers = []
    st.session_state.user_answered = False
    st.session_state.last_feedback = None

def go_home():
    st.session_state.page = 'home'
    st.session_state.quiz_instance = None

def start_quiz(loader, file_list, mode, num_q):
    if not file_list:
        st.error("파일을 선택해주세요.")
        return

    # Combine data from all selected files (Scalability for test-1 + test-2)
    # Ensure file_list is a list
    if isinstance(file_list, str):
        file_list = [file_list]
        
    all_data = []
    for f in file_list:
        if mode == 'vocabulary':
            all_data.extend(loader.load_vocabulary(f))
        elif mode == 'grammar':
            all_data.extend(loader.load_grammar(f))
        elif mode == 'reading':
            all_data.extend(loader.load_reading(f))
        else:
            all_data.extend(loader.load_listening(f))
    
    if len(all_data) < 4 and (mode == 'vocabulary' or mode == 'reading'):
        st.error("데이터가 너무 적습니다 (최소 4개 이상 필요).")
        return
    
    if mode == 'vocabulary' or mode == 'reading':
        quiz = VocabularyQuiz(all_data)
    elif mode == 'grammar':
        quiz = GrammarQuiz(all_data)
    else:
        quiz = ListeningQuiz(all_data)
        
    quiz.prepare_quiz(num_q)
    
    st.session_state.quiz_instance = quiz
    st.session_state.mode = mode
    reset_quiz()
    # Reset specific listening state
    st.session_state.show_answer = False
    st.session_state.page = 'quiz'
    st.rerun()

# --- Screens ---

def render_home(loader):
    st.title("🧠 TEPS Remember")
    st.caption("Customizable Quiz Master")
    
    st.markdown("### 🎯 Choose Your Mode")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📘 어휘 (Vocabulary)", use_container_width=True):
            st.session_state.mode = 'vocabulary'
            st.session_state.page = 'setup'
            st.rerun()
            
    with col2:
        if st.button("📗 문법 (Grammar)", use_container_width=True):
            st.session_state.mode = 'grammar'
            st.session_state.page = 'setup'
            st.rerun()

    st.markdown("---")
    if st.button("🎧 청해 (Listening) - Flashcard Mode", use_container_width=True):
        st.session_state.mode = 'listening'
        st.session_state.page = 'setup'
        st.rerun()

    if st.button("📖 독해 (Reading)", use_container_width=True):
        st.session_state.mode = 'reading'
        st.session_state.page = 'setup'
        st.rerun()

def render_setup(loader):
    st.title("⚙️ Quiz Setup")
    
    mode = st.session_state.mode
    
    if mode == 'vocabulary':
        dir_name = 'vocabulary'
        files = loader.get_vocabulary_files()
    elif mode == 'grammar':
        dir_name = 'grammar'
        files = loader.get_grammar_files()
    elif mode == 'reading':
        dir_name = 'reading'
        files = loader.get_reading_files()
    else: # listening
        dir_name = 'listening'
        files = loader.get_listening_files()
        
    if not files:
        st.error(f"No files found in data/{dir_name}")
        if st.button("Back"):
            go_home()
            st.rerun()
        return

    # File Selection (Multi-select allowed)
    file_map = {os.path.basename(f): f for f in files}
    selected_names = st.multiselect(
        "Select Test Files", 
        list(file_map.keys()),
        default=[list(file_map.keys())[0]]
    )
    
    selected_files = [file_map[name] for name in selected_names]
    
    # Calculate max questions
    total_items = 0
    for f in selected_files:
        if mode == 'vocabulary':
            total_items += len(loader.load_vocabulary(f))
        elif mode == 'grammar':
            total_items += len(loader.load_grammar(f))
        elif mode == 'reading':
            total_items += len(loader.load_reading(f))
        else:
            total_items += len(loader.load_listening(f))
            
    num_q = st.slider("Number of Questions", min_value=1, max_value=total_items if total_items > 0 else 1, value=min(10, total_items))
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("⬅️ Back"):
            go_home()
            st.rerun()
    with col2:
        if st.button("🚀 Start Quiz!", type="primary", use_container_width=True):
            start_quiz(loader, selected_files, mode, num_q)

def render_quiz():
    quiz = st.session_state.quiz_instance
    idx = st.session_state.current_idx
    
    # Finished?
    if idx >= len(quiz.questions):
        st.session_state.page = 'result'
        st.rerun()
        return

    q = quiz.get_question(idx)
    total = len(quiz.questions)
    
    # Progress Bar
    progress = (idx / total)
    st.progress(progress)
    st.caption(f"Question {idx+1} / {total} | Score: {st.session_state.score}")

    # Question Card
    st.markdown(f"""
    <div class="question-card">
        <div class="meaning-text">What is the meaning (or answer)?</div>
        <div class="question-text">{q['text']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hint (Grammar Only)
    if st.session_state.mode == 'grammar':
        with st.expander("💡 Show Hint"):
            st.info(f"Meaning: {q.get('meaning', 'No hint available')}")

    # Answer Logic
    def handle_answer(option_idx):
        correct = (option_idx == q['correct_index'])
        if correct:
            st.session_state.score += 1
            st.session_state.last_feedback = "correct"
            st.balloons()
        else:
            st.session_state.wrong_answers.append(q)
            st.session_state.last_feedback = "wrong"
            st.toast(f"❌ Wrong! Review: {q['options'][q['correct_index']]}", icon="❌")
        
        # Move to next
        time.sleep(0.5) # Short delay to see click effect
        st.session_state.current_idx += 1
        st.rerun()

    # Layout Options
    if st.session_state.mode == 'listening':
        # Flashcard Mode UI
        if 'show_answer' not in st.session_state:
            st.session_state.show_answer = False
            
        if not st.session_state.show_answer:
            st.markdown(f"""
            <div style="text-align: center; margin: 20px;">
                <h2 style="color: #6C63FF;">Thinking Time... 💭</h2>
            </div>
            """, unsafe_allow_html=True)
            if st.button("👀 답변 보기 (Show Answer)", type="primary", use_container_width=True):
                st.session_state.show_answer = True
                st.rerun()
        else:
            # Show Answer and Rating
            st.markdown(f"""
            <div class="result-card-correct" style="text-align: center;">
                <h3>{q['meaning']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("❌ 몰랐음 (Again)", use_container_width=True):
                    # Treat as wrong
                    st.session_state.wrong_answers.append(q)
                    st.session_state.last_feedback = "wrong"
                    st.session_state.show_answer = False
                    st.session_state.current_idx += 1
                    st.rerun()
            with c2:
                if st.button("⭕ 알았음 (Easy)", use_container_width=True):
                     # Treat as correct
                    st.session_state.score += 1
                    st.session_state.last_feedback = "correct"
                    st.session_state.show_answer = False
                    st.session_state.current_idx += 1
                    st.rerun()
                    
    else: # Vocab or Grammar
        options = q['options']
        
        if len(options) == 4:
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"1. {options[0]}", use_container_width=True): handle_answer(0)
                if st.button(f"3. {options[2]}", use_container_width=True): handle_answer(2)
            with c2:
                if st.button(f"2. {options[1]}", use_container_width=True): handle_answer(1)
                if st.button(f"4. {options[3]}", use_container_width=True): handle_answer(3)
        else:
            # Standard vertical or side-by-side
            cols = st.columns(len(options))
            for i, opt in enumerate(options):
                with cols[i]:
                    if st.button(opt, use_container_width=True): handle_answer(i)

    # Stop Button
    st.markdown("---")
    if st.button("🚫 Quit Quiz"):
        go_home()
        st.rerun()

def render_result():
    st.title("🏆 Quiz Finished!")
    
    score = st.session_state.score
    total = len(st.session_state.quiz_instance.questions)
    percentage = int((score / total) * 100)
    
    # Score Display
    st.metric("Final Score", f"{score} / {total}", f"{percentage}%")
    
    if percentage == 100:
        st.balloons()
        st.success("Perfect! You are a master! 🎉")
    elif percentage >= 80:
        st.info("Great job! Keep it up! 👍")
    else:
        st.warning("Keep practicing! You can do it! 💪")
        
    # Wrong Answers / Note
    wrong_list = st.session_state.wrong_answers
    if wrong_list:
        st.subheader("📝 Wrong Answer Note")
        
        for w in wrong_list:
            if w['options'] and w['correct_index'] >= 0:
                correct_ans = w['options'][w['correct_index']]
                meaning_display = w.get('meaning', '-')
            else:
                # Listening mode (Flashcard) - Answer is the meaning itself
                correct_ans = w.get('meaning', '-')
                meaning_display = "" # Don't show meaning twice

            st.markdown(f"""
            <div class="result-card-wrong">
                <b>Question:</b> {w['text']} <br>
                <b>Correct Answer:</b> {correct_ans} <br>
                {f'<small>Meaning: {meaning_display}</small>' if meaning_display else ''}
            </div>
            """, unsafe_allow_html=True)
            
        if st.button("🔄 Retry Wrong Answers Only"):
            # Create a new quiz with only wrong questions
            # We need to reconstruct the format Expected by Quiz Classes? 
            # Actually, we can just reset the quiz instance with these questions.
            # But the Quiz Class 'data' vs 'questions' structure is different.
            # Easier way: Just inject these questions directly into a new quiz instance.
            
            # Simple hack: Just restart the loop with these specific questions
            # But QuizManager randomly picks from DATA.
            # So let's extract the 'data-like' items from the wrong questions.
            
            # Reconstruct 'item' from question to pass to prepare_quiz is hard because distractors are lost.
            # Better specific logic:
            new_quiz = st.session_state.quiz_instance
            new_quiz.questions = wrong_list # Just reuse the prepared questions
            # Shuffle them?
            import random
            random.shuffle(new_quiz.questions)
            
            st.session_state.quiz_instance = new_quiz
            reset_quiz()
            st.session_state.page = 'quiz'
            st.rerun()
            
    else:
        st.markdown("""
        <div class="result-card-correct">
            No wrong answers! Perfect score!
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🏠 Return Home", type="primary"):
        go_home()
        st.rerun()

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loader = DataLoader(base_dir)
    
    if st.session_state.page == 'home':
        render_home(loader)
    elif st.session_state.page == 'setup':
        render_setup(loader)
    elif st.session_state.page == 'quiz':
        render_quiz()
    elif st.session_state.page == 'result':
        render_result()

if __name__ == "__main__":
    main()
