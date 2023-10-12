!pip install -q datasets transformers rouge-score
!apt install -q git-lfs
!pip install -q accelerate -U

from huggingface_hub import notebook_login
import transformers
import datasets
import random
import pandas as pd
from IPython.display import display, HTML
from transformers import EarlyStoppingCallback, AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer

if __name__ == "__main__":
    notebook_login()
    model_checkpoint = "eenzeenee/t5-base-korean-summarization"

    df = pd.read_csv("traindata.csv")
    df['본문'] = df['본문'].fillna('내용 링크 본문 참고')
    df['태그'] = df['태그'].fillna('')
    df['text'] = df['작성자'] + ' ' + df['공지'] + ' ' + df['제목'] + ' ' + df['본문']
    df = df[['text', '태그']]

    dataset = datasets.Dataset.from_pandas(df)

    train_test_dataset = dataset.train_test_split(test_size=0.05)
    test_valid = train_test_dataset['test'].train_test_split(test_size=0.01)
    train_test_valid_dataset = datasets.DatasetDict({
        'train': train_test_dataset['train'],
        'test': test_valid['test'],
        'valid': test_valid['train']})

    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

    if model_checkpoint in ["t5-small", "t5-base", "t5-large", "t5-3b", "t5-11b"]:
        prefix = "summarize: "
    else:
        prefix = ""

    max_input_length = 1024
    max_target_length = 48
    
    def preprocess_function(examples):
        model_inputs = tokenizer(examples["text"], max_length=max_input_length, truncation=True)
    
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(examples["태그"], max_length=max_target_length, truncation=True)
    
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_datasets = train_test_valid_dataset.map(preprocess_function, batched=True)

    model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)

    batch_size = 4
    model_name = model_checkpoint.split("/")[-1]
    args = Seq2SeqTrainingArguments(
        f"FingerFriend-t5-base-v1",
        evaluation_strategy = "epoch",
        save_strategy = "epoch",
        logging_strategy = 'epoch',
        learning_rate=1e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        weight_decay=0.01,
        num_train_epochs=20,
        predict_with_generate=True,
        fp16=True,
        metric_for_best_model = 'eval_loss',
        load_best_model_at_end = True,
        push_to_hub=False,
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    trainer = Seq2SeqTrainer(
        model,
        args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["valid"],
        data_collator=data_collator,
        tokenizer=tokenizer,
        callbacks=[EarlyStoppingCallback(early_stopping_patience = 1,early_stopping_threshold=0.01)]
    )   

    trainer.train()

    trainer.push_to_hub()