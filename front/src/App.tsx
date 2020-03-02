import React, { useState } from 'react';
import { ApolloProvider } from '@apollo/react-hooks';
import { IconButton } from '@material-ui/core';
import PlaceOutlinedIcon from '@material-ui/icons/PlaceOutlined';
import ViewListOutlinedIcon from '@material-ui/icons/ViewListOutlined';

import { client } from './lib/graphql';
import Buildings from './Buildings';

import './App.css';

const App = (): JSX.Element => {

  const [isViewMap, setIsViewMap] = useState(false);

  const toggleMenu = (): void => setIsViewMap(!isViewMap);

  return (
    <ApolloProvider client={client}>
      <header className="header">
        <IconButton aria-label="menu" color="default" onClick={toggleMenu}>
          {!isViewMap && <PlaceOutlinedIcon style={{ fill: 'white' }}/>}
          {isViewMap && <ViewListOutlinedIcon style={{ fill: 'white' }}/>}
        </IconButton>
      </header>
      {!isViewMap && <Buildings/>}
      {isViewMap && 'Incoming...'}
    </ApolloProvider>
  );
};

export default App;
