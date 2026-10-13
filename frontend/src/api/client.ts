export type QueryParams = Record<string, string | number | undefined>;

export class ApiError extends Error {
  readonly status: number;
  readonly body: unknown;

  constructor(status: number, body: unknown) {
    super(`API request failed with status ${status}`);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

export function toQueryString(params: QueryParams = {}): string {
  const search = new URLSearchParams();
  for (const [name, value] of Object.entries(params)) {
    if (value !== undefined && value !== "") search.set(name, String(value));
  }
  const query = search.toString();
  return query ? `?${query}` : "";
}

// Paths are relative so the same code works behind the dev server proxy and
// behind the production reverse proxy.
export async function getJson<T>(path: string, params?: QueryParams): Promise<T> {
  const response = await fetch(`/api${path}${toQueryString(params)}`, {
    headers: { Accept: "application/json" },
  });
  const body: unknown = await response.json().catch(() => null);
  if (!response.ok) throw new ApiError(response.status, body);
  return body as T;
}
