from sypht.client import SyphtClient


class AIService:
    _client = None

    def __init__(self, client_id: str, client_secret: str):
        if AIService._client is None:
            AIService._client = SyphtClient(client_id, client_secret)

    @property
    def client(self):
        return self._client

    def extract_invoice(self, file):
        fid = self.client.upload(file, products=["invoices"])
        return self.client.fetch_results(fid)
