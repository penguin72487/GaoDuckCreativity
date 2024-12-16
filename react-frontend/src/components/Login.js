import React, { useState } from "react";
import axios from "axios";

const Login = () => {
    const [formData, setFormData] = useState({ email: "", password: "" });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post("http://127.0.0.1:5000/api/login", formData)
            .then(response => alert(response.data.message))
            .catch(error => console.error("Error during login:", error));
    };

    return (
        <div className="page">
            <h1>登入</h1>
            <form onSubmit={handleSubmit}>
                <label>Email</label>
                <input type="email" name="email" onChange={handleChange} required />

                <label>密碼</label>
                <input type="password" name="password" onChange={handleChange} required />

                <button type="submit">登入</button>
            </form>
        </div>
    );
};

export default Login;
