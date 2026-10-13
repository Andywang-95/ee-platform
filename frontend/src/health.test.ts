import { afterEach, expect, test, vi } from "vite-plus/test";
import { fetchHealth, type Health } from "./health.ts";

const healthy: Health = { status: "ok", platform_db: true, parts_db: true, part_count: 3 };

function respondWith(body: unknown, status: number) {
  vi.stubGlobal(
    "fetch",
    vi.fn(async () => new Response(JSON.stringify(body), { status })),
  );
}

afterEach(() => {
  vi.unstubAllGlobals();
});

test("returns the health body when the backend is healthy", async () => {
  respondWith(healthy, 200);

  expect(await fetchHealth()).toEqual(healthy);
});

test("returns the health body when a database is down", async () => {
  const unhealthy: Health = { ...healthy, status: "error", parts_db: false, part_count: null };
  respondWith(unhealthy, 503);

  expect(await fetchHealth()).toEqual(unhealthy);
});

test("throws on any other error response", async () => {
  respondWith({ detail: "Not found." }, 404);

  await expect(fetchHealth()).rejects.toThrow("404");
});
