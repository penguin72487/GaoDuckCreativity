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
        rater_title: "None",
        role: "student" // 預設為學生
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

    const getRoleSpecificLabel = () => {
        switch (formData.role) {
            case "student":
                return "學號";
            case "teacher":
                return "老師ID";
            case "rater":
                return "評審ID";
            default:
                return "管理者ID";
        }
    };

    return (
        <div className="page">
            <h1>註冊帳號</h1>
            <form onSubmit={handleSubmit}>

                <label>使用者名稱</label>
                <input type="text" name="ID_num" onChange={handleChange} />

                <label>{getRoleSpecificLabel()}</label>
                <input type="text" name="stu_id" onChange={handleChange} />

                <label>中文名</label>
                <input type="text" name="name" onChange={handleChange} />

                <label>電話號碼</label>
                <input type="text" name="phone" onChange={handleChange} />

                <label>Email</label>
                <input type="email" name="email" onChange={handleChange} />

                <label>密碼</label>
                <input type="password" name="password" onChange={handleChange} />

                {formData.role === "rater" && (
                    <>
                        <label>評審頭銜</label>
                        <input type="text" name="rater_title" onChange={handleChange} />
                    </>
                )}

                <label>帳號類別</label>
                <select name="role" onChange={handleChange}>
                    <option value="student">學生</option>
                    <option value="teacher">老師</option>
                    <option value="rater">評委</option>
                    <option value="admin">管理者</option>
                </select>

                <button type="submit">註冊</button>
            </form>
        </div>
    );
};

export default RegisterAccount;