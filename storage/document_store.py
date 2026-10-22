from db.mongo import documents
class DocumentStore:
    def save_document(self, document):
        """
        Save a new document.
        """
        return documents.insert_one(document)
    def find_by_url(self, url):
        """
        Find a document using its URL.
        """
        return documents.find_one({"url": url})
    def find_by_content_hash(self, content_hash):
        """
        Find duplicate content.
        """
        return documents.find_one({"content_hash": content_hash})
    def get_document(self, document_id):
        """
        Get document by MongoDB ObjectId.
        """
        from bson import ObjectId
        return documents.find_one({"_id": ObjectId(document_id)})
    def update_document(self, url, updated_fields):
        """
        Update an existing document.
        """
        return documents.update_one(
            {"url": url},
            {"$set": updated_fields}
        )
    def delete_document(self, url):
        """
        Delete a document.
        """
        return documents.delete_one({"url": url})
    def get_all_documents(self):
        """
        Return all indexed documents.
        """
        return documents.find()