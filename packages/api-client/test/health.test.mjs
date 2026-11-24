import assert from "node:assert/strict";
import { test } from "node:test";
import { ApiError, createApiClient } from "../index.js";

test("consome o endpoint de saúde", async () => {
  const client = createApiClient("http://localhost:8000", async (url) => {
    assert.equal(url.href, "http://localhost:8000/health");
    return Response.json({ status: "ok" });
  });
  assert.deepEqual(await client.health(), { status: "ok" });
});

test("preserva o identificador de requisição em erros HTTP", async () => {
  const client = createApiClient(
    "http://localhost:8000",
    async () =>
      new Response(null, { status: 503, headers: { "X-Request-ID": "abc" } }),
  );
  await assert.rejects(client.health(), {
    name: ApiError.name,
    status: 503,
    requestId: "abc",
  });
});

test("rejeita dados fora do contrato", async () => {
  const client = createApiClient("http://localhost:8000", async () =>
    Response.json({ status: "unknown" }),
  );
  await assert.rejects(client.health(), TypeError);
});
