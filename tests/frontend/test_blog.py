import pytest

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.desktop.frontend.blog import BlogHomepage, ArticlePage
from pages.desktop.frontend.details import Detail
from pages.desktop.frontend.home import Home
from pages.desktop.frontend.users import User


@pytest.mark.sanity
@pytest.mark.nondesstructive
def test_blog_homepage_header_logo_button(base_url, selenium):
    page = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    page.header.click_title()
    homepage = Home(selenium, base_url)
    assert homepage.primary_hero.is_displayed()


@pytest.mark.sanity
@pytest.mark.nondesstructive
def test_articles_elements_are_displayed(base_url, selenium):
    page = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    for article in page.articles:
        assert article.image.is_displayed()
        assert article.title.is_displayed()
        assert article.date.is_displayed()
        assert article.intro_text.is_displayed()
        assert article.read_more_link.is_displayed()


@pytest.mark.sanity
@pytest.mark.nondesstructive
def test_open_article_by_clicking_article_image(base_url, selenium):
    page = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    article_title = page.articles[0].title.text
    page.articles[0].image.click()
    article_page = ArticlePage(selenium, base_url)
    assert article_title.lower() in article_page.title.text.lower()


@pytest.mark.sanity
@pytest.mark.nondesstructive
def test_open_article_by_clicking_article_title(base_url, selenium):
    page = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    article_title = page.articles[0].title.text
    page.articles[0].title.click()
    article_page = ArticlePage(selenium, base_url)
    assert article_title.lower() in article_page.title.text.lower()


@pytest.mark.nondesstructive
def test_open_article_by_clicking_read_more_link(base_url, selenium):
    page = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    article_title = page.articles[0].title.text
    page.articles[0].read_more_link.click()
    article_page = ArticlePage(selenium, base_url)
    assert article_title.lower() in article_page.title.text.lower()


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_article_page_loaded_correctly(base_url, selenium, variables):
    blog_homepage = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    page = blog_homepage.articles[0].click_read_more_link()
    assert page.header_logo.is_displayed()
    assert page.title.is_displayed()
    assert page.author.name.is_displayed()
    assert page.author.picture.is_displayed()
    assert page.author.twitter_link.is_displayed()
    assert page.author.pocket_link.is_displayed()
    for link in page.nav_bar_links:
        assert link.is_displayed()
    # verify that the article has at least one paragraph
    assert page.content_paragraphs[0].is_displayed()
    # verify that at least one of next/prev article links is displayed
    try:
        assert page.next_article.is_displayed()
    except NoSuchElementException:
        page.previous_article.is_displayed()


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_article_page_header_logo_button(base_url, selenium, variables):
    blog_homepage = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    page = blog_homepage.articles[0].click_read_more_link()
    page.header_logo.click()
    homepage = Home(selenium, base_url)
    assert homepage.primary_hero.is_displayed()


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_navbar_frontend_homepage_link(base_url, selenium, variables):
    blog_homepage = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    page = blog_homepage.articles[0].click_read_more_link()
    page.nav_bar_links[0].click()
    homepage = Home(selenium, base_url)
    assert homepage.primary_hero.is_displayed()


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_navbar_blog_homepage_link(base_url, selenium, variables):
    blog_homepage = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    page = blog_homepage.articles[0].click_read_more_link()
    page.nav_bar_links[1].click()
    blog_homepage = BlogHomepage(selenium, base_url)
    assert blog_homepage.articles[0].title.is_displayed()


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_navbar_current_article_link(base_url, selenium, variables):
    blog_homepage = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    page = blog_homepage.articles[0].click_read_more_link()
    initial_title = page.title.text
    page.nav_bar_links[2].click()
    assert initial_title in page.title.text


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_next_and_previous_article_links(base_url, selenium, variables):
    blog_homepage = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    page = blog_homepage.articles[0].click_read_more_link()
    initial_title = page.title.text
    page.next_article.click()
    assert initial_title not in page.title.text
    page.previous_article.click()
    assert initial_title in page.title.text


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_addon_cards_loaded_correctly(base_url, selenium, variables):
    blog_homepage = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    page = blog_homepage.articles[0].click_read_more_link()
    for card in page.addon_cards:
        assert card.title.is_displayed()
        assert card.author.is_displayed()
        assert len(card.summary) > 0
        assert 0 <= card.rating <= 5
        assert card.users_number >= 0
        assert card.add_to_firefox_button.is_displayed()


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_addon_card_recommendation_badge_link(base_url, selenium, variables):
    blog_homepage = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    page = blog_homepage.articles[0].click_read_more_link()
    for addon_card in page.addon_cards:
        if addon_card.is_recommended:
            addon_card.recommended_link.click()
            initial_window = page.driver.window_handles[0]
            child_window = page.driver.window_handles[1]
            page.driver.switch_to.window(child_window)
            page.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "sumo-page-heading"))
            )
            assert (
                "Add-on Badges"
                in page.driver.find_element(By.CLASS_NAME, "sumo-page-heading").text
            )
            page.driver.switch_to.window(initial_window)


@pytest.mark.prod_only
@pytest.mark.nondestructive
def test_blog_install_addon(
    base_url, selenium, variables, firefox, firefox_notifications, wait
):
    blog = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    article = blog.articles[3].click_read_more_link()
    # install add-on from a blog article
    addon_name = article.addon_cards[0].title.text
    addon_summary = article.addon_cards[0].summary
    article.addon_cards[0].add_to_firefox_button.click()
    firefox.browser.wait_for_notification(
        firefox_notifications.AddOnInstallConfirmation
    ).install()
    # verify about:addons to make sure the add-on was installed;
    selenium.get("about:addons")
    selenium.find_element(By.CSS_SELECTOR, 'button[name = "extension"]').click()
    try:
        wait.until(
            lambda _: addon_name
            in selenium.find_element(By.CSS_SELECTOR, ".addon-name a").text,
            message="The addon names did not match; checking summary next",
        )
    # there is an inconsistency between AMO and about:addons concerning addon names;
    # while on AMO the add-on name can be modified in DevHub, about:addons takes the
    # name from the manifest, resulting in possible mismatches; in such cases,
    # an alternative check for the add-on summary might help identify the addon correctly
    except TimeoutException:
        assert (
            addon_summary
            in selenium.find_element(By.CLASS_NAME, "addon-description").text
        )


@pytest.mark.prod_only
@pytest.mark.nondestructive
def test_addon_link_in_article_addon_cards(base_url, selenium):
    blog = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    article = blog.articles[3].click_read_more_link()
    # make a note of the add-on name in the article card
    addon_name = article.addon_cards[0].title.text
    # click om the add-on name to open the detail page on AMO
    article.addon_cards[0].title.click()
    addon_detail = Detail(selenium, base_url).wait_for_page_to_load()
    # check that the addon from the article and the one in the detail page are matching
    assert addon_name == addon_detail.name


@pytest.mark.prod_only
@pytest.mark.nondestructive
def test_author_link_in_article_addon_cards(base_url, selenium):
    blog = BlogHomepage(selenium, base_url).open().wait_for_page_to_load()
    article = blog.articles[3].click_read_more_link()
    # make a note of the addon author in the article card
    addon_author = article.addon_cards[0].author.text
    # click on the author name to open the user profile page on AMO
    article.addon_cards[0].author.click()
    user_name = User(selenium, base_url).wait_for_page_to_load()
    # check that the author from the article and the one in the profile page are matching
    assert addon_author == user_name.user_display_name.text
