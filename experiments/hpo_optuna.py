import optuna, mlflow, mlflow.sklearn
from sklearn.svm import LinearSVC
# …

def objective(trial):
    C   = trial.suggest_float("C", 1e-3, 5.0, log=True)
    tol = trial.suggest_float("tol", 1e-5, 1e-1, log=True)

    pipeline = make_pipeline(
        TfidfVectorizer(max_features=15000, ngram_range=(1,2)),
        LinearSVC(C=C, tol=tol)
    )
    with mlflow.start_run(nested=True):
        f1 = cross_val_score(pipeline, X, y, scoring="f1", cv=3).mean()
        mlflow.log_params({"C": C, "tol": tol})
        mlflow.log_metric("f1", f1)
    return f1

if __name__ == "__main__":
    mlflow.set_experiment("wine_sentiment_hpo")
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=40)
    print("Best:", study.best_value, study.best_params)
