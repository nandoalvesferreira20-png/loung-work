import { createApiClient } from "@loung/api-client";

export const api = createApiClient(
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000",
);
