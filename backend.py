import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass

# Đối tượng các ngày trong tuần
class Days_in_week:
    def __init__(self, name):
        self.name = name
        self.morningshift = [] # Danh sách các nhân viên làm việc ca sáng
        self.afternoonshift = [] # Danh sách các nhân viên làm việc ca chiều
        self.absent = []    # Danh sách các nhân viên vắng

    def dis_play(self):
        print(self.morningshift)
        print(self.afternoonshift)
        print(self.absent)

    def add_morningshift(self, name):
        if name in self.morningshift:
            return self.morningshift
        return self.morningshift.append(name)

    def add_afternoonshift(self,name):
        if name in self.afternoonshift:
            return self.afternoonshift
        return self.afternoonshift.append(name)

    def add_absent(self,name):
        if name in self.absent:
            return self.absent
        return self.absent.append(name)

class Week:
    def __init__(self):
        self.week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.schedules = {}

    def dis_play(self):
        for i in self.schedules:
            print(f'{i}-Morning-{[name for name in self.schedules[i].morningshift]}')
            print(f'{i}-Afternoon-{[name for name in self.schedules[i].afternoonshift]}')
            print(f'{i}-Absent-{[name for name in self.schedules[i].absent]}\n')

    def add_day(self,schedule):
        self.schedules[schedule.name] = schedule
        return self.schedules
    
    def check_enough(self,n):
        report = {}
        for i in self.schedules:
            if len(self.schedules[i].morningshift)<n:
                report[i] = f" Morning - lack of {n-len(self.schedules[i].morningshift)} staffs"
            elif len(self.schedules[i].afternoonshift)<n:
                report[i] = f" Afternoon - lack of {n-len(self.schedules[i].afternoonshift)} staffs"
        return report
    
    def write_to_file(self,n):
        report = self.check_enough(n)
        with open("staff.txt", "a+", encoding="utf-8") as file:
            for pen in self.schedules:
                if pen in report:
                    text = report[pen].split('-')[1]
                    if "Morning" in report[pen]:
                        file.write(f'\n{pen}-Morning-{[name for name in self.schedules[pen].morningshift]}-{text}\n')
                        file.write(f'{pen}-Afternoon-{[name for name in self.schedules[pen].afternoonshift]} \n')
                    elif "Afternoon" in report[pen]:
                        file.write(f'\n{pen}-Morning-{[name for name in self.schedules[pen].morningshift]} \n')
                        file.write(f'{pen}-Afternoon-{[name for name in self.schedules[pen].afternoonshift]}-{text}\n')
                else:
                    file.write(f'\n{pen}-Morning-{[name for name in self.schedules[pen].morningshift]} \n')
                    file.write(f'{pen}-Afternoon-{[name for name in self.schedules[pen].afternoonshift]} \n')
                file.write(f'{pen}-Absent-{[name for name in self.schedules[pen].absent]} \n')
            file.close()

def is_exist(data, name):
    if name in data:
        return True
    return False

def arrange_schedule(data, day):
    new_data = []
    for i in range(len(data)):
        c = data.iloc[i].to_dict()
        new_data.append(c)

    morning = [day, "sáng"]    # Danh sách nhân viên làm ca sáng
    afternoon = [day, "tối"]  # Danh sách nhân viên làm ca chiều
    absent = [day, "vắng"]     # Danh sách nhân viên nghỉ
    for i in new_data:
        name = i["Họ và Tên"]
        if i[day] == "Sáng":
            if is_exist(morning, name): # Kiểm tra xem nhân viên x có lịch làm việc hôm đó chưa
                continue
            morning.append(name)
        elif i[day] == "Tối":
            if is_exist(afternoon, name):
                continue
            afternoon.append(i['Họ và Tên'])
        else:
            absent.append(i["Họ và Tên"])
    
    return morning, afternoon, absent
'''
____________________________________________________________________________________________________________________________________
RUNNING PROGRAM
____________________________________________________________________________________________________________________________________
'''
model = Week()  # Tạo đối tượng tuần

name_file = input("Hãy nhập tên file:")
data = pd.read_excel(f"{name_file}.xlsx")
for i,j in zip(data.columns[3:10], model.week): # Chuyển tên các ngày trong tuần thành tiếng anh
    data = data.rename(columns={i:j})


n = int(input("Hãy nhập số nhân sự làm trong ca đó:"))
for day in model.week:
        schedule = Days_in_week(day)
        a,b,c = arrange_schedule(data, day)
        for employee1 in a[2::]:
                if len(schedule.morningshift)>=n:
                        break
                schedule.add_morningshift(employee1)
        for employee2 in b[2::]:
                if len(schedule.afternoonshift)>=n:
                        break
                schedule.add_afternoonshift(employee2)
        for employee3 in c[2::]:
                schedule.add_absent(employee3)
        model.add_day(schedule)

a = model.check_enough(n)
model.write_to_file()
'''
____________________________________________________________________________________________________________________________
SENDING EMAIL TO MANAGER
____________________________________________________________________________________________________________________________
'''
try:
    # thông tin tài khoản gửi email
    sender_email = "yourmail@gmail.com"
    sender_password = getpass.getpass("Nhập mật khẩu tại đây:")

    # thông tin tài khoản nhận email
    receiver_email = "receiver@gmail.com"

    # tạo một thông điệp email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Test email"

    # thêm nội dung email
    text = "Hello, this is a test email!"
    message.attach(MIMEText(text, "plain"))

    # thêm tệp tin đính kèm
    with open("staff.txt", "r", encoding='utf-8') as attachment:
        file = MIMEText(attachment.read())
        file.add_header("Content-Disposition", "attachment", filename="staff.txt")
        message.attach(file)

    # gửi email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
  except:
    print("Fail to send!)
