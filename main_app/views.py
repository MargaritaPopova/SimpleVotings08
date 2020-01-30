from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponseRedirect
from . import models
from .forms import EditProfileForm


def get_menu_context(request):
    menu_login = []
    if request.user.is_authenticated:
        menu_login.append({'url': '/logout/', 'name': 'Выйти'})
        menu_login.append({'url': '/profile/'+str(request.user.id), 'name': request.user})
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
             {'url': '/profile/' + str(request.user.id), 'name': 'Профиль'},
             {'url': '/edit_profile/', 'name': 'Редактировать'},
         ]},
        {'url': '/about/', 'name': 'О нас'},
    ]
    return menu


def greeting(request):
    if request.user.is_authenticated:
        if request.user.first_name:
            messages.add_message(request, messages.SUCCESS,
                                 'Добро пожаловать, {} {}!'.format(request.user.first_name, request.user.last_name))
        else:
            messages.add_message(request, messages.SUCCESS,
                                 'Добро пожаловать, {}!'.format(request.user))
    else:
        messages.add_message(request, messages.WARNING,'Вы вошли как гость. Чтобы продолжить, нужно авторизоваться')


@login_required
def home(request):
    context = {
        'pagetitle': 'Голосования',
        'votings': models.Voting.objects.all(),
        'menu': get_menu_context(request),
        'user': request.user,
        'loginform': AuthenticationForm(),
        'main_message': 'Здесь отображаются все голосования',
        'expand': True
    }
    if False and request:
        context['vote_errors'] = request.errors.vote

    return render(request, 'home.html', context)


def index(request):
    context = {
        'pagetitle': 'Стартовая',
        'menu': get_menu_context(request),
        'msg': 'Это стартовая страница',
        'main_message': 'Приветствуем!',
        'auth_msg': greeting(request)

    }
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
    answers = {}
    if request.method == "POST":
        try:
            curr_vot = models.Voting.objects.get(id=request.POST.get('voting_id', -1))
            if 'delete' in request.POST and request.user.id == curr_vot.author_id:
                try:
                    curr_vot.delete()
                    messages.add_message(request, messages.WARNING, 'Голосование удалено')
                except:
                    messages.add_message(request, messages.ERROR, 'Невозможно удалить голосование')
                return redirect(curr_vot.voting_view())
            if 'edit' in request.POST and request.user.id == curr_vot.author_id:
                return HttpResponseRedirect('/edit/' + str(curr_vot.id))

            if request.user.id in curr_vot.users() or request.user.id in curr_vot.users_text():
                messages.add_message(request, messages.ERROR, 'Вы уже голосовали!')
                return redirect(curr_vot.voting_view())

            if curr_vot.type == "text_input":
                if request.POST.get('answer'):
                    answer = models.TextOption(voting_id=curr_vot.id,
                                               answer=request.POST.get('answer'),
                                               user_id=request.user.id)
                    answer.save()
                    messages.add_message(request, messages.SUCCESS, 'Ваш голос принят')
                    return redirect(curr_vot.voting_view())
                else:
                    messages.add_message(request, messages.ERROR, 'Пустой ответ. Проигнорировано.')
                return HttpResponseRedirect(curr_vot.voting_view())

            opt = {e.id: e.option for e in curr_vot.options()}

            if curr_vot.type == "radio":
                tmp = request.POST.get(str(curr_vot.id))
                if not tmp:
                    messages.add_message(request, messages.ERROR, 'Пустой ответ. Проигнорировано.')
                if tmp not in opt.values():
                    messages.add_message(request, messages.ERROR,
                                         "Значение не найдено! Невозможно выбрать неучтённый вариант!")
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
                messages.add_message(request, messages.ERROR, 'Пустой ответ. Проигнорировано.')

            for e in answers.keys():
                models.Vote(option_id=e,
                            user_id=request.user.id,
                            voting_id=curr_vot.id).save()

            messages.add_message(request, messages.SUCCESS, 'Ваш голос принят')
            return HttpResponseRedirect(curr_vot.voting_view())
        except models.Voting.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Голосование не найдено!')
            return redirect(curr_vot.voting_view())
    return HttpResponseRedirect('/')


def voting(request, voting):
    context = {'answers': []}
    try:
        v = models.Voting.objects.get(id=voting)
        context['voting'] = v
        if v.type == 'text_input':
            try:
                ans = models.TextOption.objects.filter(voting_id=voting)
                for a in ans:
                    context['answers'].append({
                        'user': User.objects.get(id=a.user_id).username,
                        'answer': a.answer
                    })
                context['user_input'] = ans.get(user_id=request.user.id).answer
            except:
                context['answers'] = 'Ответов еще не было'
    except:
        messages.add_message(request, messages.ERROR, "Такого голосования нет")
    context['pagetitle'] = 'Просмотр голосования'
    context['menu'] = get_menu_context(request)
    context['main_message'] = 'Просмотр голосования'
    context['expand'] = False

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
        messages.add_message(request, messages.SUCCESS, "Голосование успешно создано")

        count = request.POST.get('count')

        for i in range(1, int(count) + 1):
            o = models.Options()
            o.option = request.POST.get('option' + str(i))
            o.voting = v
            o.save()

        return HttpResponseRedirect(v.voting_view())

    context = {
        'menu': get_menu_context(request),
        'pagetitle': 'Создание голосования',
    }
    return render(request, 'create.html', context)


def voting_types(type):
    types = [
        {'type': 'radio', 'value': 'С единственным выбором'},
        {'type': 'checkbox', 'value': 'С множественным выбором'},
        {'type': 'text_input', 'value': 'Свободный ответ'},
    ]
    if type == 'radio':
        return types
    elif type == 'checkbox':
        types = [types[1], types[2], types[0]]
    else:
        types = [types[2], types[0], types[1]]
    return types


@login_required()
def edit(request, id):
    v = models.Voting.objects.get(id=id)
    context = {
        'voting': v,
        'pagetitle': 'Редактировать голосование',
        'menu': get_menu_context(request),
        'user': request.user,
        'main_message': 'Редактировать голосование',
        'result': '',
        'id': id,
        'voting_types': voting_types(v.type)
    }

    if request.user.id == context['voting'].author_id:
        options = models.Options.objects.filter(voting_id=id)

        if request.method == 'POST':
            print(request.POST)
            for o in options:
                if not ('option_' + str(o.id)) in request.POST:
                    o.delete()
                else:
                    o.option = request.POST.get("option_" + str(o.id))
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
                print(o.option)
                o.voting = context['voting']
                o.save()

            title = request.POST.get('title')
            context['voting'].question = title
            context['voting'].save()
            messages.add_message(request, messages.SUCCESS, "Изменения сохранены")

            return redirect(context['voting'].voting_view())

    return render(request, 'edit.html', context)


@login_required()
def profile(request, id):
    votes = models.Vote.objects.filter(user_id=request.user.id)

    context = {
        'pagetitle': 'Мой профиль',
        'menu': get_menu_context(request),
        'user': request.user,
        'main_message': 'Мой профиль',
        'id': id,
        'votings': models.Voting.objects.filter(author_id=request.user.id),
        'my_votes': {models.Voting.objects.get(id=v.voting_id) for v in votes},
        'expand': True
    }

    return render(request, 'profile.html', context)


@login_required()
def edit_profile(request):
    context = {
        'pagetitle': 'Мой профиль',
        'menu': get_menu_context(request),
        'user': request.user,
        'main_message': 'Мой профиль',
    }
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Изменения сохранены!")
            return redirect('/profile/' + str(context['user'].id))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return redirect('/profile/' + str(context['user'].id))
    else:
        form = EditProfileForm(instance=request.user)
        context['form'] = form
        return render(request, 'edit_profile.html', context)


@login_required()
def change_password(request):
    context = {
        'pagetitle': 'Изменить пароль',
        'menu': get_menu_context(request),
        'user': request.user,
        'main_message': 'Изменить пароль',
    }
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.add_message(request, messages.SUCCESS, "Ваш пароль изменён")
            return redirect('/profile/' + str(context['user'].id))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return redirect('/password/')
    else:
        form = PasswordChangeForm(user=request.user)
        context['form'] = form
        return render(request, 'registration/password.html', context)


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
