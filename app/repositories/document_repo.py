from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from app.models.document import Base, DocumentModel

class DocumentRepository:

    def __init__(self, db_path = "sqlite:///documind.db"):

        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_document(self, filename : str, source_path : str, total_chunks : int, total_pages : int)->int:
        doc = DocumentModel(
            filename=filename,
            source_path=source_path,
            total_chunks=total_chunks,
            total_pages=total_pages
        )
        self.session.add(doc)  
        self.session.commit()
        return doc.id

    def get_all_documents(self) -> list[DocumentModel]:
        result = self.session.execute(select(DocumentModel))
        return result.scalars().all()

    def close(self):
        self.session.close()