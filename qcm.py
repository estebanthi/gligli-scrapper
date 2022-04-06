

class QCM:

    def __init__(self, raw_qcm, category, theme=None):

        question_text = raw_qcm['question'].get_text()
        self.question = self.format_text(question_text)

        self.linked_image = raw_qcm['linked_image']

        responses = [response.get_text() for response in raw_qcm['responses']]
        good_response = raw_qcm['good_response'].get_text()
        self.responses = [self.format_text(response) for response in responses + [good_response]]
        self.good_response = self.format_text(good_response)

        correction = raw_qcm['correction'].get_text()
        self.correction = self.format_text(correction)

        self.correction_image = raw_qcm['correction_image']

        self.category = category
        self.theme = theme

    def __repr__(self):
        return f"{self.question} (question image : {self.linked_image}): \n" + "\n".join(self.responses) + \
               f"Good response : {self.good_response}\n\nCorrection : {self.correction}\n" \
               f"Correction image : {self.correction_image}"

    def get_json(self):
        return {'question': self.question, 'linked_image': self.linked_image, 'responses': self.responses,
                'good_response': self.good_response, 'correction': self.correction,
                'correction_image': self.correction_image, 'category': self.category, 'theme': self.theme}

    @staticmethod
    def format_text(text):
        text = text.replace('Ã©', 'é').replace('Ã¨', 'è').replace('Ã ', 'à').replace('Ã¯', 'ï').replace('Ã®', 'î') \
            .replace('Ãª', 'ê').replace('Ã§', 'ç').replace('Ã´', 'ô')
        return text
