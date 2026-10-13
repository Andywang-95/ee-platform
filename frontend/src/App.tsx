import { Layout, Typography } from "antd";
import { PartsPage } from "./parts/PartsPage.tsx";

function App() {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Layout.Header style={{ display: "flex", alignItems: "center" }}>
        <Typography.Title level={4} style={{ margin: 0, color: "#fff" }}>
          EE Platform
        </Typography.Title>
      </Layout.Header>
      <Layout.Content style={{ padding: 24 }}>
        <PartsPage />
      </Layout.Content>
    </Layout>
  );
}

export default App;
