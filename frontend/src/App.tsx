import { useEffect, useState } from "react";
import { fetchHealth, type Health } from "./health.ts";

type State =
  | { phase: "loading" }
  | { phase: "loaded"; health: Health }
  | { phase: "failed"; message: string };

function App() {
  const [state, setState] = useState<State>({ phase: "loading" });

  useEffect(() => {
    let cancelled = false;
    fetchHealth()
      .then((health) => {
        if (!cancelled) setState({ phase: "loaded", health });
      })
      .catch((error: unknown) => {
        const message = error instanceof Error ? error.message : String(error);
        if (!cancelled) setState({ phase: "failed", message });
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main>
      <h1>EE Platform</h1>
      {state.phase === "loading" && <p>正在連線到後端…</p>}
      {state.phase === "failed" && <p role="alert">無法連線到後端：{state.message}</p>}
      {state.phase === "loaded" && (
        <dl>
          <dt>後端</dt>
          <dd>{state.health.status === "ok" ? "正常" : "異常"}</dd>
          <dt>平台庫</dt>
          <dd>{state.health.platform_db ? "已連線" : "無法連線"}</dd>
          <dt>零件庫</dt>
          <dd>{state.health.parts_db ? "已連線" : "無法連線"}</dd>
          <dt>零件筆數</dt>
          <dd>{state.health.part_count ?? "—"}</dd>
        </dl>
      )}
    </main>
  );
}

export default App;
