import React, { useState } from "react";
import axios from "axios";

const RegisterAccount = () => {
    const [formData, setFormData] = useState({
        ID_num: "",
        stu_id: "",
        name: "",
        phone: "",
        email: "",
        password: "",
        address: "",
        admin_type: "",
        rater_title: "",
        role: "1" // 預設為學生
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Form Data:", formData); // Debug 用
        axios.post("http://127.0.0.1:5000/api/accounts/register", formData)
            .then(response => alert(response.data.message))
            .catch(error => console.error("Error registering:", error));
    };

    return (
        <div className="page">
            <h1>註冊帳號</h1>
            <form onSubmit={handleSubmit}>

                <label>身份證字號</label>
                <input type="text" name="ID_num" onChange={handleChange} />
                
                <label>學號</label>
                <input type="text" name="stu_id" onChange={handleChange} />

                <label>中文名</label>
                <input type="text" name="name" onChange={handleChange} />

                <label>電話號碼</label>
                <input type="text" name="phone" onChange={handleChange} />

                <label>Email</label>
                <input type="email" name="email" onChange={handleChange} />

                <label>密碼</label>
                <input type="password" name="password" onChange={handleChange} />

                <label>住址</label>
                <input type="text" name="address" onChange={handleChange} />

                <label>管理者類型</label>
                <input type="text" name="admin_type" onChange={handleChange} />

                <label>評審標題</label>
                <input type="text" name="rater_title" onChange={handleChange} />

                <label>帳號類別</label>
                <select name="role" onChange={handleChange}>
                    <option value="student">學生</option>
                    <option value="teacher">老師</option>
                    <option value="judge">評審</option>
                    <option value="admin">管理者</option>
                    <option value="1">學生</option>
                    <option value="2">老師</option>
                    <option value="3">評委</option>
                    <option value="999">管理者</option>
                </select>

                <button type="submit">註冊</button>
            </form>
        </div>
    );
};

export default RegisterAccount;