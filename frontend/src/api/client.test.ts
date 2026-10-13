import { afterEach, expect, test, vi } from "vite-plus/test";
import { ApiError, getJson, toQueryString } from "./client.ts";

function respondWith(body: unknown, status: number) {
  const fetchMock = vi.fn(async (_url: string) => new Response(JSON.stringify(body), { status }));
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

afterEach(() => {
  vi.unstubAllGlobals();
});

test("toQueryString skips empty and undefined values", () => {
  expect(toQueryString({ type: "R", search: "", page: 2, package: undefined })).toBe(
    "?type=R&page=2",
  );
  expect(toQueryString({})).toBe("");
});

test("toQueryString encodes special characters", () => {
  expect(toQueryString({ tolerance: "1%", search: "a b" })).toBe("?tolerance=1%25&search=a+b");
});

test("getJson requests under /api and returns the body", async () => {
  const fetchMock = respondWith([{ code: "R" }], 200);

  expect(await getJson("/parts/types/")).toEqual([{ code: "R" }]);
  expect(fetchMock.mock.calls[0][0]).toBe("/api/parts/types/");
});

test("getJson throws an ApiError carrying the status and body", async () => {
  respondWith({ detail: "Not found." }, 404);

  const error = await getJson("/parts/999/").catch((caught: unknown) => caught);

  expect(error).toBeInstanceOf(ApiError);
  expect(error).toMatchObject({ status: 404, body: { detail: "Not found." } });
});
