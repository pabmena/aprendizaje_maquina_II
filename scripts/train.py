@click.command()
@click.option("--input-path",  default="s3://data/processed/wine_train.parquet")
@click.option("--output-model", default="wine_model")
def main(input_path, output_model):
    df = wr.s3.read_parquet(input_path)
    X, y = df["review"], df["label"]

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=20000)),
        ("clf",  LogisticRegression(max_iter=200, n_jobs=-1))
    ])

    with mlflow.start_run():
        pipe.fit(X, y)
        y_pred = cross_val_predict(pipe, X, y, cv=5)
        f1 = f1_score(y, y_pred)
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(pipe, artifact_path=output_model)
        mlflow.register_model(f"runs:/{mlflow.active_run().info.run_id}/{output_model}",
                              name="WineSentiment")
