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


def interactive(request):
    assert isinstance(request, HttpRequest)

    s = _get_session_info(request)
    s.interactive = True
    s.save()

    na_ids = _get_na_ids(request)
    return render(request, 'star/interactive.html', {'na_ids': na_ids})


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
                [
                    "Which of these is a valid IP address?", 
                    "** placeholder for hints **"
                ],
                [
                    "192.1688.1.1",
                    "257.2.22.2",
                    "192.168.1.1",
                    "192.168.1.400"
                ]
            ],
            [
                [
                    "Does IP address stand for Internet Protocal address?", 
                    "** placeholder for hints **"
                ],
                [
                    "Yes",
                    "No",
                ]
            ],
            [
                [
                    "What does DNS stand for?", 
                    "** placeholder for hints **"
                ],
                [
                    "Domain Name Stuff",
                    "Domain Name Server",
                    "Domain Naming Service",
                    "Digital Marketing Strategy"
                ]
            ],
            [
                [
                    "Which of the following statements is true?", 
                    "** placeholder for hints **"
                ],
                [
                    "DNS translates web addresses, which are easily remembered by humans, into IP Addresses.",
                    "All of the statements are true",
                    "DNS translates IP addresses, which are easily remembered by machines, into web addresses.",
                    "DNS stands for Data Not Saved"
                ]
            ],
            [
                [
                    "Which of the following statements is NOT true?", 
                    "** placeholder for hints **"
                ],
                [
                    "The Internet will not work without the DNS.",
                    "Without DNS you cannot use the Internet.",
                    "None of the statements are true",
                    "Without DNS you cannot use your computer."
                ]
            ],
    ]

    keys = [
        '3',
        '1',
        '2',
        '1',
        '4'
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
            s.read_1 = True
            s.save()
            return render(request, 'star/first_quizzes.html', { 'na_ids': na_ids, 'questions': questions })
        else:
            return render(request, 'star/first_quizzes_with_hint.html', { 'na_ids': na_ids, 'questions': questions })

    
def second_quizzes(request):
    assert isinstance(request, HttpRequest)

    s = _get_session_info(request)
                
    questions = [ 
            [
                [
                    "Which of these statment is false?", 
                    "** placeholder for hints **",
                ],
                [
                    "A server will never know your local IP address",
                    "A private IP address is unique",
                    "A public IP address is unique",
                ]
            ],
            [
                [
                    "What is a router", 
                    "** placeholder for hints **",
                ],
                [
                    "A type of circuit board inside all modems",
                    "A specialized computer",
                    "A useful concept for understanding internet data flow",
                ]
            ],
            [
                [
                    "What does a router do", 
                    "** placeholder for hints **",
                ],
                [
                    "Make sure data sent over the Internet goes where it needs to go and not where it isn't needed",
                    "Act like a traffic controller, working to cut down on congestion and keep everything flowing smoothly along the best possible path",
                    "Both"
                ]
            ],
            [
                [
                    "Which of the following tools is designed to test connectivity between two systems", 
                    "** placeholder for hints **",
                ],
                [
                    "ipconfig",
                    "netstat",
                    "ping",
                    "nslookup"
                ]
            ],
    ]

    keys = [
        '2',
        '2',
        '3',
        '3'
    ]

    na_ids = _get_na_ids(request)

    if request.method == 'POST':
        answers = []
        for i in range(len(keys)):
            print(len(keys))
            print(request.POST['q1'])
            print(request.POST['q2'])
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
            s.read_2 = True
            s.save()
            return render(request, 'star/second_quizzes.html', { 'na_ids': na_ids, 'questions': questions })
        else:
            return render(request, 'star/second_quizzes_with_hint.html', { 'na_ids': na_ids, 'questions': questions })
