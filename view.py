from flet import (
IconButton,
icons,
border_radius,
Icon,
Theme,
Column,
Row,
ListView,
ExpansionTile,
SafeArea,
Container,
Checkbox,
Text,
TextField,
AlertDialog,
FloatingActionButton,
ElevatedButton,
border,
TextAlign,
TextStyle,
MainAxisAlignment,
Dropdown,
dropdown,
SnackBar,
Divider,
RoundedRectangleBorder
)
from header import Header
from palette import *
from controller import GlossaryManager
from model import GlossaryModel,session


        
class GlossaryPage:
    """
    This class represents a page for managing a glossary of terms.

    Attributes:
        page: The Flet Page object to display the glossary on.
        manager: An instance of GlossaryManager to handle term operations.
        cards: A Column widget to hold the glossary term cards.
        search_bar: A TextField widget for searching terms.
        checkboxes: A list of Checkbox widgets for filtering terms by approval status.
        add_term_button: A FloatingActionButton widget for adding new terms.
        header: An instance of the Header class to display the page header.

    Methods:
        __init__: Initializes the GlossaryPage object.
        page_setup: Sets up the layout and appearance of the page.
        create_search_bar: Creates and returns the search bar widget.
        create_checkboxes: Creates and returns the checkboxes for filtering.
        create_add_term_button: Creates and returns the button for adding terms.
        filter_terms: Filters the displayed terms based on search text and checkboxes.
        update_cards: Updates the displayed cards based on the provided list of terms.
        open_add_term_dialog: Opens a dialog to add a new term to the glossary.
        load_terms_from_db: Loads existing terms from the database and displays them.
        create_card: Creates a card widget for a single glossary term.
        on_update: Handles updates to the glossary, including new terms and deletions.
        on_hover: Handles hover events for glossary term cards.
    """
    def __init__(self, page):
        self.page = page
        self.page.scroll="always"
        self.manager = GlossaryManager()
        self.cards = Column()
        self.search_bar = self.create_search_bar()
        self.checkboxes = self.create_checkboxes()
        self.add_term_button = self.create_add_term_button()
        self.page.floating_action_button_location="END_DOCKED"
        self.header = Header("إدارة التوثيق", "ذاكرة الحقول", "مدير النظام", on_logout=callable, on_changeUsr=callable, on_changePWD=callable, on_notif=callable, page=self.page)
        self.header.start_clock_thread()
        self.page.appbar = self.header.get_app_bar()
        self.page_setup()

        self.page.pubsub.subscribe(self.on_update)
        self.load_terms_from_db()

    def page_setup(self):
        """Sets up the layout and appearance of the page."""
        self.page.title = "ذاكرة شرح الحقول المتكررة"
        self.page.theme_mode="Light"
        self.page.rtl = True
        self.page.window_maximized = True
        self.page.fonts={
        "lalezar": "fonts/Lalezar-Regular.ttf"
    }
        self.page.theme = Theme(font_family="lalezar")
        self.page.add(
            SafeArea(
                Container(
                    content=Column(
                        scroll="hidden",
                        controls=[
                            Row([self.search_bar,Container(Row([Text("الفلترة بـحالة الاعتماد"),Icon(icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED),*self.checkboxes]),padding=10,height=65,border_radius=15,border=border.all(1,fade_clr)) ,self.add_term_button]),
                            Container(
                                scale=0.9,
                                content=ListView(
                                    auto_scroll=False,
                                    controls=[self.cards],
                                    
                                ),
                                height=720,
                            ),
                        ]
                    )
                )
            )
        )

    def create_search_bar(self):
        """Creates and returns the search bar widget."""
        return TextField(
            prefix_icon=icons.SEARCH_ROUNDED,
            label="البحث في المصطلحات أو الشروحات أو الملاحظات أو رقم كود البطاقة",
            on_change=self.filter_terms,
            expand=True,
            border_color=fade_clr,
            border_radius=15,
            border_width=1,
            height=65
        )

    def create_checkboxes(self):
        """Creates and returns the checkboxes for filtering."""
        self.checkbox_approved = Checkbox(label="معتمد", value=False, on_change=self.filter_terms)
        self.checkbox_not_approved = Checkbox(label="غير معتمد", value=False, on_change=self.filter_terms)
        self.checkbox_approved_with_note = Checkbox(label="معتمد مع ملاحظة", value=False, on_change=self.filter_terms)
        return [self.checkbox_approved, self.checkbox_not_approved, self.checkbox_approved_with_note]

    def create_add_term_button(self):
        """Creates and returns the button for adding terms."""
        return FloatingActionButton(
            bgcolor="#7077A1",
            icon=icons.ADD,
            on_click=self.open_add_term_dialog,
            tooltip="إضافة نص جديد للذاكرة",
            
        )

    def filter_terms(self, e):
        """Filters the displayed terms based on search text and checkboxes."""
        search_text = self.search_bar.value
        filters = []
        if self.checkbox_approved.value:
            filters.append("معتمد")
        if self.checkbox_not_approved.value:
            filters.append("غير معتمد")
        if self.checkbox_approved_with_note.value:
            filters.append("معتمد مع ملاحظة")
        filtered_terms = self.manager.search_terms(search_text, filters)
        self.update_cards(filtered_terms)

    def update_cards(self, terms):
        """Updates the displayed cards based on the provided list of terms."""
        self.cards.controls.clear()
        for term in terms:
            card = self.create_card(term)
            self.cards.controls.append(card)
        self.page.update()

    def open_add_term_dialog(self, e):
        """Opens a dialog to add a new term to the glossary."""
        self.term_title = TextField(label="عنوان النص", rtl=True, label_style=TextStyle(color=fade_clr), text_style=TextStyle(color=scndry_clr),height=65,border_color=fade_clr,border_radius=15,border_width=1)
        self.term_title_en = TextField(label="عنوان النص -أجنبي", label_style=TextStyle(color=fade_clr), text_style=TextStyle(color=scndry_clr),height=65,border_color=fade_clr,border_radius=15,border_width=1)
        self.term_desc_en = TextField(label="شرح النص", rtl=True, label_style=TextStyle(color=fade_clr), text_style=TextStyle(color=scndry_clr),height=65,border_color=fade_clr,border_radius=15,border_width=1)
        self.term_desc_other = TextField(label="شرح النص -أجنبي", label_style=TextStyle(color=fade_clr), text_style=TextStyle(color=scndry_clr),height=65,border_color=fade_clr,border_radius=15,border_width=1)
        self.term_notes_en = TextField(label="ملاحظات", rtl=True, label_style=TextStyle(color=fade_clr), text_style=TextStyle(color=scndry_clr),height=65,border_color=fade_clr,border_radius=15,border_width=1)
        self.term_notes_other = TextField(label="ملاحظات - أجنبي", label_style=TextStyle(color=fade_clr), text_style=TextStyle(color=scndry_clr),height=65,border_color=fade_clr,border_radius=15,border_width=1)
        self.approval_status = Dropdown(
            content_padding=10,
            hint_text="حالة الاعتماد",
            hint_style=TextStyle(color=fade_clr),
            value="غير معتمد",
            options=[
                dropdown.Option("معتمد"),
                dropdown.Option("غير معتمد"),
                dropdown.Option("معتمد مع ملاحظة"),
            ],
            border_radius=border_radius.only(bottom_left=10, bottom_right=10),
            border_color=fade_clr,
        )

        def add_term(e):
            term = self.term_title.value
            term_en = self.term_title_en.value
            desc_en = self.term_desc_en.value
            desc_other = self.term_desc_other.value
            notes_en = self.term_notes_en.value
            notes_other = self.term_notes_other.value
            approval = self.approval_status.value
            if term or term_en or (desc_en and desc_other):
                new_term = self.manager.add_term(term, term_en, desc_en, desc_other, notes_en, notes_other, approval)
                self.cards.controls.append(self.create_card(new_term))
                self.page.close_dialog()
                self.page.pubsub.send_others(new_term)
                self.page.snack_bar = SnackBar(content=Text("تم إضافة نص جديد!",size=24,color=scndry_clr),bgcolor="Green")
                self.page.snack_bar.open = True
                self.page.update()
    


        add_term_dialog = AlertDialog(
            title=Text("إضافة نص جديد للذاكرة", **alrt_dlg_title_style),
            content=Column(
                scroll="always",
                width=800,
                expand=True,
                controls=[
                    self.term_title,
                    self.term_desc_en,
                    self.term_notes_en,
                    Divider(15, 1, fade_clr),
                    self.term_title_en,
                    self.term_desc_other,
                    self.term_notes_other,
                    self.approval_status,
                    Divider(15, 5, fade_clr),
                ]
            ),
            actions=[
                ElevatedButton(icon=icons.NEW_LABEL, text="إضافة", on_click=add_term, **ElevatedBtn_style),
                ElevatedButton(icon=icons.CANCEL_OUTLINED, text="إلغاء", on_click=lambda e: self.page.close_dialog(), **ElevatedBtn_style2),
            ],
            actions_alignment=MainAxisAlignment.CENTER,
            bgcolor=prim_clr,
        )
        self.page.dialog = add_term_dialog
        add_term_dialog.open = True
        self.page.update()
    
    def load_terms_from_db(self):
        """Loads existing terms from the database and displays them at initiation."""
        terms = session.query(GlossaryModel).all()
        self.cards.controls.clear()
        self.cards.update
        for term in terms:
            card = self.create_card(term)
            self.cards.controls.append(card)
        self.page.update()

    def create_card(self, term):
        """Creates a card widget for a single glossary term added.

         Also, Includes other functions that can be viewed on each single card created:
         1 -Copy each languages Description field, 
         2- Edit each language Description & Notes fields, 
         3- Clear each language Description & Notes fields,
         4- Save updates of edits and approval status,
         5- Delete entire card from db
           """
        
        def on_copy_desc(e):
            self.page.update()
            self.page.set_clipboard(desc_en_widget.value)
            self.page.snack_bar = SnackBar(content=Text("تم نسخ الشرح العربي!",color=scndry_clr),bgcolor=prim_clr)
            self.page.snack_bar.open = True
            self.page.update()
            
            

        def on_copy_desc_en(e):
            self.page.update()
            self.page.set_clipboard(desc_other_widget.value)
            self.page.snack_bar = SnackBar(content=Text("تم نسخ الشرح الأجنبي!",color=scndry_clr),bgcolor=prim_clr)
            self.page.snack_bar.open = True
            self.page.update()
            
            
        def on_edit_desc(e):
            for widget in [desc_en_widget, notes_en_widget]:
                widget.disabled = not widget.disabled
            self.page.update()

        def on_edit_desc_en(e):
            for widget in [desc_other_widget, notes_other_widget]:
                widget.disabled = not widget.disabled
            self.page.update()

        def on_clear(e):
            for widget in [desc_en_widget, notes_en_widget]:
                widget.value = ""
            self.page.update()

        def on_clear_en(e):
            for widget in [desc_other_widget, notes_other_widget]:
                widget.value = ""
            self.page.update()

        def on_delete(e):
            def confirm_delete(e):
                self.manager.delete_term(term.id)
                self.cards.controls.remove(card)
                self.page.snack_bar = SnackBar(content=Text("تم حذف النص!",size=24,color=scndry_clr),bgcolor=err_clr)
                self.page.snack_bar.open = True
                self.page.pubsub.send_others(term.id)
                self.page.close_dialog()  # Close the confirmation dialog
                self.page.update()

            self.page.dialog = AlertDialog(
                bgcolor=prim_clr,
                modal=True,
                title=Text("تأكيد الحذف",**alrt_dlg_title_style,),
                content=Text("هل أنت متأكد أنك تريد حذف هذا النص؟",color=scndry_clr),
                actions=[
                    ElevatedButton(text="حذف", **ElevatedBtn_style, on_click=confirm_delete),
                    ElevatedButton(text="إلغاء", **ElevatedBtn_style2, on_click=lambda e: self.page.close_dialog()),
                ],
                actions_alignment=MainAxisAlignment.END
            )
            self.page.dialog.open = True
            self.page.update()

        def on_approve_status_change(e):
            term.approval_status = e.control.value
            self.filter_terms(e)
        
        def on_save_changes(e):
            try:
                # Retrieve the term object from the database based on ID
                term_to_update = session.query(GlossaryModel).filter(GlossaryModel.id == term.id).one_or_none()

                if term_to_update:
                    # Update the attributes of the retrieved term
                    term_to_update.desc_en = desc_en_widget.value
                    term_to_update.notes_en = notes_en_widget.value
                    term_to_update.desc_other = desc_other_widget.value
                    term_to_update.notes_other = notes_other_widget.value

                    # Commit the changes to the database
                    session.commit()

                    self.page.snack_bar = SnackBar(
                        content=Text("تم حفظ التعديلات!", size=24, color=scndry_clr),
                        bgcolor="Green"
                    )
                    self.page.snack_bar.open = True

                else:
                    # Handle the case where the term with the given ID is not found
                    self.page.snack_bar = SnackBar(
                        content=Text("حدث خطأ أثناء الحفظ!", size=24, color=scndry_clr),
                        bgcolor=err_clr  # Assuming err_clr is defined in your palette
                    )
                    self.page.snack_bar.open = True

            except Exception as e:
                # Handle any potential exceptions during the database update
                session.rollback()
                print(f"Error updating term: {e}")
                self.page.snack_bar = SnackBar(
                    content=Text("حدث خطأ أثناء الحفظ!", size=24, color=scndry_clr),
                    bgcolor=err_clr
                )
                self.page.snack_bar.open = True

            self.page.update()

        desc_en_widget = TextField(
            multiline=True,
            max_lines=3,
            value=term.desc_en,
            disabled=True,
            expand=True,
            prefix_text="شرح النص:  ",
            prefix_style=TextStyle(size=13, weight="w200", color=prim_clr),
            prefix_icon=icons.DESCRIPTION_OUTLINED,
            border_color=fade_clr,
            tooltip="شرح النص عربي",
            
        )
        desc_other_widget = TextField(
            rtl=False,
            multiline=True,
            max_lines=3,
            value=term.desc_other,
            disabled=True,
            expand=True,
            prefix_text="شرح النص -أجنبي:  ",
            prefix_style=TextStyle(size=13, weight="w200", color=prim_clr),
            prefix_icon=icons.DESCRIPTION_OUTLINED,
            border_color=fade_clr,
            tooltip="شرح النص أجنبي",
        )
        notes_en_widget = TextField(
            multiline=True,
            max_lines=3,
            value=term.notes_en,
            disabled=True,
            expand=True,
            prefix_text="ملاحظات:  ",
            prefix_style=TextStyle(size=13, weight="w200", color=highlight_clr),
            prefix_icon=icons.STICKY_NOTE_2_OUTLINED,
            border_color=fade_clr,
            tooltip="ملاحظات عربي",
        )
        notes_other_widget = TextField(
            rtl=False,
            multiline=True,
            max_lines=3,
            value=term.notes_other,
            disabled=True,
            expand=True,
            prefix_text="ملاحظات - أجنبي:  ",
            prefix_style=TextStyle(size=13, weight="w200", color=highlight_clr),
            prefix_icon=icons.STICKY_NOTE_2_OUTLINED,
            border_color=fade_clr,
            tooltip="ملاحظات أجنبي",
        )

        approval_status_dropdown = Dropdown(
            content_padding=10,
            hint_text="حالة الاعتماد",
            width=145,
            height=40,
            options=[
                dropdown.Option("معتمد"),
                dropdown.Option("غير معتمد"),
                dropdown.Option("معتمد مع ملاحظة"),
            ],
            on_change=on_approve_status_change,
            value=term.approval_status,
            border_radius=border_radius.only(bottom_left=10, bottom_right=10),
            border_color=fade_clr,
        )

        inner_card = ExpansionTile(
            tooltip=f"  اضغط للحصول على معلومات بطاقة رقم # ({term.id})\n بعنوان ({term.term} - {term.term_en})",
            scale=0.9,
            shape=RoundedRectangleBorder(),
            title=Text(f"{term.term} - {term.term_en}", text_align=TextAlign.CENTER, weight="Bold", color=prim_clr,size=28),
            leading=Text(f"كود# {term.id}", text_align=TextAlign.CENTER, weight="Bold", color=prim_clr,size=28),
            controls=[
                Column([
                    Row([
                        desc_en_widget,
                        IconButton(icon=icons.COPY_ALL, on_click=on_copy_desc,tooltip="نسخ الشرح العربي"),
                        IconButton(icon=icons.EDIT, on_click=on_edit_desc,tooltip="تعديل الشرح العربي والملاحظات"),
                        IconButton(icon=icons.CLEAR_OUTLINED, on_click=on_clear,tooltip="مسح الشرح العربي والملاحظات"),
                        approval_status_dropdown,
                    ]),
                    Container(notes_en_widget),
                    Divider(15, 1, fade_clr),
                    Row([
                        desc_other_widget,
                        IconButton(icon=icons.COPY_ALL, on_click=on_copy_desc_en,tooltip="Copy English Description"),
                        IconButton(icon=icons.EDIT, on_click=on_edit_desc_en,tooltip="Edit English Desc & Notes"),
                        IconButton(icon=icons.CLEAR_OUTLINED, on_click=on_clear_en,tooltip="Clear English Description & Notes"),
                    ]),
                    Container(notes_other_widget),
                    Divider(15, 5, fade_clr, opacity=0.5),
                    Row(
                        controls=[
                            ElevatedButton(text="حفظ التعديلات", icon=icons.SAVE_ROUNDED,**ElevatedBtn_style2,on_click=on_save_changes),
                            ElevatedButton(text="حذف البطاقة", icon=icons.DELETE_FOREVER,**ElevatedBtn_style, on_click=on_delete),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    Divider(25, 1, "transparent"),
                ]),
            ],
        )

        card = Container(
            margin=10,
            padding=20,
            content=inner_card,
            border=border.all(2, prim_clr),
            border_radius=border_radius.all(15),
            on_hover=lambda e: self.on_hover(e, term),
            bgcolor=scndry_clr,
        )

        term.card= card
        return card

    # def on_new_term(self, term):
    #     card = self.create_card(term)
    #     self.cards.controls.append(card)
    #     self.page.update()
    def on_update(self, data):
            """Handles updates from other users."""
            if isinstance(data, GlossaryModel):  # New term added
                self.cards.controls.append(self.create_card(data))
                self.page.snack_bar = SnackBar(content=Text("تم إضافة نص جديد!",size=24,color=scndry_clr),bgcolor="Green")
                self.page.snack_bar.open = True
            elif isinstance(data, int):  # Term deleted
                for i, card in enumerate(self.cards.controls):
                    # Access the Text control within the ExpansionTile's leading
                    if int(card.content.leading.value.split("# ")[1]) == data:
                        del self.cards.controls[i]
                        self.page.snack_bar = SnackBar(content=Text("تم حذف النص!",size=24,color=scndry_clr),bgcolor=err_clr)
                        self.page.snack_bar.open = True
                        break

            self.page.update()
        

    def on_hover(self, e, term):  # Pass the term object directly
            """Handles hover events for glossary term cards."""
            card = term.card  # Access the card using the stored reference
            if e.data == "true":
                card.border = border.all(4, highlight_clr)
            else:
                card.border = border.all(2, prim_clr)
            card.update()

# >> For Testing view <<<
# def main(page: Page):

    
#     # page.floating_action_button=FloatingActionButton("Test")
#     # page.floating_action_button_location="END_DOCKED"
#     GlossaryPage(page)

# app(target=main,view=AppView.WEB_BROWSER,host="10.0.5.8",port=8000,name="TDM",assets_dir="assets")
# #app(target=main)
