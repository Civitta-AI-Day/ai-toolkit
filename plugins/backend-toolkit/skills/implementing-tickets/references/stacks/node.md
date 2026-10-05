# Node.js (Express, NestJS, Fastify)

- **Validation:** the project's schema library (zod, Joi, class-validator DTOs, Fastify JSON schema) at
  the route boundary. Never trust `req.query` directly.
- **Access:** the project's auth middleware or guards, plus an ownership check on the loaded resource.
- **Large responses:** stream with a cursor or batched queries (`for await` over a cursor, `.stream()` in
  Knex, Prisma `findMany` with `cursor`/`take` in batches) piped to the response.
- **Rate limits:** the project's limiter (`express-rate-limit`, `@nestjs/throttler`, `@fastify/rate-limit`).
- **Indexes:** a new migration (Prisma, Knex, TypeORM, Sequelize); never edit an applied one.
- **Tests:** the existing runner (Jest, Vitest, node:test) with supertest or the framework's test client.
