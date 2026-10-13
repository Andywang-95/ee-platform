import { getJson, type QueryParams } from "../api/client.ts";
import type { components } from "../api/schema.d.ts";

export type PartType = components["schemas"]["PartType"];
export type PartField = components["schemas"]["Field"];

// Rows are keyed by database column names, which differ per part type.
export type Part = { id: number } & Record<string, string | number | null>;

export type PartPage = Omit<components["schemas"]["PartPage"], "results"> & { results: Part[] };

export type FilterOptions = Record<string, string[]>;

export type PartListQuery = {
  type: string;
  search: string;
  filters: Record<string, string | undefined>;
  // A list field name, prefixed with "-" for descending order.
  ordering: string | undefined;
  page: number;
  pageSize: number;
};

export function toListParams(query: PartListQuery): QueryParams {
  return {
    ...query.filters,
    type: query.type,
    search: query.search.trim(),
    ordering: query.ordering,
    page: query.page,
    page_size: query.pageSize,
  };
}

export function fetchPartTypes(): Promise<PartType[]> {
  return getJson("/parts/types/");
}

export function fetchFilterOptions(typeCode: string): Promise<FilterOptions> {
  return getJson(`/parts/types/${encodeURIComponent(typeCode)}/filter-options/`);
}

export function fetchParts(query: PartListQuery): Promise<PartPage> {
  return getJson("/parts/", toListParams(query));
}

export function fetchPart(id: number): Promise<Part> {
  return getJson(`/parts/${id}/`);
}
