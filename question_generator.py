import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_question_paper(one_mark_qs, two_mark_qs, five_mark_qs, num_questions_1, num_questions_2, num_questions_5):
    selected_questions = {
        '1 mark': one_mark_qs.sample(n=num_questions_1).tolist(),
        '2 marks': two_mark_qs.sample(n=num_questions_2).tolist(),
        '5 marks': five_mark_qs.sample(n=num_questions_5).tolist()
    }
    return selected_questions

def create_pdf(questions):
    pdf_filename = 'question_paper.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    y_position = 750  # Starting y-position for questions

    for category, qs in questions.items():
        c.drawString(100, y_position, f"{category} Questions:")
        y_position -= 20  # Move the y-position up
        for q in qs:
            c.drawString(120, y_position, q)
            y_position -= 15  # Move the y-position up for the next question
        y_position -= 30  # Add extra space between categories

    c.save()
    return pdf_filename

def main():
    st.title('Question Paper Generator')

    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx'])

    if uploaded_file is not None:
        excel_data = pd.read_excel(uploaded_file)
        excel_data = excel_data.fillna('')
        
        one_mark_questions = excel_data['1 mark']
        two_mark_questions = excel_data['2 marks']
        five_mark_questions = excel_data['5 marks']

        num_questions_1_mark = st.selectbox("Select number of questions for 1 mark", list(range(1, 11)), index=2)
        num_questions_2_marks = st.selectbox("Select number of questions for 2 marks", list(range(1, 11)), index=2)
        num_questions_5_marks = st.selectbox("Select number of questions for 5 marks", list(range(1, 11)), index=2)

        if st.button('Generate Questions'):
            selected_questions = generate_question_paper(
                one_mark_questions, two_mark_questions, five_mark_questions,
                num_questions_1_mark, num_questions_2_marks, num_questions_5_marks
            )
            st.write("Selected Questions:")
            for category, qs in selected_questions.items():
                st.write(f"{category} Questions:")
                for q in qs:
                    st.write(f"- {q}")


            st.write('### Edit or Add New Questions:')
            edited_questions = {}
            edited_questions['1 mark'] = st.text_area("Edit or Add 1 mark questions", '\n'.join(selected_questions['1 mark']))
            edited_questions['2 marks'] = st.text_area("Edit or Add 2 marks questions", '\n'.join(selected_questions['2 marks']))
            edited_questions['5 marks'] = st.text_area("Edit or Add 5 marks questions", '\n'.join(selected_questions['5 marks']))

            # if st.button('Regenerate Question Paper'):
            #     selected_questions = {
            #         '1 mark': edited_questions['1 mark'].split('\n'),
            #         '2 marks': edited_questions['2 marks'].split('\n'),
            #         '5 marks': edited_questions['5 marks'].split('\n')
            #     }
            st.write("Question Paper Regenerated!")
                
            pdf_filename = create_pdf(selected_questions)
            st.download_button(
                    label="Download Question Paper",
                    data=open(pdf_filename, 'rb').read(),
                    file_name="question_paper.pdf",
                    mime="application/pdf"
                )

if __name__ == "__main__":
    main()
