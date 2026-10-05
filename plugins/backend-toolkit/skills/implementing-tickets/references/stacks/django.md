# Django and Django REST Framework

- **Validation:** a `serializers.Serializer` per endpoint for query parameters
  (`XQuerySerializer(data=request.query_params).is_valid(raise_exception=True)`). Cross-field rules in
  `validate()`. A parameter named after a Python keyword (`from`) is added in `get_fields()`.
- **Access:** `permission_classes` plus `self.check_object_permissions(request, obj)` for object-level
  checks; querysets filtered to what the user may see for lists.
- **Large responses:** `StreamingHttpResponse` with a generator; `csv.writer` over an object whose
  `write()` returns the value; `.values_list(...).iterator(chunk_size=1000)`.
- **Rate limits:** `throttle_classes = [ScopedRateThrottle]`, `throttle_scope = "..."`, and the scope's
  rate in `REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]`. Tests clear the cache between runs.
- **Indexes:** `Meta.indexes = [models.Index(fields=[...], name=...)]`, then `makemigrations`. Never
  edit an existing migration.
- **Tests:** pytest-django, `pytestmark = pytest.mark.django_db`, DRF's `APIClient` with
  `force_authenticate`. Streaming bodies: `b"".join(response.streaming_content)`.
