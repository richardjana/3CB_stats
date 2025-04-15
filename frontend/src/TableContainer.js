import React from 'react';
import { Link } from 'react-router';
import { useSortBy, useTable } from 'react-table';

import InfoHover from './InfoHover';

const TableContainer = ({ columns, data }) => {
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable(
      {
        columns,
        data,
      },
      useSortBy // Apply the useSortBy plugin here
    );

  const generateSortingIndicator = (column) => {
    return column.isSorted
      ? column.isSortedDesc
        ? ' \u23F7'
        : ' \u23F6'
      : ' \u23FA';
  };

  return (
    <table {...getTableProps()}>
      <thead>
        {headerGroups.map((headerGroup) => {
          const { key, ...restHeadProps } = headerGroup.getHeaderGroupProps();
          return (
            <tr key={key} {...restHeadProps}>
              {headerGroup.headers.map((column) => {
                const { key, ...restProps } = column.getHeaderProps(
                  column.getSortByToggleProps()
                );
                return (
                  <th key={key} {...restProps}>
                    {column.render('Header')}
                    {column.infoHover && <InfoHover type={column.infoHover} />}
                    {generateSortingIndicator(column)}
                  </th>
                );
              })}
            </tr>
          );
        })}
      </thead>

      <tbody {...getTableBodyProps()}>
        {rows.map((row) => {
          prepareRow(row);
          const { key, ...restRowProps } = row.getRowProps();
          return (
            <tr key={key} {...restRowProps}>
              {row.cells.map((cell) => {
                const { key, ...restCellProps } = cell.getCellProps();
                if (cell.column.Header === 'Name') {
                  return (
                    <td
                      key={key}
                      {...restCellProps}
                      style={{ textAlign: 'left' }}
                    >
                      <Link to={`/player/${cell.value}`}>
                        {cell.render('Cell')}
                      </Link>
                    </td>
                  );
                }
                return (
                  <td
                    key={key}
                    {...restCellProps}
                    style={{ textAlign: 'right' }}
                  >
                    {cell.render('Cell')}
                  </td>
                );
              })}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default TableContainer;
