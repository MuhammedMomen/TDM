from model import GlossaryModel, session
from sqlalchemy import func

class GlossaryManager:
    def __init__(self):
        #self.counter = session.query(func.max(GlossaryModel.id)).scalar() or 0
        pass

    def add_term(self, term, term_en, desc_en, desc_other, notes_en, notes_other, approval_status):
        self.counter = session.query(func.max(GlossaryModel.id)).scalar() or 0
        self.new_counter = self.counter+ 1
        new_term = GlossaryModel(
            id=self.new_counter,
            term=term, term_en=term_en,
            desc_en=desc_en, desc_other=desc_other,
            notes_en=notes_en, notes_other=notes_other,
            approval_status=approval_status
        )
        try:
            session.add(new_term)
            session.commit()
            return new_term
        except Exception as e:
            session.rollback()
            raise e

    def search_terms(self, query, filters):
        query = f"%{query}%"
        filtered_terms = session.query(GlossaryModel).filter(
            (GlossaryModel.term.ilike(query) | GlossaryModel.term_en.ilike(query) |
             GlossaryModel.desc_en.ilike(query) | GlossaryModel.desc_other.ilike(query) |
             GlossaryModel.notes_en.ilike(query) | GlossaryModel.notes_other.ilike(query))
        )
        if filters:
            filtered_terms = filtered_terms.filter(GlossaryModel.approval_status.in_(filters))
        return filtered_terms.all()

    def delete_term(self, term_id):
        try:
            term = session.query(GlossaryModel).filter(GlossaryModel.id == term_id).one()
            session.delete(term)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
