import * as React from 'react';

import { Building } from './types';

import './MapClusterMarker.css';

interface MapClusterMarkerProps {
  lng: number;
  lat: number;
  points: Building[];
}
const MapClusterMarker = (props: MapClusterMarkerProps): JSX.Element => {
  return (
    <div className="cluster-marker"
      style={{ backgroundColor: 'purple', cursor: 'pointer'}}
    >
      <span>{props.points.length}</span>
    </div>
  );
};

export default React.memo(MapClusterMarker);
