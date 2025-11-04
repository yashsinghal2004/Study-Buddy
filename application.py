import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helpers import *
from src.generator.question_generator import QuestionGenerator


load_dotenv()

def main():
    st.set_page_config(page_title="Study Buddy AI", page_icon="")

    if 'quiz_manager' not in st.session_state: # in session states when submit button is clicked the data will be erased and to avoid that we use session states
        st.session_state.quiz_manager=QuizManager() #obj of the quiz manager class

    if 'quiz_generated' not in st.session_state: # special type of variables that dont get affected by refreshing of streamlit
        st.session_state.quiz_generated=False

    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted=False  

    if 'rerun_trigger' not in st.session_state: #whenever the new option or anything is selected the reload is done and handled by session state
        st.session_state.rerun_trigger=False  

    st.title("Study Buddy")

    st.sidebar.header("Quiz Settings")

    question_type=st.sidebar.selectbox(
        "Select Question Type",
        ["Multiple Choice","Fill in the Blank"],
        index=0
    )

    topic=st.sidebar.text_input("Enter Topic", placeholder="Java, Python, Typescript")

    difficulty=st.sidebar.selectbox(
        "Difficulty Level",
        ["Easy","Medium","Hard"],
        index=1
    )

    num_questions=st.sidebar.number_input(
        "Number of Questions",
        min_value=1, max_value=10, value=5
    )





    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_submitted=False

        generator=QuestionGenerator()
        success=st.session_state.quiz_manager.generate_questions(
            generator,
            topic,
            question_type,difficulty,num_questions
        )     

        st.session_state.quiz_generated=success # bydaufault was false now success
        rerun() #imp as we need changes on the UI now after clicking on generate quiz button

    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.header("Quiz")
        st.session_state.quiz_manager.attempt_quiz() #storing them in user answers array mentioned in helper func

        if st.button("Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted=True #once submitted we use evaluate quiz method 
            rerun()

    
    if st.session_state.quiz_submitted:
        st.header("Quiz Results")
        results_df=st.session_state.quiz_manager.generate_result_dataframe()

        if not results_df.empty:
            correct_count=results_df['is_correct'].sum()
            total_questions=len(results_df)
            score_percentage=(correct_count/total_questions)*100
            st.write(f"Score : {score_percentage}")

            for _, result in results_df.iterrows(): #iterating over each question
                question_num=result['question_number']
                if result['is_correct']: #if ans correct showing message
                    st.success(f"✅ Question {question_num} : {result['question']}")
                else:
                    st.error(f"❌ Question {question_num} : {result['question']}")
                    st.write(f"Your answer : {result['user_answer']}")
                    st.write(f"Correct answer : {result['correct_answer']}")

                st.markdown("---------")


            if st.button("Save Results"):
                saved_files=st.session_state.quiz_manager.save_to_csv()#using from helper func 
                if saved_files:
                    with open(saved_files,'rb') as f:
                        st.download_button(
                            label="Download Results",
                            data=f.read(),
                            file_name=os.path.basename(saved_files),
                            mime='text/csv'
                        ) # since it is last method no need to rerun method
                else:
                    st.warning("No results available")


if __name__=="__main__":
        main()