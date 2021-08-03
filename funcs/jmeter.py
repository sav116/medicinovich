import os
from data.project import DATA


def runJmeterFromBars(script_name, key):
    os.system(f"sudo rm -f temp/{key}")
    command = f"sudo /opt/jmeter/bin/jmeter -n -t /var/www/ovirtmedicinovich/conf/jmeter_profiles/local_profiles/{script_name}"
    os.system(command)


def getReportFromCod(sftp, key):
    file = sftp.open(f'temp/{key}')
    secs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = 0
    for line in file.readlines():
        if '№' in line:
            sec = round(int(line.split(',')[1]) / 1000, 2)
            secs[index] = sec
            index += 1
            if line == 11:
                break

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
\nСуммарное время операций : {round(sum(secs), 2)} с."
    return report


def runJmeterFromCod(chat_id, script_name, key):
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    hostname = DATA[chat_id]['cod_server_ip']
    port = DATA[chat_id]['cod_server_port']
    username = DATA[chat_id]['user']
    password = DATA[chat_id]['password']
    try:
        ssh.connect(hostname=hostname, port=port,
                    username=username,
                    password=password)
    except:
        return "Не могу подключиться к ЦОДу по ssh!"
    commands = ['rm -rf temp/', f'/opt/jmeter/bin/jmeter -n -t /opt/jmeter/profile/remote_profiles/{script_name}']
    try:
        for com in commands:
            stdin, stdout, stderr = ssh.exec_command(com)
            print(stdout.readlines())
    except:
        return f"Не могу выполнить следующую команду в ЦОДе:\n{commands[1]}"
    sftp = ssh.open_sftp()
    report = getReportFromCod(sftp, key)
    ssh.close()
    return report
