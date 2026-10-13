import { useQuery } from "@tanstack/react-query";
import { Alert, Descriptions, Drawer, Skeleton } from "antd";
import { fetchPart, type PartType } from "./api.ts";

type Props = {
  partId: number | null;
  partType: PartType;
  onClose: () => void;
};

export function PartDetailDrawer({ partId, partType, onClose }: Props) {
  const {
    data: part,
    isPending,
    isError,
  } = useQuery({
    queryKey: ["parts", "detail", partId],
    queryFn: () => fetchPart(partId!),
    enabled: partId !== null,
  });

  // The table has far more columns than one part uses; empty ones are noise.
  const items = part
    ? partType.detail_fields
        .filter(({ name }) => part[name] !== null && part[name] !== "")
        .map(({ name, label }) => ({ key: name, label, children: part[name] }))
    : [];

  return (
    <Drawer title="零件資料" size="large" open={partId !== null} onClose={onClose}>
      {isError && <Alert type="error" showIcon title="無法載入零件資料" />}
      {!isError && isPending && <Skeleton active />}
      {part && <Descriptions column={1} bordered size="small" items={items} />}
    </Drawer>
  );
}
