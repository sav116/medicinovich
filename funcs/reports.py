def getReport(key):
    secs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    with open(f"temp/{key}") as f:
        index = 0
        for line in f:
            if '№' in line:
                sec = round(int(line.split(',')[1]) / 1000, 2)
                secs[index] = sec
                index += 1

    report = f"Авторизация в МИС: {secs[0]} с.\n\
Выбор ЛПУ: {secs[1]} с.\n\
Формирование дневника врача: {secs[2]} с.\n\
Открытие окна приема: {secs[3]} с.\n\
Запись на повторный прием (расписание): {secs[4]} с.\n\
Запись на повторный прием (формирование окна записи на прием): {secs[5]} с.\n\
Запись на повторный прием (сохранение записи на прием): {secs[6]} с.\n\
Сохранение приема врача: {secs[7]} с.\n\
Формирование окна Расписание: {secs[8]} с.\n\
Поиск пациента в расписании по ФИО/по номеру карты: {secs[9]} с.\n\
Сохранение записи на прием: {secs[10]} с.\n\
\nСуммарное время операций : {round(sum(secs),2)} с."
    return report
