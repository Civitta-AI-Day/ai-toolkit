# Go

- **Validation:** decode into a request struct and validate with the project's validator
  (go-playground/validator or hand-written `Validate()` methods). Parse query parameters explicitly
  with typed errors.
- **Access:** the project's auth middleware puts the user in `context.Context`; check ownership on the
  loaded resource in the handler or service layer.
- **Large responses:** `rows.Next()` loop writing to an `encoding/csv` writer on the `http.ResponseWriter`,
  flushing periodically; never collect rows into a slice first.
- **Rate limits:** the project's middleware (`golang.org/x/time/rate`, httprate for Chi).
- **Indexes:** a new numbered SQL migration (golang-migrate, goose); never edit an applied one.
- **Tests:** table-driven tests with `httptest`, following existing helpers.
