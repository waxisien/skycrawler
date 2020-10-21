import React from 'react';
import { useQuery } from '@apollo/react-hooks';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import { FixedSizeList, ListChildComponentProps } from 'react-window';
import AutoSizer from 'react-virtualized-auto-sizer';

import { BUILDINGS } from './lib/queries';
import { Building } from './types';

const MapViewList = (): JSX.Element => {
  const { loading, error, data } = useQuery(BUILDINGS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  const renderRow = (props: ListChildComponentProps): JSX.Element => {
    const { index, style } = props;

    const building: Building = data.buildings[index];
  
    return (
      <ListItem button style={style} key={index}>
        <ListItemText primary={`${building.name} - ${building.city.name}`} />
      </ListItem>
    );
  };

  return (
    <AutoSizer>
      {({ height, width}): JSX.Element => (
        <FixedSizeList
          height={height}
          width={width}
          itemSize={46}
          itemCount={data.buildings.length}
        >
          {renderRow}
        </FixedSizeList>
      )}
    </AutoSizer>
  );
}

export default MapViewList;
