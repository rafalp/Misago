from datetime import timedelta

import pytest
from ariadne import gql
from django.utils import timezone

from ....attachments.models import Attachment
from ....users.datadownloads import request_user_data_download
from ....users.deletesrecord import record_user_deleted_by_self
from ....users.test import create_test_user
from ..analytics import cumulate_data


test_query = gql(
    """
        query getAnalytics($span: Int!) {
            analytics(span: $span) {
                users {
                    ...data
                }
                userDeletions {
                    ...data
                }
                threads {
                    ...data
                }
                posts {
                    ...data
                }
                attachments {
                    ...data
                }
                dataDownloads {
                    ...data
                }
            }
        }

        fragment data on AnalyticsData {
            current
            currentCumulative
            previous
            previousCumulative
        }
    """
)


previous_datetime = timezone.now() - timedelta(days=30)
excluded_datetime = timezone.now() - timedelta(days=60)


def test_query_without_data_executes_without_errors(admin_graphql_client):
    result = admin_graphql_client.query(test_query, {"span": 30})
    assert result["analytics"]


def test_all_analytics_are_limited_to_requested_span(admin_graphql_client):
    result = admin_graphql_client.query(test_query, {"span": 30})
    for model_analytics in result["analytics"].values():
        assert len(model_analytics["current"]) == 30
        assert len(model_analytics["currentCumulative"]) == 30
        assert len(model_analytics["previous"]) == 30
        assert len(model_analytics["previousCumulative"]) == 30


def test_large_analytics_span_is_reduced_to_360(admin_graphql_client):
    result = admin_graphql_client.query(test_query, {"span": 3000})
    for model_analytics in result["analytics"].values():
        assert len(model_analytics["current"]) == 360
        assert len(model_analytics["currentCumulative"]) == 360
        assert len(model_analytics["previous"]) == 360
        assert len(model_analytics["previousCumulative"]) == 360


def test_short_analytics_span_is_extended_to_30(admin_graphql_client):
    result = admin_graphql_client.query(test_query, {"span": 0})
    for model_analytics in result["analytics"].values():
        assert len(model_analytics["current"]) == 30
        assert len(model_analytics["currentCumulative"]) == 30
        assert len(model_analytics["previous"]) == 30
        assert len(model_analytics["previousCumulative"]) == 30


def test_recent_user_registration_appears_in_current_analytics(admin_graphql_client):
    create_test_user("User", "user@example.com")
    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["users"]
    assert sum(analytics["current"]) == 2  # includes admin
    assert sum(analytics["previous"]) == 0


def test_older_user_registration_appears_in_previous_analytics(admin_graphql_client):
    create_test_user("User", "user@example.com", joined_on=previous_datetime)
    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["users"]
    assert sum(analytics["current"]) == 1  # includes admin
    assert sum(analytics["previous"]) == 1


def test_old_user_registration_is_excluded_from_analytics(admin_graphql_client):
    create_test_user("User", "user@example.com", joined_on=excluded_datetime)
    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["users"]
    assert sum(analytics["current"]) == 1  # includes admin
    assert sum(analytics["previous"]) == 0


def test_recent_thread_appears_in_current_analytics(
    admin_graphql_client, thread_factory, default_category
):
    thread_factory(default_category)
    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["threads"]
    assert sum(analytics["current"]) == 1
    assert sum(analytics["previous"]) == 0


def test_older_thread_appears_in_previous_analytics(
    admin_graphql_client, thread_factory, default_category
):
    thread_factory(default_category, started_at=previous_datetime)
    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["threads"]
    assert sum(analytics["current"]) == 0
    assert sum(analytics["previous"]) == 1


def test_old_thread_is_excluded_from_analytics(
    admin_graphql_client, thread_factory, default_category
):
    thread_factory(default_category, started_at=excluded_datetime)
    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["threads"]
    assert sum(analytics["current"]) == 0
    assert sum(analytics["previous"]) == 0


def test_recent_post_appears_in_current_analytics(
    admin_graphql_client, thread_factory, default_category
):
    thread_factory(default_category)
    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["posts"]
    assert sum(analytics["current"]) == 1
    assert sum(analytics["previous"]) == 0


def test_older_post_appears_in_previous_analytics(
    admin_graphql_client, thread_factory, default_category
):
    thread_factory(default_category, started_at=previous_datetime)
    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["posts"]
    assert sum(analytics["current"]) == 0
    assert sum(analytics["previous"]) == 1


def test_old_post_is_excluded_from_analytics(
    admin_graphql_client, thread_factory, default_category
):
    thread_factory(default_category, started_at=excluded_datetime)
    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["posts"]
    assert sum(analytics["current"]) == 0
    assert sum(analytics["previous"]) == 0


def test_recent_attachment_appears_in_current_analytics(admin_graphql_client):
    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploaded_at=timezone.now(),
        name="text.txt",
        slug="text-txt",
        upload="attachments/text.txt",
        size=1024 * 1024,
        filetype_id="txt",
    )

    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["attachments"]
    assert sum(analytics["current"]) == 1
    assert sum(analytics["previous"]) == 0


def test_older_attachment_appears_in_previous_analytics(admin_graphql_client):
    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploaded_at=previous_datetime,
        name="text.txt",
        slug="text-txt",
        upload="attachments/text.txt",
        size=1024 * 1024,
        filetype_id="txt",
    )

    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["attachments"]
    assert sum(analytics["current"]) == 0
    assert sum(analytics["previous"]) == 1


def test_old_attachment_is_excluded_from_analytics(admin_graphql_client):
    Attachment.objects.create(
        uploader_name="Anonymous",
        uploader_slug="anonymous",
        uploaded_at=excluded_datetime,
        name="text.txt",
        slug="text-txt",
        upload="attachments/text.txt",
        size=1024 * 1024,
        filetype_id="txt",
    )

    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["attachments"]
    assert sum(analytics["current"]) == 0
    assert sum(analytics["previous"]) == 0


def test_recent_data_download_appears_in_current_analytics(admin_graphql_client, user):
    request_user_data_download(user)

    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["dataDownloads"]
    assert sum(analytics["current"]) == 1
    assert sum(analytics["previous"]) == 0


def test_older_data_download_appears_in_previous_analytics(admin_graphql_client, user):
    download = request_user_data_download(user)
    download.requested_on = previous_datetime
    download.save()

    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["dataDownloads"]
    assert sum(analytics["current"]) == 0
    assert sum(analytics["previous"]) == 1


def test_old_data_download_is_excluded_from_analytics(admin_graphql_client, user):
    download = request_user_data_download(user)
    download.requested_on = excluded_datetime
    download.save()

    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["dataDownloads"]
    assert sum(analytics["current"]) == 0
    assert sum(analytics["previous"]) == 0


def test_recent_user_deletion_appears_in_current_analytics(admin_graphql_client):
    record_user_deleted_by_self()
    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["userDeletions"]
    assert sum(analytics["current"]) == 1
    assert sum(analytics["previous"]) == 0


def test_older_user_deletion_appears_in_previous_analytics(admin_graphql_client):
    deletion = record_user_deleted_by_self()
    deletion.deleted_on = previous_datetime
    deletion.save()

    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["userDeletions"]
    assert sum(analytics["current"]) == 0
    assert sum(analytics["previous"]) == 1


def test_old_user_deletion_is_excluded_from_analytics(admin_graphql_client):
    deletion = record_user_deleted_by_self()
    deletion.deleted_on = excluded_datetime
    deletion.save()

    result = admin_graphql_client.query(test_query, {"span": 30})
    analytics = result["analytics"]["userDeletions"]
    assert sum(analytics["current"]) == 0
    assert sum(analytics["previous"]) == 0


def test_data_is_cumulated():
    assert cumulate_data([1, 2]) == [1, 3]
