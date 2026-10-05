# API change checklist

Works for any stack. Each item says what to look for in the existing code before writing new code.

## Input
- [ ] Every query parameter and body field is validated by the project's validation layer
      (serializer, form request, schema, DTO), not by hand in the handler.
- [ ] Dates, enums and ranges are checked, including rules across fields ("to" not before "from",
      maximum range).
- [ ] Invalid input returns 400 or 422 with field-level errors, in the same format as other endpoints.

## Access
- [ ] Authentication is required unless the ticket says otherwise.
- [ ] Authorization uses the project's existing permission or policy mechanism for that resource.
      Find how a sibling endpoint checks access and do exactly the same.
- [ ] A user without access gets 403 (or 404 if the project hides existence); never someone else's data.

## Data
- [ ] Queries filter and sort on indexed columns. Check the existing indexes in the models or migrations when there's a lot of data.
- [ ] Large results are paginated or streamed and read in chunks, never loaded into memory at once.
- [ ] Money, time zones and number formats follow the project's existing helpers.

## Side effects
- [ ] Sensitive actions (exports, deletes, permission changes) are audited through the project's
      audit or logging helper.
- [ ] Expensive endpoints are rate limited with the project's existing mechanism.
- [ ] Schema changes are new migrations; existing migrations are never edited.

## Response
- [ ] Output goes through the project's serialization layer (serializer, resource, DTO).
- [ ] File downloads set the content type and a `Content-Disposition` filename.

## Tests
- [ ] Happy path, no access, invalid input, empty result, plus each rule in the ticket.
- [ ] Tests use the project's fixtures and factories, and follow existing naming.
