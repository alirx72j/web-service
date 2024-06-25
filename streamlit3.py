import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd
import json

# https://docs.google.com/spreadsheets/d/1fACnV8ivr7q7nMVVTRZ7KacQNVqco4hlgCkrcEq4_8s/edit?gid=0#gid=0

cd = {
     "type": "service_account",
  "project_id": "aliiran-2eb80",
  "private_key_id": "5f6db4830f84ea2bd2f784c162abcfa9e1df2592",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDJxcjiUMypln2c\nf1jjAeWlN9uC0zTadOWZtv+esb+7EFBqggS4bDmQJBWy5MhCR7KlGxsN4HwgOdy9\nXRgMUF9ToXxBsRsp2F6rpWXNuiK6pa0exjK3BrAM1dCH3izMdEkadI2LNptdaHLl\n6RZlim1X+TUdUvPz4xuGtijvEXPjL8XoA//FNLZF26VA7TqHvLhOhUCaLEwdl1v8\nfYF11jDWQzm2AjegF7jjRMs/l8iGQTrtNEVDeipZ/IqxCctfIy4IW4kRIRoBiQ6z\nMQBTraaBrtZhVPq3EZbFvgjHo/Ul/hb00BF7piMr+1wfH7rQXSCf9tmpqQAzP1hC\nbFZS0ZcBAgMBAAECggEAFZ4Uqzan7sV6WMGGFvA1l/F3mbkiMQOUM9dY5Lo7hgG1\n8+tRMScbNbfAAWYklIFVAP559A8ojVVVso4eTPdxdybWhr1AYUfWwMIcOaHnJaMp\nfKIUfeqAAygHSv9BQnh0+pohLhigJa5SnRJPfXqKw4GmMKmaDHe5E8JBeXefuGfN\npgsusJdNdKH0vUpvASq+7+kxOJJBg49Dr5COtdK5/ZNSxYV2kX1ahOrHyQHKZE3A\ny7i0b2+lcyEZDd+wFV8/8q1PvE/kQR3DY1Dodg3IcguhO38OOKMoUyWJ22brD39U\nBurx0Zf2Nc7dNtfy/E4j7QK1CCvOzK2q139XU9wooQKBgQDuG0HOVmJJqsFk2AFL\nmKCffZJJ/ubOUmGNqfZOMqt8jN0QH/D38dQNLhboU4XdoVXzwOtUHh0XHybMX7dy\n+6HaRjvmJ1RF/fS69q36quYCyo5omJ4uGWDhIG+c1Z8E9cotzGW52dNrWLjcZtqS\n7iiI9Byxzgh3UWmc50dGxRoXaQKBgQDY74dgIKKNIUt1Ul15u0FazVW6JawfIjE4\nqZ7xjG8zOj0dXBaa4sAkmO4z3q/FvRTykdxlgEpbe354lwqhj4SPdptKsfU0YEI4\nY47l1OMJ74bVUwMxLqz5Tamt9RcPWJFDqNOcP1X/WUzaQl9gWZsEUKAzrNr/nOQr\nR9CJMXTn2QKBgHY2UBh56Lg8L2G6oAIBF5W3SR61j69VVRt5C1DNdTgT01jDEuZ2\nSFn2zOaxON/MzpiC6hLMFJM7Iw8KYlCSv0tX3TspwXwyVgNQnxW5LRKrr8IcK0Ql\n02RRrzgFErrqsGLGfKalj4JW/QhnhBK4bKV51Jkt+iQK5k1AwbFP/+EpAoGAfxNg\n46h6T92vDByhcQuF7yDVFOO4fcxTtPN3jdtL0GBPKIGnJDergkSrVGsf398xBB75\nUePiqtAed5lSuu0NI9TAhvLTxkiUwd9f97XLASj0fMXR2t+Sp78cpDArv+uLvGyK\n+L4JLDktUbULla8npVFtZpfc+Vr4NXot6A+2gZECgYEAiIgWvtFe3PtPK/JI3EDN\n45oUs9Vx0s4RM3aCqxrbh64VqGlC14X6sgN7AWslM5U6utm3oUE3wGHbaDGqNeMS\njM8VKJlqY2rL9pkoMGmWIrZx+jKyN6n9rqQQx4juvxtZtjNQalDl/RGjM8ZcqACX\nlm7ehR7C9ktAo/3jPOkDKdY=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-57lxv@aliiran-2eb80.iam.gserviceaccount.com",
  "client_id": "110053912889598425476",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-57lxv%40aliiran-2eb80.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
with open('credentials.json', 'w') as outfile:
    json.dump(cd, outfile)
credentials = Credentials.from_service_account_file('credentials.json', scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credentials)

sheet = client.open_by_key('1fACnV8ivr7q7nMVVTRZ7KacQNVqco4hlgCkrcEq4_8s').sheet1

def save_task(task, description, due_date, status):
  num_rows = len(sheet.get_all_values())
  task_id = num_rows
  new_row = [task_id, task, description, due_date.strftime("%Y-%m-%d"), status]
  sheet.append_row(new_row)
def get_all_tasks():
  all_data = sheet.get_all_values()[1:]
  df = pd.DataFrame(all_data, columns=["Task ID","Task", "Description", "Due Date", "Status"])
  return df

def mark_task_complete(task_id):
  index = int(task_id) - 1
  sheet.update_cell(index+2, 4, "Complete")

st.title("مدیریت وظایف")

st.header("افزودن وظیفه جدید")
new_task = st.text_input("عنوان وظیفه:")
new_description = st.text_input("توضیحات:")
new_due_date = st.date_input("تاریخ سررسید:")
add_task_button = st.button("افزودن")

if add_task_button:
  if new_task and new_description and new_due_date:
    save_task(new_task, new_description, new_due_date, "Pending")
    st.success("وظیفه با موفقیت اضافه شد!")
  else:
    st.error("لطفاً تمام فیلدهای مورد نیاز را پر کنید.")

st.header("لیست وظایف")
all_tasks_df = get_all_tasks()
st.write(all_tasks_df)

complete_task_id = st.selectbox("انتخاب وظیفه برای تکمیل:", all_tasks_df.index + 1, format_func=lambda x: f"وظیفه {x}")
complete_task_button = st.button("تکمیل")

if complete_task_button and complete_task_id:
  mark_task_complete(complete_task_id)
  st.success("وظیفه با موفقیت تکمیل شد!")
