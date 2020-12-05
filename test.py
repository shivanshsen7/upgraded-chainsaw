def abusiveCheck(str1):
    import joblib
    import string
    import re
       
    import nltk
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    from nltk.corpus import stopwords
       
       	# nltk.download('wordnet')
    lemmatiser = WordNetLemmatizer()
    stemmer = PorterStemmer()
       
    jb = joblib.load("job_tfv")
    jb1 = joblib.load("job_model")
    
    
    
    punctuation_edit = string.punctuation.replace('\'','') +"0123456789"
    outtab = "                                         "
    trantab = str.maketrans(punctuation_edit, outtab)
    ps = PorterStemmer()
    lm = WordNetLemmatizer()
    c = []
    str1 = re.sub('[^a-zA-Z]', ' ', str1)
    str1= str1.lower()
    str1 = str1.split()
    str1 = [word for word in str1 if not word in set(stopwords.words('english'))]
    str1 = [ps.stem(lm.lemmatize(word)) for word in str1]
    str1 = " ".join(str1)
    c.append(str1)
       
    test = jb.transform(c).toarray()
    pred = jb1.predict(test) # type(pred)
    
    
    if pred[:,:].toarray().any() == 1:
        abusive_flag = "abusive comment."
    else:
        abusive_flag = "comment is fine."
    
    classes = ['toxic', 'severe_toxic' , 'obscene' , 'threat' , 'insult' , 'identity_hate']
    categories = list()
    for k in range(0,6):
        if pred[0,k] == 1:
            categories.append(classes[k])
        if pred[:,:].toarray().any() == 1:
            abusive_cat = categories
        else:
            abusive_cat = None
                
    output = (abusive_flag, abusive_cat)
    return (output)
