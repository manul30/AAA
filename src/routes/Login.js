import logo from '../logo.png';
import '../App.css';
import './Login.css'
import { Button, Card, CardContent, TextField } from '@mui/material';
import { Container } from '@mui/system';
import { Link } from "react-router-dom";

import React, { useState, useEffect, useRef } from "react";

const API = process.env.REACT_APP_API;
//const API = "http://127.0.0.1:5000";

export const Login = () =>{
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [intentos, setIntento] = useState("");

    const [editing, setEditing] = useState(false);
    const [id, setId] = useState("");
  
    const nameInput = useRef(null);
  
    let [users, setUsers] = useState([]);


    const login = async (e) => {
        e.preventDefault();
        console.log("Hello World");
        console.log(API);
        const res = await fetch(`/login`,{
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                password,
            }),
        });
        const data = await res.json();
        console.log(data)
        //sawait res.json();
    };

    const register = async () => {
        const res = await fetch(`${API}/users`);
        const data = await res.json();
        //setUsers(data);
        console.log(data);
      };
    
      const handleSubmit = async (e) => {
        e.preventDefault();
        if (!editing) {
          const res = await fetch(`${API}/users`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name,
              email,
              password,
            }),
          });

          const data = await res.json();
          console.log(data);
        } else {
          const res = await fetch(`${API}/users/${id}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name,
              email,
              password,
            }),
          });
          const data = await res.json();
          console.log(data);
          setEditing(false);
          setId("");
        }
        
    
        setName("");
        setEmail("");
        setPassword("");
        nameInput.current.focus();
      };

    return (
        <Container className="LoginContainer" maxWidth="sm">

        <div className="LogoContainer">
            <div>
                <img src={logo} className="App-logo" alt="logo" />
            </div>
            Social Find
        </div>
        <div class="card">
        <h1>Bienvenido</h1>
        <form method="post">
            <div class="txt_field">
                <input type="text" required/>
                <span></span>
                <label for="Username">Correo</label>
            </div>
            <div class="txt_field">
                <input type="password" required/>
                <span></span>
                <label for="password">Contraseña</label>
            </div>
            <div class="pass">Contraseña olvidada?</div>
            <input type="submit" value="Login" onClick={login}/>
            <div class="signup_link">
            No eres miembro? <a href="#">Regístrate</a>
            <input type="submit" value="Register" onClick={register}/>
            <div>

            
            </div>
            </div>
        </form>
            <div>
            </div>

        </div>
        </Container>
    );
}

export default Login;