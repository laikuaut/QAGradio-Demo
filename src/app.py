import re

import gradio as gr


def copy(source_text: str) -> str:
    """_summary_

    Args:
        source_text (str): _description_

    Returns:
        str: _description_
    """
    return source_text


def trim(text):
    return text.strip().replace('"', "")


def norm(text):
    return text.replace('"', "")


def convert(source_text, answer_text):
    # print(type(source_text))
    source_text = source_text.strip()
    answers = answer_text.strip().split("\n")
    for i, (j, answer) in enumerate(
        sorted(enumerate(answers, start=1), key=lambda x: x[1], reverse=True)
    ):
        source_text = re.sub(re.escape(answer), f"({j})", source_text)
        # time.sleep(0.1)
        if i == (len(answers) - 1):
            yield source_text
        else:
            yield source_text + "\n\n" + ".." * (i + 1)


def revert(source_text, answer_text):
    source_text = source_text.strip()
    answers = answer_text.strip().split("\n")
    for i, answer in enumerate(answers, start=1):
        source_text = re.sub(f"\\({i}\\)", answer, source_text)
        if i == (len(answers)):
            yield source_text
        else:
            yield source_text + "\n\n" + ".." * (i + 1)


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            source_text = gr.Textbox(
                label="原文", placeholder="原文を入力してください", lines=2
            )
            answer_text = gr.Textbox(
                label="問題の回答", placeholder="問題の回答を改行区切りで入力してください", lines=2
            )

        question_text = gr.Textbox(
            label="穴埋め問題",
            placeholder="穴埋め問題文が出力されます",
            show_copy_button=True,
            lines=7,
        )

    with gr.Row():
        create = gr.Button("穴埋め問題を作成する")
        reverse = gr.Button("穴埋め文を元に戻す")

    clear = gr.ClearButton([source_text, answer_text, question_text])

    source_text.change(trim, source_text, source_text, queue=False)
    answer_text.change(norm, answer_text, answer_text, queue=False)

    create.click(
        fn=convert, inputs=[source_text, answer_text], outputs=question_text
    )
    reverse.click(
        fn=revert, inputs=[source_text, answer_text], outputs=question_text
    )

if __name__ == "__main__":
    demo.queue()
    demo.launch()
