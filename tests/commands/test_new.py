import json

from redash.commands.new import new, DEFAULT_QUERY_NAME


def test_new_query(cli_runner, mock_client):
    query_id = 12345
    expected_new_query_response = dict(id=query_id)
    job_id_response = dict(job=dict(id=1))
    query_result_id = 1
    query_result_id_response = dict(job=dict(query_result_id=query_result_id))
    download_response = "Success"

    client = mock_client(
        [
            expected_new_query_response,
            job_id_response,
            query_result_id_response,
            download_response,
        ]
    )
    result = cli_runner.invoke(
        new, ["--query", "select 1", "--data-source-id", 1], obj=client
    )

    assert not result.exception
    assert download_response in result.stdout
    assert (
        client.called_endpoint == f"queries/{query_id}/results/{query_result_id}.json"
    )


def test_new_query_with_skip_execution(cli_runner, mock_client):
    query_id = 12345
    expected_new_query_response = dict(id=query_id)

    client = mock_client([expected_new_query_response])
    result = cli_runner.invoke(
        new,
        ["--query", "select 1", "--data-source-id", 1, "--execute", False],
        obj=client,
    )

    assert not result.exception
    assert expected_new_query_response == json.loads(result.stdout)
    assert "results" not in client.called_endpoint


def test_new_query_without_name_provides_name(cli_runner, mock_client):
    expected = dict(id=12345)
    client = mock_client(expected)
    result = cli_runner.invoke(
        new,
        ["--query", "select 1", "--data-source-id", 1, "--execute", False],
        obj=client,
    )

    assert not result.exception
    assert expected == json.loads(result.stdout)
    assert client.recorded_payload.get("name") == DEFAULT_QUERY_NAME


def test_new_query_with_name(cli_runner, mock_client):
    expected_result = dict(id=12345)
    expected_name = "Custom redash-cli query name"
    client = mock_client(expected_result)
    result = cli_runner.invoke(
        new,
        [
            "--query",
            "select 1",
            "--data-source-id",
            1,
            "--name",
            expected_name,
            "--execute",
            False,
        ],
        obj=client,
    )

    assert not result.exception
    assert expected_result == json.loads(result.stdout)
    assert client.recorded_payload.get("name") == expected_name
