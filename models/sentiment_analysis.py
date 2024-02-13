from transformers import pipeline

class SentimentAnalysis:
    def __init__(self, model = 'distilbert/distilbert-base-uncased-finetuned-sst-2-english'):
        self.sentiment_pipeline = pipeline(model=model)

    def analyse(self, data):
        result = self.sentiment_pipeline(data)
        if result:
            return result
        return None