import React, { useState } from 'react';
import { useQuery } from '@apollo/react-hooks';
import GoogleMapReact, { Bounds, ChangeEventValue, Coords } from 'google-map-react';
import supercluster from 'points-cluster';

import { BUILDINGS } from './lib/queries';
import { Building } from './types';
import MapMarker from './MapMarker';
import MapClusterMarker from './MapClusterMarker';

const adaptBuildingList = (buildings: Building[]) =>
  buildings.map((building: Building) => ({
    id: building.id,
    lat: building.city.latitude,
    lng: building.city.longitude,
    text: building.name,
  }));

const MapView = (): JSX.Element => {
  const defaultCenter = {lat: 40, lng: 30};
  const defaultZoom = 2;
  const minZoom = 2;
  const maxZoom = 7;

  const { loading, error, data } = useQuery(BUILDINGS);
  const [clusters, setClusters] = useState([]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  const buildings = adaptBuildingList(data.buildings);

  const getClusters = (center: Coords, zoom: number, bounds: Bounds) => {
    const mapOptions = {
      minZoom,
      maxZoom,
      radius: 50,
    }
    return supercluster(buildings, mapOptions)({ center, zoom, bounds });
  };

  const createClusters = (center: Coords, zoom: number, bounds: Bounds) => {
    if (!bounds) return [];

    return getClusters(center, zoom, bounds).map(
      (cluster: any) => ({
        lat: cluster.wy,
        lng: cluster.wx,
        numPoints: cluster.numPoints,
        key: `${cluster.numPoints}_${cluster.points[0].id}`,
        points: cluster.points,
      }));
  };

  const onMapChange = (value: ChangeEventValue): void =>
    setClusters(createClusters(value.center, value.zoom, value.bounds));

  return (
    <div className={'map'}>
      <GoogleMapReact
        bootstrapURLKeys={{ key: process.env.REACT_APP_GOOGLE_MAP_API_KEY as string }}
        defaultCenter={defaultCenter}
        defaultZoom={defaultZoom}
        onChange={onMapChange}
        options={{ minZoom, maxZoom }}
      >
        {clusters.map((item: any) => {
          if (item.numPoints === 1) {
            return (
              <MapMarker
                key={item.key}
                lat={item.points[0].lat}
                lng={item.points[0].lng}
                text={item.points[0].text}
              />
            );
          } else {
            return (
              <MapClusterMarker
                key={item.key}
                lat={item.lat}
                lng={item.lng}
                points={item.points}
              />
            )
          }
        })}
      </GoogleMapReact>
    </div>
  );
};

export default MapView;
