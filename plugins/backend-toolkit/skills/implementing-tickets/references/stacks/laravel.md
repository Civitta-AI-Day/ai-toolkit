# Laravel

- **Validation:** a `FormRequest` per endpoint (`rules()`, plus `after()` or `withValidator()` for
  cross-field rules). Never `$request->input()` without validation.
- **Access:** Policies (`$this->authorize('view', $customer)` or `can:` middleware).
- **Large responses:** `response()->streamDownload()` with `->lazy(1000)` or `->chunk(1000)` on the query.
- **Rate limits:** `RateLimiter::for()` in a service provider and `throttle:<name>` middleware.
- **Responses:** API Resources (`JsonResource`), never raw arrays.
- **Indexes:** a new migration (`php artisan make:migration`); never edit an existing one.
- **Tests:** feature tests with `actingAs()`, factories, `assertForbidden()`, `assertUnprocessable()`.
