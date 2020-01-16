from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect

from . import models
from .forms import VoteForm

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

# Алфавит составлен из непохожих символов
url_alph = "23459bfghinpstuwzDFGJLRSUWZ_"


def convert_base(num: str, to_base: int = 10, from_base: int = 10,
                 alph_t: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                 alph_f: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
    num = str(num)
    if to_base <= 0:
        to_base = len(alph_t)
    if from_base <= 0:
        from_base = len(alph_f)
    # A -> 10
    a = {e: i for i, e in enumerate(alph_f)}
    # 10 -> A
    b = dict(enumerate(alph_t))
    num2, num3 = 0, ""
    for e in num:
        num2 *= from_base
        num2 += a[e]
    while num2:
        num3 += b[num2 % to_base]
        num2 //= to_base
    return num3[::-1]


def get_menu_context(request):
    menu_login = []
    if request.user.is_authenticated:
        menu_login.append({'url': '/logout/', 'name': 'Выйти'})
    else:
        menu_login += [{'url': '/signup/', 'name': 'Регистрация'},
                       {'url': '/login/', 'name': 'Войти'}]

    menu = [
        menu_login,
        {'url': '/', 'name': 'Главная'},
        {'url': '', 'name': 'Голосования',
         'dropdown': [
             {'url': '/home/', 'name': 'Просмотреть все'},
             {'url': '/create/', 'name': 'Создать'},
         ]},
        {'url': '/', 'name': 'Моя страница',
         'dropdown': [
             {'url': '/my_votings/', 'name': 'Посмотреть мои'},
             {'url': '/create/', 'name': 'Создать голосование'},
         ]},
        {'url': '/about/', 'name': 'О нас'},
    ]
    return menu


@login_required
def home(request):
    context = {
        'pagetitle': 'Голосования',
        'votings': models.Voting.objects.all(),
        'menu': get_menu_context(request),
        'user': request.user,
        'loginform': AuthenticationForm(),
        'main_message': 'Здесь отображаются все голосования'
    }
    if False and request:
        context['vote_errors'] = request.errors.vote
    if request.user.is_authenticated:
        context['auth_msg'] = 'Добро пожаловать, {}!'.format(context['user'])


    return render(request, 'home.html', context)


def index(request):
    context = {
        'pagetitle': 'Стартовая',
        'menu': get_menu_context(request),
        'msg': 'Это стартовая страница',
        'main_message': 'Приветствуем!'

    }
    if not request.user.is_authenticated:
        context['auth_no'] = 'Вы вошли как гость. Чтобы продолжить, нужно авторизоваться'
    else:
        context['auth_yes'] = 'Добро пожаловать, {}!'.format(request.user)
    return render(request, 'index.html', context)


def about(request):
    context = {'menu': get_menu_context(request)}
    from random import choice, randint
    context['dialog'] = choice([
        "Всегда хотел себе рандом-сплеши",
        "Django прекрасен, НО...",
        "Случайная надпись через...",
        "F5 - Для обновления страницы",
        "Тихо шифером шурша, едет крыша не спеша...",
        "Ехал {0} через {1}, видит {0}:\nв {2} {3}. Сунул {0} {4} в {1} -\n{3} за {4} {0} хвать!".format(*choice([
            "Грека реку реке рак руку",
            "Жека реку реке зэк руку",
            "DDoS'ер network фрейме crack ether",
            "Object object object tab object",
            "Promise promise promise bug report",
            "Process system system log event",
        ]).split()),
        "Адекватность? Какая адекватность?",
        "В Neverhood был целый коридор, который переводчики из\n"
        "'Дядюшки Ресёрча' наполнили баянистыми анекдотами,\n"
        "а я всего-то арендовал ваш title",
        "'Notepad++', 'Sublime Text', 'Atom'...\nВыбери сторону!",
        "GNU is Not a Unix",
        "..:^:..iёi..:^:..",
        "П͇̲̇͒̽р̡͆̂́͏̟̭о̩̲̺̤̻͌̍̕в̡̺̬̩̮͎̰̼͎ͭ̐ͫ͝е̢͇͓͔͙͔̲ͯ̈́̔̄ͅр̯͈̫̮̈́̓́̾̆̃͝к͈̌́ͫ̎̉ͧ͡ӓ͇̤́ͧͮͥ̉͛̽ ̧̻̠̰͙̤͉̼ͨ̿̆͟н̵̞̘̻̞̞͉̭̍͊͘͠а͍̭̜̇̍̄ͧ̕ ̛̳͖̐ч̤̮͓̫̭̠̠͛ͥ̾̾͘и̧̦͈̾̿ͯ̕т̵̮̙͈̮͉̘͔̀͂͐̏͗ӓ̝̜͇͖͚̥͙̤́̎̾͟͡е̺̞͔̑ͨͦ̋͗ͬͥ͘м̱̗̘̣ͦͫͫо̭͙ͯͧͮͤ̓ͤ̄ͦ͜с̧̹͖̗̗͍̯̟͖͗ͣ̆т͍̪̳̫̯͚̟̾ͩ͛͐ͩ̀͢ь̡̠̥̘̞̠͆̓",
        f"Текст написан {randint(26, 31)}.12.2019 в {randint(6, 11)} часов утра!",
    ])

    return render(request, 'about.html', context)


def signup_view(request):
    form = UserCreationForm(request.POST)
    context = {
        'pagetitle': 'Регистрация',
        'form': form,
        'menu': get_menu_context(request)
    }
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'registration/signup.html', context)


@login_required
def vote(request):
    if request.method == "POST":
        curr_vot = models.Voting.objects.get(id=request.POST.get('voting_id', -1))
        if not curr_vot:
            return HttpResponse('Голосование не найдено!')
        else:
            if 'delete' in request.POST and request.user.id == curr_vot.author_id:
                try:
                    curr_vot.delete()
                    return HttpResponse('Вы успешно удалили голосование')
                except:
                    return HttpResponse('Невозможно удалить голосование')
            if 'edit' in request.POST and request.user.id == curr_vot.author_id:
                return HttpResponseRedirect('/edit/'+str(curr_vot.id))

            if request.user.id in curr_vot.users() or request.user.id in curr_vot.users_text():
                return HttpResponse('Вы уже голосовали!')

            if curr_vot.type == "text_input":
                if request.POST.get('answer'):
                    answer = models.TextOption(voting_id=curr_vot.id,
                                            answer=request.POST.get('answer'),
                                            user_id=request.user.id)
                    answer.save()
                    return HttpResponseRedirect(curr_vot.voting_view())
                return HttpResponse("Пустой ответ. Проигнорировано.")

            opt = {e.id: e.option for e in curr_vot.options()}

            if curr_vot.type == "radio":
                tmp = request.POST.get(str(curr_vot.id))
                if not tmp:
                    return HttpResponse("Пустой ответ. Проигнорировано.")
                if tmp not in opt.values():
                    return HttpResponse("Значение не найдено! Невозможно выбрать неучтённый вариант!")
                for k, v in opt.items():
                    if tmp == v:
                        answers = {k: v}
                        break
            else:
                answers = {e: request.POST.get(str(e))
                           for e in opt.keys()
                           if request.POST.get(str(e)) and
                           request.POST.get(str(e)) == opt[e]}

            if not answers:
                return HttpResponse(f"Пустой ответ. Проигнорировано.")

            for e in answers.keys():
                models.Vote(option_id=e,
                            user_id=request.user.id,
                            voting_id=curr_vot.id).save()

            return HttpResponseRedirect(curr_vot.voting_view())

    return HttpResponseRedirect('/')


def voting(request, voting):
    context = {'answers': []}
    try:
        v = models.Voting.objects.get(id=voting)
        if v.type == 'text_input':
            ans = models.TextOption.objects.filter(voting_id=voting)
            for a in ans:
                context['answers'].append({
                    'user': User.objects.get(id=a.user_id).username,
                    'answer': a.answer
                })
            context['user_input'] = ans.get(user_id=request.user.id).answer
    except:
        v = None
    context['pagetitle'] = 'Просмотр голосования'
    context['voting'] = v
    context['menu'] = get_menu_context(request)
    context['main_message'] = 'Просмотр голосования'

    return render(request, 'voting.html', context)

@login_required()
def create(request):
    if request.method == "POST":

        title = request.POST.get('title')

        v = models.Voting()
        v.question = title
        v.author = request.user
        if request.POST.get('voting_type') == 'radio':
            v.type = 'radio'
        elif request.POST.get('voting_type') == 'checkbox':
            v.type = 'checkbox'
        elif request.POST.get('voting_type') == 'text_input':
            v.type = 'text_input'
        v.save()

        count = request.POST.get('count')

        for i in range(1, int(count) + 1):
            o = models.Options()
            o.option = request.POST.get('option' + str(i))
            o.voting = v
            o.save()

        return HttpResponseRedirect('/home/')

    context = {
        'menu': get_menu_context(request),
        'pagetitle': 'Создание голосования',
        'main_message': 'Создание голосования'
    }
    return render(request, 'create.html', context)


@login_required()
def my_votings(request):
    context = {
        'pagetitle': 'Мои голосования',
        'votings': models.Voting.objects.filter(author_id=request.user.id),
        'menu': get_menu_context(request),
        'user': request.user,
        'loginform': AuthenticationForm(),
        'main_message': 'Мои голосования'
    }
    if False and request:
        context['vote_errors'] = request.errors.vote
    if request.user.is_authenticated:
        context['auth_msg'] = 'Добро пожаловать, {}!'.format(context['user'])

    return render(request, 'my_votings.html', context)


@login_required()
def edit(request, id):
    context = {
        'voting': models.Voting.objects.get(id=id),
        'pagetitle': 'Редактировать голосование',
        'menu': get_menu_context(request),
        'user': request.user,
        'main_message': 'Редактировать голосование',
        'result': '',
        'id': id
    }
    if request.user.id == context['voting'].author_id:
        options = models.Options.objects.filter(voting_id=id)

        if request.method == 'POST':
            for o in options:
                if ('del_'+str(o.id)) in request.POST:
                    o.delete()
                elif ('save_'+str(o.id)) in request.POST:
                    o.option = request.POST.get(str(o.id))
                    o.save()

            if 'voting_type' in request.POST:
                if request.POST.get('voting_type') == 'radio':
                    context['voting'].type = 'radio'
                elif request.POST.get('voting_type') == 'checkbox':
                    context['voting'].type = 'checkbox'
                elif request.POST.get('voting_type') == 'text_input':
                    context['voting'].type = 'text_input'
                context['voting'].save()

            count = request.POST.get('count')

            for i in range(1, int(count) + 1):
                o = models.Options()
                o.option = request.POST.get('option' + str(i))
                o.voting = context['voting']
                o.save()

    return render(request, 'edit.html', context)


def get_suffix(x: int, zero: str, one: str, two: str, ):
    x %= 100
    if 9 < x < 20:
        return zero
    x %= 10
    if x is 1:
        return one
    elif x in [2, 3, 4]:
        return two
    else:
        return zero
