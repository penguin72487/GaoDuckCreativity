import React, { useState } from "react";
import axios from "axios";

const RegisterAccount = () => {
    const [formData, setFormData] = useState({
        name: "",
        student_id: "",
        email: "",
        password: "",
        role: "student"
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post("http://127.0.0.1:5000/api/accounts/register", formData)
            .then(response => alert(response.data.message))
            .catch(error => console.error("Error registering:", error));
    };

    return (
        <div className="page">
            <h1>註冊帳號</h1>
            <form onSubmit={handleSubmit}>
                <label>姓名</label>
                <input type="text" name="name" onChange={handleChange} />

                <label>學號</label>
                <input type="text" name="student_id" onChange={handleChange} />

                <label>Email</label>
                <input type="email" name="email" onChange={handleChange} />

                <label>密碼</label>
                <input type="password" name="password" onChange={handleChange} />

                <label>帳號類別</label>
                <select name="role" onChange={handleChange}>
                    <option value="student">學生</option>
                    <option value="admin">管理者</option>
                    <option value="judge">評審</option>
                </select>

                <button type="submit">註冊</button>
            </form>
        </div>
    );
};

export default RegisterAccount;
