import React from 'react';
import { useQuery } from '@apollo/react-hooks';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import { FixedSizeList, ListChildComponentProps } from 'react-window';
import AutoSizer from 'react-virtualized-auto-sizer';
import { Bounds } from 'google-map-react';

import { BUILDINGS } from './lib/queries';
import { Building, City } from './types';

interface MapViewListProps {
  mapBounds: Bounds | undefined;  
}
const MapViewList = (props: MapViewListProps): JSX.Element => {
  const { mapBounds } = props;
  const { loading, error, data } = useQuery(BUILDINGS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  const isInBoundaries = (building: Building) => {
    if (!mapBounds) return false;

    const city: City = building.city;
    const lat = city.latitude;
    const lng = city.longitude;

    return mapBounds.ne.lat > lat && mapBounds.ne.lng > lng &&
      mapBounds.nw.lat > lat && mapBounds.nw.lng < lng &&
      mapBounds.se.lat < lat && mapBounds.se.lng > lng &&
      mapBounds.sw.lat < lat && mapBounds.sw.lng < lng
  };

  const compareByHeight = (a: Building, b: Building) => b.height - a.height;

  const buildings = data.buildings.filter(isInBoundaries).sort(compareByHeight);

  const handleClick = (link: string) => (): void => {
    window.open(link, '_blank')
  };

  const renderRow = (props: ListChildComponentProps): JSX.Element => {
    // eslint-disable-next-line
    const { index, style } = props;

    const building: Building = buildings[index];
  
    const primaryLabel = `${building.name} - ${building.city.name}`;
    const secondaryLabel = building.height ? `${building.height}m`: '';

    return (
      <ListItem button style={style} key={index} onClick={handleClick(building.link)}>
        <ListItemText primary={primaryLabel} secondary={secondaryLabel}/>
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
          itemCount={buildings.length}
        >
          {renderRow}
        </FixedSizeList>
      )}
    </AutoSizer>
  );
}

export default React.memo(MapViewList);
