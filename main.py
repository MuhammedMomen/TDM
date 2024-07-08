from flet import Page,app, AppView
from view import GlossaryPage

        
def main(page: Page):

    GlossaryPage(page)

app(target=main,view=AppView.WEB_BROWSER,host="10.0.5.8",port=9500,name="TDM",assets_dir="assets")
#app(target=main,view=AppView.WEB_BROWSER,host="192.168.1.14",port=8000,name="TDM",assets_dir="assets")
#app(target=main)
