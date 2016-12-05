from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from star.models import SessionInfo

import uuid

# Create your views here.
def _get_session_info(request):
    sid = request.session['sid']
    s = SessionInfo.objects.get(sid=sid)

    return s


def _get_na_ids(request):
    s = _get_session_info(request)
    return s.get_not_available_ids()


def index(request):
    assert isinstance(request, HttpRequest)

    session_id = str(uuid.uuid1())
    request.session['sid'] = session_id

    s = SessionInfo(sid=session_id)
    s.save()

    return render(request, 'star/index.html', {})


def done(request):
    assert isinstance(request, HttpRequest)

    na_ids = _get_na_ids(request)
    return render(request, 'star/done.html', {'na_ids': na_ids})


def first_video(request):
    assert isinstance(request, HttpRequest)

    s = _get_session_info(request)
    s.vid_1 = True
    s.save()

    na_ids = _get_na_ids(request)
    return render(request, 'star/first_video.html', {'na_ids': na_ids})


def first_reading(request):
    assert isinstance(request, HttpRequest)

    s = _get_session_info(request)
    s.read_1 = True
    s.save()

    na_ids = _get_na_ids(request)
    return render(request, 'star/first_reading.html', {'na_ids': na_ids})


def second_video(request):
    assert isinstance(request, HttpRequest)

    s = _get_session_info(request)
    s.vid_2 = True
    s.save()

    na_ids = _get_na_ids(request)
    return render(request, 'star/second_video.html', {'na_ids': na_ids})


def second_reading(request):
    assert isinstance(request, HttpRequest)

    s = _get_session_info(request)
    s.read_2 = True
    s.save()

    na_ids = _get_na_ids(request)
    return render(request, 'star/second_reading.html', {'na_ids': na_ids})


def _calculate_score(answers, keys):
    total_correct = 0
    for i in range(len(answers)):
        if keys[i] == answers[i]:
            total_correct += 1

    return total_correct    


def _get_quiz_context(answers, keys, questions):
    for i in range(len(keys)):
        questions[i].append(int(answers[i]))
        questions[i].append(int(keys[i]))

    tc = _calculate_score(answers, keys)
    sp = tc/len(keys)*100
    passed = sp > 80

    context = {
        'questions': questions,
        'total_score': tc,
        'score_percent': sp,
        'passed': passed
    }

    return context


def first_quizzes(request):
    assert isinstance(request, HttpRequest)

    s = _get_session_info(request)
                
    questions = [ 
            [
                "This is the first qustion?", 
                [
                    "choice1",
                    "choice2",
                    "choice3"
                ]
            ],
            [
                "second question!", 
                [
                    "choice1",
                    "choice2",
                    "choice3",
                    "choice4"
                ]
            ],
    ]

    keys = [
        '2',
        '1'
    ]

    na_ids = _get_na_ids(request)

    if request.method == 'POST':
        answers = []
        for i in range(len(keys)):
            answer = request.POST['q{}'.format(i+1)]
            answers.append(answer)

        context = _get_quiz_context(answers, keys, questions)

        if context['passed']:
            s.quiz_1_passed = True
            s.set_answers(answers)
            s.save()

        context['na_ids'] = na_ids
        return render(request, 'star/first_quizzes_result.html', context)
    
    else:
        if s.quiz_1_passed:
            answers = s.get_answers()
            context = _get_quiz_context(answers, keys, questions)

            context['na_ids'] = na_ids
            return render(request, 'star/first_quizzes_result.html', context)
        elif not s.quiz_1:
            s.quiz_1 = True
            s.save()
            return render(request, 'star/first_quizzes.html', { 'na_ids': na_ids, 'questions': questions })
        else:
            return render(request, 'star/first_quizzes_with_hint.html', { 'na_ids': na_ids, 'questions': questions })

    
def second_quizzes(request):
    assert isinstance(request, HttpRequest)

    s = _get_session_info(request)
                
    questions = [ 
            [
                "This is the first qustion?", 
                [
                    "choice1",
                    "choice2",
                    "choice3"
                ]
            ],
            [
                "second question!", 
                [
                    "choice1",
                    "choice2",
                    "choice3",
                    "choice4"
                ]
            ],
    ]

    keys = [
        '2',
        '1'
    ]

    na_ids = _get_na_ids(request)

    if request.method == 'POST':
        answers = []
        for i in range(len(keys)):
            answer = request.POST['q{}'.format(i+1)]
            answers.append(answer)

        context = _get_quiz_context(answers, keys, questions)

        if context['passed']:
            s.quiz_2_passed = True
            s.set_answers(answers)
            s.save()

        context['na_ids'] = na_ids
        return render(request, 'star/second_quizzes_result.html', context)
    
    else:
        if s.quiz_2_passed:
            answers = s.get_answers()
            context = _get_quiz_context(answers, keys, questions)

            context['na_ids'] = na_ids
            return render(request, 'star/second_quizzes_result.html', context)
        elif not s.quiz_2:
            s.quiz_2 = True
            s.save()
            return render(request, 'star/second_quizzes.html', { 'na_ids': na_ids, 'questions': questions })
        else:
            return render(request, 'star/second_quizzes_with_hint.html', { 'na_ids': na_ids, 'questions': questions })
