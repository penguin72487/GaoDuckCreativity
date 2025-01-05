import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const [formData, setFormData] = useState({ ID_num: "", password: "" });
    const [error, setError] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setError(""); // 清空之前的錯誤
        setSuccessMessage(""); // 清空之前的成功消息

        axios
            .post("http://127.0.0.1:5000/api/auth/login", formData)
            .then((response) => {
                const { name, role, token } = response.data.data;

                // 存儲令牌到 localStorage
                localStorage.setItem("authToken", token);

                // 更新成功消息並跳轉
                setSuccessMessage(`歡迎, ${name}! 您的身份是: ${role}`);
                setTimeout(() => navigate("/"), 1000); // 延時 1 秒後跳轉到首頁
            })
            .catch((error) => {
                if (error.response && error.response.data) {
                    setError(error.response.data.message);
                } else {
                    setError("無法連接到伺服器，請稍後再試！");
                }
            });
    };

    return (
        <div className="page">
            <h1>登入</h1>
            <form onSubmit={handleSubmit}>
                <label>使用者名稱</label>
                <input type="text" name="ID_num" onChange={handleChange} required />

                <label>密碼</label>
                <input type="password" name="password" onChange={handleChange} required />

                <button type="submit">登入</button>
            </form>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {successMessage && <p style={{ color: "green" }}>{successMessage}</p>}
        </div>
    );
};

export default Login;
