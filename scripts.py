import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson

commendations = (
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
    "Ты, как всегда, точен!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Ты сегодня прыгнул выше головы!",
    "Я поражен!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Замечательно!",
    "Прекрасное начало!",
    "Так держать!",
    "Ты на верном пути!",
    "Здорово!",
    "Это как раз то, что нужно!",
    "Я тобой горжусь!",
    "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!",
    "Ты растешь над собой!",
    "Ты многое сделал, я это вижу!",
    "Теперь у тебя точно все получится!",
)


def get_child(name):
    try:
        return Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.DoesNotExist:
        print("Ошибка! Такого ученика нет.")
        return
    except Schoolkid.MultipleObjectsReturned:
        print("Ошибка! Укажите полное имя, так как под указанное подходит сразу несколько учеников.")
        return


def fix_marks(name):
    schoolkid = get_child(name)
    if not schoolkid:
        return
    marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for mark in marks:
        mark.points = 5
        mark.save()
    print("Оценки исправлены.")


def remove_chastisements(name):
    schoolkid = get_child(name)
    if not schoolkid:
        return
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()
    print("Замечания удалены.")


def create_commendation(name, lesson_title):
    child = get_child(name)
    if not child:
        return

    lesson = Lesson.objects.filter(
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
        subject__title=lesson_title
    ).order_by("-date").first()
    if not lesson:
        print("Ошибка! Такого предмета нет, попробуйте другой.")
        return

    Commendation.objects.create(
        text=random.choice(commendations),
        schoolkid=child,
        subject=lesson.subject,
        teacher=lesson.teacher,
        created=lesson.date
    )
    print("Похвала добавлена.")
