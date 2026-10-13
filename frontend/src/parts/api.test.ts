import { expect, test } from "vite-plus/test";
import { toListParams, type PartListQuery } from "./api.ts";

const query: PartListQuery = {
  type: "R",
  search: "",
  filters: {},
  ordering: undefined,
  page: 1,
  pageSize: 50,
};

test("maps the query to the API parameter names", () => {
  expect(toListParams({ ...query, search: " 10K ", ordering: "-value", page: 3 })).toEqual({
    type: "R",
    search: "10K",
    ordering: "-value",
    page: 3,
    page_size: 50,
  });
});

test("passes filters through as their own parameters", () => {
  const params = toListParams({ ...query, filters: { package: "0402", tolerance: undefined } });

  expect(params.package).toBe("0402");
  expect(params.tolerance).toBeUndefined();
});

test("a filter cannot override the reserved parameters", () => {
  expect(toListParams({ ...query, filters: { type: "C" } }).type).toBe("R");
});
