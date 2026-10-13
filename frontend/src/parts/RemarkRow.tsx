import { Tooltip } from "antd";
import type { HTMLAttributes } from "react";

export type RemarkRowProps = HTMLAttributes<HTMLTableRowElement> & {
  remark?: string | null;
};

// Table row that shows the part's remark while the pointer is over it.
export function RemarkRow({ remark, ...rowProps }: RemarkRowProps) {
  const row = <tr {...rowProps} />;
  if (!remark) return row;
  return (
    <Tooltip title={remark} placement="topLeft" mouseEnterDelay={0.2}>
      {row}
    </Tooltip>
  );
}
