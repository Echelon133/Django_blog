from selenium.webdriver.common.by import By


class BasePageLocators:
    homepage_link = (By.XPATH, '//*[@id="main-header"]/h1/a')
    description = (By.XPATH, '//*[@id="main-header"]/h5')


class PageWithLoginLocators(BasePageLocators):
    # elements below are available when user is not logged in
    username_field = (By.ID, 'id_username')
    password_field = (By.ID, 'id_password')
    login_button = (By.XPATH, '//button[@class="btn"][1]')
    signup_link = (By.XPATH, '//li[@class="nav-item"]/a')
    # elements available when logged in
    logged_as_text = (By.XPATH, '//li[@class="nav-item"][1]/p')
    logout_link = (By.XPATH, 'li[@class="nav-item"][2]/a')


class SignupPageLocators(BasePageLocators):
    username_field = (By.ID, 'id_username')
    password1_field = (By.ID, 'id_password1')
    password2_field = (By.ID, 'id_password2')
    signup_button = (By.XPATH, '//form/div[@class="text-center"]/button')
    alert_text = (By.CLASS_NAME, 'alert')


class ListedArticlesPageLocators(PageWithLoginLocators):
    article_titles = (By.CLASS_NAME, 'card-title')
    article_links = (By.XPATH, '//div[@class="card-block"]/h4/a')
    author_name = (By.XPATH, '//section[@id="right-section"]/aside/section/header')
    author_description = (By.XPATH, '//*[@id="right-section"]/aside/section/p')
    author_links = (By.XPATH, '//ul[@id="contact"]/li')
    paginator_links = (By.XPATH, '//span[@class="step-links"]/a')


class HomePageLocators(ListedArticlesPageLocators):
    pass


class ByDatePageLocators(ListedArticlesPageLocators):
    date_text = (By.CLASS_NAME, 'searching-by')


class ByCategoryPageLocators(ListedArticlesPageLocators):
    category_text = (By.CLASS_NAME, 'searching-by')


class SpecificArticlePageLocators(PageWithLoginLocators):
    title = (By.XPATH, '//article[@id="single-article"]/header/h2')
    date = (By.XPATH, '//ul[@class="outer-list"]/li[1]')
    categories = (By.XPATH, '//ul[@class="outer-list"]/li[2]')
    body = (By.XPATH, '//*[@id="single-article"]/section')
    comment_body = (By.CLASS_NAME, 'card-blockquote')
    comment_field = (By.XPATH, '//*[@id="id_body"]')
    send_button = (By.XPATH, '//div[@class="form-group"][2]/button')


class NotFoundPageLocators(PageWithLoginLocators):
    error_code = (By.CLASS_NAME, 'error-code')
    error_text = (By.CLASS_NAME, 'error-text')

