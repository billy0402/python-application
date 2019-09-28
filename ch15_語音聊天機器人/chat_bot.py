import chat_bot_module

question_dict = {'你是誰': '我是機器人', '聽不懂': '請再說一次問題'}
question = chat_bot_module.bot_listen()
print(f'question: {question}')

if question in question_dict:
    answer = question_dict[question]
    print(f'answer: {answer}')
    chat_bot_module.bot_speak(answer, 'zh-tw')
else:
    keyword = chat_bot_module.bot_get_google(question)
    content = chat_bot_module.bot_get_wiki(keyword)
    if content:
        chat_bot_module.bot_speak_re(content)
    else:
        print('找不到相關的維基百科資料')
        chat_bot_module.bot_speak('找不到相關的維基百科資料', 'zh-tw')
