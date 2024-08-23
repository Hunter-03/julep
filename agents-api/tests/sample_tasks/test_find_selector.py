# Tests for task queries

import os
from uuid import uuid4

from ward import test

from ..fixtures import cozo_client, test_agent, test_developer_id
from ..utils import patch_embed_acompletion, patch_http_client_with_temporal

this_dir = os.path.dirname(__file__)


@test("workflow sample: find-selector")
async def _(
    cozo_client=cozo_client,
    developer_id=test_developer_id,
    agent=test_agent,
):
    agent_id = str(agent.id)
    task_id = str(uuid4())

    with patch_embed_acompletion(), open(
        f"{this_dir}/find_selector.yaml", "r"
    ) as sample_file:
        task_def = sample_file.read()

        async with patch_http_client_with_temporal(
            cozo_client=cozo_client, developer_id=developer_id
        ) as (
            make_request,
            client,
        ):
            make_request(
                method="POST",
                url=f"/agents/{agent_id}/tasks/{task_id}",
                headers={"Content-Type": "application/x-yaml"},
                data=task_def,
            )

            # execution_data = dict(input={"test": "input"})

            # make_request(
            #     method="POST",
            #     url=f"/tasks/{task_id}/executions",
            #     json=execution_data,
            # )
