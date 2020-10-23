import React from 'react';
import { Bounds } from 'google-map-react';

import MapView from "./MapView"
import MapViewList from './MapViewList';

const MapViewLayout = (): JSX.Element => {
  // TODO: use store
  const [bounds, setBounds] = React.useState<Bounds>();

  const onBoundsChange = (_bounds: Bounds) => setBounds(_bounds);

  return (
    <div className="map-view-layout">
      <div className="map-view-column">
        <MapView onBoundsChange={onBoundsChange}/>
      </div>
      <div className='map-view-list-column'>
        <MapViewList mapBounds={bounds}/>
      </div>
    </div>
  );
}

export default MapViewLayout;
