def compare_and_promote(**context):
    client   = mlflow.tracking.MlflowClient()
    prod     = client.get_model_version_by_alias("WineSentiment", "Production")
    challenger_run_id = context["ti"].xcom_pull(key="run_id")

    prod_metric        = float(prod.tags["f1_score"])
    challenger_metric  = float(
        client.get_run(challenger_run_id).data.metrics["f1_score"]
    )

    if challenger_metric > prod_metric:
        client.set_registered_model_alias(
            name="WineSentiment",
            alias="Staging",
            version=prod.version,
        )
        client.set_registered_model_alias(
            name="WineSentiment",
            alias="Production",
            version=client.get_latest_versions(
                "WineSentiment", stages=["None"]
            )[0].version,
        )
