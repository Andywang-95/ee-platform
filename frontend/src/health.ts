export type Health = {
  status: "ok" | "error";
  platform_db: boolean;
  parts_db: boolean;
  part_count: number | null;
};

// The backend answers 503 with the same body when a database is down, so the
// body is read for both outcomes.
export async function fetchHealth(): Promise<Health> {
  const response = await fetch("/api/health/");
  if (!response.ok && response.status !== 503) {
    throw new Error(`Unexpected response from backend: ${response.status}`);
  }
  return (await response.json()) as Health;
}
