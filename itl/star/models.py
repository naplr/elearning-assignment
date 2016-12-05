from django.db import models

import json

class SessionInfo(models.Model):
    sid = models.CharField(max_length=128, primary_key=True)
    vid_1 = models.BooleanField(default=False)
    read_1 = models.BooleanField(default=False)
    quiz_1 = models.BooleanField(default=False)
    quiz_1_passed = models.BooleanField(default=False)
    vid_2 = models.BooleanField(default=False)
    read_2 = models.BooleanField(default=False)
    quiz_2 = models.BooleanField(default=False)
    quiz_2_passed = models.BooleanField(default=False)

    answers = models.CharField(max_length=256)

    def set_answers(self, a):
        self.answers = json.dumps(a)

    def get_answers(self):
        return list(json.loads(self.answers))


    def get_not_available_ids(self):
        id_maps = {
            'vid_1': '#nav-vid-1',
            'read_1': '#nav-read-1',
            'quiz_1': '#nav-quiz-1',
            'vid_2': '#nav-vid-2',
            'read_2': '#nav-read-2',
            'quiz_2': '#nav-quiz-2',
        }

        li = []
        if not self.vid_1:
            li.append(id_maps['vid_1'])
        if not self.read_1:
            li.append(id_maps['read_1'])
        if not self.quiz_1:
            li.append(id_maps['quiz_1'])
        if not self.vid_2:
            li.append(id_maps['vid_2'])
        if not self.read_2:
            li.append(id_maps['read_2'])
        if not self.quiz_2:
            li.append(id_maps['quiz_2'])

        return li


    def __str__(self):
        return sid
