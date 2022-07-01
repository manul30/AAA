
import React from "react";
import { Button, Card, CardContent, TextField } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Container } from '@mui/system';
import { Users } from './routes/Users.js';
import { Login } from './routes/Login.js';
//import { Link } from "react-router-dom";


function App() {
  return (
    <Router>
    <div className="App">
     <Routes>
          <Route path="/" component={Login} />
          <Route path="/users" component={Users} />
      </Routes> 
    </div>
    </Router>
  );
}

export default App;
