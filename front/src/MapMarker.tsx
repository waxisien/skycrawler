import * as React from 'react';

import './MapMarker.css';

interface MapMarkerProps {
  text: string;
  lng: number;
  lat: number;
}
const MapMarker = (props: MapMarkerProps): JSX.Element => {
  return (
    <div className="marker"
      style={{ backgroundColor: 'blue', cursor: 'pointer'}}
      title={props.text}
    />
  );
};

export default React.memo(MapMarker);
