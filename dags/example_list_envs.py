from __future__ import annotations

import os
from functools import partial

import pendulum
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)


@dag(
    start_date=pendulum.datetime(2022, 12, 1, tz="UTC"),
    schedule_interval=None,
    catchup=False,
    tags=["example"],
)
def example_list_envs():

    deployment = os.environ.get("DEPLOYMENT", "DUMMY")

    k8s_op = partial(
        KubernetesPodOperator,
        namespace="airflow",
        image="docker.io/library/alpine:3.17.0",
        image_pull_policy="Always",
        in_cluster=True,
        cmds=["/bin/sh", "-c"],
        arguments=[f"echo {deployment}"],
    )

    (
        EmptyOperator(task_id="start")
        >> k8s_op(name="list_envs", task_id="list_envs")
        >> EmptyOperator(task_id="end")
    )


mydag = example_list_envs()
