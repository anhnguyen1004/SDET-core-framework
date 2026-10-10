class LoginPage:
    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.username = username
        self.password = password

    def extractLocator(self, field: str):
        return f"[data-test='{field}']"

    def login(self, page):
        page.goto(self.url)

        page.locator(self.extractLocator("username")).fill(self.username)
        page.locator(self.extractLocator("password")).fill(self.password)
        page.locator(self.extractLocator("login-button")).click()
        
        return page
