import React from 'react';
import { useQuery } from '@apollo/react-hooks';
import { gql } from 'apollo-boost';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TableSortLabel from '@material-ui/core/TableSortLabel';
import Paper from '@material-ui/core/Paper';

import { Building } from './types';

const BUILDINGS = gql`
  {
    buildings {
      id
      floors
      height
      name
      city {
        name
      }
      status
    }
  }
`;

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

type Order = 'asc' | 'desc';

type CompareResult = -1 | 0 | 1; 

function descendingComparator<T>(a: T, b: T, orderBy: keyof T): CompareResult {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator<Key extends keyof any>(  // eslint-disable-line
  order: Order,
  orderBy: Key,
): (a: { [key in Key]: number | string }, b: { [key in Key]: number | string }) => number {
  return order === 'desc'
    ? (a, b): CompareResult => descendingComparator(a, b, orderBy)
    : (a, b): CompareResult => -descendingComparator(a, b, orderBy) as CompareResult;
}

function stableSort<T>(array: T[], comparator: (a: T, b: T) => number): T[] {
  const stabilizedThis = array.map((el, index) => [el, index] as [T, number]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  return stabilizedThis.map(el => el[0]);
}

const Buildings = (): JSX.Element => {
  const classes = useStyles();
  const { loading, error, data } = useQuery(BUILDINGS);

  const [order, setOrder] = React.useState<Order>('desc');

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  const handleRequestSort = (): void => {
    const isAsc = order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
  };

  return (
    <TableContainer component={Paper}>
      <Table className={classes.table} stickyHeader size="small">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>City</TableCell>
            <TableCell align="right" sortDirection={order}>
              <TableSortLabel
                active={true}
                direction={order}
                onClick={handleRequestSort}
              >
                Height (m)
              </TableSortLabel>
            </TableCell>
            <TableCell align="right">Floors</TableCell>
            <TableCell align="right">Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {stableSort<Building>(data.buildings, getComparator(order, 'height')).map((building) => (
            <TableRow key={building.id}>
              <TableCell component="th" scope="row">
                {building.name}
              </TableCell>
              <TableCell>{building.city.name}</TableCell>
              <TableCell align="right">{building.height}</TableCell>
              <TableCell align="right">{building.floors}</TableCell>
              <TableCell align="right">{building.status}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default Buildings;
