def mutateSentiment(df, colname_sentence='sentence_text', colname_sentiment = 'sentiment') :
    df_new = df.copy()
    df_new[colname_sentiment] = [textEngine.getSentiment(text) for text in df[colname_sentence]]
    return df_new
