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
import Paper from '@material-ui/core/Paper';

import { IBuilding } from './types';

const BUILDINGS = gql`
  {
    buildings {
      id
      height
      name
      city {
        name
      }
    }
  }
`;

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

const Buildings = () => {
  const classes = useStyles();
  const { loading, error, data } = useQuery(BUILDINGS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  return (
    <TableContainer component={Paper}>
      <Table className={classes.table} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell align="right">Height (m)</TableCell>
            <TableCell align="right">City</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.buildings.map((building: IBuilding) => (
            <TableRow key={building.id}>
              <TableCell component="th" scope="row">
                {building.name}
              </TableCell>
              <TableCell align="right">{building.height}</TableCell>
              <TableCell align="right">{building.city.name}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>);
};

export default Buildings;
