!pip install -q konlpy

import random
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt
from scipy.spatial import distance

def extract_tags_from_title(title):
    tags = []
    if any(keyword in title for keyword in _24):
        tags.append('2024년')
    if any(keyword in title for keyword in _23):
        tags.append('2023년')
    if any(keyword in title for keyword in _22):
        tags.append('2022년')
    if any(keyword in title for keyword in _21):
        tags.append('2021년')
    if any(keyword in title for keyword in _20):
        tags.append('2020년')
    if any(keyword in title for keyword in _19):
        tags.append('2019년')
    if any(keyword in title for keyword in _18):
        tags.append('2018년')
    if any(keyword in title for keyword in 상반기):
        tags.append('1학기')
    if any(keyword in title for keyword in 하반기):
        tags.append('2학기')
    return ', '.join(tags)

def tokenizer(raw_texts):
    return okt.morphs(raw_texts)
    
if __name__ == "__main__":
    df = pd.read_csv('/content/drive/MyDrive/대학교/DSL/모델링 스터디/모델링 프로젝트/final/traindata.csv')
    df['본문'] = df['본문'].fillna('내용 링크 본문 참고')
    df['date'] = pd.to_datetime(df['등록일'], errors='coerce', format='%Y-%m-%d')
    df['date'].fillna(pd.to_datetime(df['등록일'], errors='coerce', format='%Y.%m.%d'), inplace=True)
    df['date'].fillna(pd.to_datetime(df['등록일'], errors='coerce', format='%y.%m.%d'), inplace=True)
    df['date'] = df['date'].dt.date

    상반기 = ['1학기', '-1', '상반기', '여름', '봄', '하절기']
    하반기 = ['2학기', '-2', '하반기', '가을', '겨울', '동절기']
    _24 = ['2024', '24년', '24학']
    _23 = ['2023', '23년', '23학']
    _22 = ['2022', '22년', '22학']
    _21 = ['2021', '21년', '21학']
    _20 = ['2020', '20년', '20학']
    _19 = ['2019', '19년', '19학']
    _18 = ['2018', '18년', '18학']

    tqdm.pandas()
    df['tags'] = df['제목'].progress_apply(extract_tags_from_title)

    okt = Okt()
    
    df = df.dropna(axis = 0)
    df = df.reset_index(drop = True)
    df['cons1'] = df['작성자'] + ' ' + df['제목'] + ' ' + df['태그'] + ' ' + df['date'].astype('str') + ' ' + df['본문']

    vectorizer = TfidfVectorizer(tokenizer=tokenizer)
    
    tfidf_matrix = vectorizer.fit_transform(df['cons1']).toarray()

    keywords = vectorizer.get_feature_names_out()
    tf_idf_matrix = tfidf_matrix
    tfidf_matrix = tf_idf_matrix

    keyword_bias = '''대회
    공모전
    인턴
    채용
    교환
    장학
    기숙사
    졸업
    복수전공
    복학
    휴학
    성적
    신청
    변경
    철회
    축제
    등록
    셔틀
    학식
    AI
    창업
    학사
    일정
    '''
    
    keyword_bias_list = keyword_bias.strip().split('\n')
    
    keywords = vectorizer.get_feature_names_out()
    
    # Apply bias to the keyword in the TF-IDF matrix
    weight = 2.0  # Define a weight > 1 to bias the keyword
    for keyword in keyword_bias_list:
        # 토크나이즈
        tokens = tokenizer(keyword)
    
        # 각 토큰에 대한 인덱스를 찾아 TF-IDF 행렬의 가중치 조절
        for token in tokens:
            keyword_indices = np.where(keywords == token)[0]
            print(f"{token} : {keyword_indices}")
            if keyword_indices.size > 0:
                keyword_index = keyword_indices[0]
                tfidf_matrix[:, keyword_index] *= weight

    date_bias = '''
    2023
    2022
    2021
    2020
    2019
    2018
    2017
    2016
    '''

    date_bias_list = date_bias.strip().split('\n')
    
    keywords = vectorizer.get_feature_names_out()
    
    # Apply bias to the keyword in the TF-IDF matrix
    weight = 4.0  # Define a weight > 1 to bias the keyword
    for date_bias in date_bias_list:
        # 토크나이즈
        tokens = tokenizer(date_bias)
    
        # 각 토큰에 대한 인덱스를 찾아 TF-IDF 행렬의 가중치 조절
        for token in tokens:
            keyword_indices = np.where(keywords == token)[0]
            print(f"{token} : {keyword_indices}")
            if keyword_indices.size > 0:
                keyword_index = keyword_indices[0]
                tfidf_matrix[:, keyword_index] *= weight

    major_bias = '''
    응용통계학
    경제학
    인공지능
    컴퓨터과학
    상경
    '''

    keyword_bias_list = major_bias.strip().split('\n')
    
    keywords = vectorizer.get_feature_names_out()
    
    # Apply bias to the keyword in the TF-IDF matrix
    weight = 2.0  # Define a weight > 1 to bias the keyword
    for major_bias in keyword_bias_list:
        # 토크나이즈
        tokens = tokenizer(major_bias)
    
        # 각 토큰에 대한 인덱스를 찾아 TF-IDF 행렬의 가중치 조절
        for token in tokens:
            keyword_indices = np.where(keywords == token)[0]
            print(f"{token} : {keyword_indices}")
            if keyword_indices.size > 0:
                keyword_index = keyword_indices[0]
                tfidf_matrix[:, keyword_index] *= weight

    iterations = 30
    q_string_1 = ["AI 공모전 2023"]
    q_vec = vectorizer.transform(q_string_1).toarray()
    q_dist = [distance.cosine(q_vec.ravel(), t.ravel()) for t in tfidf_matrix]
    closest_index = sorted(range(len(q_dist)), key=lambda k: q_dist[k])[1:]
    results_1 = df['제목'].loc[closest_index[:iterations]]
    q_string_2 = ["인공지능 공모전 2023"]
    q_vec = vectorizer.transform(q_string_2).toarray()
    q_dist = [distance.cosine(q_vec.ravel(), t.ravel()) for t in tfidf_matrix]
    closest_index = sorted(range(len(q_dist)), key=lambda k: q_dist[k])[1:]
    results_2 = df['제목'].loc[closest_index[:iterations]]

    count = 0
    for i in results_1.index:
      for j in results_2.index:
        if i == j:
          count += 1
    print("Count : ", count)
    print("Iterations : ", iterations)
    print(f"Similarity Rate between {q_string_1} and {q_string_2} : {count / iterations * 100} %")