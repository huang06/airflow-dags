from __future__ import annotations

import pendulum
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator


@dag(
    start_date=pendulum.datetime(2022, 12, 1, tz="UTC"),
    schedule_interval=None,
    catchup=False,
    tags=["example"],
)
def example_taskflow_k8s():
    @task.kubernetes(
        namespace="ds",
        image="docker.io/apache/airflow:2.4.3-python3.10",
        in_cluster=True,
    )
    def helloworld():
        print("Hello world")

    @task.kubernetes(
        namespace="ds",
        image="docker.io/apache/airflow:2.4.3-python3.10",
        in_cluster=True,
    )
    def lib_time():
        import time

        print(time.time())

    EmptyOperator(task_id="start") >> [helloworld(), lib_time()] >> EmptyOperator(task_id="end")


mydag = example_taskflow_k8s()
