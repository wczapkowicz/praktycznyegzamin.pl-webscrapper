from selenium import webdriver
from selenium.webdriver.common.by import By

import urllib.request
import json


class Question:

    def __init__(self, q_id: int = 0, q_title: str = '', q_answers: dict = {}, correct_answer: str = '', img_url: \
            str | bool = False):
        if q_answers is None:
            q_answers = {str, str}
        self.question_id = q_id
        self.question_title = q_title
        self.question_answers = q_answers
        self.correct_answer = correct_answer
        self.image_link = img_url


def main():
    driver = webdriver.Chrome()

    driver.get(url)

    raw_questions_objs = driver.find_elements(by=By.CLASS_NAME, value='question')

    question_objects = []

    for obj in raw_questions_objs:

        heading = obj.find_element(by=By.CLASS_NAME, value='title').text

        id, title = heading.split('. ', 1)

        answers = {}
        [answers.update({n.text.split(". ", 1)[0]: n.text.split(". ", 1)[1]})
         for n in obj.find_elements(by=By.CLASS_NAME, value='answer')]

        correct_answer = obj.find_element(by=By.CLASS_NAME, value='correct').text.split('. ', 1)[0]

        if len(obj.find_elements(by=By.TAG_NAME, value='img')) > 0:
            image = obj.find_element(by=By.TAG_NAME, value='img').get_attribute('src')
            print(f'===> Saving image for question no. {id}')
            urllib.request.urlretrieve(image, f'images/{image_folder_name}/{id}.png')
            img_url = f'images/{image_folder_name}/{id}.png'
        else:
            img_url = None

        print(f'Getting question no. {id}')
        question_objects.append(Question(id, title, answers, correct_answer, img_url))

    print('done.')
    driver.close()

    with open(questions_json_file, 'w') as file:
        file.write(json.dumps([question_objects[n].__dict__ for n in range(len(question_objects))], ensure_ascii=False))


if __name__ == '__main__':
    url = 'https://www.praktycznyegzamin.pl/inf03ee09e14/teoria/wszystko/'
    image_folder_name =  'inf03'
    questions_json_file = 'questions.json'
    main()
