from KoBERTSentimentEngine import predict2

def get_sentiments_KoBERT(text_seq) :
    sentiments = predict2.predict(text_seq)
    return sentiments


a = get_sentiments_KoBERT(["나는 코버트를 정복하였다!", "어제 잠을 못잤더니 머리가 좀 빙빙 돌아가는듯"])
print(a)