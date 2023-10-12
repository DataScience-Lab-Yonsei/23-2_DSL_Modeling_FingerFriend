import openai
import numpy as np
import pandas as pd
from tqdm.notebook import tqdm

if __name__ == "__main__":
    ## 전처리
    openai.api_key = ####

    df_1 = pd.read_csv("응용통계학과.csv")
    df_2 = pd.read_csv('공식홈페이지.csv')
    df_3 = pd.read_csv('국제처.csv')
    df_4 = pd.read_csv('도서관.csv')
    df_5 = pd.read_csv('AI_link.csv')
    df_6 = pd.read_csv('econs_link.csv')
    df_7 = pd.read_csv('생활관_최종.csv')
    df_8 = pd.read_csv('인공지능융합대학_최종.csv')

    df_1.rename(columns = {"학과":"작성자",
                           "서브":"공지"},
                inplace = True)
    df_1.drop(columns = "id", inplace = True)
    df_2.rename(columns = {"학과":"공지",
                           "서브":"작성자"},
                inplace = True)
    df_3.rename(columns = {"국제처":"작성자",
                           "공지사항":"공지"},
                inplace = True)
    df_4.rename(columns = {"도서관":"작성자"},
                inplace = True)
    df_4.drop(columns = "id", inplace = True)
    df_5.drop(columns = "id", inplace = True)
    df_6.drop(columns = "id", inplace = True)
    df_7['생활관'] = df_7['생활관'] + ' ' + df_7['카테고리']
    df_7.rename(columns = {"생활관":"작성자",
                           "서브":"공지"},
                inplace = True)
    df_7.drop(columns = "카테고리", inplace = True)
    df_7.drop(columns = "id", inplace = True)
    df_8.rename(columns = {"인공지능융합대학":"작성자",
                          "작성일":"등록일"},
                inplace = True)
    df_8.drop(columns = "id", inplace = True)

    df = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8])
    df = df.reset_index(drop = True)

    # 프롬프트 사용해 태그 생성
    sampled_dfs = []
    for author, group in df.groupby('작성자'):
        if len(group) <= 100:
            sampled_dfs.append(group)
        else:
            sampled_dfs.append(group.sample(n=100))
            
    df_1 = pd.concat(sampled_dfs)
    df_1 = df_1.reset_index(drop = True)


    input = []
    answer = []
    
    for _ in tqdm(range(len(df_1))):
        try:
            if pd.isna(df_1['본문'][_]) == True:
                input.append(df_1['제목'][_])
                answer.append('내용 링크 본문 참고')
            else:
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"""
                Generate five or less popular general tags related to the domain of these texts in Korean.
                Always include specified 기간 in accordance to instruction.
                instruction:
                * 공모 기간 : 2022. 7. 12.(화) ~ 2022. 8. 8.(월)
                * 공모 기간 : 2022. 1. 19.(수) ~ 2022. 2. 11.(금)
                * 서류 접수 2022. 5. 18.(수) ~ 5. 31.(화)
                
                
                ### Title : {df_1['제목'][_]}
                
                ### Text :  {df_1['본문'][_]}
                        """}
                    ],
                    temperature = 0.2,
                    top_p = 0.1,
                    max_tokens=256
                )
                input.append(df_1['제목'][_])
                answer.append(resp.choices[0]['message']['content'].strip())
        except Exception as e:
            print(f"Error occurred: {str(e)}")

    dataframe = pd.DataFrame({'제목' : input,
                             '태그' : answer})

    dataframe.to_csv('prompt.csv', index = False)