import re

import gradio as gr
import MeCab

wakati = MeCab.Tagger("-Owakati")
tagger = MeCab.Tagger()
re_hiragana = re.compile("[\u3041-\u309F]+")


def copy(source_text: str) -> str:
    return source_text


def trim(text):
    return text.strip().replace('"', "")


def norm(text):
    return text.replace('"', "")


def convert(source_text, answer_text):
    source_text = source_text.strip()
    answers = answer_text.strip().split("\n")
    for i, (j, answer) in enumerate(
        sorted(enumerate(answers, start=1), key=lambda x: x[1], reverse=True)
    ):
        source_text = re.sub(re.escape(answer), f"({j})", source_text)
        if i == (len(answers) - 1):
            yield source_text
        else:
            yield source_text + "\n\n" + ".." * (i + 1)


def convert_md(source_text, answer_text):
    source_text = source_text.strip()
    answers = answer_text.strip().split("\n")
    for i, (j, answer) in enumerate(
        sorted(enumerate(answers, start=1), key=lambda x: x[1], reverse=True)
    ):
        source_text = re.sub(
            re.escape(answer),
            f'<strong><span style="color:#0000ff">{answer}</span></strong>',
            source_text,
        )
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


def remove_duplicate_list(words):
    remove_count = 0
    tmp_words = words.copy()
    for i, word in enumerate(tmp_words):
        if word in tmp_words[0:i]:
            print(f"remove_duplicate: {word}")
            words.pop(i - remove_count)
            remove_count += 1


def remove_word_conditions(words):
    tmp_words = words.copy()
    for word in tmp_words:
        if re_hiragana.fullmatch(word):
            print(f"remove_conditions: {word}")
            words.remove(word)


def extract_works(source_text):
    if not source_text:
        return

    # last_hinshi1 = ""
    last_hinshi2 = ""
    node = tagger.parseToNode(source_text)
    words = []
    while node:
        hinshi1 = node.feature.split(",")[0]
        hinshi2 = node.feature.split(",")[1]
        print(f"{node.surface}: {hinshi1}-{hinshi2}")
        if last_hinshi2 == "普通名詞":
            if hinshi1 == "接尾辞" or hinshi2 == "普通名詞":
                words[-1] += node.surface
        elif hinshi2 == "普通名詞":
            words.append(node.surface)

        node = node.next
        # last_hinshi1 = hinshi1
        last_hinshi2 = hinshi2

    remove_duplicate_list(words)
    remove_word_conditions(words)
    return "\n".join(words)


with gr.Blocks() as demo:
    source_text = gr.Textbox(label="原文", placeholder="原文を入力してください", lines=2)
    with gr.Row():
        auto_markdown = gr.Markdown(label="ハイライト")
        auto_answer_text = gr.Textbox(
            label="回答の候補",
            placeholder="回答とする単語候補を出力します",
            lines=10,
            show_copy_button=True,
        )

        auto_question_text = gr.Textbox(
            label="穴埋め問題(自動)",
            placeholder="候補を元に穴埋め問題文が出力されます",
            show_copy_button=True,
            lines=10,
        )

    with gr.Row():
        text_markdown = gr.Markdown(label="ハイライト")
        answer_text = gr.Textbox(
            label="問題の回答",
            placeholder="問題の回答を改行区切りで入力してください",
            lines=10,
            show_copy_button=True,
        )
        question_text = gr.Textbox(
            label="穴埋め問題",
            placeholder="穴埋め問題文が出力されます",
            show_copy_button=True,
            lines=10,
        )

    with gr.Row():
        create = gr.Button("穴埋め問題を作成する")
        reverse = gr.Button("穴埋め文を元に戻す")

    clear = gr.ClearButton([source_text, answer_text, question_text])

    source_text.change(trim, source_text, source_text, queue=False)
    answer_text.change(norm, answer_text, answer_text, queue=False)

    source_text.change(
        extract_works, source_text, auto_answer_text, queue=False
    )
    auto_answer_text.change(
        convert, [source_text, auto_answer_text], auto_question_text
    )
    auto_answer_text.change(
        convert_md, [source_text, auto_answer_text], auto_markdown
    )

    answer_text.change(convert, [source_text, answer_text], question_text)
    answer_text.change(convert_md, [source_text, answer_text], text_markdown)
    create.click(
        fn=convert, inputs=[source_text, answer_text], outputs=question_text
    )
    create.click(
        fn=convert_md, inputs=[source_text, answer_text], outputs=text_markdown
    )
    reverse.click(
        fn=revert, inputs=[source_text, answer_text], outputs=question_text
    )

if __name__ == "__main__":
    demo.queue()
    demo.launch()
