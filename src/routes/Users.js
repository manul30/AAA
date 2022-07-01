import logo from '../logo.png';
import '../App.css';
import { Button, Card, CardContent, TextField } from '@mui/material';
import { Container } from '@mui/system';
import { Link } from "react-router-dom";
import  Linearbar from '../components/Linearbar.js'
import Piechart from '../components/Piechart';



export const Users = () => {

  return (
    <div className="App">
      <nav
        style={{
          borderBottom: "solid 1px",
          paddingBottom: "1rem",
        }}
      >
        <Link to="/invoices">Invoices</Link> |{" "}
        <Link to="/expenses">Expenses</Link>
      </nav>
      <Linearbar/>
      <Piechart></Piechart>
    </div>
  );
}

export default Users;
