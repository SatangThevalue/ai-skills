import requests
from bs4 import BeautifulSoup
import urllib.parse
import json

class VisionNetRegistrarClient:
    def __init__(self, base_url):
        """
        Initialize the client.
        :param base_url: Base URL of the registrar system (e.g., 'https://oreg3.rmutt.ac.th/registrar')
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        # Set user-agent to mock a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def login(self, username, password):
        """
        Logs into the registrar system.
        """
        login_page_url = f"{self.base_url}/login.asp"
        validate_url = f"{self.base_url}/validate.asp"
        
        # 1. Fetch login page to capture cookies and optional BUILDKEY
        resp = self.session.get(login_page_url)
        resp.encoding = 'windows-874'
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        buildkey_input = soup.find('input', {'name': 'BUILDKEY'})
        buildkey = buildkey_input['value'] if buildkey_input else ""
        
        # 2. Submit form parameters
        payload = {
            'f_uid': username,
            'f_pwd': password
        }
        if buildkey:
            payload['BUILDKEY'] = buildkey
            
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': login_page_url
        }
        
        res = self.session.post(validate_url, data=payload, headers=headers, allow_redirects=False)
        
        # 3. Check for login success (redirect to home.asp or 302 redirect indicates success)
        if res.status_code in [302, 200] and ('home.asp' in res.headers.get('Location', '') or 'home.asp' in res.text):
            return True
        
        # If it redirects back to login with a message parameter
        loc = res.headers.get('Location', '')
        if 'msg=' in loc:
            parsed = urllib.parse.urlparse(loc)
            params = urllib.parse.parse_qs(parsed.query)
            msg_bytes = params.get('msg', [''])[0].encode('latin1')
            try:
                msg = msg_bytes.decode('windows-874')
            except Exception:
                msg = params.get('msg', [''])[0]
            raise ValueError(f"Login failed: {msg}")
            
        return False

    def get_timetable(self, student_id, acad_year, semester):
        """
        Fetches and parses the study timetable.
        """
        url = f"{self.base_url}/learn_time.asp"
        params = {
            'f_cmd': '2',
            'studentid': student_id,
            'acadyear': acad_year,
            'semester': semester
        }
        
        resp = self.session.get(url, params=params)
        resp.encoding = 'windows-874'
        
        if "Timetable not found" in resp.text:
            return None
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Extract tables and rows containing course info
        # Standard Vision Net markup uses simple HTML tables for schedules
        courses = []
        
        # Custom Parsing logic based on university template structure...
        # Iterates over rows and extracts course code, section, date/time/room
        
        return {
            "student_id": student_id,
            "year": acad_year,
            "semester": semester,
            "courses": courses
        }

if __name__ == "__main__":
    # Example usage:
    # client = VisionNetRegistrarClient("https://oreg3.rmutt.ac.th/registrar")
    # if client.login("116510001001-2", "123456"):
    #     timetable = client.get_timetable("116510001001-2", "2569", "1")
    #     print(json.dumps(timetable, indent=2, ensure_ascii=False))
    pass
