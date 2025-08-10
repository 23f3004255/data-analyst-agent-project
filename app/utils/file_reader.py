
def read_question_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        # print(f.read().strip())
        return f.read().strip()


# if __name__ == "__main__":
#     text=read_question_file("../../data/questions.txt")
#     q=extract_questions(text)
#     for x in q:
#         print(x)