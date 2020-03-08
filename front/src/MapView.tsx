import React from 'react';
import { useQuery } from '@apollo/react-hooks';
import GoogleMapReact from 'google-map-react';

import { BUILDINGS } from './lib/queries';
import { Building } from './types';
import MapMarker from './MapMarker';

const MapView = (): JSX.Element => {
  const center = {lat: 59.938043, lng: 30.337157};

  const { loading, error, data } = useQuery(BUILDINGS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <GoogleMapReact
        bootstrapURLKeys={{ key: process.env.REACT_APP_GOOGLE_MAP_API_KEY as string }}
        defaultCenter={center}
        defaultZoom={1}
      >
        {data.buildings.map((building: Building) => (
          <MapMarker
            key={building.id}
            lat={building.city.latitude}
            lng={building.city.longitude}
            text={building.name}
          />
        ))}
      </GoogleMapReact>
    </div>
  );
};

export default MapView;
