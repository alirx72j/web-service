import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

# https://docs.google.com/spreadsheets/d/18kxoD_tjpMYXxZEa-O-xjrWGQeX1H2KddWvmsO3nahM/edit?gid=0#gid=0
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

sheet = client.open_by_key('18kxoD_tjpMYXxZEa-O-xjrWGQeX1H2KddWvmsO3nahM').sheet1

event_data = {
    "Name": [],
    "Email": [],
    "Phone Number": [],
    "Organization": [],
    "Registration Date": []
}

def save_registration(name, email, phone_number, organization, registration_date):
    new_row = [name, email, phone_number, organization, registration_date]
    sheet.append_row(new_row)

def get_all_registrations():
    all_data = sheet.get_all_values()
    if not all_data:
        return pd.DataFrame(columns=["Name", "Email", "Phone Number", "Organization", "Registration Date"])
    df = pd.DataFrame(all_data[1:], columns=["Name", "Email", "Phone Number", "Organization", "Registration Date"])
    return df
def get_registrations_by_event(event_name):
    all_registrations = get_all_registrations()
    filtered_registrations = all_registrations[all_registrations["Event Name"] == event_name]
    return filtered_registrations
def analyze_registrations(df):
    org_counts = df['Organization'].value_counts()
    st.bar_chart(org_counts)
    reg_date_counts = df['Registration Date'].value_counts()
    st.line_chart(reg_date_counts)

st.title("ثبت نام رویداد")

st.header("ثبت نام در رویداد")
event_name = st.text_input("نام رویداد:")
name = st.text_input("نام:")
email = st.text_input("ایمیل:")
phone_number = st.text_input("شماره تلفن:")
organization = st.text_input("سازمان:")
registration_date = st.date_input("تاریخ ثبت نام:")
register_button = st.button("ثبت نام")

if register_button:
    if event_name and name and email and phone_number and organization and registration_date:
        event_data["Name"].append(name)
        event_data["Email"].append(email)
        event_data["Phone Number"].append(phone_number)
        event_data["Organization"].append(organization)
        event_data["Registration Date"].append(registration_date.strftime("%Y-%m-%d"))
        save_registration(name, email, phone_number, organization, registration_date.strftime("%Y-%m-%d"))
        st.success("با موفقیت ثبت نام شد!")
    else:
        st.error("لطفا تمام فیلدهای مورد نیاز را پر کنید.")

st.header("لیست ثبت نام شدگان")
all_registrations_df = get_all_registrations()
st.write(all_registrations_df)

st.header("تحلیل داده های ثبت نام")
analyze_registrations(all_registrations_df)