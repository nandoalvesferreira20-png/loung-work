export type Health = { status: "ok" };

export class ApiError extends Error {
  readonly status: number;
  readonly requestId: string | null;
  constructor(status: number, requestId: string | null);
}

export function createApiClient(
  baseUrl: string,
  fetcher?: typeof fetch,
): {
  health(options?: { signal?: AbortSignal }): Promise<Health>;
};
