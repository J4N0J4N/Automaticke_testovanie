import pytest
from playwright.sync_api import Page, expect

# Fixture na vytvorenie a zatvorenie stránky 
@pytest.fixture
def test_page(page: Page):
    print("Setting up test page")
    yield page
    print("Closing test page")

# ENGETO.cz 

# Test overí, že hlavný nadpis obsahuje správny text a že tlačidlo "Zobrazit kurzy" je viditeľné
def test_engeto_heading_and_main_button(test_page):
    print("Navigating to engeto.cz")
    test_page.goto("https://engeto.cz")

    heading = test_page.locator("h1")
    expect(heading).to_contain_text("Staň se novým IT talentem")

    button = test_page.get_by_role("link", name="Zobrazit kurzy")
    expect(button).to_be_visible()

# Test overí, že ak sa zobrazí cookie banner, je možné ho skryť kliknutím
def test_engeto_cookie_button(test_page):
    print("Checking cookie button")
    test_page.goto("https://engeto.cz")

    cookie_button = test_page.get_by_role("button", name="Povolit vše")
    if cookie_button.is_visible():
        cookie_button.click()
        assert not cookie_button.is_visible()

# DEMOQA.COM

# Parametrizovaný test pre kontrolu výberu checkboxov (Desktop, Documents, Downloads)
@pytest.mark.parametrize("item", ["Desktop", "Documents", "Downloads"])
def test_demoqa_checkbox_selection(test_page: Page, item: str):
    print(f"Testing checkbox selection for: {item}")
    test_page.goto("https://demoqa.com/checkbox")

    # Rozbalenie všetkých možností
    expand_button = test_page.locator("button[title='Expand all']")
    expand_button.click()

    # Kliknutie na požadovaný checkbox
    label = test_page.get_by_text(item, exact=True)
    label.click()

    # Kontrola, či sa výber zobrazil v sekcii s výstupmi
    selected_items = test_page.locator("span.text-success").all_text_contents()
    print("Selected items:", selected_items)
    assert any(item.lower() in text.lower() for text in selected_items)

# PYTHON.org 

# Test kontroluje, či existuje tlačidlo s textom na stiahnutie Pythonu
def test_python_download_button(test_page):
    print("Navigating to python.org")
    test_page.goto("https://www.python.org")

    # Cielené hľadanie textu obsahujúceho "Download Python"
    download_btn = test_page.get_by_text("Download Python", exact=False).first
    expect(download_btn).to_be_visible()

    text = download_btn.inner_text()
    print(f"Button text: {text}")
    assert "Download Python" in text

# Test vyhľadáva výraz "pytest" a kontroluje, že sa načítala stránka s výsledkami
def test_python_search_functionality(test_page):
    print("Searching on python.org")
    test_page.goto("https://www.python.org")

    search = test_page.locator("input#id-search-field")
    expect(search).to_be_visible()

    search.fill("pytest")
    search.press("Enter")

    url = test_page.url
    print(f"URL: {url}")
    assert "search" in url
