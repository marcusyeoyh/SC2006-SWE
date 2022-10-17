import React from 'react';
import Navbar from './components/Navbar';
import './App.css';
import Home from './components/pages/Home';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import MLAlgorithm from './components/pages/MLAlgorithm';
import Products from './components/pages/Products';
import SignUp from './components/pages/SignUp';
import SignUpProper from './components/pages/SignUpProper';
import Pwordreset from './components/pages/Pwordreset';


function App() {
  return (
    <>
      <Router>
        <Navbar />
        <Switch>
          <Route path='/' exact component={Home} />
          <Route path='/MLAlgorithm' component={MLAlgorithm} />
          <Route path='/products' component={Products} />
          <Route path='/sign-up' component={SignUp} />
          <Route path='/signupproper' component={SignUpProper} />
          <Route path='/pwordreset' component={Pwordreset} />
        </Switch>
      </Router>
    </>
  );
}

export default App;
