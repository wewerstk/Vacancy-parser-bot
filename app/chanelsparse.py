from telethon import TelegramClient
import re
from dotenv import load_dotenv
from config import API_HASH, API_ID

class ChannelResearch():
    def __init__(self):
        self.keywords = ["django", "drf", "fastapi", "postgresql", "sqlite", "redis", "git",
            "ci/cd", "django orm", "kafka", "rabbitmq", "celery", "docker",
            "юнит тесты", "unit", "тесты", "#senior", "#middle"]
        self.ex_keywords = ["#cv", "lead", "лид"]
        self.channel_list = ['job_python', 'p_rabota', 'ru_pythonjobs', 'django_jobs_board']
        self.main_words = ["senior", "middle"]
        self.salary_min = 150000
    
    @staticmethod
    def extract_salary(text):
        matches = re.findall(r'(\d[\d\s\xa0]{4,})', text)
        for m in matches:
            cleaned = re.sub(r'\s+', '', m)  
            try:
                number = int(cleaned)
                return number
            except ValueError:
                continue
        return None

    @staticmethod
    def extract_contacts(text):
        cut_phrases = [
            r"⬇️\s*Другие каналы.*", 
            r"Другие каналы.*",        
        ]
        for phrase in cut_phrases:
            text = re.split(phrase, text, flags=re.IGNORECASE)[0]

        contacts = []
        pattern = re.compile(r"контакт[^\n]*[:\n]?", re.IGNORECASE)
        matches = list(pattern.finditer(text))
        for match in matches:
            start = match.end()
            snippet = text[start:start+300]
            found = re.findall(r"(https?://\S+|@\w+)", snippet)
            contacts.extend(found)

        if not contacts:
            contacts = re.findall(r"(https?://\S+|@\w+)", text)

        return contacts
    
    async def parse_vacancies_async(self):
        results = []
        load_dotenv(override=True)
        async with TelegramClient('session_vacancies', api_id=API_ID, api_hash=API_HASH) as client:
            for channel in self.channel_list:
                found = False
                async for message in client.iter_messages(channel, limit=50):
                    if message.text:
                        text = message.text.lower()
                        if (
                            any(main_w in text for main_w in self.main_words)
                            and
                            any(word in text for word in self.keywords)
                            and not any(bad in text for bad in self.ex_keywords)
                        ):
                            salary = self.extract_salary(text)
                            if salary and salary >= self.salary_min:
                                contacts = self.extract_contacts(message.text)
                                contacts_text = '\n'.join(contacts) if contacts else 'Контакты не найдены.'
                                post_link = f"https://t.me/{channel}/{message.id}"
                                vacancy_msg = (
                                    f"📌 <b>Вакансия из @{channel}</b>\n"
                                    f"🔗 Пост: {post_link}\n"
                                    f"📞 Контакты для связи: {contacts_text}\n"
                                )
                                results.append(vacancy_msg)
                                found = True
                                break
                if not found:
                    pass
        return results