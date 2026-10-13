import { MessageOutlined } from "@ant-design/icons";
import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { Alert, Flex, Input, Select, Skeleton, Table, Tabs, type TableProps } from "antd";
import { useState } from "react";
import { fetchFilterOptions, fetchPartTypes, fetchParts, type Part, type PartType } from "./api.ts";
import { PartDetailDrawer } from "./PartDetailDrawer.tsx";
import { RemarkRow, type RemarkRowProps } from "./RemarkRow.tsx";

const DEFAULT_PAGE_SIZE = 50;

// What the user has chosen within one part type. Reset when the type changes.
type View = {
  search: string;
  filters: Record<string, string | undefined>;
  ordering: string | undefined;
  page: number;
  pageSize: number;
};

const INITIAL_VIEW: View = {
  search: "",
  filters: {},
  ordering: undefined,
  page: 1,
  pageSize: DEFAULT_PAGE_SIZE,
};

export function PartsPage() {
  const types = useQuery({ queryKey: ["parts", "types"], queryFn: fetchPartTypes });
  const [selectedCode, setSelectedCode] = useState<string>();

  if (types.isError) return <Alert type="error" showIcon title="無法載入零件類型" />;
  if (types.isPending) return <Skeleton active />;

  const partType = types.data.find(({ code }) => code === selectedCode) ?? types.data[0];
  if (!partType) return <Alert type="warning" showIcon title="尚未設定任何零件類型" />;

  return (
    <>
      <Tabs
        activeKey={partType.code}
        onChange={setSelectedCode}
        items={types.data.map(({ code, label }) => ({ key: code, label }))}
      />
      {/* The key gives every part type its own search, filters and page. */}
      <PartTable key={partType.code} partType={partType} />
    </>
  );
}

function PartTable({ partType }: { partType: PartType }) {
  const [view, setView] = useState<View>(INITIAL_VIEW);
  const [openPartId, setOpenPartId] = useState<number | null>(null);

  const options = useQuery({
    queryKey: ["parts", "filter-options", partType.code],
    queryFn: () => fetchFilterOptions(partType.code),
  });
  const query = { type: partType.code, ...view };
  const parts = useQuery({
    queryKey: ["parts", "list", query],
    queryFn: () => fetchParts(query),
    // Keep the current rows on screen while the next page or search loads.
    placeholderData: keepPreviousData,
  });

  // Any change to what is being searched goes back to the first page.
  const narrow = (change: Partial<View>) => setView({ ...view, ...change, page: 1 });

  const columns: TableProps<Part>["columns"] = partType.list_fields.map(
    ({ name, label }, index) => ({
      key: name,
      dataIndex: name,
      title: label,
      sorter: true,
      sortOrder: sortOrderOf(view.ordering, name),
      render: (value: Part[string], part) =>
        index === 0 && part[partType.remark_field] ? (
          <Flex gap="small" align="center">
            {value}
            <MessageOutlined aria-label="有備註" />
          </Flex>
        ) : (
          value
        ),
    }),
  );

  const onTableChange: TableProps<Part>["onChange"] = (pagination, _filters, sorter, extra) => {
    if (extra.action === "sort") {
      const { columnKey, order } = Array.isArray(sorter) ? sorter[0] : sorter;
      narrow({
        ordering: order ? `${order === "descend" ? "-" : ""}${String(columnKey)}` : undefined,
      });
    } else {
      setView({
        ...view,
        page: pagination.current ?? 1,
        pageSize: pagination.pageSize ?? DEFAULT_PAGE_SIZE,
      });
    }
  };

  return (
    <Flex vertical gap="middle">
      <Flex gap="small" wrap>
        <Input.Search
          allowClear
          placeholder="搜尋料號、值、描述"
          style={{ width: 280 }}
          onSearch={(search) => narrow({ search })}
        />
        {partType.filter_fields.map(({ name, label }) => (
          <Select
            key={name}
            allowClear
            showSearch
            placeholder={label}
            style={{ minWidth: 140 }}
            value={view.filters[name]}
            options={(options.data?.[name] ?? []).map((value) => ({ value, label: value }))}
            onChange={(value: string | undefined) =>
              narrow({ filters: { ...view.filters, [name]: value } })
            }
          />
        ))}
      </Flex>

      {parts.isError && <Alert type="error" showIcon title="無法載入零件資料" />}

      <Table<Part>
        rowKey="id"
        size="small"
        columns={columns}
        dataSource={parts.data?.results}
        loading={parts.isFetching}
        components={{ body: { row: RemarkRow } }}
        onRow={(part): RemarkRowProps => ({
          remark: part[partType.remark_field] as string | null,
          style: { cursor: "pointer" },
          onClick: () => setOpenPartId(part.id),
        })}
        onChange={onTableChange}
        pagination={{
          current: view.page,
          pageSize: view.pageSize,
          total: parts.data?.count,
          showSizeChanger: true,
          pageSizeOptions: [20, 50, 100, 200],
          showTotal: (total) => `共 ${total} 筆`,
        }}
        scroll={{ x: "max-content" }}
      />

      <PartDetailDrawer
        partId={openPartId}
        partType={partType}
        onClose={() => setOpenPartId(null)}
      />
    </Flex>
  );
}

function sortOrderOf(ordering: string | undefined, field: string) {
  if (ordering === field) return "ascend" as const;
  if (ordering === `-${field}`) return "descend" as const;
  return null;
}
