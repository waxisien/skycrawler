import React from 'react';
import logo from './logo.svg';
import './App.css';
import { graphqlTest } from './lib/graphql';

const App = () => {

  graphqlTest();
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        Root
      </header>
    </div>
  );
};

export default App;
