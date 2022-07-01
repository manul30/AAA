import React, { useState, useEffect, useRef } from "react";

const API = process.env.REACT_APP_API;

export const Users = () =>{
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [intentos, setIntentos] = useState("");

    const [editing, setEditing] = useState(false);
    const [id, setId] = useState("");

    const nameInput = useRef(null);

    let [users, setUsers] = useState([]);


    const getUsers = async () => {
        const res = await fetch(`${API}/users`);
        const data = await res.json();
        setUsers(data);
        //console.log(data);
      };

    const deleteUser = async (id) => {
        const userResponse = window.confirm("Are you sure you want to delete it?");
        if (userResponse) {
          const res = await fetch(`${API}/users/${id}`, {
            method: "DELETE",
          });
          const data = await res.json();
          console.log(data);
          await getUsers();
        }
    };

    const editUser = async (id) => {
        const res = await fetch(`${API}/users/${id}`);
        const data = await res.json();
    
        setEditing(true);
        setId(id);
    
        // Reset
        setName(data.name);
        setEmail(data.email);
        setPassword(data.password);
        nameInput.current.focus();
      };
    
      useEffect(() => {
        getUsers();
      }, []);

    return ; 
};
