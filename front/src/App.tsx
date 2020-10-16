import React from 'react';
import { ApolloProvider } from '@apollo/react-hooks';
import { IconButton } from '@material-ui/core';
import PlaceOutlinedIcon from '@material-ui/icons/PlaceOutlined';
import ViewListOutlinedIcon from '@material-ui/icons/ViewListOutlined';
import InfoOutlined from '@material-ui/icons/InfoOutlined';

import { client } from './lib/graphql';
import BuildingListView from './BuildingListView';
import InfoDialog from './InfoDialog';
import MapView from './MapView';

import './App.css';

const App = (): JSX.Element => {

  const [isViewMap, setIsViewMap] = React.useState(true);
  const [infoDialogOpen, setInfoDialogOpen] = React.useState(false);

  const toggleMenu = (): void => setIsViewMap(!isViewMap);
  const toggleDialogInfo = (): void => setInfoDialogOpen(!infoDialogOpen);

  return (
    <ApolloProvider client={client}>
      <header className="header">
        <IconButton aria-label="menu" color="default" onClick={toggleMenu}>
          {!isViewMap && <PlaceOutlinedIcon style={{ fill: 'white' }}/>}
          {isViewMap && <ViewListOutlinedIcon style={{ fill: 'white' }} />}
        </IconButton>
        Skycrawler
        <IconButton className='info-dialog-icon' aria-label="menu" color="default" onClick={toggleDialogInfo}>
          <InfoOutlined style={{ fill: 'white' }} />
        </IconButton>
        <InfoDialog open={infoDialogOpen} onClose={toggleDialogInfo}/>
      </header>
      {!isViewMap && <BuildingListView/>}
      {isViewMap && <MapView/>}
    </ApolloProvider>
  );
};

export default App;
